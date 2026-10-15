"""Preserve primary line-level annotations; never infer sound values or merge IDs."""
import collections as C
import hashlib
import json
import re
from analyze import ROOT,canonical,save
DIRECTIONS={'1':'RTL','2':'LTR','3':'single','4':'vertical','5':'symmetric','9':'doubtful','0':'none'}
BOOK='https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/The%20Indus%20Script.%20Text%2C%20Concordance%20and%20Tables%20-Iravathan%20Mahadevan.pdf'

def book_page(sign):return 43 if sign<=110 else 44 if sign<=219 else 45 if sign<=329 else 46

def normalize(row):
    f=row['fields'];raw=[str(f[f'S{i}']).strip() if f[f'S{i}'] is not None else '' for i in range(1,15)]
    tokens=[];reasons=[];closed=False
    for i,s in enumerate(raw):
        if not s:closed=True;continue
        if closed:reasons.append('discontinuous_slots')
        match=re.fullmatch(r'(\*)?(\d+)',s)
        if not match:reasons.append('malformed_sign');continue
        n=int(match[2]);doubt=bool(match[1]);sign=f'M{n:03}' if n else '<GAP>'
        tokens.append({'slot':i+1,'raw':s,'sign':sign,'doubtful':doubt,'integer':n+3 if 1<=n<=417 else 1})
        if doubt:reasons.append('doubtful_sign')
        if n==0:reasons.append('unknown_stretch')
        if not 0<=n<=417:reasons.append('out_of_inventory')
    if not tokens:reasons.append('no_text')
    if str(f['posnum'])!=str(len(tokens)) or str(f['signnum'])!=str(sum(t['sign']!='<GAP>' for t in tokens)):
        reasons.append('count_metadata_mismatch')
    combined=str(f['sideline']);side=line=None
    if re.fullmatch(r'\d+',combined):side,line=divmod(int(combined),10)
    else:reasons.append('malformed_side_line')
    if side not in range(7):reasons.append('unknown_side')
    if line!=0:reasons.append('not_single_line')
    direction=str(f['dir'])
    if direction not in ('1','2','3'):reasons.append('nonhorizontal_or_uncertain_direction')
    if direction=='3' and len(tokens)!=1:reasons.append('single_sign_direction_mismatch')
    return {'document_id':row['document_id'],'textnum':str(f['textnum']),'side':side,'line':line,
            'raw_side_line':combined,'direction_code':direction,'direction_label':DIRECTIONS.get(direction,'unrecognized'),
            'object_code':str(f['inscobj']),'field_symbol_code':str(f['fs80']),
            'locus':f['locus'],'level':f['level'],'signnum':f['signnum'],'posnum':f['posnum'],
            'tokens':tokens,'signs':[t['sign'] for t in tokens],'integer_slots':[t['integer'] for t in tokens],
            'exclusion_reasons':sorted(set(reasons))}

def secondary_audit(primary,secondary):
    groups=C.defaultdict(list)
    for r in primary:
        if r['tokens']:groups[(r['textnum'],r['side'])].append(r)
    ledger=[]
    for row in secondary:
        m=re.fullmatch(r'(\d+)(?:-([A-F]))?',row['id'])
        if not m:ledger.append({'id':row['id'],'status':'malformed_secondary_id'});continue
        side=ord(m[2])-ord('A')+1 if m[2] else 0
        sources=sorted(groups.get((m[1],side),[]),key=lambda r:(r['line'],r['document_id']))
        if not sources:ledger.append({'id':row['id'],'status':'no_primary_side'});continue
        tokens=[t for r in sources for t in r['tokens']]
        seq=[0 if t['sign']=='<GAP>' else int(t['sign'][1:]) for t in tokens]
        status='same_base_sequence' if seq==row['seq'] else 'sequence_disagreement'
        ledger.append({'id':row['id'],'status':status,'primary_documents':[r['document_id'] for r in sources],
                       'primary_lines':len(sources),'doubtful_tokens_stripped':sum(t['doubtful'] for t in tokens),
                       'secondary_sequence':row['seq'],'reconstructed_primary_sequence':seq})
    return {'counts':dict(C.Counter(r['status'] for r in ledger)),
        'rows_with_stripped_doubtful_tokens':sum(r.get('doubtful_tokens_stripped',0)>0 for r in ledger),
        'rows_concatenating_primary_lines':sum(r.get('primary_lines',0)>1 for r in ledger),'ledger':ledger}

def main():
    for manifest in ('mahadevan_primary_manifest.json','mahadevan_secondary_manifest.json'):
        m=json.loads((ROOT/'data/raw'/manifest).read_text())
        for name,digest in m['output_sha256'].items():
            assert hashlib.sha256((ROOT/'data/raw'/name).read_bytes()).hexdigest()==digest,name
    raw=json.loads((ROOT/'data/raw/mahadevan_primary.json').read_text());rows=[normalize(r) for r in raw]
    identities=C.Counter((r['textnum'],r['side'],r['line']) for r in rows)
    for r in rows:
        if identities[(r['textnum'],r['side'],r['line'])]>1:r['exclusion_reasons'].append('duplicate_line_identity')
    clean=[r for r in rows if not r['exclusion_reasons']]
    inventory=[{'id':f'M{i:03}','integer':i+3,'namespace':'Mahadevan1977','source_pdf_page':book_page(i),
                'source_printed_page':book_page(i)-11,'source_url':BOOK+f'#page={book_page(i)}'} for i in range(1,418)]
    (ROOT/'data/processed/mahadevan_primary_lines.json').write_text(json.dumps(rows,indent=2)+'\n')
    (ROOT/'data/processed/mahadevan_sign_catalog.json').write_text(json.dumps({'reserved':{'PAD':0,'UNK_or_gap_slot':1,'BOS':2,'EOS':3},'signs':inventory,'scope':'Original sign-list page references; separate numeric namespace. Gap slots can span an unknown number of signs. Raster book pages are not redistributed.'},indent=2)+'\n')
    secondary=json.loads((ROOT/'data/raw/mahadevan_secondary.json').read_text())
    audit={'design':'docs/EXPERIMENT_013.md','primary_rows':len(rows),'text_rows':sum(bool(r['tokens']) for r in rows),
        'strict_singleline_rows':len(clean),'strict_canonical_texts':len({canonical(r['signs']) for r in clean}),
        'raw_observed_ids':len({t['sign'] for r in rows for t in r['tokens'] if t['sign']!='<GAP>'}),
        'strict_observed_ids':len({s for r in clean for s in r['signs']}),
        'doubtful_tokens':sum(t['doubtful'] for r in rows for t in r['tokens']),
        'exclusion_counts':dict(C.Counter(x for r in rows for x in r['exclusion_reasons'])),
        'direction_counts':dict(C.Counter(r['direction_code'] for r in rows)),
        'secondary_comparison':secondary_audit(rows,secondary),
        'scope':'Acquisition/encoding only. No model scores, motif semantics, namespace merge or phonetic values. Strict eligibility is a declared screen, not original-object verification.'}
    save('mahadevan_primary_audit.json',audit)
    print(json.dumps({k:v for k,v in audit.items() if k!='secondary_comparison'}|{'secondary_comparison':{k:v for k,v in audit['secondary_comparison'].items() if k!='ledger'}},indent=2))
if __name__=='__main__':main()

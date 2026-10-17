"""Source-attributed variant references and a non-propagating occurrence lookup."""
import collections as C
import hashlib
import json
import re
from analyze import ROOT,save

def expand(source):
    ordinals=C.Counter();forms=[]
    for segment in source['segments']:
        key=(segment['section'],segment['base'])
        for local,citation in enumerate(segment['references'],1):
            ordinals[key]+=1;ordinal=ordinals[key];section,base=key
            forms.append({'id':f'MV{base:03}-{section}-{ordinal:02}','integer':len(forms)+4,
                'namespace':'MahadevanGraphic1977','base_id':f'M{base:03}','section':section,'family_ordinal':ordinal,
                'position_in_segment':local,'pdf_page':segment['pdf_page'],'printed_page':segment['printed_page'],'column':segment['column'],
                'citation_raw':citation,'citation_uncertain':local in segment['uncertain_ordinals'],
                'source_url':source['source_url']+f'#page={segment["pdf_page"]}',
                'identity_scope':'Research ordinal for a source-drawn form, not a historical phonetic unit'})
    return forms

def lookup(form,rows_by_text):
    m=re.fullmatch(r'(\d{4})(.*)',form['citation_raw'])
    if not m:return {'status':'unparsed_citation','candidates':[],'automatic_assignment':False}
    number,suffix=m.groups();rows=rows_by_text.get(number,[]);found=[]
    for r in rows:
        for t in r['tokens']:
            if t['sign']==form['base_id']:
                found.append({'document_id':r['document_id'],'side':r['side'],'line':r['line'],'slot':t['slot'],
                              'doubtful':t['doubtful'],'row_exclusions':r['exclusion_reasons']})
    if form['citation_uncertain']:status='uncertain_transcription'
    elif suffix:status='unresolved_suffix'
    elif not rows:status='missing_text'
    elif not found:status='base_absent'
    elif len(found)>1:status='multiple_base_occurrences'
    else:status='unique_base_occurrence'
    return {'textnum_candidate':number,'suffix_raw':suffix,'status':status,'candidates':found,'automatic_assignment':False}

def main():
    manifest=json.loads((ROOT/'data/raw/mahadevan_graphic_manifest.json').read_text())
    for name,digest in manifest['output_sha256'].items():assert hashlib.sha256((ROOT/'data/raw'/name).read_bytes()).hexdigest()==digest
    source=json.loads((ROOT/'data/raw/mahadevan_graphic_variants.json').read_text());forms=expand(source)
    rows=json.loads((ROOT/'data/processed/mahadevan_primary_lines.json').read_text());by_text=C.defaultdict(list)
    for r in rows:by_text[r['textnum']].append(r)
    ledger=[{'variant_id':r['id'],'base_id':r['base_id'],'citation_raw':r['citation_raw']}|lookup(r,by_text) for r in forms]
    counts={section:{'families':len({r['base_id'] for r in forms if r['section']==section}),'forms':sum(r['section']==section for r in forms)} for section in ('main','addendum')}
    family_count=len({r['base_id'] for r in forms})
    addon=[{'id':f'M{n:03}','integer':n+3,'namespace':'Mahadevan1977_postscript',
            'pdf_page':36,'printed_page':25,'source_url':source['source_url']+'#page=36',
            'scope':'Postscript source drawing; absent from the frozen 417-ID primary application inventory'} for n in source['postscript']['new_signs']]
    catalogue={'reserved':{'PAD':0,'UNK':1,'BOS':2,'EOS':3},'variants':forms,'base_sign_addenda':addon,
        'scope':source['scope'],'source_sha256':source['source_sha256']}
    (ROOT/'data/processed/mahadevan_graphic_catalog.json').write_text(json.dumps(catalogue,indent=2)+'\n')
    summary={'design':'docs/EXPERIMENT_016.md','families':family_count,'forms':len(forms),'sections':counts,
        'source_stated_totals':source['source_stated_totals'],
        'transcription_digit_corrections':len(source.get('transcription_revisions',[])),
        'matches_source_totals':family_count==source['source_stated_totals']['families'] and len(forms)==source['source_stated_totals']['forms'],
        'lookup_counts':dict(C.Counter(r['status'] for r in ledger)),
        'unique_candidates_in_flagged_context':sum(r['status']=='unique_base_occurrence' and bool(r['candidates'][0]['row_exclusions']) for r in ledger),
        'missing_postscript_texts':[n for n in source['postscript']['referenced_inscriptions'] if n not in by_text],
        'base_sign_addenda':addon,'lookup_ledger':ledger,
        'scope':'Source-count reconciliation and citation lookup only. Parentheses and repeated occurrences remain unresolved. No variants assigned to primary tokens, signs merged or sounds inferred.'}
    save('graphic_variant_audit.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k!='lookup_ledger'},indent=2))
if __name__=='__main__':main()

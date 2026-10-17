"""Audit FC-number candidates; identical numbers do not certify object identity."""
import collections as C
import hashlib
import json
import math
import random
from analyze import ROOT,canonical,save

def candidates(refs,parpola,primary):
    ps=C.defaultdict(list);ms=C.defaultdict(list)
    for r in parpola:ps[r['id']].append(r)
    for r in primary:ms[r['textnum']].append(r)
    accepted=[];rejected=[]
    for ref in refs:
        obj=ref['cisi_object'];source=ps.get(obj+'A',[]);number=str(int(ref['fc_raw']))
        targets=[r for r in ms.get(number,[]) if r['side']==0 and r['line']==0]
        reason=None
        if ref['uncertain_digits']:reason='uncertain_reference_digits'
        elif not 1001<=int(number)<=3513:reason='outside_supported_mohenjo_daro_range'
        elif len(source)!=1:reason='missing_or_ambiguous_parpola_face'
        elif source[0]['exclusion_reasons']:reason='parpola_ineligible'
        elif len(targets)!=1:reason='missing_or_ambiguous_primary_single_side_line'
        elif targets[0]['exclusion_reasons']:reason='primary_ineligible'
        elif len(source[0]['signs'])!=len(targets[0]['signs']):reason='unequal_lengths'
        if reason:rejected.append(ref|{'reason':reason,'primary_candidate_textnum':number});continue
        accepted.append({'object':obj,'fc_raw':ref['fc_raw'],'primary_document':targets[0]['document_id'],
                         'primary_textnum':number,'parpola_id':source[0]['id'],'parpola_signs':source[0]['signs'],
                         'mahadevan_signs':targets[0]['signs'],'identity_status':'unverified numeric-reference candidate'})
    return accepted,rejected

def partition(pairs):
    parents=list(range(len(pairs)))
    def find(i):
        while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
        return i
    seen={}
    for i,p in enumerate(pairs):
        for key in ('parpola_signs','mahadevan_signs'):
            signature=(key,canonical(p[key]))
            if signature in seen:
                a,b=find(i),find(seen[signature]);parents[max(a,b)]=min(a,b)
            else:seen[signature]=i
    groups=C.defaultdict(list)
    for i,p in enumerate(pairs):groups[find(i)].append(p)
    pilot=[k for k,g in groups.items() if any(p['object']=='M-1' for p in g)]
    if len(pilot)!=1:raise ValueError('Pilot group missing/ambiguous')
    keys=sorted(k for k in groups if k not in pilot);random.Random(42).shuffle(keys)
    a,b=int(.8*len(keys)),int(.9*len(keys))
    return [[p for k in ks for p in groups[k]] for ks in (pilot+keys[:a],keys[a:b],keys[b:])],groups

def aligned(pair,orientation):
    target=pair['mahadevan_signs'] if orientation=='direct' else pair['mahadevan_signs'][::-1]
    return zip(pair['parpola_signs'],target)

def fit(pairs,orientation):
    counts=C.defaultdict(C.Counter);objects=C.defaultdict(set)
    for p in pairs:
        for a,b in aligned(p,orientation):counts[a][b]+=1;objects[a].add(p['object'])
    return counts,objects

def entropy(counts):
    total=sum(sum(c.values()) for c in counts.values())
    return -sum(n/total*math.log2(n/sum(c.values())) for c in counts.values() for n in c.values())

def evaluate(pairs,orientation,counts):
    total=correct=known=whole=0;records=[]
    for p in pairs:
        positions=[]
        for a,b in aligned(p,orientation):
            row=counts.get(a,{});prediction=min(row,key=lambda s:(-row[s],s)) if row else None
            positions.append({'parpola':a,'mahadevan_candidate':b,'prediction':prediction,'correct':prediction==b,'training_candidates':dict(sorted(row.items()))})
            total+=1;correct+=prediction==b;known+=bool(row)
        full=all(r['correct'] for r in positions);whole+=full
        records.append({'object':p['object'],'fc_raw':p['fc_raw'],'primary_candidate_textnum':p['primary_textnum'],'positions':positions,'whole_correct':full})
    return {'candidate_objects':len(pairs),'positions':total,'correct':correct,'known_source_positions':known,
            'top1':correct/total if total else None,'source_coverage':known/total if total else None,'whole_correct':whole,'records':records}

def main():
    manifest=json.loads((ROOT/'data/raw/cisi1_fc_manifest.json').read_text())
    for name,digest in manifest['output_sha256'].items():assert hashlib.sha256((ROOT/'data/raw'/name).read_bytes()).hexdigest()==digest
    refs=json.loads((ROOT/'data/raw/cisi1_fc_candidates.json').read_text())['records']
    ps=json.loads((ROOT/'data/processed/cisi_all.json').read_text());ms=json.loads((ROOT/'data/processed/mahadevan_primary_lines.json').read_text())
    pairs,rejected=candidates(refs,ps,ms);parts,groups=partition(pairs);train,val,test=parts
    entropies={o:entropy(fit(train,o)[0]) for o in ('direct','reversed')};orientation=min(entropies,key=lambda o:(entropies[o],o!='direct'))
    counts,objects=fit(train,orientation);mapping=[]
    for a,row in sorted(counts.items()):
        target=min(row,key=lambda s:(-row[s],s));n=sum(row.values());purity=row[target]/n
        mapping.append({'parpola':a,'majority_mahadevan':target,'support':n,'purity':purity,'candidate_objects':sorted(objects[a]),
            'distribution':dict(sorted(row.items())),'review_priority':n>=3 and len(objects[a])>=2 and purity>=.9})
    output={'design':'docs/EXPERIMENT_015.md','reference_rows':len(refs),'accepted_numeric_candidates':len(pairs),
            'rejection_counts':dict(C.Counter(r['reason'] for r in rejected)),'rejected':rejected,'pairs':pairs,
            'groups':len(groups),'split_objects':{name:[p['object'] for p in part] for name,part in zip(('train','validation','test'),parts)},
            'pilot':'M-1 component forced into training; source aliases and original photo were seen before design',
            'training_alignment_entropy':entropies,'selected_alignment':orientation,'mapping_candidates':mapping,
            'review_priority_count':sum(r['review_priority'] for r in mapping),'validation':evaluate(val,orientation,counts),'test':evaluate(test,orientation,counts),
            'scope':'FC numbers are not uniformly Mahadevan numbers. Accuracy measures consistency of numeric-reference candidate transcriptions, not independently verified object identities or sound values. No automatic crosswalk propagation.'}
    save('reference_candidates.json',output)
    print(json.dumps({k:v for k,v in output.items() if k not in ('pairs','rejected','mapping_candidates','split_objects')}|{'validation':{k:v for k,v in output['validation'].items() if k!='records'},'test':{k:v for k,v in output['test'].items() if k!='records'}},indent=2))
if __name__=='__main__':main()

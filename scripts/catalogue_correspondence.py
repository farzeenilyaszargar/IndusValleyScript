"""Candidate paired-object crosswalk; never assign sounds or merge inventories."""
import collections as C
import json
import math
import random
import re
from analyze import ROOT, canonical, save

def pair_records(parpola,icit):
    index=C.defaultdict(list)
    for r in icit:
        if r['site']=='Mohenjo-daro':index[r['cisi']].append(r)
    pairs=[];rejected=[]
    for p in parpola:
        match=re.fullmatch(r'M-(\d+)A',p['id'])
        key=f'M-{int(match[1])}' if match else None
        candidates=index.get(key,[]);reason=None
        if not match:reason='unsupported_face_id'
        elif p['exclusion_reasons']:reason='parpola_ineligible'
        elif not candidates:reason='missing_object'
        elif len(candidates)!=1:reason='ambiguous_object_rows'
        elif candidates[0]['exclusion_reasons']:reason='icit_ineligible'
        elif len(p['signs'])!=len(candidates[0]['signs']):reason='unequal_lengths'
        if reason:
            rejected.append({'parpola_id':p['id'],'object_label':key,'reason':reason,
                             'parpola_length':len(p['signs']),
                             'icit_rows':[{'id':r['id'],'length':len(r['signs'])} for r in candidates]})
        else:
            i=candidates[0]
            pairs.append({'object':key,'parpola_id':p['id'],'icit_row_id':i['id'],
                          'parpola_signs':p['signs'],'icit_signs':i['signs'],
                          'morphology':p['allographs']})
    return pairs,rejected

def grouped_split(pairs):
    parent=list(range(len(pairs)))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    seen={}
    for i,p in enumerate(pairs):
        for namespace in ('parpola_signs','icit_signs'):
            key=(namespace,canonical(p[namespace]))
            if key in seen:
                a,b=find(i),find(seen[key]);parent[max(a,b)]=min(a,b)
            else:seen[key]=i
    groups=C.defaultdict(list)
    for i,p in enumerate(pairs):groups[find(i)].append(p)
    values=list(groups.values());random.Random(42).shuffle(values)
    a,b=int(.8*len(values)),int(.9*len(values))
    parts=[[p for g in gs for p in g] for gs in (values[:a],values[a:b],values[b:])]
    return parts,values

def aligned(pair,orientation):
    seq=pair['icit_signs'] if orientation=='direct' else pair['icit_signs'][::-1]
    return list(zip(seq,pair['parpola_signs']))

def fit(pairs,orientation):
    counts=C.defaultdict(C.Counter);objects=C.defaultdict(set)
    for p in pairs:
        for i,c in aligned(p,orientation):counts[i][c]+=1;objects[i].add(p['object'])
    return counts,objects

def mapping_entropy(counts):
    total=sum(sum(c.values()) for c in counts.values())
    return -sum(n/total*math.log2(n/sum(c.values())) for c in counts.values() for n in c.values())

def evaluate(pairs,orientation,counts):
    records=[];known=correct=total=whole=0;known_loss=0.0
    target_vocab={p for row in counts.values() for p in row}|{'<UNK>'}
    for pair in pairs:
        positions=[]
        for i,p in aligned(pair,orientation):
            row=counts.get(i,{})
            predicted=min(row,key=lambda s:(-row[s],s)) if row else None
            target=p if p in target_vocab else '<UNK>'
            probability=(row.get(target,0)+.5)/(sum(row.values())+.5*len(target_vocab)) if row else None
            if probability is not None:known_loss-=math.log2(probability)
            known+=bool(row);correct+=predicted==p;total+=1
            positions.append({'icit':i,'parpola':p,'prediction':predicted,'correct':predicted==p,
                              'smoothed_target_probability_when_source_known':probability,
                              'training_candidates':dict(sorted(row.items()))})
        full=all(r['correct'] for r in positions);whole+=full
        records.append({'object':pair['object'],'positions':positions,'whole_sequence_correct':full})
    return {'objects':len(pairs),'positions':total,'known_source_positions':known,
            'known_coverage':known/total if total else 0,'correct_positions':correct,
            'top1_rate_all_positions':correct/total if total else 0,
            'known_source_logloss_bits':known_loss/known if known else None,
            'logloss_policy':'Known source IDs only; additive 0.5 over training Parpola IDs plus UNK; unseen target IDs collapse to UNK. Unseen source positions remain explicit prediction failures.',
            'whole_sequences_correct':whole,'records':records}

def main():
    ps=json.loads((ROOT/'data/processed/cisi_all.json').read_text())
    xs=json.loads((ROOT/'data/processed/icit_all.json').read_text())
    pairs,rejected=pair_records(ps,xs);parts,groups=grouped_split(pairs)
    train,val,test=parts
    comparisons={orientation:mapping_entropy(fit(train,orientation)[0]) for orientation in ('direct','reversed')}
    orientation=min(comparisons,key=lambda o:(comparisons[o],o!='direct'))
    counts,objects=fit(train,orientation)
    catalog={r['id']:r for r in json.loads((ROOT/'data/processed/parpola_catalog.json').read_text())}
    candidates=[]
    for i,row in sorted(counts.items()):
        winner=min(row,key=lambda s:(-row[s],s));support=sum(row.values());purity=row[winner]/support
        candidates.append({'icit':i,'parpola_majority':winner,'support':support,'training_objects':sorted(objects[i]),
                           'candidate_distribution':dict(sorted(row.items())),'purity':purity,
                           'review_priority':support>=3 and len(objects[i])>=2 and purity>=.9,
                           'source_wells_alias_agrees':('W'+i) in catalog[winner]['wells_graphemes'],
                           'status':'candidate from paired transcriptions; not glyph verified'})
    save('catalogue_correspondence.json',{'design':'docs/EXPERIMENT_006.md','accepted_pairs':len(pairs),
        'rejected_count':len(rejected),'rejection_reasons':dict(C.Counter(r['reason'] for r in rejected)),
        'group_count':len(groups),'split_seed':42,'split_objects':{name:[p['object'] for p in part]
                       for name,part in zip(('train','validation','test'),parts)},
        'orientation_train_entropy':comparisons,'selected_alignment':orientation,
        'candidates':candidates,'review_priority_count':sum(c['review_priority'] for c in candidates),
        'review_priority_source_alias_agreement':sum(c['review_priority'] and c['source_wells_alias_agrees'] for c in candidates),
        'alias_check_scope':'Exploratory comparison to supplied Wells cross-references after inference; shared source metadata, not independent glyph verification.',
        'validation':evaluate(val,orientation,counts),'test':evaluate(test,orientation,counts),
        'pairs':pairs,'rejected':rejected,
        'limitation':'No independent face/glyph/object verification. Shared source ancestry, small holdout and segmentation exclusions limit inference. No sounds, meanings or automatic sign merging.'})
    print(json.dumps({'accepted':len(pairs),'rejected':len(rejected),'orientation':orientation,
          'training_entropy':comparisons,'review_candidates':sum(c['review_priority'] for c in candidates),
          'validation':{k:v for k,v in evaluate(val,orientation,counts).items() if k!='records'},
          'test':{k:v for k,v in evaluate(test,orientation,counts).items() if k!='records'}},indent=2))

if __name__=='__main__':main()

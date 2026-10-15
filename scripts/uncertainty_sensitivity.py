"""Annotated-reading sensitivity; wider transcriptions are hypotheses, not truth."""
import collections as C
import json
from analyze import ROOT,Model,avg_loss,canonical,save
from allographs import partition
from metadata_models import interval
from catalogue_correspondence import pair_records,aligned

def broader_eligible(row):return set(row['exclusion_reasons'])<= {'damage_or_uncertainty'}

def eligible_additions(rows,validation,test,limit=None):
    forbidden_ids={r['id'] for r in validation+test}
    forbidden_texts={canonical(r['signs']) for r in validation+test}
    accepted=[]
    for r in rows:
        if not broader_eligible(r) or r['id'] in forbidden_ids or canonical(r['signs']) in forbidden_texts:continue
        if limit is not None and any(g['features'][0]>limit or g['features'][2]>limit for g in r['allographs']):continue
        accepted.append(r)
    return accepted

def main():
    rows=json.loads((ROOT/'data/processed/cisi_all.json').read_text())
    clean=[r for r in rows if not r['exclusion_reasons']]
    train,val,test=partition(clean,42)
    ts=lambda rs:[r['signs'] for r in rs]
    conditions={'clean':train,'raw_codes_le25':eligible_additions(rows,val,test,25),
                'all_known_singleline_readings':eligible_additions(rows,val,test,None)}
    output={'design':'docs/EXPERIMENT_010.md','clean_validation_ids':[r['id'] for r in val],
            'clean_test_ids':[r['id'] for r in test],'conditions':{},
            'scoring':'Fixed clean holdouts; EOS included; unseen base IDs collapse to UNK',
            'limitation':'Raw annotation codes are not calibrated error probabilities; broader texts include guessed readings. Increased coverage or smoothing changes are not validation of glyphs.'}
    baseline=None
    for name,records in conditions.items():
        model=min((Model(ts(records),2,s) for s in (1,5,20,100)),key=lambda m:avg_loss(m.losses(ts(val))))
        losses=model.losses(ts(test))
        if name=='clean':baseline=losses
        added=[r for r in records if r['id'] not in {x['id'] for x in train}]
        output['conditions'][name]={'training_objects':len(records),'added_objects':len(added),
            'training_ids':[r['id'] for r in records],'added_ledger':[{'id':r['id'],'signs':r['signs'],
                'annotations':[{'sign':g['id'],'raw_damage_code':g['features'][0],'raw_uncertainty':g['features'][2]}
                               for g in r['allographs']],'original_exclusions':r['exclusion_reasons']} for r in added],
            'strength':model.strength,'validation_bits':avg_loss(model.losses(ts(val))),
            'test_bits':avg_loss(losses),'unknown_test_tokens':sum(s not in model.uni for t in ts(test) for s in t),
            'clean_baseline_improvement':interval(test,baseline,losses)}
    # Clear only the one permitted exclusion for matching; retain originals in lookup.
    allowable=[dict(r,exclusion_reasons=[]) for r in rows if broader_eligible(r)]
    rawicit=json.loads((ROOT/'data/processed/icit_all.json').read_text())
    pairs,rejected=pair_records(allowable,rawicit)
    catalog={r['id']:r for r in json.loads((ROOT/'data/processed/parpola_catalog.json').read_text())}
    originals={r['id']:r for r in rows};audit=[]
    for p in pairs:
        source=originals[p['parpola_id']]
        positions=[]
        for pos,(i,c) in enumerate(aligned(p,'reversed')):
            g=source['allographs'][pos]
            positions.append({'position':pos,'icit_id':i,'parpola_id':c,'alias_list_contains_id':('W'+i) in catalog[c]['wells_graphemes'],
                              'raw_damage_code':g['features'][0],'raw_uncertainty':g['features'][2]})
        audit.append({'object':p['object'],'parpola_id':p['parpola_id'],
                      'has_annotated_damage_or_uncertainty':bool(source['exclusion_reasons']),
                      'alias_absence_positions':[r for r in positions if not r['alias_list_contains_id']],
                      'positions':positions})
    output['source_consistency']={'accepted_pairs':len(pairs),'rejected_candidates':rejected,'objects':audit,
        'alias_absences':sum(len(r['alias_absence_positions']) for r in audit),
        'aligned_positions':sum(len(r['positions']) for r in audit),
        'scope':'Supplied Wells aliases, not independent glyph verification. Absence may reflect variant splitting, errors or incomplete crosswalk; no automatic corrections.'}
    output['source_consistency']['zero_annotation_alias_absences']=sum(
        p['raw_damage_code']==0 and p['raw_uncertainty']==0 for r in audit for p in r['alias_absence_positions'])
    save('uncertainty_sensitivity.json',output)
    print(json.dumps({'conditions':{k:{x:y for x,y in v.items() if x not in ('training_ids','added_ledger')}
                                  for k,v in output['conditions'].items()},
        'source_consistency':{k:v for k,v in output['source_consistency'].items() if k not in ('objects','rejected_candidates')}},indent=2))

if __name__=='__main__':main()

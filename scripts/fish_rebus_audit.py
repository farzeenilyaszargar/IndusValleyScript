"""Observable fish/stroke witnesses and competing hypothetical readings."""
import collections as C
import json
import random
import statistics as S
from analyze import ROOT,save

def extract_events(texts,counts,reverse=False):
    events=[]
    for row in texts:
        signs=row['signs'][::-1] if reverse else row['signs']
        for i,s in enumerate(signs):
            if s in counts and i>0 and signs[i-1] not in counts:
                events.append({'row_id':row['id'],'cisi':row['cisi'],'stored_or_reversed_position':i,
                               'stroke_id':s,'described_count':counts[s],'head_id':signs[i-1]})
    return events

def enrichment(events):
    fish=[e for e in events if e['head_id']=='220'];others=[e for e in events if e['head_id']!='220']
    special={3,6,7}
    n=sum(e['described_count'] in special for e in fish)
    def statistic(values):return sum(v in special for e,v in zip(events,values) if e['head_id']=='220')
    values=[e['described_count'] for e in events];rng=random.Random(20261015);null=[]
    for _ in range(999):
        shuffled=values[:];rng.shuffle(shuffled);null.append(statistic(shuffled))
    return {'fish_slots':len(fish),'other_slots':len(others),'fish_3_6_7_slots':n,
        'other_3_6_7_slots':sum(e['described_count'] in special for e in others),
        'fish_count_distribution':dict(sorted(C.Counter(e['described_count'] for e in fish).items())),
        'other_count_distribution':dict(sorted(C.Counter(e['described_count'] for e in others).items())),
        'null_mean_special_fish_slots':S.mean(null),'p_upper':(1+sum(v>=n for v in null))/1000,
        'trials':999,'seed':20261015,
        'scope':'Exploratory operational test for counts 3/6/7; not a full prediction of the published star hypothesis. Unstratified slot exchangeability assumed.'}

def main():
    catalog={r['id']:r for r in json.loads((ROOT/'data/processed/parpola_catalog.json').read_text())}
    glyph={r['sign']:r for r in json.loads((ROOT/'data/processed/glyph_morphology.json').read_text())['descriptors']}
    counts={alias[1:]:i-120 for i in range(121,131) for alias in catalog[f'P{i}']['wells_graphemes']}
    checks=[]
    for s,n in sorted(counts.items()):
        actual=glyph[s]['connected_components_8']
        checks.append({'id':s,'described_count':n,'reference_components':actual,'match':n==actual})
        if n!=actual:raise ValueError('Unconfirmed simple stroke morphology')
    raw=json.loads((ROOT/'data/processed/icit_all.json').read_text())
    unique=json.loads((ROOT/'data/processed/icit_unique.json').read_text())
    eligible=[r for r in raw if not r['exclusion_reasons']]
    cisi=json.loads((ROOT/'data/processed/cisi_all.json').read_text())
    witnesses=[]
    for key in ('H-9','M-112','M-241'):
        witnesses.append({'cisi_label':key,'icit_records':[r for r in raw if r['cisi']==key],
                          'annotated_cisi_records':[r for r in cisi if r['id']==key+'A']})
    direct=extract_events(unique,counts);reversed_events=extract_events(unique,counts,True)
    output={'design':'docs/EXPERIMENT_009.md','short_stroke_mapping_checks':checks,'named_witnesses':witnesses,
        'complete_unique_diagnostic':enrichment(direct),'opposite_order_diagnostic':enrichment(reversed_events),
        'plain_fish_stroke_objects_unique':[e for e in direct if e['head_id']=='220'],
        'plain_fish_stroke_object_occurrences':[e for e in extract_events(eligible,counts) if e['head_id']=='220'],
        'hypothetical_H9_readings':[
          {'model':'Published astronomical rebus','graphic_tokens':['220','017'],
           'conditional_rendering':'IF the strokes encode seven and the fish sign represents proposed miin/star, Parpola reads the sequence as eZu-miin (seven stars / Ursa Major).',
           'phonetic_value_status':'Published proposal, not independently established Indus phonetics',
           'independent_semantic_anchor':None},
          {'model':'Unknown quantity plus category','graphic_tokens':['220','017'],
           'conditional_rendering':'IF strokes encode quantities, seven units of an unknown category.',
           'phonetic_value_status':'No sounds assigned','independent_semantic_anchor':None},
          {'model':'Unknown category/rate label','graphic_tokens':['220','017'],
           'conditional_rendering':'IF the strokes encode a fixed category/rate, a seven-valued rule or label associated with an unknown category.',
           'phonetic_value_status':'No sounds assigned','independent_semantic_anchor':None}],
        'identifiability':'All three templates admit the same observed graphics; this evidence alone cannot select their semantics.',
        'M112_disagreement':'ICIT export uses plain-fish code 220; annotated CISI uses P056 (modified fish) after P126. Damage/uncertainty elsewhere excludes the object from the earlier clean CISI subset.',
        'limitation':'Reference-based codes, incomplete/provisional crosswalk and stored-order convention; named witnesses checked retrospectively. No independent constellation, quantity or rate label exists.'}
    save('fish_rebus_audit.json',output)
    print(json.dumps({k:v for k,v in output.items() if k in ('complete_unique_diagnostic','opposite_order_diagnostic','M112_disagreement')},indent=2))

if __name__=='__main__':main()

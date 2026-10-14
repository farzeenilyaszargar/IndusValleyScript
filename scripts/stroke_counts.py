"""Graphic stroke counts and follower dependencies; no semantic decoding."""
import collections as C
import json
import math
import random
import statistics as S
from analyze import ROOT, save

COUNTS={f'P{i:03}':('short',i-120) for i in range(121,131)}
COUNTS.update({f'P{i:03}':('tall',n) for i,n in [(144,1),(145,2),(147,3),(150,4),(151,5)]})

def mutual_information(events):
    joint=C.Counter((e['stroke_count'],e['follower']) for e in events)
    counts=C.Counter(e['stroke_count'] for e in events);followers=C.Counter(e['follower'] for e in events)
    total=len(events)
    if not total:return 0.0
    return sum(n/total*math.log2(n*total/(counts[a]*followers[b])) for (a,b),n in joint.items())

def permuted(events,rng):
    result=[dict(e) for e in events];strata=C.defaultdict(list)
    for i,e in enumerate(events):strata[(e['height'],e['position_role'])].append(i)
    for indices in strata.values():
        counts=[events[i]['stroke_count'] for i in indices];rng.shuffle(counts)
        for i,n in zip(indices,counts):result[i]['stroke_count']=n
    return result

def association(events):
    observed=mutual_information(events);rng=random.Random(20261015)
    values=[mutual_information(permuted(events,rng)) for _ in range(999)]
    p=(1+sum(v>=observed-1e-12 for v in values))/1000
    return {'events':len(events),'mutual_information_bits':observed,'null_mean_bits':S.mean(values),
            'null_sd_bits':S.stdev(values),'p_upper':p,'bonferroni_two_tests_p':min(1,2*p),
            'trials':999,'seed':20261015,'null_values':values,
            'strata':[{ 'height':h,'position':p,'events':n} for (h,p),n in sorted(C.Counter(
                      (e['height'],e['position_role']) for e in events).items())]}

def main():
    records=json.loads((ROOT/'data/processed/cisi_unique.json').read_text())
    catalog={r['id']:r for r in json.loads((ROOT/'data/processed/parpola_catalog.json').read_text())}
    events=[];excluded=[];allslots=[]
    for r in records:
        for i,g in enumerate(r['allographs']):
            if g['id'] not in COUNTS:continue
            height,n=COUNTS[g['id']]
            event={'object_id':r['id'],'position':i,'position_role':'initial' if i==0 else 'medial',
                   'height':height,'stroke_sign':g['id'],'stroke_count':n,
                   'follower':r['signs'][i+1] if i+1<len(r['signs']) else None}
            allslots.append(event)
            if event['follower'] is None:excluded.append(event|{'reason':'terminal_tally'})
            elif event['follower'] in COUNTS:excluded.append(event|{'reason':'tally_follower'})
            else:
                event['follower_custom_features']=r['allographs'][i+1]['features'][3:]
                events.append(event)
    groups=C.defaultdict(list)
    for e in events:groups[e['follower']].append(e)
    followers=[]
    for sign,es in sorted(groups.items()):
        counts=C.Counter(e['stroke_count'] for e in es)
        followers.append({'sign':sign,'description':catalog[sign]['description'],'events':len(es),
                          'distinct_stroke_counts':len(counts),'stroke_count_distribution':dict(sorted(counts.items())),
                          'dominant_fraction':max(counts.values())/len(es),'support_at_least_5':len(es)>=5,
                          'object_ids':sorted({e['object_id'] for e in es})})
    result={'design':'docs/EXPERIMENT_005.md','corpus':'CISI complete deduplicated Mohenjo-daro subset',
        'objects':len(records),'all_tally_slots':len(allslots),'excluded':excluded,
        'mapping':[{'sign':s,'height':h,'described_stroke_count':n,'description':catalog[s]['description']}
                   for s,(h,n) in sorted(COUNTS.items())],
        'all_counts_association':association(events),
        'short_only_association':association([e for e in events if e['height']=='short']),
        'followers':followers,'events':events,
        'tally_slot_distribution':[{'height':h,'described_count':n,'occurrences':k} for (h,n),k in
                                    sorted(C.Counter((e['height'],e['stroke_count']) for e in allslots).items())],
        'evidence_gap':'No independently measured commodity amounts, matched object weights, verified metrological scale or bilingual labels in these records.',
        'interpretation':'Counts describe catalogue morphology. Association cannot establish quantities, rates, stars, words, commodities or a language family.'}
    save('stroke_count_constraints.json',result)
    print(json.dumps({'objects':len(records),'all_tally_slots':len(allslots),'usable_events':len(events),
                      'supported_followers':[f for f in followers if f['support_at_least_5']]},indent=2))
    for name in ('all_counts_association','short_only_association'):
        print(name,{k:v for k,v in result[name].items() if k!='null_values'})

if __name__=='__main__':main()

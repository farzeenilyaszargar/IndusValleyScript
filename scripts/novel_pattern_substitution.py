"""Retrospective collapse-disjoint evaluation of frozen substitution keys."""
import collections as C
import gzip
import hashlib
import json
import math
import random
from analyze import ROOT,canonical,save,split
from substitution_search import K,costs,encode_case,objective,rank_key,score,statistics

NAMES=('train','validation','test')

def retain_novel(parts):
    training={canonical(t) for t in parts[0]}
    val=[i for i,t in enumerate(parts[1]) if canonical(t) not in training]
    validation={canonical(parts[1][i]) for i in val}
    kept=[list(range(len(parts[0]))),val,[i for i,t in enumerate(parts[2]) if canonical(t) not in training|validation]]
    reasons=[]
    for part,rows in enumerate(parts):
        retained=set(kept[part])
        reasons.append(['retained' if i in retained else 'training_pattern' if canonical(t) in training else 'validation_pattern' for i,t in enumerate(rows)])
    sets=[{canonical(parts[p][i]) for i in indices} for p,indices in enumerate(kept)]
    if any(sets[a]&sets[b] for a in range(3) for b in range(a)):raise ValueError('Collapsed pattern crossed retained partitions')
    if any(not indices for indices in kept):raise ValueError('Empty retained partition')
    return kept,reasons

def percentile(values,q):
    position=q*(len(values)-1);i=int(position);f=position-i
    return values[i]*(1-f)+values[min(i+1,len(values)-1)]*f

def interval(records,trials=5000):
    groups=C.defaultdict(lambda:[0.,0])
    for r in records:
        g=groups[canonical(r['encoded'])];g[0]+=r['baseline_total_bits']-r['selected_total_bits'];g[1]+=r['tokens']
    values=list(groups.values());rng=random.Random(20261017);draws=[]
    for _ in range(trials):
        selected=[values[rng.randrange(len(values))] for _ in values]
        draws.append(sum(v[0] for v in selected)/sum(v[1] for v in selected))
    draws.sort()
    return {'groups':len(values),'trials':trials,'seed':20261017,
            'gain_bits_per_token':sum(v[0] for v in values)/sum(v[1] for v in values),
            'percentile95':[percentile(draws,.025),percentile(draws,.975)],
            'percentile98_75_four_comparison_sensitivity':[percentile(draws,.00625),percentile(draws,.99375)],
            'scope':'Corpus-conditional canonical collapsed-pattern bootstrap; not verified artifact families or language evidence.'}

def evaluate(parts,labels,original,source,old):
    uni,bi=costs(source);kept,reasons=retain_novel(parts)
    filtered=[[rows[i] for i in ids] for rows,ids in zip(parts,kept)]
    baseline=rank_key(parts[0],K);training=statistics(parts[0],K+1);validation=statistics(filtered[1],K+1)
    runs=[]
    for r in old['runs']:
        key=r['key_indices'];loss=score(training,key,uni,bi)
        if not math.isclose(loss,r['train_bits'],abs_tol=1e-12,rel_tol=1e-12):raise ValueError('Frozen training key/loss changed')
        runs.append({'start':r['start'],'key_indices':key,'train_bits':loss,'retained_validation_bits':score(validation,key,uni,bi)})
    chosen=min(range(len(runs)),key=lambda i:(round(runs[i]['retained_validation_bits'],12),i));key=runs[chosen]['key_indices']
    old_key=next(r['key_indices'] for r in runs if r['start']==old['selected_start'])
    test=[]
    for i in kept[2]:
        t=parts[2][i];st=statistics([t],K+1)
        test.append({'original_split_index':i,'source':list(original[2][i]),'encoded':t,'tokens':len(t),
                     'baseline_total_bits':objective(st,baseline,uni,bi),'selected_total_bits':objective(st,key,uni,bi),
                     'original_key_total_bits':objective(st,old_key,uni,bi)})
    total=sum(r['tokens'] for r in test)
    assignments=[{'partition':name,'rows':[{'original_split_index':i,'source':list(original[p][i]),'encoded':t,'status':reasons[p][i]} for i,t in enumerate(rows)]} for p,(name,rows) in enumerate(zip(NAMES,parts))]
    out={'original_split_sizes':dict(zip(NAMES,map(len,parts))),'retained_sizes':dict(zip(NAMES,map(len,filtered))),
         'exclusion_counts':{name:dict(C.Counter(x for x in reason if x!='retained')) for name,reason in zip(NAMES,reasons)},
         'mapped_token_fraction':{name:sum(s<K for t in rows for s in t)/sum(map(len,rows)) for name,rows in zip(NAMES,filtered)},
         'retained_pattern_counts':{name:len({canonical(t) for t in rows}) for name,rows in zip(NAMES,filtered)},
         'all_retained_pattern_sets_disjoint':True,'training_source_labels':list(labels),'runs':runs,'selected_start':runs[chosen]['start'],
         'original_selected_start':old['selected_start'],'frequency_test_bits':sum(r['baseline_total_bits'] for r in test)/total,
         'selected_test_bits':sum(r['selected_total_bits'] for r in test)/total,'original_key_same_subset_test_bits':sum(r['original_key_total_bits'] for r in test)/total,
         'gain':interval(test),'test_rows':test,'assignments':assignments,
         'scope':'Retrospective novel-pattern subset of an already scored corpus; narrow conditional unit hypothesis, not a reading.'}
    if 'known_cipher_diagnostic' in old:
        truth=old['known_cipher_diagnostic']['secret_key_for_audit'];counts=C.Counter(s for t in filtered[2] for s in t if s<K)
        out['known_cipher_diagnostic']={'key_accuracy':sum(key[i]==truth[i] for i in range(K))/K,
            'covered_token_accuracy':sum(n for i,n in counts.items() if key[i]==truth[i])/sum(counts.values()),
            'all_original_rows_retained':all(len(ids)==len(rows) for ids,rows in zip(kept,parts)),
            'test_score_matches_previous':math.isclose(out['selected_test_bits'],old['selected_test_bits'],abs_tol=1e-12,rel_tol=1e-12)}
        if not out['known_cipher_diagnostic']['all_original_rows_retained'] or not out['known_cipher_diagnostic']['test_score_matches_previous']:raise ValueError('Unexpected positive-control change')
    return out

def main():
    path=ROOT/'data/substitution';manifest=json.loads((path/'manifest.json').read_text());raw=gzip.decompress((path/'inputs.json.gz').read_bytes())
    if hashlib.sha256(raw).hexdigest()!=manifest['sha256_uncompressed']:raise ValueError('Source-count input drift')
    inputs=json.loads(raw);previous=json.loads((ROOT/'results/substitution_search.json').read_text())
    indus=[r['signs'] for r in json.loads((ROOT/'data/processed/icit_unique.json').read_text())]
    admin=[r['signs'] for r in json.loads((ROOT/'results/administrative_control.json').read_text())['realizations']['17']['records']]
    cases={'Indus':encode_case(indus),'nonphonetic_control':encode_case(admin)}
    result={'design':'docs/EXPERIMENT_018.md','source_input_sha256':manifest['sha256_uncompressed'],'languages':{},'scope':'Retrospective leakage sensitivity; no new independent holdout or validated phonetic key.'}
    for language,source in inputs['languages'].items():
        parts=split(source['cipher_texts'],42);labels=[f'C{i:02}' for i in range(K)]
        datasets={'known_cipher':(parts,labels,parts),**cases};result['languages'][language]={}
        for name,(parts,labels,original) in datasets.items():
            r=evaluate(parts,labels,original,source,previous['languages'][language][name]);result['languages'][language][name]=r
            print(language,name,r['retained_sizes'],r['selected_start'],r['gain'],flush=True)
    save('novel_pattern_substitution.json',result)
if __name__=='__main__':main()

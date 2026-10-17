"""Calibrated bijective proxy-unit recoding; no historical readings are adopted."""
import collections as C
import gzip
import hashlib
import json
import math
import random
import statistics as S
from analyze import ROOT,canonical,save,split
K=32

def statistics(texts,n):
    initial=[0]*n;bi=[[0]*n for _ in range(n)];tokens=0
    for t in texts:
        if t:initial[t[0]]+=1
        tokens+=len(t)
        for a,b in zip(t,t[1:]):bi[a][b]+=1
    return {'initial':initial,'bi':bi,'tokens':tokens}

def costs(source):
    uni=source['unigram_counts'];bi=source['bigram_counts'];total=sum(uni);n=len(uni)
    p=[(c+.5)/(total+.5*n) for c in uni]
    return [-math.log2(v) for v in p],[[-math.log2((c+20*p[j])/(sum(row)+20)) for j,c in enumerate(row)] for row in bi]

def objective(stats,key,uni,bi):
    return sum(c*uni[key[i]] for i,c in enumerate(stats['initial']))+sum(c*bi[key[i]][key[j]] for i,row in enumerate(stats['bi']) for j,c in enumerate(row))

def swap_delta(stats,key,a,b,uni,bi):
    ka,kb=key[a],key[b];m=stats['bi'];initial=stats['initial']
    value=initial[a]*(uni[kb]-uni[ka])+initial[b]*(uni[ka]-uni[kb])
    for j,kj in enumerate(key):
        new=kb if j==a else ka if j==b else kj
        value+=m[a][j]*(bi[kb][new]-bi[ka][kj])+m[b][j]*(bi[ka][new]-bi[kb][kj])
        if j!=a and j!=b:value+=m[j][a]*(bi[kj][kb]-bi[kj][ka])+m[j][b]*(bi[kj][ka]-bi[kj][kb])
    return round(value,8)

def rank_key(texts,k):
    freq=C.Counter(s for t in texts for s in t);order=sorted(range(k),key=lambda i:(-freq[i],i));key=[0]*(k+1)
    for target,source in enumerate(order):key[source]=target
    key[k]=k;return key

def optimize(stats,start,uni,bi,seed,steps=20000):
    key=list(start);k=len(key)-1;rng=random.Random(seed);current=objective(stats,key,uni,bi);best=current;best_key=list(key)
    for step in range(steps):
        a,b=rng.sample(range(k),2);delta=swap_delta(stats,key,a,b,uni,bi)
        temperature=20*(.05/20)**(step/max(1,steps-1))
        if delta<=0 or rng.random()<math.exp(-delta/temperature):
            key[a],key[b]=key[b],key[a];current+=delta
            if current<best-1e-6:
                exact=objective(stats,key,uni,bi)
                if round(exact,8)<round(best,8):best=exact;best_key=list(key)
        if step%200==0:current=objective(stats,key,uni,bi)
    key=best_key
    for _ in range(2):
        changed=False
        for a in range(k):
            for b in range(a+1,k):
                if swap_delta(stats,key,a,b,uni,bi)<0:key[a],key[b]=key[b],key[a];changed=True
        if not changed:break
    return key

def score(stats,key,uni,bi):return objective(stats,key,uni,bi)/stats['tokens']

def encode_case(texts):
    full=split(texts,42);freq=C.Counter(s for t in full[0] for s in t);vocab=sorted(freq,key=lambda s:(-freq[s],s))[:K]
    if len(vocab)!=K:raise ValueError('Too few input signs')
    enc={s:i for i,s in enumerate(vocab)}
    return [[[enc.get(s,K) for s in t] for t in part] for part in full],vocab,full

def solve(parts,labels,source,original=None,truth=None):
    uni,bi=costs(source);stats=[statistics(part,K+1) for part in parts];baseline=rank_key(parts[0],K);starts=[('frequency',baseline,7)]
    for seed in (17,29,43,59):
        key=list(range(K));random.Random(seed).shuffle(key);starts.append((str(seed),key+[K],seed))
    runs=[]
    for name,start,seed in starts:
        key=optimize(stats[0],start,uni,bi,seed)
        runs.append({'start':name,'key_indices':key,'train_bits':score(stats[0],key,uni,bi),'validation_bits':score(stats[1],key,uni,bi)})
    selected=min(range(len(runs)),key=lambda i:(round(runs[i]['validation_bits'],12),i));key=runs[selected]['key_indices']
    # Test is scored after validation selection. Other restart tests are diagnostics only.
    for r in runs:r['test_bits_diagnostic_only']=score(stats[2],r['key_indices'],uni,bi)
    randoms=[]
    for seed in range(1000,1020):
        rk=list(range(K));random.Random(seed).shuffle(rk);rk.append(K)
        randoms.append({'seed':seed,'train_bits':score(stats[0],rk,uni,bi),'validation_bits':score(stats[1],rk,uni,bi),'test_bits':score(stats[2],rk,uni,bi)})
    pairs=[sum(a==b for a,b in zip(runs[i]['key_indices'][:K],runs[j]['key_indices'][:K]))/K for i in range(len(runs)) for j in range(i)]
    training={canonical(t) for t in parts[0]};test=parts[2]
    out={'split_sizes':dict(zip(('train','validation','test'),map(len,parts))),
         'mapped_token_fraction':{name:sum(s<K for t in part for s in t)/sum(map(len,part)) for name,part in zip(('train','validation','test'),parts)},
         'collapsed_test_patterns_seen_in_train':sum(canonical(t) in training for t in test),'runs':runs,'selected_start':runs[selected]['start'],
         'frequency_baseline':{name:score(st,baseline,uni,bi) for name,st in zip(('train','validation','test'),stats)},
         'random_baselines':randoms,'random_test_mean':S.mean(r['test_bits'] for r in randoms),
         'selected_test_bits':score(stats[2],key,uni,bi),'test_gain_vs_frequency':score(stats[2],baseline,uni,bi)-score(stats[2],key,uni,bi),
         'mean_pairwise_key_agreement':S.mean(pairs),
         'conditional_key':[{'source_id':str(s),'proxy_writing_unit':source['units'][key[i]],'target_rank':key[i]} for i,s in enumerate(labels)],
         'first20_test_hypothetical_recodings':[{'source':list(original[2][i]) if original is not None else [labels[s] if s<K else '<UNK>' for s in t],
                    'hypothetical_units':[source['units'][key[s]] if s<K else '<UNK>' for s in t]} for i,t in enumerate(test[:20])],
         'scope':'Conditional bijective writing-unit hypotheses; no translations or accepted historical sound values. UNK slots retained.'}
    if truth is not None:
        weights=C.Counter(s for t in test for s in t if s<K);true=truth+[K]
        out['known_cipher_diagnostic']={'key_accuracy':sum(a==b for a,b in zip(key[:K],truth))/K,
            'covered_test_token_accuracy':sum(n for i,n in weights.items() if key[i]==truth[i])/sum(weights.values()),
            'frequency_key_accuracy':sum(a==b for a,b in zip(baseline[:K],truth))/K,
            'true_key_test_bits':score(stats[2],true,uni,bi),'true_key_train_bits':score(stats[0],true,uni,bi),
            'secret_key_for_audit':truth,'scope':'Truth consulted only after search and validation selection, never passed into optimizer.'}
    return out

def main():
    folder=ROOT/'data/substitution';manifest=json.loads((folder/'manifest.json').read_text());raw=gzip.decompress((folder/'inputs.json.gz').read_bytes())
    if hashlib.sha256(raw).hexdigest()!=manifest['sha256_uncompressed']:raise ValueError('Substitution input drift')
    inputs=json.loads(raw);indus=[r['signs'] for r in json.loads((ROOT/'data/processed/icit_unique.json').read_text())]
    admin=[r['signs'] for r in json.loads((ROOT/'results/administrative_control.json').read_text())['realizations']['17']['records']]
    ip,il,io=encode_case(indus);ap,al,ao=encode_case(admin)
    output={'design':'docs/EXPERIMENT_017.md','alphabet_size':K,'search_steps_per_start':20000,'restarts':5,'languages':{},
            'scope':'Proxy writing-unit substitution under a narrow artificial channel; language-family and real-key accuracy are not identifiable from these scores.'}
    for language,source in inputs['languages'].items():
        # Positive calibration precedes unknown and non-phonetic inputs.
        print(language,'known cipher',flush=True)
        control=solve(split(source['cipher_texts'],42),[f'C{i:02}' for i in range(K)],source,truth=source['secret_key_diagnostic_only'])
        print(language,'Indus',flush=True);actual=solve(ip,il,source,io)
        print(language,'administrative control',flush=True);negative=solve(ap,al,source,ao)
        output['languages'][language]={'target_unit_labels':source['units'],'target_known_token_fraction':source['target_known_token_fraction'],
            'model_document_count':len(source['lm_document_ids']),'calibration_source_document_count':len(source['held_document_ids']),
            'known_cipher':control,'Indus':actual,'nonphonetic_control':negative}
        print(language,{name:(r['selected_test_bits'],r['test_gain_vs_frequency'],r['mean_pairwise_key_agreement']) for name,r in [('cipher',control),('Indus',actual),('admin',negative)]},flush=True)
    save('substitution_search.json',output)
if __name__=='__main__':main()

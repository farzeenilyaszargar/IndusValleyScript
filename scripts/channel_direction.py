"""Retrospective validation-only direction selection for frozen glyph channels."""
import collections as C
import gzip
import hashlib
import json
import math
import random
import statistics as S
from analyze import ROOT,save
from homophonic_channel import Channel,K,UNK,homophones,mean_loss,optimize,prepare
from substitution_search import costs
EXPECTED_KEYS='65212253eaa1c20f7e149adc5c5673ab9f0dc9c122721385520ee398c8d6b4a3'
DIRECTIONS=('stored','reverse_stored')

def key_digest(previous):
    payload={l:{n:{'source_ids':[x['source_id'] for x in v['conditional_key']],'keys':{x['start']:x['key_indices'] for x in v['runs']}} for n,v in cases.items()} for l,cases in previous['languages'].items()}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def oriented_parts(parts,reverse):return [[list(reversed(t)) if reverse else list(t) for t in rows] for rows in parts]

def select(candidates):
    return min(range(len(candidates)),key=lambda i:(round(candidates[i]['validation_bits'],12),candidates[i]['direction_index'],candidates[i]['start_index']))

def baseline_rows(model,texts):
    total=sum(model.freq);n=len(model.freq);p=[(f+.5)/(total+.5*n) for f in model.freq]
    edge=dict(model.edges);row=C.Counter()
    for (a,b),c in model.edges:row[a]+=c
    out=[]
    for t in texts:
        u=-sum(math.log2(p[s]) for s in t)
        b=-math.log2(p[t[0]])-sum(math.log2((edge.get((a,z),0)+20*p[z])/(row[a]+20)) for a,z in zip(t,t[1:]))
        out.append({'tokens':len(t),'unigram_total_bits':u,'bigram_total_bits':b})
    return out

def average(rows,field):return sum(r[field] for r in rows)/sum(r['tokens'] for r in rows)

def bootstrap(rows,field,trials=5000):
    grouped=C.defaultdict(lambda:[0.,0])
    for r in rows:
        grouped[r['component']][0]+=r[field]-r['channel_total_bits'];grouped[r['component']][1]+=r['tokens']
    groups=[{'component':g,'gain_total_bits':v[0],'tokens':v[1]} for g,v in sorted(grouped.items())]
    rng=random.Random(20261018);values=[]
    for _ in range(trials):
        selected=[groups[rng.randrange(len(groups))] for _ in groups]
        values.append(sum(g['gain_total_bits'] for g in selected)/sum(g['tokens'] for g in selected))
    values.sort()
    def q(p):
        at=p*(len(values)-1);i=int(at);f=at-i
        return values[i]*(1-f)+values[min(i+1,len(values)-1)]*f
    return {'gain_bits_per_token':sum(g['gain_total_bits'] for g in groups)/sum(g['tokens'] for g in groups),
            'percentile95':[q(.025),q(.975)],'percentile98_75_indus_four_comparison_sensitivity':[q(.00625),q(.99375)],
            'groups':groups,'trials':trials,'seed':20261018,
            'scope':'Original similarity-component bootstrap; corpus conditional, selection uncertainty not fully included. 98.75% family correction is specified only for four Indus comparisons.'}

def reverse_fit(parts,labels,source):
    uni,bi=costs(source);model=Channel(parts[0],len(labels),uni,bi);n=len(labels)
    starts=[('cyclic',[i%K for i in range(n)]+[K],7)]
    for seed in (17,29,43,59):
        key=[i%K for i in range(n)];random.Random(seed).shuffle(key);starts.append((str(seed),key+[K],seed))
    runs=[]
    for name,start,seed in starts:
        key=optimize(model,start,seed)
        runs.append({'start':name,'key_indices':key,'train_bits':model.objective(key)/sum(model.freq),'validation_bits':mean_loss(model.losses(parts[1],key))})
    return model,runs

def evaluate(prepared,source,previous,truth=None):
    parts,labels,original,meta=prepared;uni,bi=costs(source);models=[Channel(parts[0],len(labels),uni,bi)];oriented=[oriented_parts(parts,False),oriented_parts(parts,True)]
    forward=[]
    if labels!=[r['source_id'] for r in previous['conditional_key']]:raise ValueError('Frozen source index changed')
    for r in previous['runs']:
        for actual,stored in ((models[0].objective(r['key_indices'])/sum(models[0].freq),r['train_bits']),
                              (mean_loss(models[0].losses(parts[1],r['key_indices'])),r['validation_bits'])):
            if not math.isclose(actual,stored,abs_tol=1e-12,rel_tol=1e-12):raise ValueError('Frozen training/validation score drift')
        forward.append({k:r[k] for k in ('start','key_indices','train_bits','validation_bits')})
    reverse_model,reverse=reverse_fit(oriented[1],labels,source);models.append(reverse_model);runs=[forward,reverse]
    candidates=[{'direction_index':d,'direction':DIRECTIONS[d],'start_index':i,**r} for d,rr in enumerate(runs) for i,r in enumerate(rr)]
    chosen=select(candidates);selected=candidates[chosen];direction=selected['direction_index'];key=selected['key_indices']
    # Both channel and generic bigram choices use validation only, before new test scoring.
    val_baseline=[baseline_rows(m,pp[1]) for m,pp in zip(models,oriented)]
    baseline_direction=min(range(2),key=lambda d:(round(average(val_baseline[d],'bigram_total_bits'),12),d))
    loss=models[direction].losses(oriented[direction][2],key)
    test_baseline=[baseline_rows(m,pp[2]) for m,pp in zip(models,oriented)]
    if not math.isclose(average(test_baseline[0],'unigram_total_bits'),average(test_baseline[1],'unigram_total_bits'),abs_tol=1e-12,rel_tol=1e-12):raise ValueError('Unigram changed under reversal')
    for r in candidates:r['test_bits_diagnostic_only']=mean_loss(models[r['direction_index']].losses(oriented[r['direction_index']][2],r['key_indices']))
    old_best=next(r for r in candidates if r['direction_index']==0 and r['start']==previous['selected_start'])
    if not math.isclose(old_best['test_bits_diagnostic_only'],previous['test_bits'],abs_tol=1e-12,rel_tol=1e-12):raise ValueError('Frozen forward test changed')
    rows=[]
    for i,r in enumerate(loss):
        rows.append({'original_test_index':i,'component':meta['test_group_ids'][i],'source_stored_order':original[2][i],
                     'tokens':r['tokens'],'channel_total_bits':r['total_bits'],'channel_language_bits':r['language_bits'],'channel_emission_bits':r['emission_bits'],
                     'unigram_total_bits':test_baseline[0][i]['unigram_total_bits'],'bigram_total_bits':test_baseline[baseline_direction][i]['bigram_total_bits']})
    enc={s:i for i,s in enumerate(labels)};n=len(labels)
    out={'split_reference':'results/homophonic_channel.json','split_sizes':meta['split_sizes'],'components':meta['components'],
         'known_source_token_fraction':meta['known_source_token_fraction'],'source_labels':labels,'candidates':candidates,
         'selected_direction':DIRECTIONS[direction],'selected_start':selected['start'],'selected_validation_bits':selected['validation_bits'],
         'selected_test_bits':average(rows,'channel_total_bits'),'test_language_bits':average(rows,'channel_language_bits'),'test_emission_bits':average(rows,'channel_emission_bits'),
         'stored_selected_test_bits':previous['test_bits'],'generic_bigram_selected_direction':DIRECTIONS[baseline_direction],
         'generic_validation_bits_by_direction':{DIRECTIONS[d]:average(val_baseline[d],'bigram_total_bits') for d in range(2)},
         'unigram_test_bits':average(rows,'unigram_total_bits'),'bigram_test_bits':average(rows,'bigram_total_bits'),
         'gain_vs_unigram':bootstrap(rows,'unigram_total_bits'),'gain_vs_bigram':bootstrap(rows,'bigram_total_bits'),
         'within_direction_key_agreement':{DIRECTIONS[d]:S.mean(sum(a==b for a,b in zip(rr[i]['key_indices'][:n],rr[j]['key_indices'][:n]))/n for i in range(5) for j in range(i)) for d,rr in enumerate(runs)},
         'conditional_key':[{'source_id':s,'proxy_writing_unit':source['units'][key[i]],'target_rank':key[i]} for i,s in enumerate(labels)],
         'test_rows':rows,'first20_hypothetical_recodings':[{'source_stored_order':t,'evaluated_order':DIRECTIONS[direction],
            'units':[source['units'][key[enc[s]]] if s in enc else UNK for s in (t[::-1] if direction else t)]} for t in original[2][:20]],
         'scope':'Retrospective stored-vs-reverse sensitivity; neither absolute archaeological direction nor sound values identified.'}
    if truth is not None:
        real=[truth[s] for s in labels];counts=C.Counter(s for t in parts[2] for s in t if s<n);num=den=0
        for t,encoded in zip(original[2],oriented[direction][2]):
            decoded=[key[s] for s in encoded]
            for s,pred in zip(t,decoded):
                if s in enc:num+=pred==truth[s];den+=1
        out['known_cipher_diagnostic']={'original_direction_selected':direction==0,'key_accuracy':sum(a==b for a,b in zip(real,key))/n,
            'covered_test_symbol_accuracy':sum(v for s,v in counts.items() if key[s]==real[s])/sum(counts.values()),
            'original_order_covered_sequence_token_accuracy':num/den,'scope':'Truth used after joint validation selection only.'}
    return out

def main():
    folder=ROOT/'data/substitution';manifest=json.loads((folder/'manifest.json').read_text());raw=gzip.decompress((folder/'inputs.json.gz').read_bytes())
    if hashlib.sha256(raw).hexdigest()!=manifest['sha256_uncompressed']:raise ValueError('Frozen target input drift')
    source=json.loads(raw);previous=json.loads((ROOT/'results/homophonic_channel.json').read_text())
    if key_digest(previous)!=EXPECTED_KEYS:raise ValueError('Frozen forward key/source digest mismatch')
    indus=[r['signs'] for r in json.loads((ROOT/'data/processed/icit_unique.json').read_text())]
    admin=[r['signs'] for r in json.loads((ROOT/'results/administrative_control.json').read_text())['realizations']['17']['records']]
    ip,ap=prepare(indus),prepare(admin);out={'design':'docs/EXPERIMENT_020.md','forward_key_sha256':EXPECTED_KEYS,'languages':{}}
    for lang,profile in source['languages'].items():
        text,truth=homophones(profile);out['languages'][lang]={}
        for name,prepared,answer in (('known_homophonic_cipher',prepare(text),truth),('Indus',ip,None),('nonphonetic_control',ap,None)):
            print(lang,name,'fit reverse',flush=True);r=evaluate(prepared,profile,previous['languages'][lang][name],answer);out['languages'][lang][name]=r
            print(lang,name,r['selected_direction'],r['selected_test_bits'],r['unigram_test_bits'],r['bigram_test_bits'],r.get('known_cipher_diagnostic'),flush=True)
    save('channel_direction.json',out)
if __name__=='__main__':main()

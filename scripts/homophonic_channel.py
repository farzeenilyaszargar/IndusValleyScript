"""Full training-vocabulary deterministic homophonic channel, not decipherment."""
import collections as C
import gzip
import hashlib
import json
import math
import random
import statistics as S
from analyze import ROOT,canonical,save
from near_copy import components
from substitution_search import costs
K=32
UNK='<UNK>'

class Channel:
    def __init__(self,texts,n,uni,bi):
        self.n=n;self.uni=uni;self.bi=bi
        self.freq=[0]*(n+1);self.initial=[0]*(n+1);edges=C.Counter()
        for t in texts:
            self.initial[t[0]]+=1
            for s in t:self.freq[s]+=1
            edges.update(zip(t,t[1:]))
        self.edges=sorted(edges.items());self.incident=[set() for _ in range(n+1)]
        for i,((a,b),_) in enumerate(self.edges):self.incident[a].add(i);self.incident[b].add(i)
        self.weights=[f+.5 for f in self.freq]
        self.constant=sum(f*math.log2(w) for f,w in zip(self.freq[:n],self.weights[:n]))
    def groups(self,key):
        freq=[0]*K;size=[0]*K
        for i,g in enumerate(key[:self.n]):freq[g]+=self.freq[i];size[g]+=1
        if not all(size):raise ValueError('Key is not surjective')
        return freq,size
    def objective(self,key):
        f,s=self.groups(key)
        language=sum(c*self.uni[key[i]] for i,c in enumerate(self.initial))
        language+=sum(c*self.bi[key[a]][key[b]] for (a,b),c in self.edges)
        emission=sum(c*math.log2(c+.5*size) for c,size in zip(f,s))-self.constant
        return language+emission
    def delta(self,key,f,size,changes):
        changes={i:g for i,g in changes.items() if g!=key[i]}
        df=C.Counter();ds=C.Counter();edges=set();value=0.
        for i,g in changes.items():
            old=key[i];df[old]-=self.freq[i];df[g]+=self.freq[i];ds[old]-=1;ds[g]+=1
            edges.update(self.incident[i]);value+=self.initial[i]*(self.uni[g]-self.uni[old])
        for g in set(df)|set(ds):
            if size[g]+ds[g]==0:return None
            nf=f[g]+df[g];ns=size[g]+ds[g]
            value+=nf*math.log2(nf+.5*ns)-f[g]*math.log2(f[g]+.5*size[g])
        for j in sorted(edges):
            (a,b),c=self.edges[j]
            value+=c*(self.bi[changes.get(a,key[a])][changes.get(b,key[b])]-self.bi[key[a]][key[b]])
        return round(value,8)
    def apply(self,key,f,size,changes):
        for i,g in changes.items():
            old=key[i];f[old]-=self.freq[i];size[old]-=1;f[g]+=self.freq[i];size[g]+=1;key[i]=g
    def losses(self,texts,key):
        f,size=self.groups(key);emission=[math.log2(f[key[i]]+.5*size[key[i]])-math.log2(self.weights[i]) for i in range(self.n)]+[0.]
        out=[]
        for t in texts:
            language=self.uni[key[t[0]]]+sum(self.bi[key[a]][key[b]] for a,b in zip(t,t[1:]))
            e=sum(emission[s] for s in t)
            out.append({'tokens':len(t),'language_bits':language,'emission_bits':e,'total_bits':language+e})
        return out

def mean_loss(rows):return sum(r['total_bits'] for r in rows)/sum(r['tokens'] for r in rows)

def optimize(model,start,seed,steps=30000):
    key=list(start);freq,size=model.groups(key);rng=random.Random(seed);current=model.objective(key);best=current;best_key=list(key)
    for step in range(steps):
        if rng.random()<.5:changes={rng.randrange(model.n):rng.randrange(K)}
        else:
            a,b=rng.sample(range(model.n),2);changes={a:key[b],b:key[a]}
        delta=model.delta(key,freq,size,changes)
        if delta is not None:
            temperature=20*(.05/20)**(step/max(1,steps-1))
            if delta<=0 or rng.random()<math.exp(-delta/temperature):
                model.apply(key,freq,size,changes);current+=delta
                if current<best-1e-6:
                    exact=model.objective(key)
                    if round(exact,8)<round(best,8):best=exact;best_key=list(key)
        if step%200==0:current=model.objective(key)
    key=best_key;freq,size=model.groups(key)
    for _ in range(2):
        changed=False
        for i in range(model.n):
            for g in range(K):
                d=model.delta(key,freq,size,{i:g})
                if d is not None and d<0:model.apply(key,freq,size,{i:g});changed=True
        if not changed:break
    return key

def prepare(texts):
    groups=components(texts);random.Random(42).shuffle(groups);a,b=int(.8*len(groups)),int(.9*len(groups))
    assign={t:p for p,gs in enumerate((groups[:a],groups[a:b],groups[b:])) for group in gs for t in group}
    original=[[t for t in texts if assign[canonical(t)]==p] for p in range(3)]
    if any(not rows for rows in original):raise ValueError('Empty similarity-component partition')
    count=C.Counter(s for t in original[0] for s in t if s!=UNK);labels=sorted(count,key=lambda s:(-count[s],s));enc={s:i for i,s in enumerate(labels)}
    if len(labels)<K:raise ValueError('Source alphabet smaller than target inventory')
    parts=[[[enc.get(s,len(labels)) for s in t] for t in rows] for rows in original]
    component_id={t:i for i,group in enumerate(groups) for t in group}
    metadata={'components':len(groups),'largest_component_canonical_texts':max(map(len,groups)),
              'split_sizes':dict(zip(('train','validation','test'),map(len,parts))),
              'training_sign_types':len(labels),'source_types_entire_input':len({s for t in texts for s in t if s!=UNK}),
              'known_source_token_fraction':{name:sum(s<len(labels) for t in rows for s in t)/sum(map(len,rows)) for name,rows in zip(('train','validation','test'),parts)},
              'component_assignments':[{'component':i,'split':('train','validation','test')[assign[group[0]]],'canonical_source_texts':[list(t) for t in group]} for i,group in enumerate(groups)],
              'test_group_ids':[component_id[canonical(t)] for t in original[2]]}
    known_train={canonical(t) for t in parts[0]};metadata['fixed_unknown_test_patterns_seen_in_train']=sum(canonical(t) in known_train for t in parts[2])
    return parts,labels,original,metadata

def baselines(model,parts):
    freq=model.freq;total=sum(freq);n=len(freq);p=[(f+.5)/(total+.5*n) for f in freq]
    edges=dict(model.edges);row=C.Counter()
    for (a,b),c in model.edges:row[a]+=c
    output={}
    for order in (1,2):
        scores=[]
        for texts in parts:
            loss=0.;tokens=sum(map(len,texts))
            for t in texts:
                loss-=math.log2(p[t[0]])
                for a,b in zip(t,t[1:]):loss-=math.log2(p[b] if order==1 else (edges.get((a,b),0)+20*p[b])/(row[a]+20))
            scores.append(loss/tokens)
        output['unigram' if order==1 else 'bigram'] = dict(zip(('train','validation','test'),scores))
    return output

def solve(prepared,source,truth=None):
    parts,labels,original,meta=prepared;n=len(labels);uni,bi=costs(source);model=Channel(parts[0],n,uni,bi)
    cyclic=[i%K for i in range(n)]+[K];starts=[('cyclic',cyclic,7)]
    for seed in (17,29,43,59):
        key=[i%K for i in range(n)];random.Random(seed).shuffle(key);starts.append((str(seed),key+[K],seed))
    runs=[]
    for name,start,seed in starts:
        key=optimize(model,start,seed)
        runs.append({'start':name,'key_indices':key,'train_bits':model.objective(key)/sum(model.freq),'validation_bits':mean_loss(model.losses(parts[1],key))})
    selected=min(range(len(runs)),key=lambda i:(round(runs[i]['validation_bits'],12),i));key=runs[selected]['key_indices']
    losses=model.losses(parts[2],key);baseline=baselines(model,parts);cyclic_score=mean_loss(model.losses(parts[2],cyclic))
    for r in runs:r['test_bits_diagnostic_only']=mean_loss(model.losses(parts[2],r['key_indices']))
    token_total=sum(map(len,parts[2]));f,size=model.groups(key)
    result={'split':meta,'runs':runs,'selected_start':runs[selected]['start'],'test_bits':mean_loss(losses),
            'test_language_bits':sum(r['language_bits'] for r in losses)/token_total,'test_emission_bits':sum(r['emission_bits'] for r in losses)/token_total,
            'cyclic_test_bits':cyclic_score,'generic_baselines':baseline,'gain_vs_unigram':baseline['unigram']['test']-mean_loss(losses),
            'mean_pairwise_key_agreement':S.mean(sum(a==b for a,b in zip(runs[i]['key_indices'][:n],runs[j]['key_indices'][:n]))/n for i in range(5) for j in range(i)),
            'assigned_glyphs_per_unit':size,'training_tokens_per_unit':f,
            'conditional_key':[{'source_id':s,'target_rank':key[i],'proxy_writing_unit':source['units'][key[i]],'training_tokens':model.freq[i]} for i,s in enumerate(labels)],
            'unseen_source_types_without_key':sorted({s for t in original[1]+original[2] for s in t if s!=UNK and s not in set(labels)}),
            'test_rows':[{'source':original[2][i],'component':meta['test_group_ids'][i],**r} for i,r in enumerate(losses)],
            'first20_hypothetical_recodings':[{'source':original[2][i],'units':[source['units'][key[s]] if s<n else UNK for s in t]} for i,t in enumerate(parts[2][:20])],
            'scope':'Conditional surjective glyph channel; every training ID distinct, unseen source slots unknown, no historical sound values or translations.'}
    if truth is not None:
        counts=C.Counter(s for t in parts[2] for s in t if s<n);real=[truth[s] for s in labels]
        oracle=real+[K];surjective=len(set(real))==K
        result['known_cipher_diagnostic']={'key_accuracy_on_training_types':sum(a==b for a,b in zip(key[:n],real))/n,
              'covered_test_token_accuracy':sum(v for s,v in counts.items() if key[s]==real[s])/sum(counts.values()),
              'true_key_surjective_on_training':surjective,'true_key_test_bits':mean_loss(model.losses(parts[2],oracle)) if surjective else None,
              'truth_for_audit':dict(zip(labels,real)),'scope':'Truth used only after fitting and validation selection.'}
    return result

def homophones(source):
    rng=random.Random(2031);aliases=list(range(2*K));random.Random(1031).shuffle(aliases);truth={f'H{aliases[2*u+v]:02}':u for u in range(K) for v in range(2)}
    inverse=source['secret_key_diagnostic_only'];texts=[]
    for row in source['cipher_texts']:
        texts.append([UNK if c==K else f'H{aliases[2*inverse[c]+rng.randrange(2)]:02}' for c in row])
    return texts,truth

def main():
    folder=ROOT/'data/substitution';manifest=json.loads((folder/'manifest.json').read_text());raw=gzip.decompress((folder/'inputs.json.gz').read_bytes())
    if hashlib.sha256(raw).hexdigest()!=manifest['sha256_uncompressed']:raise ValueError('Frozen target input drift')
    inputs=json.loads(raw);indus=[r['signs'] for r in json.loads((ROOT/'data/processed/icit_unique.json').read_text())]
    admin=[r['signs'] for r in json.loads((ROOT/'results/administrative_control.json').read_text())['realizations']['17']['records']]
    ip,ap=prepare(indus),prepare(admin);out={'design':'docs/EXPERIMENT_019.md','source_input_sha256':manifest['sha256_uncompressed'],'languages':{},'steps_per_start':30000,'restarts':5}
    for lang,source in inputs['languages'].items():
        text,truth=homophones(source);out['languages'][lang]={}
        for name,prepared,answer in (('known_homophonic_cipher',prepare(text),truth),('Indus',ip,None),('nonphonetic_control',ap,None)):
            print(lang,name,'start',flush=True);r=solve(prepared,source,answer);out['languages'][lang][name]=r
            print(lang,name,'done',r['test_bits'],r['gain_vs_unigram'],r.get('known_cipher_diagnostic',{}).get('covered_test_token_accuracy'),flush=True)
    save('homophonic_channel.json',out)
if __name__=='__main__':main()

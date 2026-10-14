"""Generative HMM with explicit stopping, scaled forward/backward, and EM."""
import collections as C
import copy
import itertools
import json
import math
import random
from analyze import ROOT, Model, avg_loss, canonical, save, split

def normalized(values):
    total=sum(values)
    return [v/total for v in values]

class HMM:
    def __init__(self,texts,states,seed):
        self.k=states
        self.vocab=sorted({s for t in texts for s in t}|{'<UNK>'})
        self.index={s:i for i,s in enumerate(self.vocab)}
        counts=C.Counter(s for t in texts for s in t)
        self.prior=normalized([counts[s]+.5 for s in self.vocab])
        rng=random.Random(seed)
        self.start=normalized([rng.uniform(.5,1.5) for _ in range(states)])
        self.emission=[normalized([p*rng.uniform(.2,2) for p in self.prior]) for _ in range(states)]
        length=sum(map(len,texts))/len(texts)
        self.stop=[1/length]*states
        self.transition=[]
        for i in range(states):
            row=normalized([rng.uniform(.5,1.5) for _ in range(states)])
            self.transition.append([p*(1-self.stop[i]) for p in row])

    def encode(self,t):
        return [self.index.get(s,self.index['<UNK>']) for s in t]

    def forward(self,x):
        if not x:raise ValueError('HMM expects nonempty sequences')
        row=[self.start[j]*self.emission[j][x[0]] for j in range(self.k)]
        scale=sum(row);alpha=[[v/scale for v in row]];scales=[scale]
        for token in x[1:]:
            row=[self.emission[j][token]*sum(alpha[-1][i]*self.transition[i][j] for i in range(self.k))
                 for j in range(self.k)]
            scale=sum(row);alpha.append([v/scale for v in row]);scales.append(scale)
        terminal=sum(alpha[-1][j]*self.stop[j] for j in range(self.k))
        loss=-sum(math.log2(s) for s in scales)-math.log2(terminal)
        return alpha,scales,terminal,loss

    def posterior(self,x):
        alpha,scales,terminal,loss=self.forward(x)
        beta=[[0.0]*self.k for _ in x]
        beta[-1]=[s/terminal for s in self.stop]
        for pos in range(len(x)-2,-1,-1):
            beta[pos]=[sum(self.transition[i][j]*self.emission[j][x[pos+1]]*beta[pos+1][j]
                           for j in range(self.k))/scales[pos+1] for i in range(self.k)]
        gamma=[[alpha[pos][j]*beta[pos][j] for j in range(self.k)] for pos in range(len(x))]
        xi=[]
        for pos in range(len(x)-1):
            xi.append([[alpha[pos][i]*self.transition[i][j]*self.emission[j][x[pos+1]]*beta[pos+1][j]
                        /scales[pos+1] for j in range(self.k)] for i in range(self.k)])
        return gamma,xi,loss

    def step(self,texts):
        starts=[.5]*self.k;stops=[.5]*self.k
        trans=[[.5]*self.k for _ in range(self.k)]
        emits=[[5*p for p in self.prior] for _ in range(self.k)]
        for t in texts:
            x=self.encode(t);gamma,xi,_=self.posterior(x)
            for j in range(self.k):
                starts[j]+=gamma[0][j];stops[j]+=gamma[-1][j]
                for pos,token in enumerate(x):emits[j][token]+=gamma[pos][j]
            for matrix in xi:
                for i in range(self.k):
                    for j in range(self.k):trans[i][j]+=matrix[i][j]
        self.start=normalized(starts)
        self.emission=[normalized(row) for row in emits]
        for i in range(self.k):
            total=sum(trans[i])+stops[i]
            self.stop[i]=stops[i]/total
            self.transition[i]=[n/total for n in trans[i]]

    def losses(self,texts):
        return [(self.forward(self.encode(t))[-1],len(t)+1) for t in texts]

def paired_interval(texts,left,right,seed=42,group_keys=None):
    grouped=C.defaultdict(lambda:[0.0,0])
    keys=group_keys if group_keys is not None else [canonical(t) for t in texts]
    for key,a,b in zip(keys,left,right):
        grouped[key][0]+=a[0]-b[0]
        grouped[key][1]+=a[1]
    values=list(grouped.values());rng=random.Random(seed)
    samples=sorted(avg_loss(rng.choices(values,k=len(values))) for _ in range(500))
    return {'improvement_bits':avg_loss(values),'bootstrap95':[samples[12],samples[487]],
            'resampling_unit':'provided component' if group_keys is not None else 'exact/reverse group','groups':len(values)}

def main():
    records=json.loads((ROOT/'data/processed/icit_unique.json').read_text())
    texts=[r['signs'] for r in records]
    train,val,test=split(texts,42)
    candidates=[];best=None;selected=None
    for k in (2,4,8):
        for seed in (17,29):
            model=HMM(train,k,seed)
            for iteration in range(1,21):
                model.step(train)
                if iteration in (5,10,20):
                    row={'states':k,'initialization_seed':seed,'iteration':iteration,
                         'training_bits':avg_loss(model.losses(train)),
                         'validation_bits':avg_loss(model.losses(val))}
                    candidates.append(row)
                    print(json.dumps(row),flush=True)
                    if selected is None or row['validation_bits']<selected['validation_bits']:
                        best=copy.deepcopy(model);selected=row.copy()
    baseline=min((Model(train,2,s) for s in (1,5,20,100)),key=lambda m:avg_loss(m.losses(val)))
    hmm_loss=best.losses(test);bigram_loss=baseline.losses(test)
    result={'design':'docs/EXPERIMENT_002.md','split_seed':42,'train':len(train),'validation':len(val),'test':len(test),
            'selection':'validation loss only, state count/initialization/checkpoint selected from 18 candidates',
            'candidates':candidates,'selected':selected,'hmm_test_bits':avg_loss(hmm_loss),
            'bigram_test_bits':avg_loss(bigram_loss),'bigram_strength':baseline.strength,
            'hmm_vs_bigram':paired_interval(test,bigram_loss,hmm_loss),
            'unknown_test_tokens':sum(s not in best.index for t in test for s in t),
            'scoring':'Generative sign sequence plus STOP; denominator signs+1; unseen IDs map to one UNK event',
            'limitation':'Single reused exploratory test split; compact tested grammar, not a decipherment or semantic model.'}
    save('latent_grammar.json',result)
    profiles=[C.Counter() for _ in range(best.k)]
    for t in train:
        gamma,_,_=best.posterior(best.encode(t))
        for pos,row in enumerate(gamma):
            role='singleton' if len(t)==1 else 'initial' if pos==0 else 'final' if pos==len(t)-1 else 'medial'
            for j,w in enumerate(row):profiles[j][role]+=w
    save('latent_grammar_parameters.json',{'vocab':best.vocab,'start':best.start,'stop':best.stop,
        'transition':best.transition,'emission':best.emission,
        'states':[{'state':j,'training_position_mass':dict(profiles[j]),
                   'top_emissions':[{'sign':best.vocab[i],'probability':best.emission[j][i]}
                                    for i in sorted(range(len(best.vocab)),key=lambda i:(-best.emission[j][i],best.vocab[i]))[:12]]}
                  for j in range(best.k)],'warning':'State IDs have no phonetic or semantic values.'})
    print(json.dumps({k:v for k,v in result.items() if k!='candidates'},indent=2))

if __name__=='__main__':main()

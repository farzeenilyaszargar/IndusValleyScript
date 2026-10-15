"""Exact one/two-sign reconstruction, with fixed graphic gap lengths only."""
import collections as C
import heapq
import itertools
import json
import random
from analyze import ROOT, Model, avg_loss, canonical, save, split

class Reconstructor:
    def __init__(self, model):
        self.model=model
        self.candidates=tuple(s for s in model.vocab if s not in ('<EOS>','<UNK>'))
        self.edges={s:{t:model.prob(t,[s]) for t in self.candidates+('<EOS>',)}
                    for s in self.candidates+('<BOS>','<UNK>')}
        self.cache={}
        self.indices={s:i for i,s in enumerate(self.candidates)}

    def fill(self,left,right,length,k=5):
        if length not in (1,2):raise ValueError('Only one/two known sign positions are supported')
        left=left if left in self.edges else '<UNK>'
        right=right if right in self.candidates or right=='<EOS>' else '<UNK>'
        key=(left,right,length,k)
        if key in self.cache:return self.cache[key]
        # Unknown right observations receive their model probability; never a proposed sign.
        right_weight={s:self.model.prob(right,[s]) for s in self.candidates}
        total=0.;best=[]
        for filling in itertools.product(self.candidates,repeat=length):
            weight=self.edges[left][filling[0]]*right_weight[filling[-1]]
            if length==2:weight*=self.edges[filling[0]][filling[1]]
            total+=weight
            if len(best)<k or weight>=best[0][0]:
                item=(weight,tuple(-self.indices[s] for s in filling),filling)
                if len(best)<k:heapq.heappush(best,item)
                elif item>best[0]:heapq.heapreplace(best,item)
        ranked=sorted(best,key=lambda x:(-x[0],x[2]))
        result=[{'signs':list(t),'probability':w/total} for w,_,t in ranked]
        self.cache[key]=result
        return result

def metrics(events):
    n=len(events)
    return {'masks':n,'whole_top1':sum(e['top1'] for e in events)/n,
            'whole_top5':sum(e['top5'] for e in events)/n,
            'top1_token_accuracy':sum(e['correct_tokens'] for e in events)/sum(e['length'] for e in events),
            'whole_truth_in_training_vocabulary':sum(e['truth_covered'] for e in events)/n,
            'mean_top1_conditional_probability':sum(e['candidates'][0]['probability'] for e in events)/n,
            'posterior_bins':[{'lower':lo,'upper':hi,'masks':len(b),
                'observed_top1':sum(e['top1'] for e in b)/len(b) if b else None,
                'mean_probability':sum(e['candidates'][0]['probability'] for e in b)/len(b) if b else None}
                for lo,hi in ((0,.2),(.2,.4),(.4,.6),(.6,.8),(.8,1.00000000001))
                for b in [[e for e in events if lo<=e['candidates'][0]['probability']<hi]]]}

def bootstrap(events,baseline):
    groups=C.defaultdict(lambda:[0,0])
    for a,b in zip(events,baseline):
        assert (a['text'],a['start'],a['length'])==(b['text'],b['start'],b['length'])
        g=groups[canonical(a['text'])];g[0]+=int(a['top1'])-int(b['top1']);g[1]+=1
    values=list(groups.values());rng=random.Random(42)
    samples=[]
    for _ in range(1000):
        draw=rng.choices(values,k=len(values));samples.append(sum(a for a,_ in draw)/sum(b for _,b in draw))
    samples.sort()
    return {'difference':sum(a for a,_ in values)/sum(b for _,b in values),
            'interval95':[samples[24],samples[974]],'groups':len(values),'resamples':1000,
            'unit':'canonical inscription; overlapping masks stay together'}

def main():
    records=json.loads((ROOT/'data/processed/icit_unique.json').read_text())
    train,val,test=split([r['signs'] for r in records],42)
    strength=min((1,5,20,100),key=lambda s:avg_loss(Model(train,2,s).losses(val)))
    results={'design':'docs/EXPERIMENT_011.md','seed':42,'training_texts':len(train),
             'validation_texts':len(val),'test_texts':len(test),'bigram_strength':strength,
             'scope':'Complete held-out strings, known gap length; candidate probabilities conditional on training glyph vocabulary; no translation or unknown-stretch restoration',
             'lengths':{}}
    engines={'unigram':Reconstructor(Model(train,1,20)),'bigram':Reconstructor(Model(train,2,strength))}
    for length in (1,2):
        by_model={}
        for name,engine in engines.items():
            events=[]
            for t in test:
                for start in range(len(t)-length+1):
                    truth=list(t[start:start+length]);left=t[start-1] if start else '<BOS>'
                    right=t[start+length] if start+length<len(t) else '<EOS>'
                    ranked=engine.fill(left,right,length)
                    events.append({'text':list(t),'start':start,'length':length,'truth':truth,
                        'truth_covered':all(s in engine.candidates for s in truth),'candidates':ranked,
                        'top1':truth==ranked[0]['signs'],'top5':any(truth==r['signs'] for r in ranked),
                        'correct_tokens':sum(a==b for a,b in zip(truth,ranked[0]['signs']))})
            by_model[name]={'summary':metrics(events),'events':events}
        results['lengths'][str(length)]={'models':by_model,'paired_top1_gain':bootstrap(by_model['bigram']['events'],by_model['unigram']['events'])}
    # Existing single-mask test must be exactly reproduced (no EOS/UNK candidates).
    reference=json.loads((ROOT/'results/sequence_models.json').read_text())[0]['mask_prediction']
    observed=results['lengths']['1']['models']['bigram']['summary']
    assert abs(observed['whole_top1']-reference['top1_rate'])<1e-12
    assert abs(observed['whole_top5']-reference['top5_rate'])<1e-12
    results['single_mask_matches_prior_diagnostic']=True
    save('gap_reconstruction.json',results)
    print(json.dumps({k:{'models':{m:v['summary'] for m,v in r['models'].items()},'gain':r['paired_top1_gain']} for k,r in results['lengths'].items()},indent=2))

if __name__=='__main__':main()

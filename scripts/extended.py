"""Additional structure controls, segmentation candidates and identifiability audit."""
import collections as C
import json
import math
import random
import statistics as S
from analyze import ROOT, Model, avg_loss, conditional_entropy, describe, save, split

class SlotModel:
    """Independent positional slots: no sign-to-sign dependence; length supplied."""
    def __init__(self, texts, strength=20):
        self.base = Model(texts,1)
        self.counts = C.defaultdict(C.Counter)
        self.strength = strength
        for t in texts:
            for i,s in enumerate(t):
                role = self.role(i,len(t))
                self.counts[role][s]+=1
        self.totals = {r:sum(c.values()) for r,c in self.counts.items()}

    @staticmethod
    def role(i,n):
        return 'single' if n==1 else 'initial' if i==0 else 'final' if i==n-1 else 'medial'

    def prob(self,s,i,n):
        role=self.role(i,n)
        s=s if s in self.base.uni else '<UNK>'
        # Exclude EOS from sign-only unigram prior.
        base=(self.base.uni[s]+.5)/(self.base.total-self.base.uni['<EOS>']+.5*(len(self.base.vocab)-1))
        return (self.counts[role][s]+self.strength*base)/(self.totals.get(role,0)+self.strength)

    def losses(self,texts):
        return [(sum(-math.log2(self.prob(s,i,len(t))) for i,s in enumerate(t)),len(t)) for t in texts]

def sign_losses(model,texts):
    result=[]
    for t in texts:
        prefix=['<BOS>','<BOS>'];loss=0
        for s in t:
            # All models condition on being a sign (rather than EOS) for fair slot comparison.
            p=model.prob(s,prefix)/(1-model.prob('<EOS>',prefix))
            loss-=math.log2(p);prefix.append(s)
        result.append((loss,len(t)))
    return result

def main():
    records=json.loads((ROOT/'data/processed/icit_unique.json').read_text())
    texts=[r['signs'] for r in records]
    train,val,test=split(texts,42)
    slot=min((SlotModel(train,a) for a in (1,5,20,100)),key=lambda m:avg_loss(m.losses(val)))
    bigram=min((Model(train,2,a) for a in (1,5,20,100)),key=lambda m:avg_loss(sign_losses(m,val)))
    save('slot_control.json',{'scope':'sign tokens only, EOS excluded; length known to slot model',
        'test_texts':len(test),'unigram_bits':avg_loss(sign_losses(Model(train,1),test)),
        'independent_slot_bits':avg_loss(slot.losses(test)),
        'bigram_bits':avg_loss(sign_losses(bigram,test)),
        'slot_strength':slot.strength,'bigram_strength':bigram.strength,
        'interpretation':'Slot positions alone can predict signs without encoding spoken language.'})
    # Synthetic administrative records: independent draws from role-specific distributions.
    rng=random.Random(20261015)
    generated=[]
    for t in texts:
        g=[]
        for i in range(len(t)):
            c=slot.counts[slot.role(i,len(t))]
            signs=sorted(c); weights=[c[s] for s in signs]
            g.append(rng.choices(signs,weights=weights,k=1)[0])
        generated.append(g)
    save('synthetic_slots.json',{'generation':'Matched length list; independent role-specific draws from seed-42 training counts',
        'seed':20261015,'observed':describe(texts),'synthetic':describe(generated),
        'limitation':'Synthetic sample retains duplicate generated records; descriptive comparison only, not a calibrated classification.'})
    # Train-only adjacency PMI and repeated phrases. No inferred boundaries asserted.
    bi=C.Counter((a,b) for t in train for a,b in zip(t,t[1:]))
    left,right=C.Counter(),C.Counter()
    for (a,b),n in bi.items():left[a]+=n;right[b]+=n
    total=sum(bi.values())
    candidates=[]
    testbi=C.Counter((a,b) for t in test for a,b in zip(t,t[1:]))
    for (a,b),n in bi.items():
        pmi=math.log2(n*total/(left[a]*right[b]))
        if n>=5 and pmi>=1:
            candidates.append({'signs':[a,b],'train_count':n,'pmi_bits':pmi,'test_count':testbi[a,b]})
    candidates.sort(key=lambda r:(-r['pmi_bits'],-r['train_count'],r['signs']))
    save('segmentation_candidates.json',{'method':'Train-only adjacent PMI >=1 bit and count >=5',
        'candidates':candidates,'limitation':'Collocations, not validated words or morphemes; no pairwise significance claim.'})
    # Graph endpoints and directed degree: count support, no natural-language classification.
    incoming,outgoing=C.defaultdict(set),C.defaultdict(set)
    for a,b in bi: outgoing[a].add(b);incoming[b].add(a)
    save('transition_network.json',{'nodes':[{'sign':s,'in_degree':len(incoming[s]),'out_degree':len(outgoing[s])}
        for s in sorted(set(incoming)|set(outgoing))],
        'edges':[{'from':a,'to':b,'train_count':n} for (a,b),n in sorted(bi.items())],
        'training_only':True,'limitation':'A graph of adjacency, not semantic relations.'})
    # Every bijective substitution has identical counts and entropies.
    vocab=sorted({s for t in texts for s in t})
    keys=[]
    for seed in range(10):
        labels=[f'CV{i:03}' for i in range(len(vocab))]
        random.Random(seed).shuffle(labels)
        key=dict(zip(vocab,labels))
        recoded=[[key[s] for s in t] for t in texts]
        keys.append({'seed':seed,'conditional_entropy_bits':conditional_entropy(recoded),
                     'example_relabeling':[(s,key[s]) for s in vocab[:8]]})
    save('substitution_identifiability.json',{'experiment':'Ten bijective abstract syllable-label substitutions',
        'keys':keys,'original_entropy_bits':conditional_entropy(texts),
        'possible_bijective_labelings_log10':math.lgamma(len(vocab)+1)/math.log(10),
        'conclusion':'Frequency/entropy/adjacency structure cannot select among renamed phonetic or semantic values.',
        'limitation':'CV labels are abstract unique tokens, not historically plausible syllables; this is an invariance demonstration.'})
    # Strict direction and longer-text sensitivity.
    subsets={'length_at_least_3':[t for t in texts if len(t)>=3],
             'metadata_RL_only':[r['signs'] for r in records if r['direction'].strip().upper()=='R/L']}
    raw=json.loads((ROOT/'data/processed/icit_all.json').read_text())
    subsets['eligible_with_duplicates']=[r['signs'] for r in raw if not r['exclusion_reasons']]
    save('sensitivity.json',{name:describe(ts) for name,ts in subsets.items()})
    print('Extended controls, candidate units, network, and substitution audit complete.')

if __name__=='__main__':main()

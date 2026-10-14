"""Connected one-substitution groups and leakage-sensitive n-gram benchmark."""
import collections as C
import json
import random
from analyze import ROOT, Model, avg_loss, canonical, save, split
from latent_grammar import paired_interval

def components(texts):
    keys=sorted({canonical(t) for t in texts});parent=list(range(len(keys)))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(i,j):
        a,b=find(i),find(j)
        if a!=b:parent[max(a,b)]=min(a,b)
    buckets={}
    for i,t in enumerate(keys):
        if len(t)<3:continue
        for oriented in (t,t[::-1]):
            for pos in range(len(t)):
                pattern=oriented[:pos]+('*',)+oriented[pos+1:]
                if pattern in buckets:union(i,buckets[pattern])
                else:buckets[pattern]=i
    groups=C.defaultdict(list)
    for i,t in enumerate(keys):groups[find(i)].append(t)
    return sorted(groups.values(),key=lambda g:g[0])

def main():
    records=json.loads((ROOT/'data/processed/icit_unique.json').read_text());texts=[r['signs'] for r in records]
    groups=components(texts);random.Random(42).shuffle(groups)
    a,b=int(.8*len(groups)),int(.9*len(groups))
    assignment={t:part for part,gs in zip(('train','validation','test'),(groups[:a],groups[a:b],groups[b:]))
                for group in gs for t in group}
    datasets=[[t for t in texts if assignment[canonical(t)]==part] for part in ('train','validation','test')]
    train,val,test=datasets
    original_train,_,original_test=split(texts,42)
    train_patterns=set()
    for t in original_train:
        if len(t)<3:continue
        for orient in (tuple(t),tuple(t)[::-1]):
            for pos in range(len(t)):train_patterns.add(orient[:pos]+('*',)+orient[pos+1:])
    exposed=0;eligible=0
    for t in original_test:
        if len(t)<3:continue
        eligible+=1
        if any(orient[:pos]+('*',)+orient[pos+1:] in train_patterns
               for orient in (tuple(t),tuple(t)[::-1]) for pos in range(len(t))):exposed+=1
    scores={};losses={}
    component_id={t:i for i,group in enumerate(groups) for t in group}
    known={x for t in train for x in t}
    for order in (1,2):
        m=min((Model(train,order,s) for s in (1,5,20,100)),key=lambda m:avg_loss(m.losses(val)))
        losses[order]=m.losses(test)
        scores[str(order)]={'strength':m.strength,'validation_bits':avg_loss(m.losses(val)),
                            'test_bits':avg_loss(losses[order])}
    save('near_copy.json',{'design':'docs/EXPERIMENT_002.md','components':len(groups),
        'component_canonical_sequence_sizes':dict(sorted(C.Counter(map(len,groups)).items())),
        'largest_component':max(map(len,groups)),'train_texts':len(train),'validation_texts':len(val),'test_texts':len(test),
        'original_test_eligible_length_at_least_3':eligible,'original_test_with_train_neighbour':exposed,
        'original_test_neighbour_fraction':exposed/eligible,'scores':scores,
        'bigram_improvement':paired_interval(test,losses[1],losses[2],group_keys=[component_id[canonical(t)] for t in test]),
        'unknown_test_tokens':sum(s not in known for t in test for s in t),
        'group_rule':'equal length >=3, one sign substitution in either orientation; transitive closure; exact/reverse canonical',
        'limitation':'Similarity components are not verified artifact families; component-based split has unequal text proportions and different difficulty.'})
    save('near_copy_groups.json',{'components':[{'canonical_texts':[list(t) for t in group],
        'split':assignment[group[0]]} for group in sorted(groups,key=lambda g:g[0])]})
    print('Near-copy benchmark completed.',flush=True)

if __name__=='__main__':main()

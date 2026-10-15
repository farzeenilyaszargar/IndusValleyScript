"""Face-preserving held-out field-code prediction; no semantic sign assignments."""
import collections as C
import json
import math
import random
from analyze import ROOT,canonical,save

def site(row):
    n=int(row['textnum'])
    for lo,hi,label in ((1001,3513,'MD'),(4001,5601,'HP'),(6104,6405,'CD'),(7001,7301,'LL'),(8001,8302,'KB'),(9001,9701,'OS'),(9801,9905,'WA')):
        if lo<=n<=hi:return label
    return 'UNMAPPED'

def stratum(row):return (site(row),row['object_code'],str(min(len(row['signs']),6)))

def partition(rows,seed=42):
    parents=list(range(len(rows)))
    def find(i):
        while i!=parents[i]:parents[i]=parents[parents[i]];i=parents[i]
        return i
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b:parents[max(a,b)]=min(a,b)
    objects={};texts={}
    for i,r in enumerate(rows):
        for table,key in ((objects,r['textnum']),(texts,canonical(r['signs']))):
            if key in table:union(i,table[key])
            else:table[key]=i
    groups=C.defaultdict(list)
    for i,r in enumerate(rows):groups[find(i)].append(dict(r,component=str(find(i))))
    keys=sorted(groups);random.Random(seed).shuffle(keys);a,b=int(.8*len(keys)),int(.9*len(keys))
    return [[r for k in ks for r in groups[k]] for ks in (keys[:a],keys[a:b],keys[b:])],groups

def target_map(train,minimum=20):
    objects=C.defaultdict(set)
    for r in train:objects[r['field_symbol_code']].add(r['textnum'])
    return {k:k if len(v)>=minimum else 'RARE' for k,v in sorted(objects.items())}

class Predictor:
    def __init__(self,train,mapping,strength):
        self.mapping=mapping;self.strength=strength;self.classes=sorted(set(mapping.values())|{'RARE'})
        self.counts=C.Counter();self.meta=C.defaultdict(C.Counter);self.signs=C.defaultdict(C.Counter)
        for r in train:
            c=self.target(r);self.counts[c]+=1;self.meta[stratum(r)][c]+=1;self.signs[c].update(set(r['signs']))
        self.vocab={s for counter in self.signs.values() for s in counter}
        self.prior={c:(self.counts[c]+.5)/(len(train)+.5*len(self.classes)) for c in self.classes}
        self.emissions={c:{s:math.log((self.signs[c][s]+1)/(sum(self.signs[c].values())+len(self.vocab))) for s in self.vocab} for c in self.classes}
    def target(self,row):return self.mapping.get(row['field_symbol_code'],'RARE')
    def probabilities(self,row,weight=0):
        counts=self.meta.get(stratum(row),{});n=sum(counts.values());known=sorted(set(row['signs'])&self.vocab)
        scores={c:math.log((counts.get(c,0)+self.strength*self.prior[c])/(n+self.strength))+
                (weight*sum(self.emissions[c][s] for s in known)/len(known) if known else 0) for c in self.classes}
        maximum=max(scores.values());values={c:math.exp(v-maximum) for c,v in scores.items()};total=sum(values.values())
        return {c:v/total for c,v in values.items()}
    def losses(self,rows,weight=0):return [-math.log2(self.probabilities(r,weight)[self.target(r)]) for r in rows]

def average(xs):return sum(xs)/len(xs)

def scores(model,rows,weight):
    ledger=[]
    for r in rows:
        p=model.probabilities(r,weight);prediction=min(p,key=lambda c:(-p[c],c));truth=model.target(r)
        ledger.append({'document_id':r['document_id'],'textnum':r['textnum'],'side':r['side'],'line':r['line'],
                       'component':r['component'],'raw_field_code':r['field_symbol_code'],'target':truth,'prediction':prediction,
                       'probabilities':p,'loss_bits':-math.log2(p[truth])})
    recalls={c:{'rows':sum(r['target']==c for r in ledger),'correct':sum(r['target']==c==r['prediction'] for r in ledger)} for c in model.classes}
    confusion=C.Counter((r['target'],r['prediction']) for r in ledger)
    return {'bits_per_row':average([r['loss_bits'] for r in ledger]),'accuracy':sum(r['target']==r['prediction'] for r in ledger)/len(ledger),
            'macro_recall_present_classes':average([r['correct']/r['rows'] for r in recalls.values() if r['rows']]),
            'class_recalls':recalls,'confusion':[{'truth':a,'prediction':b,'rows':n} for (a,b),n in sorted(confusion.items())],
            'ledger':ledger}

def bootstrap(left,right):
    groups=C.defaultdict(lambda:[0.,0])
    for a,b in zip(left['ledger'],right['ledger']):
        assert a['document_id']==b['document_id']
        g=groups[a['component']];g[0]+=a['loss_bits']-b['loss_bits'];g[1]+=1
    values=list(groups.values());rng=random.Random(42);samples=[]
    for _ in range(1000):
        draw=rng.choices(values,k=len(values));samples.append(sum(x for x,n in draw)/sum(n for x,n in draw))
    samples.sort()
    return {'improvement_bits_per_row':sum(x for x,n in values)/sum(n for x,n in values),
            'interval95':[samples[24],samples[974]],'groups':len(values),'resamples':1000,
            'unit':'connected object-or-exact/reverse-text component'}

def main():
    rows=[r for r in json.loads((ROOT/'data/processed/mahadevan_primary_lines.json').read_text()) if not r['exclusion_reasons']]
    full,groups=partition(rows);parts=[[r for r in part if r['field_symbol_code'] not in ('0','999')] for part in full];train,val,test=parts
    if not all(parts):raise ValueError('Empty target split')
    component_parts={r['component']:name for name,part in zip(('train','validation','test'),full) for r in part}
    largest=sorted(groups.items(),key=lambda x:(-len(x[1]),x[0]))[:10]
    mapping=target_map(train);grid=[]
    for strength in (1,5,20,100):
        m=Predictor(train,mapping,strength);grid.append((average(m.losses(val)),strength))
    _,strength=min(grid);model=Predictor(train,mapping,strength)
    weights=[(average(model.losses(val,w)),w) for w in (0,.25,.5,1,2)];_,weight=min(weights)
    baseline=scores(model,test,0);augmented=scores(model,test,weight)
    majority=min(model.classes,key=lambda c:(-model.counts[c],c))
    result={'design':'docs/EXPERIMENT_014.md','seed':42,'all_strict_rows':len(rows),'all_components':len(groups),
            'largest_components':[{'component':str(k),'rows':len(g),'partition':component_parts[str(k)],
                'target_rows':sum(r['field_symbol_code'] not in ('0','999') for r in g)} for k,g in largest],
            'all_strict_component_assignment':[{'document_id':r['document_id'],'component':r['component'],'partition':name}
                for name,part in zip(('train','validation','test'),full) for r in part],
            'split_all_strict_rows':{name:len(part) for name,part in zip(('train','validation','test'),full)},
            'target_rows':sum(map(len,parts)),'split_rows':{name:len(part) for name,part in zip(('train','validation','test'),parts)},
            'split_documents':{name:[r['document_id'] for r in part] for name,part in zip(('train','validation','test'),parts)},
            'class_map_training_only':mapping,'training_class_counts':dict(model.counts),
            'test_raw_code_counts':dict(C.Counter(r['field_symbol_code'] for r in test)),
            'baseline_grid':[{'strength':s,'validation_bits':v} for v,s in grid],
            'weight_grid':[{'weight':w,'validation_bits':v} for v,w in weights],
            'selected_baseline_strength':strength,'selected_sign_weight':weight,
            'baseline':baseline,'sign_augmented':augmented,'paired_gain':bootstrap(baseline,augmented),
            'majority_class':majority,'majority_accuracy':sum(model.target(r)==majority for r in test)/len(test),
            'unseen_test_strata_rows':sum(stratum(r) not in model.meta for r in test),
            'unknown_test_sign_tokens':sum(s not in model.vocab for r in test for s in r['signs']),
            'test_sign_tokens':sum(len(r['signs']) for r in test),
            'scope':'Recorded literal field-code prediction; no animal labels, phonetic values, causal or translation claims. Duplicate-weighted rows; near-copy/mold families unresolved; conditional intervals on one split.'}
    save('motif_prediction.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('baseline','sign_augmented','split_documents','class_map_training_only','all_strict_component_assignment')}|
                     {'baseline':{k:v for k,v in baseline.items() if k!='ledger'},'sign_augmented':{k:v for k,v in augmented.items() if k!='ledger'}},indent=2))

if __name__=='__main__':main()

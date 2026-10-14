"""Known object metadata as context, with pooled bigram backoff."""
import collections as C
import json
import math
import random
from analyze import ROOT,Model,avg_loss,canonical,save,split

def coarse_type(row):return row['type'].split(':')[0].strip() or '<MISSING>'

def metadata(row,kind):
    if kind=='type':return coarse_type(row)
    if kind=='site':return row['site']
    if kind=='site_type':return row['site']+'|'+coarse_type(row)
    raise ValueError(kind)

def partition(records):
    parts=split([r['signs'] for r in records],42)
    keysets=[{canonical(t) for t in part} for part in parts]
    return [[r for r in records if canonical(r['signs']) in keys] for keys in keysets]

class MetadataModel:
    def __init__(self,records,kind,base_strength,strength):
        self.kind,self.strength=kind,strength
        self.base=Model([r['signs'] for r in records],2,base_strength)
        self.counts=C.defaultdict(C.Counter)
        for row in records:
            key=metadata(row,kind);previous='<BOS>'
            for s in row['signs']+['<EOS>']:
                self.counts[key,previous][s]+=1;previous=s
        self.totals={ctx:sum(c.values()) for ctx,c in self.counts.items()}

    def prob(self,s,previous,row):
        s=s if s in self.base.uni else '<UNK>'
        previous=previous if previous in self.base.uni or previous=='<BOS>' else '<UNK>'
        ctx=(metadata(row,self.kind),previous)
        prior=self.base.prob(s,[previous])
        return (self.counts.get(ctx,{}).get(s,0)+self.strength*prior)/(self.totals.get(ctx,0)+self.strength)

    def losses(self,records):
        out=[]
        for row in records:
            previous='<BOS>';loss=0
            for s in row['signs']+['<EOS>']:
                loss-=math.log2(self.prob(s,previous,row));previous=s
            out.append((loss,len(row['signs'])+1))
        return out

def interval(records,left,right):
    groups=C.defaultdict(lambda:[0.,0])
    for r,a,b in zip(records,left,right):
        key=canonical(r['signs']);groups[key][0]+=a[0]-b[0];groups[key][1]+=a[1]
    values=list(groups.values());rng=random.Random(42)
    samples=sorted(avg_loss(rng.choices(values,k=len(values))) for _ in range(1000))
    return {'improvement_bits':avg_loss(values),'bootstrap95':[samples[25],samples[974]],
            'bootstrap98_33_three_comparison':[samples[8],samples[991]],
            'resampling_unit':'exact/reverse text group','groups':len(values),'resamples':1000}

def main():
    rows=[r for r in json.loads((ROOT/'data/processed/icit_all.json').read_text()) if not r['exclusion_reasons']]
    train,val,test=partition(rows);ts=lambda rs:[r['signs'] for r in rs]
    pooled=min((Model(ts(train),2,s) for s in (1,5,20,100)),key=lambda m:avg_loss(m.losses(ts(val))))
    baseline_losses=pooled.losses(ts(test))
    output={'design':'docs/EXPERIMENT_008.md','eligible_rows':len(rows),'split_seed':42,
        'train_rows':len(train),'validation_rows':len(val),'test_rows':len(test),
        'split_row_ids':{k:[r['id'] for r in rs] for k,rs in zip(('train','validation','test'),(train,val,test))},
        'pooled':{'strength':pooled.strength,'validation_bits':avg_loss(pooled.losses(ts(val))),
                  'test_bits':avg_loss(baseline_losses)},
        'unknown_test_tokens':sum(s not in pooled.uni for r in test for s in r['signs']),
        'test_sign_tokens':sum(len(r['signs']) for r in test),
        'test_type_counts':dict(sorted(C.Counter(coarse_type(r) for r in test).items())),
        'models':{},'limitation':'Duplicate-weighted archaeological rows and uneven metadata. Exact/reverse grouping does not establish independent molds/families; no linguistic values inferred.'}
    for kind in ('type','site','site_type'):
        model=min((MetadataModel(train,kind,a,b) for a in (1,5,20,100) for b in (1,5,20,100)),
                  key=lambda m:avg_loss(m.losses(val)))
        losses=model.losses(test)
        matched_base_losses=model.base.losses(ts(test))
        bytype={}
        for category in sorted({coarse_type(r) for r in test}):
            indices=[i for i,r in enumerate(test) if coarse_type(r)==category]
            bytype[category]={'rows':len(indices),'pooled_bits':avg_loss([baseline_losses[i] for i in indices]),
                              'metadata_bits':avg_loss([losses[i] for i in indices])}
        output['models'][kind]={'base_strength':model.base.strength,'metadata_strength':model.strength,
            'validation_bits':avg_loss(model.losses(val)),'test_bits':avg_loss(losses),
            'paired_improvement':interval(test,baseline_losses,losses),'test_by_type':bytype}
        output['models'][kind]['matched_smoothing_ablation']={
            'pooled_base_strength':model.base.strength,'pooled_test_bits':avg_loss(matched_base_losses),
            'metadata_increment':interval(test,matched_base_losses,losses),
            'scope':'Exploratory diagnostic added after observing different validation-selected pooled strengths; no model is reselected using test scores.'}
    save('metadata_conditioning.json',output)
    print(json.dumps({k:v for k,v in output.items() if k!='split_row_ids'},indent=2))

if __name__=='__main__':main()

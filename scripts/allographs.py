"""Audit and encode annotated morphology; test previous-variant predictive value."""
import collections as C
import json
import math
from analyze import ROOT, Model, avg_loss, canonical, save, split
from latent_grammar import paired_interval

def variant(g):
    # Annotation confidence and layout are not morphological identity.
    return g['id']+':'+','.join(map(str,g['features'][3:]))

def partition(records,seed):
    base_keys=sorted({tuple(r['signs']) for r in records})
    tr,va,te=split(base_keys,seed)
    keysets=[{canonical(t) for t in rows} for rows in (tr,va,te)]
    return [[r for r in records if canonical(r['signs']) in keys] for keys in keysets]

class VariantHistory:
    def __init__(self,records,base_strength,variant_strength):
        self.base=Model([r['signs'] for r in records],2,base_strength)
        self.strength=variant_strength;self.counts=C.defaultdict(C.Counter)
        for r in records:
            previous='<BOS>'
            for g in r['allographs']:
                self.counts[previous][g['id']]+=1;previous=variant(g)
            self.counts[previous]['<EOS>']+=1
        self.totals={key:sum(c.values()) for key,c in self.counts.items()}

    def prob(self,target,base_previous,variant_previous):
        target=target if target in self.base.uni else '<UNK>'
        prior=self.base.prob(target,[base_previous])
        return (self.counts.get(variant_previous,{}).get(target,0)+self.strength*prior)/(self.totals.get(variant_previous,0)+self.strength)

    def losses(self,records):
        result=[]
        for r in records:
            bp,vp='<BOS>','<BOS>';loss=0
            for g in r['allographs']:
                loss-=math.log2(self.prob(g['id'],bp,vp))
                bp,vp=g['id'],variant(g)
            loss-=math.log2(self.prob('<EOS>',bp,vp));result.append((loss,len(r['signs'])+1))
        return result

def main():
    records=json.loads((ROOT/'data/processed/cisi_all.json').read_text())
    records=[r for r in records if not r['exclusion_reasons']]
    catalog={r['id']:r for r in json.loads((ROOT/'data/processed/parpola_catalog.json').read_text())}
    counts=C.Counter();examples=C.defaultdict(list);definitions={}
    for r in records:
        for g in r['allographs']:
            expected=3+len(catalog[g['id']]['features'])
            if len(g['features'])!=expected:raise ValueError(f'Invalid vector: {r["id"]} {g["id"]}')
            key=variant(g);counts[key]+=1;examples[key].append(r['id'])
            definitions[key]={'base_sign':g['id'],'description':catalog[g['id']]['description'],
                              'custom_values':g['features'][3:],'schema':catalog[g['id']]['features']}
    enc={key:i+4 for i,key in enumerate(sorted(counts))}
    inventory=[{'variant_key':key,'integer_token':enc[key],'count':counts[key],
                'object_ids':sorted(set(examples[key])),**definitions[key]} for key in sorted(counts)]
    processed=ROOT/'data/processed'
    (processed/'parpola_variant_catalog.json').write_text(json.dumps({'reserved':{'PAD':0,'UNK':1,'BOS':2,'EOS':3},
        'definition':'base ID plus custom feature vector; not confirmed independent graphemes',
        'variants':inventory},indent=2,ensure_ascii=False)+'\n')
    (processed/'parpola_variant_sequences.json').write_text(json.dumps([
        {'object_id':r['id'],'base_signs':r['signs'],'variant_tokens':[enc[variant(g)] for g in r['allographs']]}
        for r in records],indent=2)+'\n')
    runs=[]
    for seed in range(42,47):
        train,val,test=partition(records,seed)
        traintexts=[r['signs'] for r in train];valtexts=[r['signs'] for r in val];testtexts=[r['signs'] for r in test]
        baseline=min((Model(traintexts,2,s) for s in (1,5,20,100)),key=lambda m:avg_loss(m.losses(valtexts)))
        models=[VariantHistory(train,a,b) for a in (1,5,20,100) for b in (1,5,20,100)]
        chosen=min(models,key=lambda m:avg_loss(m.losses(val)))
        base_losses=baseline.losses(testtexts);feature_losses=chosen.losses(test)
        known_variants={variant(g) for r in train for g in r['allographs']}
        test_variants=[variant(g) for r in test for g in r['allographs']]
        runs.append({'seed':seed,'train_objects':len(train),'validation_objects':len(val),'test_objects':len(test),
            'baseline_strength':baseline.strength,'variant_base_strength':chosen.base.strength,'variant_strength':chosen.strength,
            'baseline_validation_bits':avg_loss(baseline.losses(valtexts)),
            'variant_validation_bits':avg_loss(chosen.losses(val)),
            'baseline_test_bits':avg_loss(base_losses),'variant_test_bits':avg_loss(feature_losses),
            'variant_improvement':paired_interval(testtexts,base_losses,feature_losses,seed=seed),
            'test_sign_tokens':len(test_variants),'test_variant_tokens_unseen_in_training':sum(v not in known_variants for v in test_variants),
            'test_base_tokens_unseen_in_training':sum(s not in baseline.uni for t in testtexts for s in t),
            'split_objects':{'train':[r['id'] for r in train],'validation':[r['id'] for r in val],'test':[r['id'] for r in test]}})
    result={'design':'docs/EXPERIMENT_003.md','eligible_objects':len(records),
        'sign_tokens':sum(counts.values()),'base_ids':len({r['base_sign'] for r in inventory}),
        'variant_ids':len(inventory),'validated_vector_lengths':True,
        'objects_with_same_base_sequence':len(records)-len({tuple(r['signs']) for r in records}),
        'runs':runs,'scoring':'Same next base-sign target; EOS included; own target morphology never provided; unknown base IDs collapsed to UNK',
        'limitation':'Selected small Mohenjo-daro sample; overlaps across seed runs; variant splitting is a representation, not a deciphered distinction.'}
    save('allograph_history.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='runs'},indent=2))
    print([(r['seed'],r['variant_improvement']) for r in runs])

if __name__=='__main__':main()

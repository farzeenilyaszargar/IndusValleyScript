"""A fictional notation with explicit semantics and no sound-value assignments."""
import collections as C
import json
import random
from analyze import ROOT, canonical, conditional_entropy, describe, evaluate, save, shuffled

SETTINGS={'institutions':160,'guilds':96,'commodities':160,'quantities':8,'ranks':4,'validators':5,
          'zipf_exponent':1.15,'license_seed':131,'guilds_per_institution':6,'commodities_per_guild':8,
          'generation_seeds':[17,29,43],'split_seed':42,'shuffle_trials':99}

def symbol(role,number):return f'{role}{number:03}'

def licenses():
    rng=random.Random(SETTINGS['license_seed'])
    return {'institution_guilds':{symbol('I',i):sorted(rng.sample(range(96),6)) for i in range(160)},
            'guild_commodities':{symbol('G',g):sorted(rng.sample(range(160),8)) for g in range(96)},
            'guild_ranks':{symbol('G',g):sorted(rng.sample(range(1,5),2)) for g in range(96)},
            'commodity_quantities':{symbol('C',c):sorted(rng.sample(range(1,9),2)) for c in range(160)}}

def templates(length):
    choices=[]
    for inst in (0,1):
        for office in (0,1):
            for terminal in (0,1):
                remain=length-inst-2*office-terminal
                if remain<0 or remain%2:continue
                ledgers=remain//2
                weight=(4 if inst else 1)*(4 if office else 1)*(4 if terminal else 1)/(1+ledgers)
                choices.append(((inst,office,ledgers,terminal),weight))
    return choices

def generate(lengths,seed):
    rules=licenses();rng=random.Random(seed);records=[]
    def zipf(size):return rng.choices(range(size),weights=[(i+1)**-1.15 for i in range(size)],k=1)[0]
    for row,length in enumerate(lengths):
        choices=templates(length);inst,office,ledgers,terminal=rng.choices([p for p,_ in choices],weights=[w for _,w in choices],k=1)[0]
        tokens=[];institution=None;guild=None
        def token(role,value):
            prefix={'institution':'I','guild':'G','commodity':'C','quantity':'Q','rank':'R','validation':'V'}[role]
            tokens.append({'sign':symbol(prefix,value),'role':role,'value':value})
        if inst:institution=zipf(160);token('institution',institution)
        if office:
            guild=rng.choice(rules['institution_guilds'][symbol('I',institution)]) if institution is not None else zipf(96)
            token('guild',guild);token('rank',rng.choice(rules['guild_ranks'][symbol('G',guild)]))
        for _ in range(ledgers):
            commodity=rng.choice(rules['guild_commodities'][symbol('G',guild)]) if guild is not None else zipf(160)
            quantity=rng.choice(rules['commodity_quantities'][symbol('C',commodity)])
            token('quantity',quantity);token('commodity',commodity)
        if terminal:token('validation',institution%5 if institution is not None else rng.randrange(5))
        assert len(tokens)==length
        records.append({'id':row,'signs':[t['sign'] for t in tokens],'semantics':tokens,
                        'template':[inst,office,ledgers,terminal]})
    return records

def audit(records,rules):
    for r in records:
        inst=next((t['value'] for t in r['semantics'] if t['role']=='institution'),None)
        guild=next((t['value'] for t in r['semantics'] if t['role']=='guild'),None)
        assert r['signs']==[t['sign'] for t in r['semantics']]
        if inst is not None and guild is not None:assert guild in rules['institution_guilds'][symbol('I',inst)]
        for i,t in enumerate(r['semantics']):
            prefix={'institution':'I','guild':'G','commodity':'C','quantity':'Q','rank':'R','validation':'V'}[t['role']]
            assert t['sign']==symbol(prefix,t['value'])
            if t['role']=='rank':assert t['value'] in rules['guild_ranks'][symbol('G',guild)]
            if t['role']=='commodity':
                assert r['semantics'][i-1]['role']=='quantity'
                assert r['semantics'][i-1]['value'] in rules['commodity_quantities'][t['sign']]
                if guild is not None:assert t['value'] in rules['guild_commodities'][symbol('G',guild)]

def main():
    source=json.loads((ROOT/'data/processed/icit_unique.json').read_text());lengths=[len(r['signs']) for r in source]
    rules=licenses();out={'design':'docs/EXPERIMENT_012.md','settings':SETTINGS,'licenses':rules,
        'scope':'Fictional administrative referents, integers and validation emblems; no phonetic assignments; length list alone matched to Indus. Not SIGIL replication, linguistic classifier or model of actual Harappan administration.',
        'real_reference':{'entropy':conditional_entropy([r['signs'] for r in source]),
                          'seed42_scores':json.loads((ROOT/'results/sequence_models.json').read_text())[0]},'realizations':{}}
    for seed in SETTINGS['generation_seeds']:
        records=generate(lengths,seed);audit(records,rules);texts=[r['signs'] for r in records]
        observed=conditional_entropy(texts);rng=random.Random(seed)
        values=[conditional_entropy(shuffled(texts,'within_text',rng)) for _ in range(99)]
        evaluation=evaluate(texts,42)
        out['realizations'][str(seed)]={'description':describe(texts),
            'canonical_groups':len({canonical(t) for t in texts}),
            'within_text_null':{'observed_bits':observed,'mean_bits':sum(values)/len(values),
                'p_lower':(1+sum(v<=observed for v in values))/(len(values)+1),'values':values},
            'evaluation':evaluation,'records':records}
    save('administrative_control.json',out)
    print(json.dumps({s:{'description':r['description'],'canonical_groups':r['canonical_groups'],
        'entropy':r['within_text_null']['observed_bits'],'p':r['within_text_null']['p_lower'],
        'unigram':r['evaluation']['order_1']['test_bits_per_token_including_EOS'],
        'bigram':r['evaluation']['order_2']['test_bits_per_token_including_EOS'],
        'gain':r['evaluation']['bigram_improvement_bits'],
        'interval':r['evaluation']['bigram_improvement_bootstrap95'],'mask':r['evaluation']['mask_prediction']}
        for s,r in out['realizations'].items()},indent=2))

if __name__=='__main__':main()

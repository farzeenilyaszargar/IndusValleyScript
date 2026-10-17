"""Complete proxy-unit inventory, lineage checks and synthetic feasibility only."""
import collections as C
import gzip
import hashlib
import json
import random
import unicodedata as U
from analyze import ROOT,save
from homophonic_channel import prepare,UNK

def coarsen_counts(profile,old_units):
    n=len(old_units);enc={s:i for i,s in enumerate(old_units)};mapping=[enc.get(s,n) for s in profile['units']]+[n]
    uni=[0]*(n+1);bi=[[0]*(n+1) for _ in range(n+1)]
    for i,c in enumerate(profile['unigram_counts']):uni[mapping[i]]+=c
    for i,row in enumerate(profile['bigram_counts']):
        for j,c in enumerate(row):bi[mapping[i]][mapping[j]]+=c
    return uni,bi

def make_cipher(windows,unit_count):
    aliases=list(range(2*unit_count));random.Random(1031).shuffle(aliases);rng=random.Random(2031)
    truth={f'F{aliases[2*u+v]:04}':u for u in range(unit_count) for v in range(2)}
    texts=[[UNK if u==unit_count else f'F{aliases[2*u+rng.randrange(2)]:04}' for u in t] for t in windows]
    return texts,truth

def main():
    folder=ROOT/'data/full_target';manifest=json.loads((folder/'manifest.json').read_text());raw=gzip.decompress((folder/'inputs.json.gz').read_bytes())
    if hashlib.sha256(raw).hexdigest()!=manifest['sha256_uncompressed']:raise ValueError('Full-target input drift')
    data=json.loads(raw);oldraw=gzip.decompress((ROOT/'data/substitution/inputs.json.gz').read_bytes())
    if hashlib.sha256(oldraw).hexdigest()!=manifest['coarse_input_sha256']:raise ValueError('Coarse source drift')
    old=json.loads(oldraw);out={'design':'docs/EXPERIMENT_021.md','input_sha256':manifest['sha256_uncompressed'],'languages':{},'scope':'Acquisition and feasibility audit; no expanded-target channel optimized, no sound values or translations.'}
    for language,p in data['languages'].items():
        prior=old['languages'][language]
        for field in ('lm_document_ids','held_document_ids','windows'):
            if p[field]!=prior[field]:raise ValueError('Frozen document/window identities changed')
        uni,bi=coarsen_counts(p,prior['units'])
        if uni!=prior['unigram_counts'] or bi!=prior['bigram_counts']:raise ValueError('Coarse count lineage mismatch')
        coarse_enc={s:i for i,s in enumerate(prior['units'])};m=len(p['units']);old_n=len(prior['units']);mapping=[coarse_enc.get(s,old_n) for s in p['units']]+[old_n]
        expected=[[prior['secret_key_diagnostic_only'][c] if c<old_n else old_n for c in t] for t in prior['cipher_texts']]
        if [[mapping[u] for u in t] for t in p['window_unit_indices']]!=expected:raise ValueError('Coarse window lineage mismatch')
        texts,truth=make_cipher(p['window_unit_indices'],m);parts,labels,original,meta=prepare(texts)
        coverage={name:sorted({truth[s] for t in rows for s in t if s!=UNK}) for name,rows in zip(('train','validation','test'),original)}
        training=set(coverage['train']);missing=[i for i in range(m) if i not in training]
        all_aliases=set(truth);observed={s for t in texts for s in t if s!=UNK}
        inventory=[{'index':i,'unit':s,'model_tokens':p['unigram_counts'][i],
             'codepoints':[f'U+{ord(c):04X}' for c in s],'unicode_names':[U.name(c,'UNNAMED') for c in s],
             'outside_tamil_block':language=='Tamil' and any(not(0xB80<=ord(c)<=0xBFF) for c in s)} for i,s in enumerate(p['units'])]
        total=sum(p['unigram_counts']);top32=sum(sorted(p['unigram_counts'][:m],reverse=True)[:32])
        held_total=p['held_tokens'];held_known=held_total-p['held_unknown_tokens']
        r={'model_units':m,'model_tokens':total,'held_only_units':p['held_only_units'],'held_tokens':held_total,'held_unknown_tokens':p['held_unknown_tokens'],
           'full_held_token_coverage':held_known/held_total,'model_top32_coverage':top32/total,'complete_model_coverage':sum(p['unigram_counts'][:m])/total,
           'inventory':inventory,'coarse_counts_exactly_reproduced':True,'coarse_windows_exactly_reproduced':True,
           'model_documents':len(p['lm_document_ids']),'held_documents':len(p['held_document_ids']),
           'synthetic_feasibility':{'split':meta,'distinct_true_units_by_partition':{name:len(v) for name,v in coverage.items()},
              'missing_true_training_unit_indices':missing,'missing_true_training_units':[p['units'][i] for i in missing],
              'true_key_surjective_on_observed_training':not missing,'training_types_at_least_target_units':len(labels)>=m,
              'planned_alias_types':2*m,'observed_alias_types':len(observed),'aliases_never_observed':sorted(all_aliases-observed),
              'training_aliases':labels,'true_unit_for_training_alias':[truth[s] for s in labels],
              'scope':'Known truth used solely to audit synthetic feasibility; no fitting or historical accuracy claim.'}}
        out['languages'][language]=r
        print(language,'model units',m,'full held coverage',r['full_held_token_coverage'],'coarse coverage',r['model_top32_coverage'],
              'missing synthetic train units',len(missing),'source train types',len(labels),flush=True)
    save('full_target_audit.json',out)
if __name__=='__main__':main()

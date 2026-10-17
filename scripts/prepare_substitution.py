"""Optional local-source preparation; normal reproduction reads frozen numeric inputs."""
import collections as C
import gzip
import hashlib
import json
import random
from analyze import ROOT,canonical
from language_compare import load_sources,clusters,sample_windows
K=32

def main():
    languages,inventory=load_sources();lengths=[len(r['signs']) for r in json.loads((ROOT/'data/processed/icit_unique.json').read_text())]
    out={'design':'docs/EXPERIMENT_017.md','alphabet_size':K,'languages':{},'source_inventory':inventory,
         'scope':'Only selected single writing-unit labels, counts and opaque calibration windows. Ancient-language hypothesis, not phonetic truth.'}
    for name,docs in languages.items():
        docs=[{'id':str(r['id']),'tokens':clusters(r['words'])} for r in docs]
        groups=C.defaultdict(list)
        for i,r in enumerate(docs):groups[canonical(r['tokens'])].append(i)
        keys=sorted(groups);random.Random(314).shuffle(keys);cut=int(.6*len(keys))
        lm_indices=[i for k in keys[:cut] for i in groups[k]];held_indices=[i for k in keys[cut:] for i in groups[k]]
        freq=C.Counter(t for i in lm_indices for t in docs[i]['tokens']);units=sorted(freq,key=lambda s:(-freq[s],s))[:K];enc={s:i for i,s in enumerate(units)}
        lm=[[enc.get(s,K) for s in docs[i]['tokens']] for i in lm_indices];uni=[0]*(K+1);bi=[[0]*(K+1) for _ in range(K+1)]
        for t in lm:
            for s in t:uni[s]+=1
            for a,b in zip(t,t[1:]):bi[a][b]+=1
        held=[{'id':docs[i]['id'],'tokens':[enc.get(s,K) for s in docs[i]['tokens']]} for i in held_indices]
        windows,where=sample_windows(held,lengths,17)
        secret=list(range(K));random.Random(1031).shuffle(secret);truth=[0]*K
        for p,c in enumerate(secret):truth[c]=p
        cipher=[[secret[s] if s<K else K for s in t] for t in windows]
        out['languages'][name]={'units':units,'unigram_counts':uni,'bigram_counts':bi,
            'lm_document_ids':[docs[i]['id'] for i in lm_indices],'held_document_ids':[docs[i]['id'] for i in held_indices],
            'lm_document_groups':cut,'held_document_groups':len(keys)-cut,'target_known_token_fraction':sum(uni[:K])/sum(uni),
            'cipher_texts':cipher,'secret_key_diagnostic_only':truth,'windows':where,
            'scope':'Language-model documents and cipher-source documents are disjoint exact/reverse groups. Cipher windows may overlap within held source documents.'}
        print(name,'model docs',len(lm_indices),'held docs',len(held_indices),'coverage',out['languages'][name]['target_known_token_fraction'],flush=True)
    directory=ROOT/'data/substitution';directory.mkdir(exist_ok=True)
    raw=json.dumps(out,separators=(',',':'),ensure_ascii=False).encode();(directory/'inputs.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    (directory/'manifest.json').write_text(json.dumps({'design':out['design'],'sha256_uncompressed':hashlib.sha256(raw).hexdigest(),
        'source_inventory_sha256':hashlib.sha256((ROOT/'docs/language_resource_inventory.json').read_bytes()).hexdigest(),
        'attribution':'See ATTRIBUTION.md; Tamil Apache-2.0, Vedic CC BY-SA4.0. Character labels are writing units, not reconstructed Indus sounds.'},indent=2)+'\n')
if __name__=='__main__':main()

"""Optional cached-source preparation; offline audit uses attributed frozen inputs."""
import collections as C
import gzip
import hashlib
import json
from analyze import ROOT
from language_compare import load_sources,clusters

def main():
    oldraw=gzip.decompress((ROOT/'data/substitution/inputs.json.gz').read_bytes());old=json.loads(oldraw)
    sources,inventory=load_sources();out={'design':'docs/EXPERIMENT_021.md','languages':{},'source_inventory':inventory}
    for language,rows in sources.items():
        docs={str(r['id']):clusters(r['words']) for r in rows}
        if len(docs)!=len(rows):raise ValueError('Nonunique source IDs')
        p=old['languages'][language];lm_ids=p['lm_document_ids'];held_ids=p['held_document_ids']
        if set(lm_ids)&set(held_ids) or set(lm_ids)|set(held_ids)!=set(docs):raise ValueError('Source partition mismatch')
        freq=C.Counter(s for i in lm_ids for s in docs[i]);units=sorted(freq,key=lambda s:(-freq[s],s));enc={s:i for i,s in enumerate(units)};m=len(units)
        uni=[0]*(m+1);bi=[[0]*(m+1) for _ in range(m+1)]
        for i in lm_ids:
            t=[enc[s] for s in docs[i]]
            for s in t:uni[s]+=1
            for a,b in zip(t,t[1:]):bi[a][b]+=1
        held=[docs[i] for i in held_ids];windows=[]
        for t,where in zip(p['cipher_texts'],p['windows']):
            row=held[where['document_index']];start=where['offset'];window=row[start:start+len(t)]
            if len(window)!=len(t):raise ValueError('Window boundary changed')
            windows.append([enc.get(s,m) for s in window])
        held_count=C.Counter(s for row in held for s in row)
        out['languages'][language]={'units':units,'unigram_counts':uni,'bigram_counts':bi,'lm_document_ids':lm_ids,'held_document_ids':held_ids,
            'held_tokens':sum(held_count.values()),'held_unknown_tokens':sum(n for s,n in held_count.items() if s not in enc),
            'held_only_units':[{'unit':s,'tokens':held_count[s]} for s in sorted(held_count) if s not in enc],
            'window_unit_indices':windows,'windows':p['windows'],
            'scope':'Complete model-document writing units; held-only units keep unknown slots, no words or translations.'}
    folder=ROOT/'data/full_target';folder.mkdir(exist_ok=True);raw=json.dumps(out,ensure_ascii=False,separators=(',',':')).encode()
    (folder/'inputs.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    (folder/'manifest.json').write_text(json.dumps({'design':out['design'],'sha256_uncompressed':hashlib.sha256(raw).hexdigest(),
        'coarse_input_sha256':hashlib.sha256(oldraw).hexdigest(),'source_inventory_sha256':hashlib.sha256((ROOT/'docs/language_resource_inventory.json').read_bytes()).hexdigest(),
        'attribution':'See ATTRIBUTION.md; Tamil Apache-2.0 and adapted Vedic CC BY-SA4.0.'},indent=2)+'\n')
    print('Prepared full target counts/windows.')
if __name__=='__main__':main()

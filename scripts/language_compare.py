"""Representation sensitivity; no sound values or language-family inference.

--sample requires pinned cached candidate texts; default runs from opaque derived
numeric samples. Token dictionaries remain local, outside committed artifacts.
"""
import argparse
import collections as C
import gzip
import hashlib
import json
import math
import random
import statistics as S
import unicodedata as U
from pathlib import Path
from analyze import ROOT, conditional_entropy, entropy, save, shuffled

SAMPLE_DIR=ROOT/'data/language_samples'

def words(text):
    # Format controls (including zero-width joiners) are ignored, not word breaks.
    text=''.join(c for c in U.normalize('NFC',text).lower() if U.category(c)!='Cf')
    tokens=[];current=''
    for c in text:
        category=U.category(c)
        if category.startswith('L') or (category.startswith('M') and current):current+=c
        elif current:tokens.append(U.normalize('NFC',current));current=''
    if current:tokens.append(U.normalize('NFC',current))
    return tokens

def clusters(word_tokens):
    result=[]
    for word in word_tokens:
        current=''
        for c in U.normalize('NFD',word):
            if U.category(c).startswith('M'):
                if current:current+=c
            else:
                if current:result.append(U.normalize('NFC',current))
                current=c
        if current:result.append(U.normalize('NFC',current))
    return result

def conllu_documents(raw,upstream_split):
    docs=[]
    for block in raw.strip().split('\n\n'):
        forms=[];metadata={}
        for line in block.splitlines():
            if line.startswith('#') and '=' in line:
                k,v=line[1:].split('=',1);metadata[k.strip()]=v.strip()
            elif not line.startswith('#'):
                fields=line.split('\t')
                if len(fields)==10 and fields[0].isdigit() and fields[3]!='PUNCT':
                    forms.extend(words(fields[1]))
        if forms:
            docs.append({'id':metadata.get('sent_id',f'block-{len(docs)}'),
                         'upstream_split':upstream_split,'citation_text':metadata.get('citation_text'),
                         'citation_chapter':metadata.get('citation_chapter'),'words':forms})
    return docs

def load_sources():
    inventory=json.loads((ROOT/'docs/language_resource_inventory.json').read_text())
    docs={'Tamil':[],'Vedic_Sanskrit':[]}
    for language,source in inventory.items():
        for info in source['files']:
            name=info['url'].split('/')[-1]
            path=ROOT/'.cache/languages'/(language+'_'+name)
            raw=path.read_bytes()
            if hashlib.sha256(raw).hexdigest()!=info['sha256']:raise ValueError(f'Unpinned source: {path}')
            if name.endswith('.json'):
                for row in json.loads(raw):
                    forms=words(row.get('classical_tamil') or '')
                    if forms:docs[language].append({'id':row['verse_id'],'source_file':name,'words':forms})
            elif name.endswith('.conllu'):
                docs[language].extend(conllu_documents(raw.decode(),name.split('-ud-')[1].split('.')[0]))
    return docs,inventory

def sample_windows(documents,lengths,seed):
    bylength={n:[i for i,doc in enumerate(documents) if len(doc['tokens'])>=n] for n in set(lengths)}
    if any(not candidates for candidates in bylength.values()):raise ValueError('No document long enough')
    rng=random.Random(seed);texts=[];windows=[]
    for n in lengths:
        i=rng.choice(bylength[n]);doc=documents[i];offset=rng.randrange(len(doc['tokens'])-n+1)
        texts.append(doc['tokens'][offset:offset+n])
        windows.append({'document_index':i,'offset':offset})
    return texts,windows

def generate_samples():
    docs,source_inventory=load_sources();SAMPLE_DIR.mkdir(parents=True,exist_ok=True)
    lengths=[len(r['signs']) for r in json.loads((ROOT/'data/processed/icit_unique.json').read_text())]
    manifest={'design':'docs/EXPERIMENT_004.md','source_inventory':source_inventory,
              'indus_lengths_sha256':hashlib.sha256(json.dumps(lengths).encode()).hexdigest(),
              'samples':{},'unicode_database_version':U.unidata_version,
              'normalization':'NFC words; NFD base-letter plus following marks recomposed to NFC; punctuation/Cf ignored',
              'license_notice':'Tamil opaque derived samples: upstream Apache-2.0; Vedic Sanskrit opaque derived samples: CC BY-SA 4.0. See ATTRIBUTION.md.'}
    for language,rows in docs.items():
        for unit in ('words','letter_marks'):
            documents=[{**{k:v for k,v in row.items() if k!='words'},
                        'tokens':row['words'] if unit=='words' else clusters(row['words'])} for row in rows]
            vocab=sorted({s for doc in documents for s in doc['tokens']});enc={s:i for i,s in enumerate(vocab)}
            for doc in documents:doc['tokens']=[enc[s] for s in doc['tokens']]
            name=language+'_'+unit
            runs=[]
            for seed in range(17,27):
                texts,windows=sample_windows(documents,lengths,seed)
                runs.append({'seed':seed,'texts':texts,'windows':windows})
            output={'language':language,'unit':unit,'source_documents':len(documents),'source_vocabulary_size':len(vocab),
                    'documents':[{k:v for k,v in doc.items() if k!='tokens'} for doc in documents],'runs':runs}
            raw=json.dumps(output,separators=(',',':'),ensure_ascii=False).encode()
            compressed=gzip.compress(raw,mtime=0)
            (SAMPLE_DIR/(name+'.json.gz')).write_bytes(compressed)
            manifest['samples'][name]={'file':name+'.json.gz','sha256_uncompressed':hashlib.sha256(raw).hexdigest(),
                                       'bytes_uncompressed':len(raw),'bytes_compressed':len(compressed)}
            # Dictionary allows local source audit, but is not packaged as text content.
            (ROOT/'.cache/languages'/(name+'_token_dictionary.json')).write_text(json.dumps(vocab,ensure_ascii=False))
    (SAMPLE_DIR/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')

def metrics(texts,seed,trials=49):
    unigram=C.Counter(s for t in texts for s in t)
    observed=conditional_entropy(texts);rng=random.Random(seed)
    null=[conditional_entropy(shuffled(texts,'global_frequency',rng)) for _ in range(trials)]
    duplicates=len(texts)-len({tuple(t) for t in texts})
    return {'texts':len(texts),'tokens':sum(unigram.values()),'vocabulary':len(unigram),
            'unigram_bits':entropy(unigram),'conditional_bits':observed,
            'hapax_fraction':sum(n==1 for n in unigram.values())/len(unigram),
            'duplicate_windows':duplicates,'null_mean_bits':S.mean(null),'null_sd_bits':S.stdev(null),
            'order_constraint_bits':S.mean(null)-observed,
            'p_lower':(1+sum(v<=observed for v in null))/(trials+1),'null_trials':trials}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--sample',action='store_true');args=parser.parse_args()
    if args.sample:generate_samples()
    manifest=json.loads((SAMPLE_DIR/'manifest.json').read_text())
    indus=[r['signs'] for r in json.loads((ROOT/'data/processed/icit_unique.json').read_text())]
    baseline=metrics(indus,17)
    output={'design':manifest['design'],'indus':baseline,'sampling':'10 seeds (17-26), exact Indus lengths, uniform eligible document then uniform offset with replacement',
            'normalization':manifest['normalization'],'comparison':{},
            'limitation':'Descriptive proxies, mixed genres and much later chronology; no sign/word equivalence, phonetic alignment, ancestry or family identification.'}
    for name,info in sorted(manifest['samples'].items()):
        raw=gzip.decompress((SAMPLE_DIR/info['file']).read_bytes())
        if hashlib.sha256(raw).hexdigest()!=info['sha256_uncompressed']:raise ValueError('Numeric sample hash mismatch')
        data=json.loads(raw);runs=[]
        for run in data['runs']:
            if list(map(len,run['texts']))!=list(map(len,indus)):raise ValueError('Length mismatch')
            result=metrics(run['texts'],run['seed'])
            result.update({'seed':run['seed'],'represented_documents':len({w['document_index'] for w in run['windows']}),
                           'absolute_conditional_entropy_distance':abs(result['conditional_bits']-baseline['conditional_bits'])})
            runs.append(result)
        summary={key:{'mean':S.mean(r[key] for r in runs),'min':min(r[key] for r in runs),'max':max(r[key] for r in runs)}
                 for key in ('conditional_bits','order_constraint_bits','absolute_conditional_entropy_distance','vocabulary','duplicate_windows')}
        output['comparison'][name]={'source_documents':data['source_documents'],'source_vocabulary_size':data['source_vocabulary_size'],
                                    'runs':runs,'summary':summary}
        print(name,json.dumps(summary),flush=True)
    output['nearest_proxy_by_representation']={unit:min(('Tamil','Vedic_Sanskrit'),key=lambda lang:
         output['comparison'][lang+'_'+unit]['summary']['absolute_conditional_entropy_distance']['mean'])
         for unit in ('words','letter_marks')}
    output['ranking_changed_between_representations']=len(set(output['nearest_proxy_by_representation'].values()))>1
    save('language_representation.json',output)
    print('Nearest proxy labels (not language identification):',output['nearest_proxy_by_representation'])

if __name__=='__main__':main()

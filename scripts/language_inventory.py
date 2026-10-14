"""Fetch pinned candidate historical-language resources and audit basic coverage.

Only metadata is committed; source texts stay in ignored .cache/languages.
This is resource acquisition, not an Indus-language identification experiment.
"""
import hashlib
import json
import re
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCES={'Tamil':{'repo':'indic-corpora/sentamizh-corpus','commit':'e833395c0535915e82156ac9d912836cabec9a29',
    'files':['data/processed/Akananuru_All.json','data/processed/Purananuru_All.json','LICENSE'],
    'license':'Repository declares Apache 2.0; Tamil text derived from Project Madurai editions'},
    'Vedic_Sanskrit':{'repo':'UniversalDependencies/UD_Sanskrit-Vedic','commit':'09c59eed987f28c2fd3a9972b4b5437439f46832',
    'files':['sa_vedic-ud-train.conllu','sa_vedic-ud-dev.conllu','sa_vedic-ud-test.conllu','LICENSE.txt'],
    'license':'CC BY-SA 4.0; authors credited in upstream README'}}

def main():
    output={}
    cache=ROOT/'.cache/languages';cache.mkdir(parents=True,exist_ok=True)
    for language,source in SOURCES.items():
        files=[]
        for path in source['files']:
            url=f'https://raw.githubusercontent.com/{source["repo"]}/{source["commit"]}/{path}'
            with urllib.request.urlopen(url,timeout=60) as response:raw=response.read()
            (cache/(language+'_'+Path(path).name)).write_bytes(raw)
            info={'url':url,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
            if path.endswith('.json'):
                rows=json.loads(raw)
                texts=[r.get('classical_tamil') for r in rows if r.get('classical_tamil')]
                info.update({'records':len(rows),'nonempty_original_texts':len(texts),
                             'unicode_codepoints':sum(map(len,texts)),
                             'upstream_period_labels':sorted({r['period'] for r in rows}),
                             'whitelisted_text_field':'classical_tamil; translations/interpretive annotations excluded',
                             'original_edition_links':sorted({r.get('source_url','') for r in rows})})
            elif path.endswith('.conllu'):
                blocks=raw.decode().strip().split('\n\n')
                forms=[line.split('\t')[1] for line in raw.decode().splitlines()
                       if re.match(r'^\d+\t',line)]
                info.update({'sentence_blocks':len(blocks),'syntactic_word_forms':len(forms),
                             'unicode_codepoints_in_word_forms':sum(map(len,forms)),
                             'representation':'CoNLL-U FORM column; excludes multiword-range and empty-node IDs'})
            files.append(info)
        output[language]={'repository':source['repo'],'commit':source['commit'],
                          'license_note':source['license'],'files':files}
    (ROOT/'docs/language_resource_inventory.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(output,indent=2,ensure_ascii=False))

if __name__=='__main__':main()

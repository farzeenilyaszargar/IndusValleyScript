"""Recompute snapshots; --check requires equivalent JSON (float tolerance 1e-12)."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def artifacts():
    paths=list((ROOT/'data/processed').glob('*.json'))+list((ROOT/'results').glob('*.json'))
    return {str(p.relative_to(ROOT)):json.loads(p.read_text()) for p in paths}

def equivalent(a,b,path='root'):
    if isinstance(a,float) and isinstance(b,(float,int)):
        if not math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12):
            raise ValueError(f'Numeric drift at {path}: {a!r} != {b!r}')
    elif isinstance(a,dict) and isinstance(b,dict):
        if a.keys()!=b.keys():raise ValueError(f'Key drift at {path}')
        for k in a:equivalent(a[k],b[k],f'{path}.{k}')
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b):raise ValueError(f'Length drift at {path}')
        for i,(x,y) in enumerate(zip(a,b)):equivalent(x,y,f'{path}[{i}]')
    elif type(a)!=type(b) or a!=b:
        raise ValueError(f'Exact value drift at {path}: {a!r} != {b!r}')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    manifest=json.loads((ROOT/'data/raw/manifest.json').read_text())
    for name,expected in manifest['output_sha256'].items():
        actual=hashlib.sha256((ROOT/'data/raw'/name).read_bytes()).hexdigest()
        if actual!=expected:raise ValueError(f'Source snapshot hash mismatch: {name}')
    before=artifacts()
    for name in ('test_pipeline.py','test_latent.py','test_allographs.py','test_language_compare.py','test_stroke_counts.py',
                 'normalize.py','analyze.py','extended.py','latent_grammar.py','near_copy.py',
                 'allographs.py','language_compare.py','stroke_counts.py','catalogue.py','report.py'):
        subprocess.run([sys.executable,str(ROOT/'scripts'/name)],check=True,cwd=ROOT)
    after=artifacts()
    if args.check:equivalent(before,after)
    print(f'Verified source hashes and reproduced {len(after)} JSON artifacts.')

if __name__=='__main__':main()

"""Recompute from snapshots; --check requires byte-identical analytical JSON."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def hashes():
    paths=list((ROOT/'data/processed').glob('*.json'))+list((ROOT/'results').glob('*.json'))
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    manifest=json.loads((ROOT/'data/raw/manifest.json').read_text())
    for name,expected in manifest['output_sha256'].items():
        actual=hashlib.sha256((ROOT/'data/raw'/name).read_bytes()).hexdigest()
        if actual!=expected:raise ValueError(f'Source snapshot hash mismatch: {name}')
    before=hashes()
    for name in ('test_pipeline.py','normalize.py','analyze.py','extended.py','catalogue.py','report.py'):
        subprocess.run([sys.executable,str(ROOT/'scripts'/name)],check=True,cwd=ROOT)
    after=hashes()
    if args.check and before!=after:
        changed=sorted(k for k in set(before)|set(after) if before.get(k)!=after.get(k))
        raise ValueError(f'Deterministic artifact mismatch: {changed}')
    print(f'Verified source hashes and reproduced {len(after)} JSON artifacts.')

if __name__=='__main__':main()

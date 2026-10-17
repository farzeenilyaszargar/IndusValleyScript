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
    for name in ('test_pipeline.py','test_latent.py','test_allographs.py','test_language_compare.py','test_stroke_counts.py','test_correspondence.py','test_metadata_models.py','test_fish_rebus.py','test_uncertainty_sensitivity.py','test_gap_reconstruction.py','test_administrative_control.py','test_mahadevan_primary.py','test_motif_prediction.py','test_reference_candidates.py','test_graphic_variants.py','test_substitution_search.py','test_novel_pattern_substitution.py','test_homophonic_channel.py','validate_glyph_snapshot.py',
                 'normalize.py','analyze.py','extended.py','latent_grammar.py','near_copy.py',
                 'allographs.py','language_compare.py','stroke_counts.py','catalogue_correspondence.py','metadata_models.py','fish_rebus_audit.py','uncertainty_sensitivity.py','gap_reconstruction.py','administrative_control.py','mahadevan_primary.py','motif_prediction.py','reference_candidates.py','graphic_variants.py','substitution_search.py','novel_pattern_substitution.py','homophonic_channel.py','catalogue.py','report.py'):
        subprocess.run([sys.executable,str(ROOT/'scripts'/name)],check=True,cwd=ROOT)
    after=artifacts()
    if args.check:equivalent(before,after)
    print(f'Verified source hashes and checked {len(after)} JSON artifacts (regenerated analyses plus validated numeric glyph snapshot).')

if __name__=='__main__':main()

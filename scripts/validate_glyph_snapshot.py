"""Network-free integrity and arithmetic checks for optional image-derived input."""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    path=ROOT/'data/processed/glyph_morphology.json'
    manifest=json.loads((ROOT/'data/raw/glyph_morphology_manifest.json').read_text())
    if hashlib.sha256(path.read_bytes()).hexdigest()!=manifest['descriptor_file_sha256']:
        raise ValueError('Glyph descriptor snapshot hash mismatch')
    data=json.loads(path.read_text())
    refs={r['sign']:r['image_url'] for r in json.loads((ROOT/'data/raw/glyph_index.json').read_text())}
    rows={r['sign']:r for r in data['descriptors']}
    if rows.keys()!=refs.keys() or len(rows)!=len(data['descriptors']):raise ValueError('Glyph inventory mismatch')
    for sign,r in rows.items():
        if r['source_url']!=refs[sign] or len(r['source_sha256'])!=64:raise ValueError('Reference metadata mismatch')
        int(r['source_sha256'],16)
        x0,y0,x1,y1=r['ink_bbox'];bw,bh=x1-x0+1,y1-y0+1
        if not(0<=x0<=x1<r['canvas_width'] and 0<=y0<=y1<r['canvas_height']):raise ValueError('Invalid ink bounds')
        if sum(r['component_sizes'])!=r['ink_pixels'] or len(r['component_sizes'])!=r['connected_components_8']:
            raise ValueError('Component mass mismatch')
        for a,b in [(r['bbox_aspect'],bw/bh),(r['bbox_ink_fraction'],r['ink_pixels']/(bw*bh)),
                    (r['canvas_ink_height_fraction'],bh/r['canvas_height']),
                    (r['canvas_ink_width_fraction'],bw/r['canvas_width'])]:
            if not math.isclose(a,b,abs_tol=1e-12,rel_tol=1e-12):raise ValueError('Descriptor arithmetic mismatch')
        if not all(math.isfinite(r[k]) for k in ('centroid_x','centroid_y','second_moment_xx','second_moment_yy','second_moment_xy')):
            raise ValueError('Nonfinite descriptor')
        if not(0<=r['centroid_x']<=1 and 0<=r['centroid_y']<=1):raise ValueError('Invalid centroid')
        if r['second_moment_xx']*r['second_moment_yy']+1e-12<r['second_moment_xy']**2:
            raise ValueError('Invalid second-moment matrix')
    print(f'Checked {len(rows)} scalar glyph records against pinned snapshot hash and arithmetic invariants.')

if __name__=='__main__':main()

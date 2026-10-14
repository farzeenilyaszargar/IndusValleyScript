"""Optional Pillow-dependent reference acquisition and scalar morphology encoding.

Raw images stay in ignored cache. Numeric descriptors and hashes are committed.
"""
import collections as C
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

def components(points):
    remaining=set(points);sizes=[]
    while remaining:
        start=min(remaining);remaining.remove(start);stack=[start];n=0
        while stack:
            x,y=stack.pop();n+=1
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    if not(dx or dy):continue
                    p=(x+dx,y+dy)
                    if p in remaining:remaining.remove(p);stack.append(p)
        sizes.append(n)
    return sorted(sizes,reverse=True)

def descriptors(im):
    im=im.convert('L');w,h=im.size
    ink={(x,y) for y in range(h) for x in range(w) if im.getpixel((x,y))<128}
    if not ink:raise ValueError('Empty glyph')
    x0=min(x for x,y in ink);x1=max(x for x,y in ink);y0=min(y for x,y in ink);y1=max(y for x,y in ink)
    bw,bh=x1-x0+1,y1-y0+1
    normalized=[((x-x0+.5)/bw,(y-y0+.5)/bh) for x,y in sorted(ink)]
    cx=sum(x for x,y in normalized)/len(ink);cy=sum(y for x,y in normalized)/len(ink)
    xx=sum((x-cx)**2 for x,y in normalized)/len(ink);yy=sum((y-cy)**2 for x,y in normalized)/len(ink)
    xy=sum((x-cx)*(y-cy) for x,y in normalized)/len(ink)
    cs=components(ink)
    return {'canvas_width':w,'canvas_height':h,'ink_bbox':[x0,y0,x1,y1],
            'ink_pixels':len(ink),'bbox_aspect':bw/bh,'bbox_ink_fraction':len(ink)/(bw*bh),
            'canvas_ink_height_fraction':bh/h,'canvas_ink_width_fraction':bw/w,
            'centroid_x':cx,'centroid_y':cy,'second_moment_xx':xx,'second_moment_yy':yy,
            'second_moment_xy':xy,'connected_components_8':len(cs),'component_sizes':cs}

def main():
    references=json.loads((ROOT/'data/raw/glyph_index.json').read_text())
    descriptor_path=ROOT/'data/processed/glyph_morphology.json'
    expected={r['sign']:r['source_sha256'] for r in json.loads(descriptor_path.read_text())['descriptors']} if descriptor_path.exists() else {}
    cache=ROOT/'.cache/glyph-reference';cache.mkdir(parents=True,exist_ok=True)
    def one(ref):
        path=cache/(ref['sign']+'.jpg')
        if not path.exists():
            with urllib.request.urlopen(ref['image_url'],timeout=45) as response:raw=response.read()
            path.write_bytes(raw)
        raw=path.read_bytes()
        if ref['sign'] in expected and hashlib.sha256(raw).hexdigest()!=expected[ref['sign']]:
            raise ValueError(f'Glyph source hash changed: {ref["sign"]}')
        with Image.open(path) as im:features=descriptors(im)
        return {'sign':ref['sign'],'source_url':ref['image_url'],'source_sha256':hashlib.sha256(raw).hexdigest(),**features}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(one,references))
    rows.sort(key=lambda r:r['sign'])
    targets={'001':1,'002':2,'003':3,'004':4,'031':1,'033':3}
    lookup={r['sign']:r for r in rows}
    checks=[{'sign':s,'expected_components':n,'observed_components':lookup[s]['connected_components_8'],
             'match':lookup[s]['connected_components_8']==n} for s,n in targets.items()]
    output={'design':'docs/EXPERIMENT_007.md','threshold':128,'images':len(rows),'descriptors':rows,
            'component_checks':checks,'representation':'Scalar thresholded morphology only; no raster pixels packaged',
            'limitation':'Standardized catalogue drawings, not original object photographs. Cropping, antialiasing and style affect features. No phonetic or semantic embedding.'}
    descriptor_path.write_text(json.dumps(output,indent=2)+'\n')
    manifest={'descriptor_file_sha256':hashlib.sha256(descriptor_path.read_bytes()).hexdigest(),
              'producer':'scripts/glyph_morphology.py (optional Pillow dependency)',
              'source_commit':'8dc5837469bc6694c05f9b310eee90b08399df9e',
              'images_packaged':False,'default_reproduction':'Validates the numeric input snapshot; does not regenerate pixels/features without optional source acquisition.'}
    (ROOT/'data/raw/glyph_morphology_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'images':len(rows),'checks':checks},indent=2))

if __name__=='__main__':main()

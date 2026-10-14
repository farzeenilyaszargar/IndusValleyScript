"""Acquire pinned public transcriptions; never ingest proposed readings."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'cisi': ('mayig/indus-valley-script-corpus', 'ad2f1e218a34b8c33c57de0d6cb8d99272765bbb'),
    'field': ('field-cady/indus_valley_script_corpus', '30308260d8da50151a79185c9e98404db9da331a'),
    'explorer': ('tejesh-raut/indus-valley-script', '8dc5837469bc6694c05f9b310eee90b08399df9e'),
}

def fetch(repo, commit, path):
    url = f'https://raw.githubusercontent.com/{repo}/{commit}/{path}'
    with urllib.request.urlopen(url, timeout=60) as response:
        raw = response.read()
    return raw, {'url': url, 'sha256': hashlib.sha256(raw).hexdigest()}

def main():
    out = ROOT / 'data/raw'
    out.mkdir(parents=True, exist_ok=True)
    manifest = {'sources': SOURCES, 'files': {}, 'retrieved_date': '2026-10-15'}
    repo, commit = SOURCES['field']
    raw, info = fetch(repo, commit, 'inscriptions.csv')
    rows = list(csv.DictReader(io.StringIO(raw.decode())))
    # Explicit whitelist: interpretations, translations, class assignments and notes excluded.
    fields = ['id', 'cisi', 'site', 'region', 'material', 'type', 'preservation',
              'complete', 'dir.', 'text length', 'text']
    with (out / 'icit_metadata.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows({k: row[k] for k in fields} for row in rows)
    manifest['files']['icit_metadata.csv'] = info | {'transformation': 'metadata whitelist; no proposed readings'}
    raw, info = fetch(repo, commit, 'LICENSE')
    (out / 'CISI_LICENSE.txt').write_bytes(raw)
    manifest['files']['CISI_LICENSE.txt'] = info
    # Clone only the transcription source, outside tracked data; verify exact revision.
    repo, commit = SOURCES['cisi']
    checkout = ROOT / '.cache/upstream/cisi'
    if not checkout.exists():
        checkout.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'clone', f'https://github.com/{repo}.git', str(checkout)], check=True)
    subprocess.run(['git', '-C', str(checkout), 'fetch', 'origin', commit], check=True, capture_output=True)
    subprocess.run(['git', '-C', str(checkout), 'checkout', '--detach', commit], check=True, capture_output=True)
    for folder in ['corpus', 'features']:
        combined = []
        for path in sorted((checkout / folder).rglob('*.json')):
            raw = path.read_bytes()
            manifest['files'][str(path.relative_to(checkout))] = {
                'sha256': hashlib.sha256(raw).hexdigest(),
                'url': f'https://raw.githubusercontent.com/{repo}/{commit}/{path.relative_to(checkout)}'}
            combined.append({'source_file': str(path.relative_to(checkout)), 'content': json.loads(raw)})
        (out / f'cisi_{folder}.json').write_text(json.dumps(combined, indent=2, ensure_ascii=False) + '\n')
    # Index available glyph images; do not redistribute image/font assets with unclear rights.
    repo, commit = SOURCES['explorer']
    raw, info = fetch(repo, commit, 'data/signs.js')
    ids = json.loads(raw.decode().split('=', 1)[1].strip().rstrip(';'))
    catalog = [{'namespace': 'ICIT', 'sign': f'{n:03}',
                'image_url': f'https://raw.githubusercontent.com/{repo}/{commit}/icit/full/S{n:03}.jpg',
                'placeholder': n in (0, 999)} for n in ids]
    (out / 'glyph_index.json').write_text(json.dumps(catalog, indent=2) + '\n')
    manifest['files']['glyph_index.json'] = info | {'transformation': 'numeric IDs and reference links only'}
    # Record output hashes too, including transformed files.
    manifest['output_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted(out.iterdir()) if p.name != 'manifest.json'}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Acquired {len(rows)} ICIT-export records and {len(ids)} glyph references.')

if __name__ == '__main__':
    main()

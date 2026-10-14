"""Conservative corpus normalization; namespaces never silently merged."""
import collections
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
OUT = ROOT / 'data/processed'

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def icit_parse(row):
    text = row['text']
    reasons = []
    if not re.fullmatch(r'\+\d{3}(?:-\d{3})*\+', text):
        reasons.append('damaged_boundary_multiline_or_nonstandard')
    signs = re.findall(r'\d{3}', text)
    if any(s in ('000', '999') for s in signs):
        reasons.append('unknown_or_separator')
    if not signs:
        reasons.append('empty')
    return signs, reasons

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader((RAW / 'icit_metadata.csv').open()))
    records, rejected = [], []
    for row in rows:
        signs, reasons = icit_parse(row)
        record = {'corpus': 'ICIT_export', 'id': row['id'], 'cisi': row['cisi'],
                  'site': row['site'], 'type': row['type'], 'direction': row['dir.'],
                  'signs': signs, 'source_text': row['text'], 'exclusion_reasons': reasons}
        records.append(record)
        if reasons:
            rejected.append(record)
    eligible = [r for r in records if not r['exclusion_reasons']]
    seen, unique = set(), []
    for r in eligible:
        key = tuple(r['signs'])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    save('icit_all.json', records)
    save('icit_unique.json', unique)
    save('icit_rejected.json', rejected)

    cisi = []
    for file in json.loads((RAW / 'cisi_corpus.json').read_text()):
        for side in file['content']:
            gs = side['graphemes']
            reasons = []
            if any(g['id'] == 'P000' for g in gs):
                reasons.append('unknown')
            if any(len(g['features']) < 3 for g in gs):
                reasons.append('short_feature_vector')
            if any(g['features'][0] != 0 or g['features'][2] != 0 for g in gs if len(g['features']) >= 3):
                reasons.append('damage_or_uncertainty')
            if len({g['features'][1] for g in gs if len(g['features']) >= 3}) != 1:
                reasons.append('multiline_or_empty')
            # Source records sealING in visual left-to-right order. Reverse to read right-to-left.
            cisi.append({'corpus': 'CISI_Parpola', 'id': side['id'], 'source_file': file['source_file'],
                         'description': side['description'], 'site': 'Mohenjo-daro',
                         'signs': [g['id'] for g in reversed(gs)],
                         'allographs': [g for g in reversed(gs)], 'exclusion_reasons': reasons})
    cseen, cunique = set(), []
    for r in cisi:
        key = tuple(r['signs'])
        if not r['exclusion_reasons'] and key not in cseen:
            cseen.add(key)
            cunique.append(r)
    save('cisi_all.json', cisi)
    save('cisi_unique.json', cunique)
    features = [x['content'] for x in json.loads((RAW / 'cisi_features.json').read_text())
                if x['content']['id'].startswith('P')]
    save('parpola_catalog.json', features)
    vocab = sorted({s for r in records for s in r['signs']} - {'000', '999'})
    cvocab = sorted({r['id'] for r in features} - {'P000'})
    # Reserve 0 for padding, 1 unknown, 2 beginning, 3 end.
    encodings = {'reserved': {'PAD': 0, 'UNK': 1, 'BOS': 2, 'EOS': 3},
                 'ICIT': {s: i+4 for i, s in enumerate(vocab)},
                 'Parpola': {s: i+4 for i, s in enumerate(cvocab)}}
    save('encodings.json', encodings)
    save('numeric_inscriptions.json', {
        'ICIT': [{'id': r['id'], 'tokens': [encodings['ICIT'][s] for s in r['signs']]} for r in unique],
        'Parpola': [{'id': r['id'], 'tokens': [encodings['Parpola'][s] for s in r['signs']]} for r in cunique]})
    glyphs = json.loads((RAW / 'glyph_index.json').read_text())
    indexed = {g['sign'] for g in glyphs if not g['placeholder']}
    audit = {'icit_raw_rows': len(rows), 'icit_eligible_rows': len(eligible),
             'icit_unique_sequences': len(unique), 'icit_observed_ids_all_records': len(vocab),
             'icit_unique_tokens': sum(len(r['signs']) for r in unique),
             'icit_unique_signs': len({s for r in unique for s in r['signs']}),
             'icit_exclusions': dict(collections.Counter(x for r in rejected for x in r['exclusion_reasons'])),
             'cisi_sides': len(cisi), 'cisi_clean_unique': len(cunique),
             'parpola_catalog_signs_excluding_damage': len(cvocab),
             'glyph_reference_ids_excluding_placeholders': len(indexed),
             'observed_icit_ids_without_glyph_reference': sorted(set(vocab)-indexed),
             'glyph_reference_ids_not_observed': sorted(indexed-set(vocab)),
             'orientation': 'ICIT stored order, not asserted reading order; CISI reversed per source convention',
             'inventory_limit': 'Public source coverage only, not every excavated sign; catalogues disagree on allographs.'}
    save('audit.json', audit)
    print(json.dumps(audit, indent=2))

if __name__ == '__main__':
    main()

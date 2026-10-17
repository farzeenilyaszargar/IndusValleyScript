"""Build a searchable local sign catalogue with attributed remote glyph references."""
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    glyphs=json.loads((ROOT/'data/raw/glyph_index.json').read_text())
    features=json.loads((ROOT/'data/processed/parpola_catalog.json').read_text())
    enc=json.loads((ROOT/'data/processed/encodings.json').read_text())
    cards=[]
    for g in glyphs:
        if g['placeholder']:continue
        sign=g['sign'];url=html.escape(g['image_url'],quote=True)
        cards.append(f'<article data-search="icit {sign}"><h3>ICIT {sign}</h3>'
                     f'<a href="{url}" target="_blank" rel="noopener"><img loading="lazy" src="{url}" alt="Reference glyph ICIT {sign}" /></a>'
                     f'<p>Integer token: {enc["ICIT"].get(sign,"unobserved")}</p>'
                     '<small>External glyph reference; transcription unverified</small></article>')
    for r in features:
        if r['id']=='P000':continue
        desc=html.escape(r['description']);sign=r['id']
        refs='; '.join(f'{key.split("_")[0]}: {", ".join(r.get(key,[]))}' for key in ('parpola_graphemes','wells_graphemes','mahadevan_graphemes'))
        search=html.escape(f'parpola {sign} {r["description"]} {refs}',quote=True)
        cards.append(f'<article data-search="{search.lower()}"><h3>Parpola {sign}</h3><p>{desc}</p>'
                     f'<p>Integer token: {enc["Parpola"].get(sign,"unobserved")}</p><small>{html.escape(refs)}</small></article>')
    mahadevan=json.loads((ROOT/'data/processed/mahadevan_sign_catalog.json').read_text())
    for r in mahadevan['signs']:
        sign=r['id'];url=html.escape(r['source_url'],quote=True)
        cards.append(f'<article data-search="mahadevan {sign.lower()} primary im77"><h3>Mahadevan {sign}</h3>'
                     f'<p>Integer token: {r["integer"]}</p><p><a href="{url}" target="_blank" rel="noopener">Original sign-list glyph, printed page {r["source_printed_page"]}</a></p>'
                     '<small>Separate Mahadevan namespace; no sound value or automatic crosswalk</small></article>')
    graphic=json.loads((ROOT/'data/processed/mahadevan_graphic_catalog.json').read_text())
    for r in graphic['base_sign_addenda']:
        url=html.escape(r['source_url'],quote=True);sign=r['id']
        cards.append(f'<article data-search="mahadevan {sign.lower()} postscript"><h3>Mahadevan {sign} postscript</h3>'
                     f'<p>Integer: {r["integer"]} (postscript namespace)</p><a href="{url}" target="_blank" rel="noopener">Source drawing, printed p.25</a>'
                     '<p>Not in frozen 417-ID application benchmark</p></article>')
    for r in graphic['variants']:
        url=html.escape(r['source_url'],quote=True);sign=r['id'];citation=html.escape(r['citation_raw'])
        search=html.escape(f'mahadevan graphic variant {sign} {r["base_id"]} {r["section"]} {r["citation_raw"]}'.lower(),quote=True)
        cards.append(f'<article data-search="{search}"><h3>{sign}</h3><p>Graphic integer: {r["integer"]}</p>'
                     f'<p>Source family {r["base_id"]}; form {r["family_ordinal"]}; example {citation}</p>'
                     f'<a href="{url}" target="_blank" rel="noopener">Printed p.{r["printed_page"]}, column {r["column"]}</a>'
                     '<p><small>Research ordinal, source-defined graphic family; no token assignment or sound value</small></p></article>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Indus sign research catalogue</title><style>
body{margin:0;background:#f5f2eb;color:#233734;font:16px system-ui}header{padding:36px max(24px,6vw);background:#153e3b;color:#fff}h1{font-size:34px;margin:0 0 10px}header p{max-width:850px;line-height:1.6}main{padding:24px max(24px,6vw)}input{padding:14px;border:1px solid #aaa;border-radius:5px;font:inherit;width:min(90%,600px)}#grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;margin-top:24px}article{background:white;padding:18px;border:1px solid #ddd;border-radius:6px}article h3{margin:0 0 12px}article p{line-height:1.5}img{height:90px;max-width:100%;object-fit:contain}small{color:#66716e;line-height:1.5}article[hidden]{display:none}a{color:#24786e}footer{padding:30px;font-size:14px}
</style><header><h1>Indus sign research catalogue</h1><p>715 ICIT glyph references, 395 Parpola descriptions and 417 separate Mahadevan sign-list references, two postscript signs and 641 indexed graphic forms. Entries overlap across catalogues and variants; this is not a count of distinct historical signs. Numeric IDs and context embeddings do not establish sounds or meanings. The catalogues remain separate; coverage is limited to the audited public sources.</p></header>
<main><label for="search">Search by sign ID, description, or catalogue</label><p><input id="search" placeholder="Try ICIT 740, P050, fish, vertical stroke"></p><p id="count" aria-live="polite"></p><section id="grid">'''+''.join(cards)+'''</section></main>
<footer>Glyph references: tejesh-raut/indus-valley-script (pinned commit 8dc5837); requires network access. Descriptions and source crosswalks: mayig/indus-valley-script-corpus (MIT). Crosswalks are attributed proposals, not validated sign equivalences. Mahadevan sign-list references: original 1977 book, printed pp. 32-35 (public scan). No externally hosted artwork is packaged here.</footer>
<script>const cards=[...document.querySelectorAll('article')],q=document.querySelector('#search'),count=document.querySelector('#count');function filter(){let n=0;const term=q.value.toLowerCase().trim();for(const c of cards){c.hidden=!c.dataset.search.includes(term);if(!c.hidden)n++}count.textContent=n+' catalogue entries shown'}q.addEventListener('input',filter);filter();</script></html>'''
    (ROOT/'docs/SIGN_CATALOGUE.html').write_text(page)
    print(f'Built catalogue with {len(cards)} entries.')

if __name__=='__main__':main()

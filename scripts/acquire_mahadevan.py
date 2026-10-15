"""Optional online acquisition of the official public archaeological collection."""
import hashlib
import json
import urllib.parse
import urllib.request
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ENDPOINT='https://firestore.googleapis.com/v1/projects/theindusscript/databases/(default)/documents/indusarray'
FIELDS=('textnum','sideline','locus','level','inscobj','fs80','dir','posnum','signnum')+tuple(f'S{i}' for i in range(1,15))

def main():
    cache=ROOT/'.cache/mahadevan-primary';cache.mkdir(exist_ok=True)
    rows=[];pages=[];token=None;seen_tokens=set();started=datetime.now(timezone.utc).isoformat()
    while True:
        query={'pageSize':1000}
        if token:query['pageToken']=token
        url=ENDPOINT+'?'+urllib.parse.urlencode(query)
        with urllib.request.urlopen(url,timeout=60) as response:raw=response.read()
        page=json.loads(raw);index=len(pages);(cache/f'page-{index:02}.json').write_bytes(raw)
        pages.append({'page':index,'sha256':hashlib.sha256(raw).hexdigest(),'documents':len(page.get('documents',[]))})
        for doc in page.get('documents',[]):
            fields=doc['fields'];record={k:next(iter(fields[k].values())) if k in fields else None for k in FIELDS}
            if any(isinstance(v,(dict,list)) for v in record.values()):raise ValueError('Unexpected field schema')
            rows.append({'document_id':doc['name'].rsplit('/',1)[-1],'source_update_time':doc.get('updateTime'),'fields':record})
        print(f'page {index}: {len(rows)} records',flush=True)
        token=page.get('nextPageToken')
        if not token:break
        if token in seen_tokens:raise ValueError('Pagination repeated')
        seen_tokens.add(token)
    ids=[r['document_id'] for r in rows]
    if len(set(ids))!=len(ids):raise ValueError('Duplicate documents during non-atomic pagination')
    rows.sort(key=lambda r:(int(r['document_id']) if r['document_id'].isdigit() else 10**9,r['document_id']))
    output=ROOT/'data/raw/mahadevan_primary.json';output.write_text(json.dumps(rows,indent=2)+'\n')
    manifest={'source':'RMRL Indus Research Centre official Indus Script application','application':'https://indusscript.in',
        'collection_url':ENDPOINT,'fields_whitelist':FIELDS,'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
        'records':len(rows),'pages':pages,'output_sha256':{output.name:hashlib.sha256(output.read_bytes()).hexdigest()},
        'scope':'Public archaeological numeric records only; no phonetic mappings. Paginated reads are not an atomic historical snapshot; raw response pages cached privately. Whitelisted snapshot is frozen for offline checks.'}
    (ROOT/'data/raw/mahadevan_primary_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()

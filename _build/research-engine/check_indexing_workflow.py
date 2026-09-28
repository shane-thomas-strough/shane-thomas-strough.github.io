import subprocess,tempfile,yaml
from pathlib import Path
p=Path(__file__).resolve().parents[2] / '.github/workflows/index-search-engines.yml'
s=p.read_text(); d=yaml.safe_load(s); steps=d['jobs']['index-search-engines']['steps']
assert 'indexing.googleapis.com' not in s and 'secrets.GOOGLE_INDEXING_KEY' not in s
assert 'https://api.indexnow.org/indexnow' in s
for step in steps:
 if 'run' not in step: continue
 body=step['run'].replace('${{ steps.detect.outputs.url_json }}','[]')
 subprocess.run(['bash','-n'],input=body,text=True,check=True)
submit=next(x['run'] for x in steps if x.get('name','').startswith('Submit to IndexNow'))
condition=submit[submit.index('if [ "$HTTP_STATUS"'):]
for status,expected in [('200',0),('202',0),('400',1),('403',1),('429',1),('500',1)]:
 r=subprocess.run(['bash','-c',condition],env={'HTTP_STATUS':status},capture_output=True,text=True)
 assert r.returncode==expected,(status,r.stdout,r.stderr)
print('PASS: YAML parse, all shell blocks syntax, restricted API removed, IndexNow retained, 6 response-status branches; no network submission')

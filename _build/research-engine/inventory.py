import json, sys, re, subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
from xml.etree import ElementTree as ET
import argparse
ap=argparse.ArgumentParser(description='Read-only local publication audit using the existing CONSENSUS raw parser')
ap.add_argument('--site',type=Path,required=True)
ap.add_argument('--consensus',type=Path,required=True)
ap.add_argument('--out',type=Path,required=True)
args=ap.parse_args()
sys.path.insert(0,str(args.consensus.resolve()))
from lens.raw_audit import Text as Parser
root=args.site.resolve()
out=args.out.resolve(); out.mkdir(parents=True,exist_ok=True)
class Links(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t in ('a','img','script','link'):
   v=a.get('href') or a.get('src')
   if v:self.links.append((t,v))
rows=[]; broken=[]
sitemap=[e.text for e in ET.parse(root/'sitemap.xml').iter() if e.tag.endswith('}loc')]
for f in sorted(root.rglob('*.html')):
 if '.git' in f.parts:continue
 p=Parser(); text=f.read_text();p.feed(text); links=Links();links.feed(text)
 schemas=[];errors=[]
 for raw in re.findall(r'<script[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>',text,re.S|re.I):
  try:schemas.append(json.loads(raw))
  except ValueError as e:errors.append(str(e))
 rel=str(f.relative_to(root));url='https://shanestrough.com/'+rel
 for tag,href in links.links:
  u=urlsplit(urljoin(url,href))
  if u.hostname!='shanestrough.com':continue
  path=unquote(u.path).lstrip('/') or 'index.html'
  if not (root/path).exists() and not path.startswith('cdn-cgi/'):
   broken.append({'source':rel,'tag':tag,'target':href})
 rows.append({'path':rel,'title':p.title,'canonical':p.canonical,'description':bool(p.meta.get('description')),'og_title':bool(p.meta.get('og:title')),'twitter_card':p.meta.get('twitter:card'),'h1':' '.join(p.h1),'raw_word_count':len(p.words),'schemas':schemas,'jsonld_errors':errors,'in_sitemap':p.canonical in sitemap,'robots':p.robots,'links':[h for t,h in links.links if t=='a']})
result={'scope':'Local working tree, including pre-existing uncommitted Bake-Off; raw HTML only, not proof of deployment/indexing','head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'pages':rows,'sitemap_urls':sitemap,'broken_local_references':broken,'source_documents':[str(p.relative_to(root)) for d in ('field-notes','Poetry','_build') for p in sorted((root/d).rglob('*')) if p.suffix in ('.md','.docx') ]}
(out/'site-inventory.json').write_text(json.dumps(result,indent=2)+'\n')
print('pages',len(rows),'sitemap',len(sitemap),'missing descriptions',sum(not r['description'] for r in rows),'missing canonical',sum(not r['canonical'] for r in rows),'jsonld errors',sum(len(r['jsonld_errors']) for r in rows))
for r in rows:print(r['path'],'|',r['title'],'|',r['canonical'],'|',','.join(str(s.get('@type')) for s in r['schemas'] if isinstance(s,dict)))
print('broken local references',len(broken))

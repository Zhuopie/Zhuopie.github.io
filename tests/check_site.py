"""Dependency-free structural/content checks for the static academic website."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.data=[]; self.jsonld=[]; self.in_script=False; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if tag=='script': self.in_script=a.get('type')=='application/ld+json'
    def handle_endtag(self, tag):
        if tag=='script': self.in_script=False
    def handle_data(self, data):
        (self.jsonld if self.in_script else self.data).append(data)
    def attrs(self, tag): return [a for t,a in self.tags if t==tag]
pages={'index.html':'/', 'research/index.html':'/research/', 'interests/index.html':'/interests/', '404.html':'/404.html'}
for file, path in pages.items():
    doc=Document((ROOT/file).read_text())
    assert doc.attrs('html')[0].get('lang')=='en',file
    assert len(doc.attrs('h1'))==1,file
    assert len(doc.attrs('main'))==1,file
    assert len(doc.attrs('title'))==1,file
    assert not re.search(r'[\u3400-\u9fff]', ''.join(doc.data)),f'Non-English visible content: {file}'
    assert any(a.get('name')=='description' and a.get('content') for a in doc.attrs('meta')),file
    assert any(a.get('rel')=='canonical' and a['href']=='https://zhuopie.github.io'+path for a in doc.attrs('link')),file
    ids=[a['id'] for _,a in doc.tags if 'id' in a]; assert len(ids)==len(set(ids)),file
    for a in doc.attrs('a') + doc.attrs('link'):
        href=a.get('href',''); u=urlsplit(href)
        if u.scheme or u.netloc: continue
        if not u.path: assert not u.fragment or u.fragment in ids,(file,href); continue
        target=ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else (ROOT/file).parent/unquote(u.path)
        if target.is_dir(): target=target/'index.html'
        assert target.is_file(),(file,href)
    assert all(a.get('type')=='application/ld+json' for a in doc.attrs('script')),'Unexpected JavaScript'
    person=json.loads(''.join(doc.jsonld)); assert person['name']=='Zhuopai Li' and person['jobTitle']=='Assistant Professor'
    robots=next(a['content'] for a in doc.attrs('meta') if a.get('name')=='robots')
    assert ('noindex' in robots)==(file in ['404.html','interests/index.html']),file
    if file!='404.html': assert len([a for a in doc.attrs('a') if a.get('aria-current')=='page'])==1,file
    print('PASS',file)
for path in ['_pages','_posts','gitbook','search.html','search_plus_index.json','index.md']:
    assert not (ROOT/path).exists(),f'Old notes remain: {path}'
assert (ROOT/'.nojekyll').is_file()
sitemap=ET.parse(ROOT/'sitemap.xml')
urls={x.text for x in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
assert urls=={'https://zhuopie.github.io/','https://zhuopie.github.io/research/'}
assert 'Sitemap: https://zhuopie.github.io/sitemap.xml' in (ROOT/'robots.txt').read_text()
research=Document((ROOT/'research/index.html').read_text()); assert len(research.attrs('article'))==6
print('PASS note removal, static deployment, sitemap, robots, and six publication records')

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
pages={'index.html':'/', 'research/index.html':'/research/', 'interests/index.html':'/interests/', 'projects/index.html':'/projects/', '404.html':'/404.html'}
for file, path in pages.items():
    doc=Document((ROOT/file).read_text())
    assert doc.attrs('html')[0].get('lang')=='en',file
    assert len(doc.attrs('h1'))==1,file
    assert len(doc.attrs('main'))==1,file
    assert len(doc.attrs('title'))==1,file
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
    assert all(a.get('type')=='application/ld+json' or (file=='index.html' and a.get('src')=='/assets/guestbook.js?v=2-bilingual') for a in doc.attrs('script')),'Unexpected JavaScript'
    person=json.loads(''.join(doc.jsonld)); assert person['name']=='Zhuopai Li' and person['jobTitle']=='Assistant Professor'
    robots=next(a['content'] for a in doc.attrs('meta') if a.get('name')=='robots')
    assert ('noindex' in robots)==(file=='404.html'),file
    if file!='404.html': assert len([a for a in doc.attrs('a') if a.get('aria-current')=='page'])==1,file
    print('PASS',file)
for path in ['_pages','_posts','gitbook','search.html','search_plus_index.json','index.md']:
    assert not (ROOT/path).exists(),f'Old notes remain: {path}'
assert (ROOT/'.nojekyll').is_file()
sitemap=ET.parse(ROOT/'sitemap.xml')
urls={x.text for x in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
assert urls=={'https://zhuopie.github.io/','https://zhuopie.github.io/research/','https://zhuopie.github.io/projects/','https://zhuopie.github.io/interests/'}
assert 'Sitemap: https://zhuopie.github.io/sitemap.xml' in (ROOT/'robots.txt').read_text()
research=Document((ROOT/'research/index.html').read_text()); assert len(research.attrs('article'))==7
home=(ROOT/'index.html').read_text()
for name in ['Lingfang (Ivy) Li', 'Chiu Yu Ko', 'Xinfei Huang']:
    assert name in home,name
text=(ROOT/'research/index.html').read_text()
for title in ['平台经济反垄断监管：立法动向、实践难题与典型案例','方言壁垒与城市间贸易：证据、机制和对策','贸易数字化政策与企业对外直接投资：来自跨境电商综合试验区的证据','出口经验与企业对外直接投资','信邦：信息化引导的管理变革']:
    assert title in text,title
assert 'Case study, 2023.' in text
projects=(ROOT/'projects/index.html').read_text()
assert projects.count('<dd>Research participant</dd>')==2
assert '<dt>Subproject PI</dt><dd><a ' in projects
assert '2022.01–2026.12' in projects
for term in ['数字经济反垄断科学监管创新研究','市场监管服务和融入全国统一大市场建设的政策研究','博士生国家奖学金','上海市优秀博士毕业生']:
    assert term in projects,term
print('PASS note removal, static deployment, sitemap, robots, six publications, separate case study, advisors, project roles, and honors')

# Owner-supplied photos and the simpler home page must remain accessible.
assert home.count('Assistant Professor') == 4  # description, OG description, JSON-LD and biography
assert 'profile-details' not in home and 'class="position"' not in home
assert 'class="eyebrow"' not in home
assert 'Outstanding Paper Award, 2026' in projects
assert '中国数字经济与管理学术会议暨中国信息学会第38届年会（2026）会议优秀论文' in projects
interests=(ROOT/'interests/index.html').read_text()
assert 'I enjoy playing badminton.' in interests and 'More to come.' not in interests
assert 'Traffic Supply' not in projects  # Do not infer or add a paper title.
image_count=0
for file in pages:
    for a in Document((ROOT/file).read_text()).attrs('img'):
        assert a.get('alt') and a.get('width') and a.get('height'), (file,a)
        assert a['src'].startswith('/assets/images/'), (file,a)
        assert (ROOT/a['src'].lstrip('/')).is_file(), (file,a)
        image_count+=1
assert image_count==3
print('PASS concise homepage, confirmed badminton interest, 2026 award, and three local accessible photos')

# Chinese journal titles retain their originals and have a separate English line.
translations = {
    "平台经济反垄断监管：立法动向、实践难题与典型案例": "Antitrust Regulation of the Platform Economy: Legislative Developments, Practical Challenges, and Illustrative Cases",
    "方言壁垒与城市间贸易：证据、机制和对策": "Dialect Barriers and Intercity Trade: Evidence, Mechanisms, and Policy Responses",
    "贸易数字化政策与企业对外直接投资：来自跨境电商综合试验区的证据": "Trade Digitalization Policy and Firms’ Outward Foreign Direct Investment: Evidence from Cross-Border E-Commerce Comprehensive Pilot Zones",
    "出口经验与企业对外直接投资": "Export Experience and Firms’ Outward Foreign Direct Investment"
}
for original, translation in translations.items():
    expected = f'<h3 lang="zh-Hans">{original}</h3>\\s*<p class="publication-translation" lang="en">{re.escape(translation)} <span class="translation-label">\\(translation\\)</span></p>'
    assert re.search(expected, text), original
assert text.count('class="publication-translation"') == 4
publication_links = [a['href'] for a in research.attrs('a') if a.get('class') == 'publication-link']
assert publication_links == [
    'https://jmsc.tju.edu.cn/jmsc/article/issue/2026_5',
    'https://jrpl.ajcass.com/Magazine/GetIssueContentList?issue=4&year=2026',
    'https://doi.org/10.1080/00036846.2026.2665336',
    'https://doi.org/10.1080/13504851.2024.2449541',
]
assert 'University record' not in text
assert 'The linked records provide publication details.' not in text
print('PASS four bilingual Chinese journal titles, no personal-profile publication links, and preserved journal/DOI links')

assert (ROOT/"assets/guestbook.js").is_file()
assert (ROOT/"assets/guestbook.css").is_file()
assert "textContent=c.body" in (ROOT/"assets/guestbook.js").read_text()
assert "innerHTML" not in (ROOT/"assets/guestbook.js").read_text()
print("PASS guestbook asset allowlist and text-only rendering")

# All owner-written guestbook copy is presented in both English and Chinese.
guestbook = home.split('<section class="guestbook-section"', 1)[1].split('</section>', 1)[0]
for english, chinese in [
    ('Guestbook', '留言板'),
    ('Leave a note to say hello.', '欢迎留下你的足迹。'),
    ('I was here /', '我来了'),
    ('Like /', '点赞'),
    ('No account needed. Reactions are remembered per browser.', '无需账号。互动状态按浏览器记录。'),
    ('optional /', '选填'),
    ('No email or account is needed.', '无需邮箱或账号'),
    ('Messages and nicknames are stored in the guestbook service', '留言与昵称存储在留言板服务中'),
    ('Reaction counts are recorded per browser, not per unique visitor', '互动计数按浏览器记录，并非独立访客统计'),
    ('the application does not store your original IP address', '本应用不存储你的原始 IP 地址'),
    ('Anonymous messages and nicknames are not verified identities.', '匿名留言与昵称不代表经过身份核验。'),
]:
    assert english in guestbook and chinese in guestbook, (english, chinese)
guestbook_js = (ROOT/'assets/guestbook.js').read_text()
for phrase in ['This message has already been submitted. / 这条留言已经提交过了。',
               'Please refresh to see your message. / 请刷新查看留言。',
               'Please refresh the page and try again. / 请刷新页面后重试。']:
    assert phrase in guestbook_js, phrase
assert '/assets/guestbook.css?v=2-bilingual' in home
assert '/assets/guestbook.js?v=2-bilingual' in home
print('PASS bilingual guestbook labels, privacy disclosures, errors, and refresh feedback')

# Translation labels should be unobtrusive and follow each English title.
assert 'English translation:' not in text
assert text.count('(translation)') == 4
assert 'provided for reference' not in text
for file in ['research/index.html', 'projects/index.html', 'interests/index.html']:
    assert 'class="eyebrow"' not in (ROOT/file).read_text(), file
print('PASS concise translation suffixes and page headings')

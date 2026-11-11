# Zhuopai Li · Academic website

Public website: https://zhuopie.github.io/

A small, accessible, all-English academic website hosted on GitHub Pages. It uses plain HTML and CSS, with no JavaScript runtime, analytics, external fonts, or package dependencies. `.nojekyll` keeps deployment static.

## Pages

- `index.html`: Home, affiliation, research interests, education, and contact.
- `research/index.html`: Published research with links to publication records.
- `interests/index.html`: A reserved page for personal interests. It is deliberately marked `noindex` until substantive content is provided.
- `404.html`: Missing and removed pages return an explanatory error page, not an automatic redirect.

## Editing and checking

Edit the HTML and `assets/style.css` directly. Check the site with:

```sh
python3 tests/check_site.py
```

For a local preview, use a static HTTP server from the repository root. No build step is required. Publishing the default branch uses the repository's existing GitHub Pages deployment.

Keep page titles, descriptions, canonical URLs, and `sitemap.xml` in sync. Only add an Interests sitemap entry after replacing its placeholder with confirmed content and removing its `noindex` directive.

## Content sources

Biographical details and published work were verified against the [Shenzhen University faculty profile](https://eco.szu.edu.cn/info/1033/5949.htm), linked journal records, and publisher DOI records. Chinese-language publication titles are shown in English translation. No unpublished projects or unverified CV, social profile, or personal interests are included.

The former notes, reading attachments, search index, and GitBook interface have been removed from the current website. Git history remains intact so previous revisions can be recovered when needed; there is no notes archive on the website.

Search-engine discovery is supported by descriptive metadata, canonical links, structured person data, robots.txt, and a sitemap. These do not guarantee indexing or ranking. Search Console ownership verification and an indexing request are separate owner actions.

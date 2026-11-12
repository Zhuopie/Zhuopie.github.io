# Zhuopai Li · Academic website

Public website: https://zhuopie.github.io/

A small, accessible, English-language academic website with original Chinese publication and project titles hosted on GitHub Pages. It uses plain HTML and CSS, with no JavaScript runtime, analytics, external fonts, or package dependencies. `.nojekyll` keeps deployment static.

## Pages

- `index.html`: A concise introduction, portrait, contact links, education, and advisors.
- `research/index.html`: Published research with original Chinese titles, English translations, and journal or article links where available, plus a separate case-study section.
- `projects/index.html`: Research-project participation and academic honors.
- `interests/index.html`: Badminton as a personal interest, with an owner-supplied photograph.
- `404.html`: Missing and removed pages return an explanatory error page, not an automatic redirect.

## Editing and checking

Edit the HTML and `assets/style.css` directly. Check the site with:

```sh
python3 tests/check_site.py
```

For a local preview, use a static HTTP server from the repository root. No build step is required. Publishing the default branch uses the repository's existing GitHub Pages deployment.

Keep page titles, descriptions, canonical URLs, and `sitemap.xml` in sync. The Interests page is indexed and included in the sitemap.

## Content sources

Biographical details and published work were verified against the [Shenzhen University faculty profile](https://eco.szu.edu.cn/info/1033/5949.htm), linked journal records, and publisher DOI records. Chinese-language journal publications use their original titles with English translations provided for reference; the translations are not represented as verified official publisher titles. Journal issue links are retained, while personal-profile links are not used as publication links. Advisor relationships, the case-study citation, and honors were supplied by the site owner. Faculty names and links were checked against their university or personal profiles. The NSFC entry is a Major Project subproject with Lingfang (Ivy) Li as subproject PI; the site owner is listed as a research participant, not PI. The Shanghai government project and completed/participant status are recorded on the Shenzhen University profile. The 2026 conference Outstanding Paper Award, its conference name, and the three photographs were supplied by the site owner. The award entry does not infer a paper title. Other award years and a government-project year are not inferred. The portrait uses a reversible CSS crop; all three image files retain their original pixels and contain no EXIF metadata.

The former notes, reading attachments, search index, and GitBook interface have been removed from the current website. There is no notes archive on the current website. This content update does not rewrite Git history.

Search-engine discovery is supported by descriptive metadata, canonical links, structured person data, robots.txt, and a sitemap. These do not guarantee indexing or ranking. Search Console ownership verification and an indexing request are separate owner actions.

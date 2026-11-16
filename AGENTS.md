# AGENTS.md — byteportal.tech

## Project

Zero-build static blog: plain HTML, Tailwind from CDN, vanilla JS. No npm, bundler, framework, or generator.

## New Post Workflow

1. Follow `prompt/new-blog-post.md` for structure, voice, SEO, and checks.
2. `mkdir -p <slug> && cp prompt/template.html <slug>/index.html`. The folder name is the URL; no date in it.
3. Add the first `<li>` to `index.html`'s `#post-feed`, the new `<item>` to `feed.xml`, the `<url>` to `sitemap.xml`, and entries to `llms.txt` and `llms-full.txt`.
4. Keep the header, footer, and theme script as they are unless the task explicitly changes them.

## Content Rules

- Search-intent title, 50–60 characters. Meta description, 140–160 characters.
- 700–1000 words. Read time is about 200 words per minute, rounded up.
- Every code block needs the correct `language-*` class (`bash`, `python`, `js`, `ts`, `json`, `html`, `css`, `rust`, `go`, `sql`, `yaml`, `text`).
- Name primary sources and link them. Say whether a post is hands-on or docs-first.

## Images and Credits

- Store images in `assets/images/<year>/<slug>/`. Never hotlink.
- Set the real `width` and `height`, write descriptive `alt` text, and add a caption.
- **Third-party images need confirmed reuse permission and a visible `Image credits` line in the article footer, naming and linking each source. A caption credit is attribution, not permission.**
- If permission is unclear, do not use the image. Replace it with an original diagram or cut it.
- The Open Graph image must be 1200×630 with `og:image:width`, `og:image:height`, and `og:image:alt`.

## Verification

- Run `python3 -m http.server 8000`, then check the post and homepage in a browser.
- Validate JSON-LD, `feed.xml`, and `sitemap.xml`.
- Confirm canonical, Open Graph, Twitter, and image URLs are correct.
- Confirm every image loads and its file dimensions match the HTML attributes.

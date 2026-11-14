# byteportal.tech

Zero-build static blog: HTML, CSS, a little vanilla JS, Tailwind from the CDN. No Node, no npm, no generator. Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. You can also just double-click `index.html` — links are relative, so the site works from a file path, from a subfolder, or from a domain root. It will **not** work behind a dev server that has SPA fallback (the `localhost:3000` style used by Next/Vite/CRA): those never serve your `.html` files, so post links silently fall back to the homepage. Use a plain static file server.

## Layout

```
index.html                  homepage + post feed (the only page you edit twice)
about/index.html            about page (/about/)
robots.txt                  crawler directives (disallows /prompt/ and /404/)
feed.xml                    RSS 2.0 feed for readers and aggregators
404.html                    custom not-found fallback
404/index.html              not-found page folder (/404/)
assets/css/style.css        custom CSS; print styles; no-Tailwind fallback layout
assets/js/main.js           theme toggle + consent bar, feed filter, code copy buttons
assets/Byte-Portal-Logo.svg header logo + tab icon (referenced from every page)
assets/images/<year>/       post images, grouped by year
<post-slug>/index.html       one folder per post; the folder name is the URL
vercel.json                 clean URLs and redirects for moved URLs
.gitignore                  OS/editor noise, test artifacts, .env
```

## Theme

Light is the default. One inline line in each page's `<head>` applies a saved dark choice before paint, so there is no flash:

```html
<script>
  if (localStorage.theme === 'dark') document.documentElement.classList.add('dark');
</script>
```

`main.js` writes `localStorage.theme` only after the reader clicks **Allow** in the consent bar, and records that answer in `localStorage['theme-consent']`. **No thanks** keeps the theme for the current page only, stores the refusal in `sessionStorage`, and deletes any saved theme — so the ask returns next visit and nothing persists. The bar is built in JS and appended to `<body>`; restyle it under `.theme-consent` in `style.css`.

## Publish a post

1. `mkdir api-gateways && cp posts/template.html api-gateways/index.html` — the folder name is the URL (`/api-gateways/`), so keep it short and readable. No date in the folder: the `<time>` tag carries it, and the feed sorts on that.
2. In the copy, replace: `<title>`, `meta[name=description]`, `link[rel=canonical]`, `og:title`, `og:description`, `og:url`, `og:image`, `article:published_time`, and the visible `<time datetime="YYYY-MM-DD">` plus its text. Canonical and `og:url` end in the folder name and a slash: `https://www.byteportal.tech/api-gateways/`.
3. Put images in `assets/images/2026/` and reference them as `../assets/images/2026/file.jpg` from inside the post folder.
4. In `index.html`, copy the commented `<li>` block into `<ol id="post-feed">`, point `href` at `api-gateways/`, update date/title/summary. Newest first.
5. Moved or renamed a folder? Add a permanent redirect in `vercel.json` so the old link keeps working.

Code blocks carry their language in the class, and `main.js` turns that into a header label plus a Copy button:

```html
<pre><code class="language-python">import boto3</code></pre>
```

Supported labels: python, bash, js/javascript, ts, json, html, css, rust, go, sql, yaml, text. Anything else is upper-cased, and a block with no class just says "Code".

Colours come from highlight.js (one CDN script + `github-dark` theme). The card background and spacing stay ours — only the token colours are borrowed. If the CDN is blocked the blocks render plain and Copy still works.

## Change once, site-wide

The site name (`byteportal.tech`), the domain in the canonical and Open Graph tags, the author name (`Your Name`), and the footer appear in `index.html` and in `posts/template.html`. Change them in those two files and in any existing posts:

```bash
rg -l "byteportal.tech|Your Name" --glob '*.html'
```

## Scaling notes

- **Duplication ceiling.** The header, footer and theme script are copied into every post; that is the price of no includes and no build. It holds to hundreds of posts. If it starts to hurt, the cheapest escapes are, in order: a ~20-line `layout.js` that injects the header/footer (cost: nav links vanish with JS off), then a one-off build step.
- **Feed length.** One `<ol>` handles a few hundred entries fine. Past that, move older entries to `archive/index.html` and link it from the homepage; the filter keeps the rest findable.
- **Search.** The homepage filter is substring matching over each entry's text, revealed only when JS runs. No index file to maintain — add the `<li>` and it is searchable.
- **Images.** A new `assets/images/<year>/` folder each January; the only path to update is the template's `<img src>`. `width`/`height` prevent layout shift — update them to the real image size.
- **Tailwind CDN.** Fine for a personal blog; it prints a production warning and means styles depend on the network. `style.css` keeps the page readable if it fails. If you ever drop the zero-build rule, compile Tailwind to `assets/css/tailwind.css` and delete the CDN tags.
- **Syntax colours.** highlight.js is a second CDN dependency (~40 KB gzipped, includes the common languages). It fails soft: no network, plain code, copy button still there. Adding a language outside the common bundle means one more `<script>` tag in every page.
- **No sitemap, RSS or JSON-LD by default.** Each is another file to update per post. Add them when a search engine or reader client actually asks.

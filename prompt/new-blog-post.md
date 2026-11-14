# Prompt: write a new post for byteportal.tech

Copy the block below into your agent, fill in the **TOPIC** section, send. It already knows the stack (zero-build static site, `prompt/template.html`, `index.html` feed) and the house style.

---

## Prompt

You are writing one new post for **byteportal.tech**, a zero-build static blog (plain HTML, Tailwind from CDN, a little vanilla JS). No npm, no build step, no generator.

### Topic

- Subject: `<topic, link, release notes, or a few bullets>`
- Primary Search Query: `<what a developer types into Google, e.g. "run aws locally", "api gateway vs reverse proxy">`
- Angle I care about: `<why this matters to a working developer, or leave blank>`
- Anything to leave out: `<or leave blank>`

If the subject is a link or a release note, fetch it and read it first. Do not guess facts, versions, dates, or command flags. Anything you cannot verify goes in the post as an open question, or is cut.

### Voice — the part that matters most

Write like you are explaining this to a smart friend over coffee.

- Short sentences. One idea each. If a sentence needs a comma to breathe, split it.
- Simple words. Say "use" not "utilise", "make" not "facilitate", "so" not "consequently".
- Second person. "You write a few lines… you wait." Put the reader in the scene.
- Concrete before abstract. A real example, a real command, a real number — then the idea behind it.
- Define a term the first time you use it, in the same sentence. Never let jargon stand alone.
- Analogies are welcome if they are one line and accurate (a stand-in, a spare key, a test kitchen).
- No filler openers ("In today's fast-paced world…"), no hype adjectives, no exclamation marks.
- Take a position. Say whether it is worth your time and say why.
- Explain the downside too. Honest posts are the engaging ones.

### Shape

1. **Hook** — the friction the reader already feels. Two or three sentences, no throat-clearing.
2. **The short version** — 3 bullets: what it is, what it does for you, what it costs or where it stops.
3. **Body** — 3–5 `h2` sections, each answering one question a reader would actually ask ("What is it really?", "How close is it to the real thing?", "What breaks?").
4. **Show, don't tell** — one short code block or command, kept to what someone would paste to try it.
   - Tag the language on the `<code>`: `<pre><code class="language-python">…</code></pre>`. The site reads that class to print the label, add the Copy button and colour the syntax. An untagged block just says "Code" and stays plain.
   - Ids that get a proper label: `python`, `bash`, `js`/`javascript`, `ts`, `json`, `html`, `css`, `rust`, `go`, `sql`, `yaml`, `text`.
5. **What it is not** — a bullet list of limits. This builds trust.
6. **Takeaway** — one sentence plus one small action the reader can do this week.
7. **Links** — the primary source(s), bare and named.

Length: 700–1000 words. If it runs longer, cut sections, not detail inside them.

---

### Complete SEO Process (Search Intent Focused, Not Brand Focused)

Every post must be engineered for Google search intent, high organic click-through rates (CTR), and rich social snippets. Do **not** waste title space on brand prefixes or generic naming like `Post Title — byteportal.tech`.

#### 1. Search-Intent Focused Title (`<title>`)
- **Formula:** `[Primary Search Query / Problem Solved] + [Specific Value or Constraint] + [Action Hook]`
- **Length:** 50–60 characters max (prevents truncation in Google SERPs).
- **Rule:** Target what developers actually type in Google ("run aws locally", "api gateway vs reverse proxy", "postgres connection pool exhaustion").
- ❌ **Bad:** `AWS Emulator — byteportal.tech` (Brand-focused, zero search intent)
- ❌ **Bad:** `AWS now runs on your laptop` (Passive, misses key search query terms)
- ✅ **Good:** `Run AWS Locally on Your Laptop with AWS Emulator (No Account Needed)`

#### 2. Search-Intent Meta Description (`<meta name="description">`)
- **Formula:** `[Target search problem solved] + [Exact tools / services / actions] + [Outcome or speed/cost benefit].`
- **Length:** 140–160 characters.
- **Rule:** Active voice, dense information, no marketing fluff ("In this post we explore..."). Answer the search query directly so users know why to click.
- ✅ **Good:** `Run S3, DynamoDB, SQS, and Lambda locally using AWS Emulator. Test AWS SDK calls in milliseconds without an AWS account, cloud deploy, or AWS bill.`

#### 3. Featured Image & Social Cards
- **Specs:** 1200×630 (or high-res diagram). Store in `assets/images/<year>/`.
- **Image Tags:** Provide explicit `og:image:width`, `og:image:height`, and a descriptive `og:image:alt` that explains the diagram.
- **Open Graph:**
  - `<meta property="og:type" content="article">`
  - `<meta property="og:title" content="[Search-intent title]">`
  - `<meta property="og:description" content="[Search-intent description]">`
  - `<meta property="og:url" content="https://www.byteportal.tech/<slug>/">`
  - `<meta property="og:site_name" content="byteportal.tech">`
  - `<meta property="og:image" content="https://www.byteportal.tech/assets/images/<year>/<file>">`
  - `<meta property="og:image:width" content="1200">`
  - `<meta property="og:image:height" content="630">`
  - `<meta property="og:image:alt" content="[Descriptive caption]">`
  - `<meta property="article:published_time" content="YYYY-MM-DD">`
- **Twitter Card:**
  - `<meta name="twitter:card" content="summary_large_image">`
  - `<meta name="twitter:title" content="[Search-intent title]">`
  - `<meta name="twitter:description" content="[Search-intent description]">`
  - `<meta name="twitter:image" content="https://www.byteportal.tech/assets/images/<year>/<file>">`

#### 4. Canonical & RSS Auto-Discovery
- `<link rel="canonical" href="https://www.byteportal.tech/<slug>/">`
- `<link rel="alternate" type="application/rss+xml" title="byteportal.tech" href="/feed.xml">`

#### 5. Schema.org JSON-LD Structured Data
Include valid `BlogPosting` schema in `<head>` so Google generates rich search snippets:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "[Search-intent title]",
  "description": "[Search-intent description]",
  "image": "https://www.byteportal.tech/assets/images/<year>/<file>",
  "datePublished": "YYYY-MM-DD",
  "dateModified": "YYYY-MM-DD",
  "author": {
    "@type": "Person",
    "name": "Your Name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "byteportal.tech",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.byteportal.tech/assets/Byte-Portal-Logo.svg"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://www.byteportal.tech/<slug>/"
  }
}
</script>
```

---

### Files to touch

1. `mkdir -p <slug> && cp prompt/template.html <slug>/index.html` — the folder name **is** the URL (`/<slug>/`), so keep it short and readable. No date in the folder; the `<time>` tag carries it.
2. In `<slug>/index.html`, update **every** SEO field:
   - `<meta name="robots" content="index, follow">` (template defaults to `noindex, nofollow` to prevent indexing draft files)
   - `<title>` (search-intent focused, 50-60 chars)
   - `meta[name=description]` (140-160 chars)
   - `link[rel=canonical]` (`https://www.byteportal.tech/<slug>/`)
   - `og:title`, `og:description`, `og:url`, `og:image`, `og:image:width`, `og:image:height`, `og:image:alt`, `article:published_time`
   - `twitter:title`, `twitter:description`, `twitter:image`
   - Schema.org JSON-LD snippet
   - The visible `<time datetime="YYYY-MM-DD">` plus its text.
3. Write the article body inside the existing `<div class="prose …">`. Keep the header, footer and theme script untouched.
4. In `index.html`, add one `<li>` as the **first** child of `<ol id="post-feed">`, matching the existing entry exactly: `href="<slug>/"`, `<time>`, `h2` title, and a one-sentence summary that reads like the post's hook.
5. In `feed.xml`, add the new `<item>` at the top of the RSS feed:
   ```xml
   <item>
     <title>[Search-intent title]</title>
     <link>https://www.byteportal.tech/<slug>/</link>
     <guid isPermaLink="true">https://www.byteportal.tech/<slug>/</guid>
     <pubDate>Day, DD Mon YYYY 00:00:00 +0000</pubDate>
     <description>[Search-intent description]</description>
   </item>
   ```
6. Read time: count words, assume ~200 words per minute, round up. Update the `· N min read` line. If you moved an existing post, add a permanent redirect in `vercel.json`.

---

### Before you say done

- [ ] Title is search-intent focused (50-60 chars), not brand-first.
- [ ] Meta description is 140-160 chars and answers search query directly.
- [ ] Canonical URL and OG URL end in `https://www.byteportal.tech/<slug>/`.
- [ ] Open Graph & Twitter Card tags have real titles, descriptions, and 1200x630 image dimensions.
- [ ] Schema.org JSON-LD `BlogPosting` block has valid syntax and URLs.
- [ ] Images exist at the paths used; `width`/`height` match real pixel size; captions and alt text are plain English.
- [ ] Every code block carries a `language-*` class, and the language shown in its header bar is the real one.
- [ ] Added entry to `index.html` feed and new `<item>` to `feed.xml`.
- [ ] Rendered check: `python -m http.server 8000`, open post and homepage, verify SEO tags in page source (`Ctrl+U`).

Report back in three lines: the file created, the images used, and anything you could not verify.

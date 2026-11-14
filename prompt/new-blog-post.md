# Prompt: write a new post for byteportal.tech

Copy the block below into your agent, fill in the **TOPIC** section, send. It already knows the stack (zero-build static site, `posts/template.html`, `index.html` feed) and the house style.

---

## Prompt

You are writing one new post for **byteportal.tech**, a zero-build static blog (plain HTML, Tailwind from CDN, a little vanilla JS). No npm, no build step, no generator.

### Topic

- Subject: `<topic, link, release notes, or a few bullets>`
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

### Images — use the ones in the site

- Look before you write: `ls -R assets/images/`. Reuse an existing image when it fits the topic — do not duplicate or re-download it.
- New images go in `assets/images/<year>/` (this year: `assets/images/2026/`), referenced from inside the post folder as `../../assets/images/2026/file.png`.
- Prefer a local image over a remote one. If you must hotlink, keep the original URL and credit the source in the caption.
- Place an image where it does the explaining — right after the paragraph that introduces the concept, never as decoration at the top.
- Each image needs: real `width`/`height` (prevents layout shift), meaningful `alt` text describing what it shows, `loading="lazy"`, `decoding="async"`, and a caption in the reader's own words — not a copy of the image's title.
- Progressive enhancement aside: if the repo has no suitable image and you cannot add one, write the post without images rather than inventing a placeholder.

### Files to touch

1. `mkdir -p posts/api-gateways && cp posts/template.html posts/api-gateways/index.html` — the folder name **is** the URL (`/posts/api-gateways/`), so keep it short and readable. No date in the folder; the `<time>` tag carries it. Never edit or copy `template.html` itself into a folder.
2. In the new file, update **every** one of: `<title>`, `meta[name=description]`, `link[rel=canonical]`, `og:title`, `og:description`, `og:url`, `og:image` (absolute URL to the local image), `article:published_time`, and the visible `<time datetime="YYYY-MM-DD">` plus its text. Canonical and `og:url` are `https://byteportal.vercel.app/posts/<folder>/`. Leave stale placeholder URLs behind and the post ships broken.
3. Write the article body inside the existing `<div class="prose …">`. Keep the header, footer and theme script untouched.
4. In `index.html`, add one `<li>` as the **first** child of `<ol id="post-feed">`, matching the existing entry exactly: `href="posts/api-gateways/"`, `<time>`, `h2` title, and a one-sentence summary that reads like the post's hook.
5. Read time: count words, assume ~200 words per minute, round up. Update the `· N min read` line. If you renamed a post folder, leave a `<meta http-equiv="refresh" content="0; url=/posts/<new-folder>/">` stub at the old path; there is no host config to fall back on.
6. Commit and push: `git add -A && git commit -m "post: <slug>" && git push`. The repo is `Byteportal-blog/BytePortal`, branch `main`.

### Before you say done

- [ ] Every head tag above points at the real file, date and title — no `first-post`, no `example.jpg`.
- [ ] Images exist at the paths used; `width`/`height` match the real pixel size; captions and alt text are plain English.
- [ ] Every code block carries a `language-*` class, and the language shown in its header bar is the real one.
- [ ] Links open (open the top two).
- [ ] The feed entry sorts above the previous newest post.
- [ ] Rendered check: `python3 -m http.server 8000`, open the post and the homepage, click the post from the feed, toggle dark mode, click a Copy button.
- [ ] Re-read the first paragraph. Would a busy developer keep reading? If not, rewrite it.
- [ ] Committed and pushed to `main` — the working tree is clean.

Report back in three lines: the file created, the images used, and anything you could not verify.

---

## Why this version is better than "make post on it"

| The old prompt | The problem | What this does |
| --- | --- | --- |
| "make post on it" | No subject, no source, no scope — the agent invents facts | Names the topic, forces a source read, bans unverified claims |
| "more engagement" | Vague; produces hype and exclamation marks | Defines engagement as: reader friction, short sentences, a real example, an honest downside |
| "simple words" | Easy to ignore | Concrete rules: split long sentences, second person, define terms inline, banned filler |
| "easy to understand" | No structure | Fixed shape: hook → 3-bullet summary → 3–5 questions → limits → action |
| "use the images in the site" | Agent guesses paths and skips them | Look first with `ls`, reuse local images, new ones go in `assets/images/<year>/`, caption + alt + dimensions required |
| (not mentioned) | Post ships with placeholder canonical/OG tags and no feed entry | Explicit head-tag checklist and the exact feed `<li>` placement |

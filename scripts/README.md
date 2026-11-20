# Cross-Posting Guide (Medium & Blogger)

BytePortal articles can easily be cross-posted to **Medium** and **Blogger** with full canonical SEO attribution to drive authority back to `byteportal.tech`.

---

## 1. Medium (10 Seconds)
1. Open 👉 **[medium.com/p/import](https://medium.com/p/import)**.
2. Paste the live post URL:
   ```text
   https://www.byteportal.tech/<slug>/
   ```
3. Click **Import**. Medium automatically copies the text, images, and sets the canonical URL.
4. Click **Publish**.

---

## 2. Blogger (30 Seconds)
1. Run the exporter script for your post:
   ```bash
   python scripts/export_blogger.py <slug>
   ```
   *Example:*
   ```bash
   python scripts/export_blogger.py coolify-vs-dokploy
   ```
   *This outputs `blogger-import.xml` with live CDN images, styled tables, and canonical attribution.*

2. Go to **blogger.com** &rarr; **Settings** &rarr; scroll to **Manage Blog**.
3. Click **Import content** &rarr; select `blogger-exports/<slug>.xml`.
4. Done!

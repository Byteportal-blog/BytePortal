#!/usr/bin/env python3
"""
BytePortal Blogger Exporter
Converts any BytePortal blog post into an official Blogger Atom XML import file.

Features:
- Converts local relative image URLs to live absolute byteportal.tech CDN URLs.
- Sanitizes raw SVGs to clean symbols (prevents oversized SVG expansion on Blogger).
- Adds inline styles to comparison tables and summary boxes for clean rendering.
- Adds canonical SEO attribution linking back to the original article on byteportal.tech.

Usage:
    python scripts/export_blogger.py <slug>
    Example: python scripts/export_blogger.py coolify-vs-dokploy
"""

import os
import sys
import re
import argparse
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOGGER_BLOG_ID = "8931891139247852068"

def parse_and_convert(slug):
    post_dir = os.path.join(BASE_DIR, 'blogs', slug)
    if not os.path.exists(post_dir):
        post_dir = os.path.join(BASE_DIR, slug)
    index_file = os.path.join(post_dir, 'index.html')
    if not os.path.exists(index_file):
        raise FileNotFoundError(f"Article not found at: {index_file}")

    with open(index_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Title
    title_m = re.search(r'<title>(.*?)</title>', html, re.I)
    title = title_m.group(1).strip() if title_m else slug

    # 2. Tags
    tags = re.findall(r'<meta property="article:tag" content="(.*?)">', html, re.I)
    if not tags:
        tags = ["Technology", "Developer", "OpenSource"]

    canonical_url = f"https://www.byteportal.tech/blogs/{slug}/"

    # 3. Extract prose body
    prose_m = re.search(r'<div class="prose[^"]*">(.*?)</div>\s*<footer', html, re.S | re.I)
    if not prose_m:
        raise ValueError(f"Could not extract prose content from {index_file}")
    
    raw_body = prose_m.group(1)

    # 4. Convert relative image paths to live BytePortal CDN URLs
    def replace_img_src(match):
        prefix = match.group(1)
        src = match.group(2)
        if src.startswith('http'):
            return f'{prefix}src="{src}"'
        clean_src = re.sub(r'^(?:\.\./|\./|/)+', '', src)
        absolute_src = f"https://www.byteportal.tech/{clean_src}"
        return f'{prefix}src="{absolute_src}"'

    clean_body = re.sub(r'(<img\s+[^>]*?)src="([^"]+)"', replace_img_src, raw_body)

    # 5. Convert relative anchor links (e.g. href="/blogs/dokploy/") to absolute
    def replace_a_href(match):
        prefix = match.group(1)
        href = match.group(2)
        if href.startswith('http') or href.startswith('#') or href.startswith('mailto:'):
            return f'{prefix}href="{href}"'
        clean_href = re.sub(r'^(?:\.\./|\./|/)+', '', href)
        if not clean_href.startswith('blogs/') and not clean_href.startswith('about') and not clean_href.startswith('privacy'):
            clean_href = f"blogs/{clean_href}"
        return f'{prefix}href="https://www.byteportal.tech/{clean_href}"'

    clean_body = re.sub(r'(<a\s+[^>]*?)href="([^"]+)"', replace_a_href, clean_body)

    # 6. Replace raw SVGs with universal inline checkmark so Blogger doesn't blow them up
    clean_body = re.sub(
        r'<svg[^>]*>.*?</svg>',
        '<span style="display:inline-block; font-size:18px; color:#059669; margin-right:6px; vertical-align:middle;">✔</span>',
        clean_body,
        flags=re.S
    )

    # 7. Add inline fallback styles for #quick-answer box
    clean_body = re.sub(
        r'<div id="quick-answer"[^>]*>',
        '<div id="quick-answer" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:18px; margin:24px 0; font-family:sans-serif;">',
        clean_body
    )

    # 8. Add inline borders and padding to table elements for clean rendering
    clean_body = re.sub(r'<table[^>]*>', '<table style="width:100%; border-collapse:collapse; margin:24px 0; font-family:sans-serif; font-size:14px; border:1px solid #e2e8f0;">', clean_body)
    clean_body = re.sub(r'<th\s+class="([^"]*)"', r'<th style="border:1px solid #e2e8f0; padding:12px 14px; background:#f1f5f9; text-align:left;" class="\1"', clean_body)
    clean_body = re.sub(r'<td\s+class="([^"]*)"', r'<td style="border:1px solid #e2e8f0; padding:12px 14px; text-align:left;" class="\1"', clean_body)

    # 9. Canonical attribution callout
    attribution = f"""
    <div style="padding: 12px 16px; background: #f4f4f5; border-left: 4px solid #18181b; margin-bottom: 24px; font-family: sans-serif;">
      <strong>Note:</strong> This article was originally published on <a href="{canonical_url}" target="_blank" rel="noopener">BytePortal</a>.
    </div>
    """
    final_content = attribution + "\n" + clean_body

    return {
        "title": title,
        "tags": tags,
        "content": final_content
    }

def export_blogger(slug):
    article = parse_and_convert(slug)
    export_dir = os.path.join(BASE_DIR, 'blogger-exports')
    os.makedirs(export_dir, exist_ok=True)
    output_xml = os.path.join(export_dir, f'{slug}.xml')
    now_iso = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')

    categories_xml = "\n    ".join([
        f"<category scheme='http://www.blogger.com/atom/ns#' term='{tag}'/>"
        for tag in article['tags']
    ])

    atom_xml = f"""<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom' xmlns:gd='http://schemas.google.com/g/2005'>
  <title type='html'>Byte Portal</title>
  <generator>Blogger</generator>
  <updated>{now_iso}</updated>
  <entry>
    <category scheme='http://schemas.google.com/g/2005#kind' term='http://schemas.google.com/blogger/2008/kind#post'/>
    {categories_xml}
    <id>tag:blogger.com,1999:blog-{BLOGGER_BLOG_ID}.post-{slug}</id>
    <published>{now_iso}</published>
    <updated>{now_iso}</updated>
    <title type='html'>{article['title']}</title>
    <content type='html'><![CDATA[{article['content']}]]></content>
    <author>
      <name>Byte Portal</name>
    </author>
  </entry>
</feed>"""

    with open(output_xml, 'w', encoding='utf-8') as f:
        f.write(atom_xml)

    rel_output = os.path.relpath(output_xml, BASE_DIR)
    print(f"\n✅ Created: {rel_output}")
    print(f"📄 Post: {article['title']}")
    print(f"🏷️  Labels: {', '.join(article['tags'])}")
    print("\n👉 How to import into Blogger:")
    print("   1. Open blogger.com")
    print("   2. In the left menu, click 'Settings'")
    print("   3. Scroll down to 'Manage Blog' -> click 'Import content'")
    print(f"   4. Select '{rel_output}'!\n")

def main():
    parser = argparse.ArgumentParser(description="Export a BytePortal article to Blogger Atom XML format")
    parser.add_argument("slug", help="Slug of the article (e.g. coolify-vs-dokploy)")
    args = parser.parse_args()
    export_blogger(args.slug)

if __name__ == "__main__":
    main()

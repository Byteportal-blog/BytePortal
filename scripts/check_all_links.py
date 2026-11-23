import os
import sys
import re
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

SITE_ROOT = r"d:\Blog\BytePortal"
CANONICAL_HOSTS = ["byteportal.tech", "www.byteportal.tech"]

html_files = []
for root, dirs, files in os.walk(SITE_ROOT):
    # Skip .git, scratch, venv, node_modules, prompt
    if any(skip in root for skip in [".git", "scratch", ".gemini", "node_modules", "prompt"]):
        continue
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

print(f"Found {len(html_files)} HTML files to check.")

broken_links = []
checked_externals = {}

for html_path in html_files:
    rel_html = os.path.relpath(html_path, SITE_ROOT)
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    # Collect all IDs in this document for anchor checks
    doc_ids = set()
    for tag in soup.find_all(attrs={"id": True}):
        doc_ids.add(tag["id"])
    for tag in soup.find_all("a", attrs={"name": True}):
        doc_ids.add(tag["name"])

    # 1. Check <a href>
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
            continue

        parsed = urlparse(href)
        
        # In-page anchor link
        if href.startswith("#"):
            anchor = href[1:]
            if anchor and anchor not in doc_ids:
                broken_links.append((rel_html, f"Anchor #{anchor}", "Anchor ID not found in file"))
            continue

        # Internal canonical absolute URL
        if parsed.netloc in CANONICAL_HOSTS:
            path = unquote(parsed.path)
            if path.startswith("/"):
                path = path[1:]
            target_path = os.path.join(SITE_ROOT, path)
            if os.path.isdir(target_path):
                target_path = os.path.join(target_path, "index.html")
            if not os.path.exists(target_path):
                broken_links.append((rel_html, href, f"Target file does not exist: {target_path}"))
            elif parsed.fragment:
                # Check anchor in target file
                with open(target_path, "r", encoding="utf-8") as tf:
                    tsoup = BeautifulSoup(tf.read(), "html.parser")
                t_ids = {t["id"] for t in tsoup.find_all(attrs={"id": True})}
                if parsed.fragment not in t_ids:
                    broken_links.append((rel_html, href, f"Anchor #{parsed.fragment} not found in {target_path}"))
            continue

        # Relative link
        if not parsed.netloc:
            # Absolute root-relative or relative
            if href.startswith("/"):
                target_rel = href[1:]
                target_path = os.path.join(SITE_ROOT, target_rel)
            else:
                target_path = os.path.normpath(os.path.join(os.path.dirname(html_path), href.split("#")[0].split("?")[0]))
            
            if os.path.isdir(target_path):
                target_path = os.path.join(target_path, "index.html")
            
            if not os.path.exists(target_path):
                broken_links.append((rel_html, href, f"Relative target missing: {target_path}"))
            elif "#" in href:
                frag = href.split("#")[1].split("?")[0]
                if frag:
                    with open(target_path, "r", encoding="utf-8") as tf:
                        tsoup = BeautifulSoup(tf.read(), "html.parser")
                    t_ids = {t["id"] for t in tsoup.find_all(attrs={"id": True})}
                    if frag not in t_ids:
                        broken_links.append((rel_html, href, f"Anchor #{frag} not found in {target_path}"))
            continue

        # External Link
        if rel_html == os.path.join("blogs", "cursor-vs-windsurf", "index.html"):
            # Check external URLs in the new post
            url = href
            if url not in checked_externals:
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                    with urllib.request.urlopen(req, context=ctx, timeout=7) as resp:
                        checked_externals[url] = resp.status
                        print(f"External URL OK ({resp.status}): {url}")
                except Exception as e:
                    checked_externals[url] = f"Error: {e}"
                    print(f"External URL warning: {url} -> {e}")

    # 2. Check <img src>
    for img in soup.find_all("img", src=True):
        src = img["src"].strip()
        if not src or src.startswith("data:"):
            continue
        parsed = urlparse(src)
        if parsed.netloc:
            continue
        if src.startswith("/"):
            target_path = os.path.join(SITE_ROOT, src[1:])
        else:
            target_path = os.path.normpath(os.path.join(os.path.dirname(html_path), src))
        if not os.path.exists(target_path):
            broken_links.append((rel_html, f"img src={src}", f"Image missing: {target_path}"))

    # 3. Check <link href>
    for link in soup.find_all("link", href=True):
        href = link["href"].strip()
        rel = link.get("rel", [])
        if "canonical" in rel or "alternate" in rel or "preconnect" in rel or "dns-prefetch" in rel:
            continue
        parsed = urlparse(href)
        if parsed.netloc:
            continue
        if href.startswith("/"):
            target_path = os.path.join(SITE_ROOT, href[1:])
        else:
            target_path = os.path.normpath(os.path.join(os.path.dirname(html_path), href))
        if not os.path.exists(target_path):
            broken_links.append((rel_html, f"link href={href}", f"Asset missing: {target_path}"))

    # 4. Check <script src>
    for script in soup.find_all("script", src=True):
        src = script["src"].strip()
        parsed = urlparse(src)
        if parsed.netloc:
            continue
        if src.startswith("/"):
            target_path = os.path.join(SITE_ROOT, src[1:])
        else:
            target_path = os.path.normpath(os.path.join(os.path.dirname(html_path), src))
        if not os.path.exists(target_path):
            broken_links.append((rel_html, f"script src={src}", f"Script missing: {target_path}"))

# Also check sitemap.xml
import xml.etree.ElementTree as ET

try:
    stree = ET.parse(os.path.join(SITE_ROOT, "sitemap.xml"))
    for loc in stree.getroot().findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        u = loc.text
        p = urlparse(u).path
        if p.startswith("/"):
            p = p[1:]
        tp = os.path.join(SITE_ROOT, p)
        if os.path.isdir(tp):
            tp = os.path.join(tp, "index.html")
        if not os.path.exists(tp):
            broken_links.append(("sitemap.xml", u, f"Target missing: {tp}"))
    print("Sitemap URLs checked.")
except Exception as e:
    broken_links.append(("sitemap.xml", "parse error", str(e)))

# Also check feed.xml
try:
    ftree = ET.parse(os.path.join(SITE_ROOT, "feed.xml"))
    for item in ftree.getroot().findall("./channel/item"):
        link = item.find("link").text
        p = urlparse(link).path
        if p.startswith("/"):
            p = p[1:]
        tp = os.path.join(SITE_ROOT, p)
        if os.path.isdir(tp):
            tp = os.path.join(tp, "index.html")
        if not os.path.exists(tp):
            broken_links.append(("feed.xml", link, f"Target missing: {tp}"))
    print("Feed items checked.")
except Exception as e:
    broken_links.append(("feed.xml", "parse error", str(e)))

print("\n" + "="*50)
if broken_links:
    print(f"❌ FOUND {len(broken_links)} BROKEN LINK(S):")
    for src_file, link, reason in broken_links:
        print(f"  In {src_file}: {link} -> {reason}")
    sys.exit(1)
else:
    print("✅ ZERO BROKEN LINKS FOUND ACROSS ALL HTML FILES!")

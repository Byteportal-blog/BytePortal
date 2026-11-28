import os
import xml.etree.ElementTree as ET

# 1. Collect all published pages
pages_on_disk = []

# Homepage
if os.path.exists('index.html'):
    pages_on_disk.append('https://www.byteportal.tech/')

# Core pages
for p in ['about', 'privacy']:
    if os.path.exists(os.path.join(p, 'index.html')):
        pages_on_disk.append(f'https://www.byteportal.tech/{p}/')

# Blog posts
blogs_dir = 'blogs'
for b in sorted(os.listdir(blogs_dir)):
    b_path = os.path.join(blogs_dir, b, 'index.html')
    if os.path.exists(b_path):
        pages_on_disk.append(f'https://www.byteportal.tech/blogs/{b}/')

print(f"Total published pages on disk: {len(pages_on_disk)}")

# 2. Collect URLs from sitemap.xml
tree = ET.parse('sitemap.xml')
root = tree.getroot()
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

sitemap_entries = []
for url_elem in root.findall('sm:url', ns):
    loc = url_elem.find('sm:loc', ns).text
    lastmod = url_elem.find('sm:lastmod', ns).text if url_elem.find('sm:lastmod', ns) is not None else None
    priority = url_elem.find('sm:priority', ns).text if url_elem.find('sm:priority', ns) is not None else None
    sitemap_entries.append({'loc': loc, 'lastmod': lastmod, 'priority': priority})

print(f"Total URLs in sitemap.xml: {len(sitemap_entries)}")

for e in sitemap_entries:
    print(f"  - {e['loc']} (lastmod: {e['lastmod']}, priority: {e['priority']})")

# 3. Check for mismatches
sitemap_locs = [e['loc'] for e in sitemap_entries]

missing_from_sitemap = [p for p in pages_on_disk if p not in sitemap_locs]
missing_from_disk = [l for l in sitemap_locs if l not in pages_on_disk]

print("\n" + "="*50)
if not missing_from_sitemap and not missing_from_disk:
    print("STATUS: 100% UP TO DATE AND IN SYNC!")
else:
    if missing_from_sitemap:
        print("Missing from sitemap.xml:", missing_from_sitemap)
    if missing_from_disk:
        print("Dead URLs in sitemap.xml:", missing_from_disk)

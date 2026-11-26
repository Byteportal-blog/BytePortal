import os
import sys
import xml.etree.ElementTree as ET
import json
import re
from PIL import Image

def verify(slug="photocraft"):
    errors = []
    print(f"=== Verifying Post: {slug} ===")

    # 1. Check sitemap.xml
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        urls = [loc.text for loc in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        if not any(slug in u for u in urls):
            errors.append(f'{slug} not found in sitemap.xml')
        print(f'Sitemap valid: {len(urls)} URLs found.')
    except Exception as e:
        errors.append(f'sitemap.xml error: {e}')

    # 2. Check feed.xml
    try:
        tree = ET.parse('feed.xml')
        root = tree.getroot()
        links = [item.find('link').text for item in root.findall('./channel/item')]
        if not any(slug in l for l in links if l):
            errors.append(f'{slug} not found in feed.xml')
        print(f'Feed valid: {len(links)} items found.')
    except Exception as e:
        errors.append(f'feed.xml error: {e}')

    # 3. Check vercel.json
    try:
        with open('vercel.json', 'r', encoding='utf-8') as f:
            vdata = json.load(f)
        destinations = [r.get('destination') for r in vdata.get('redirects', [])]
        if f'/blogs/{slug}/' not in destinations:
            errors.append(f'{slug} redirect missing in vercel.json')
        print(f'vercel.json valid: {len(vdata.get("redirects", []))} redirects found.')
    except Exception as e:
        errors.append(f'vercel.json error: {e}')

    # 4. Check llms.txt & llms-full.txt
    for fn in ['llms.txt', 'llms-full.txt']:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        if slug not in content:
            errors.append(f'{slug} missing from {fn}')
        else:
            print(f'{fn} verified.')

    # 5. Check index.html post feed
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_content = f.read()
    if f'blogs/{slug}/' not in idx_content:
        errors.append(f'blogs/{slug}/ not linked in index.html')
    else:
        print('index.html verified.')

    # 6. Check blog post HTML
    post_path = f'blogs/{slug}/index.html'
    if not os.path.exists(post_path):
        errors.append(f'{post_path} does not exist')
    else:
        with open(post_path, 'r', encoding='utf-8') as f:
            post_html = f.read()
        
        # Check JSON-LD
        json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', post_html, re.DOTALL)
        if not json_ld_matches:
            errors.append('No JSON-LD found in blog post')
        else:
            for jstr in json_ld_matches:
                try:
                    jdata = json.loads(jstr.strip())
                    key = "@graph" if "@graph" in jdata else jdata.get("@type", "Unknown")
                    print(f'JSON-LD parsed successfully: {key}')
                except Exception as e:
                    errors.append(f'JSON-LD parse error: {e}')
        
        # Check images in post
        img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', post_html)
        for src in img_matches:
            if src.startswith('http'):
                continue
            img_rel = os.path.normpath(os.path.join(f'blogs/{slug}', src))
            if not os.path.exists(img_rel):
                errors.append(f'Image missing: {img_rel} (src={src})')
            elif img_rel.lower().endswith('.svg'):
                if os.path.getsize(img_rel) == 0:
                    errors.append(f'SVG is empty: {img_rel}')
                else:
                    print(f'SVG OK: {img_rel}')
            else:
                with Image.open(img_rel) as im:
                    w, h = im.size
                print(f'Image OK: {img_rel} ({w}x{h})')

    if errors:
        print('\n❌ ERRORS FOUND:')
        for err in errors:
            print(' -', err)
        sys.exit(1)
    else:
        print('\n✅ ALL VERIFICATIONS PASSED!')

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'photocraft'
    verify(target)

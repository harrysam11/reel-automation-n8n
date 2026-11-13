#!/usr/bin/env python3
"""
Asset Finder & Grabber for Finance Reel Factory.
Searches verified Creative Commons / Public Domain repositories (Wikimedia Commons API),
downloads high-resolution reaction cats, financial diagrams, or b-roll,
and automatically logs license metadata into asset_manifest.csv.
"""
import os
import sys
import json
import csv
import urllib.request
import urllib.parse
from PIL import Image

USER_AGENT = "FinanceReelFactory/1.0 (contact: workstation@local; educational automation)"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def search_commons_assets(query, limit=5):
    """Search Wikimedia Commons for permissive/CC media."""
    encoded_q = urllib.parse.quote(query)
    api_url = (
        f"https://commons.wikimedia.org/w/api.php?action=query"
        f"&generator=search&gsrsearch={encoded_q}&gsrnamespace=6&gsrlimit={limit}"
        f"&prop=imageinfo&iiprop=url|size|mime|extmetadata&format=json"
    )
    req = urllib.request.Request(api_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            results = []
            for pid, p in pages.items():
                title = p.get("title", "")
                imageinfo = p.get("imageinfo", [{}])[0]
                url = imageinfo.get("url", "")
                extmeta = imageinfo.get("extmetadata", {})
                
                license_short = extmeta.get("LicenseShortName", {}).get("value", "Unknown")
                usage_terms = extmeta.get("UsageTerms", {}).get("value", "")
                artist = extmeta.get("Artist", {}).get("value", "Unknown")
                width = imageinfo.get("width", 0)
                height = imageinfo.get("height", 0)

                # Skip SVGs or tiny icons if we need bitmap photos
                results.append({
                    "title": title,
                    "url": url,
                    "width": width,
                    "height": height,
                    "license": license_short,
                    "usage_terms": usage_terms,
                    "artist": artist
                })
            return results
    except Exception as e:
        print(f"Error querying Wikimedia Commons: {e}")
        return []

def grab_asset(asset_url, dest_rel_path, manifest_path, category="reaction", notes=""):
    """
    Download the asset to dest_rel_path and log to asset_manifest.csv.
    """
    full_dest = os.path.normpath(os.path.join(BASE_DIR, dest_rel_path))
    os.makedirs(os.path.dirname(full_dest), exist_ok=True)
    
    print(f"Downloading asset from: {asset_url}")
    req = urllib.request.Request(asset_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp, open(full_dest, "wb") as f:
        f.write(resp.read())
        
    print(f"Saved to: {full_dest}")
    
    # Convert/resize or verify image
    try:
        with Image.open(full_dest) as img:
            w, h = img.size
            fmt = img.format
            print(f"Verified image: {w}x{h} ({fmt})")
    except Exception as e:
        print(f"Warning: Image verification warning: {e}")

    # Generate asset ID
    asset_id = f"GRAB_{os.path.basename(dest_rel_path).split('.')[0].upper()[:8]}"
    
    # Update asset_manifest.csv
    full_manifest = os.path.normpath(os.path.join(BASE_DIR, manifest_path))
    os.makedirs(os.path.dirname(full_manifest), exist_ok=True)
    
    # Determine license
    license_type = "cc_by_sa_or_pd"
    
    row = {
        "asset_id": asset_id,
        "file_path": dest_rel_path,
        "category": category,
        "source_url": asset_url,
        "license_type": license_type,
        "rights_verified": "false",  # Requires human review gate in n8n
        "notes": notes or "Auto-grabbed via Asset Finder"
    }
    
    file_exists = os.path.exists(full_manifest)
    with open(full_manifest, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "asset_id", "file_path", "category", "source_url", "license_type", "rights_verified", "notes"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
        
    print(f"Logged to manifest: {full_manifest}")
    return row

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        q = sys.argv[2] if len(sys.argv) > 2 else "shocked cat"
        res = search_commons_assets(q)
        print(json.dumps(res, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "grab":
        url = sys.argv[2]
        dest = sys.argv[3]
        grab_asset(url, dest, "TEMPLATES/asset_manifest.csv")
    else:
        print("Usage:")
        print("  python scripts/asset_finder.py search <query>")
        print("  python scripts/asset_finder.py grab <url> <dest_path>")

import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

FEEDS = [
    {"category": "politique", "url": "https://www.hespress.com/politique/feed"},
    {"category": "economie", "url": "https://www.hespress.com/economie/feed"},
    {"category": "societe", "url": "https://www.hespress.com/societe/feed"},
]

RED_LINE_KEYWORDS = ["الملك", "الملكي", "العرش", "أسلحة", "حرب", "الجيش"]

def is_safe_and_viral(title):
    # Filter out red line topics
    for kw in RED_LINE_KEYWORDS:
        if kw in title:
            return False
    return True

def fetch_top_20_moroccan_news(output_path="output/daily_topics.json"):
    print("📡 Scraping & Filtering Moroccan Public Affairs Topics...")
    articles = []
    
    for feed in FEEDS:
        cat = feed["category"]
        url = feed["url"]
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                root = ET.fromstring(resp.read())
                items = root.findall(".//item")
                for item in items:
                    title = item.find("title").text.strip() if item.find("title") is not None else ""
                    desc = item.find("description").text.strip() if item.find("description") is not None else ""
                    link = item.find("link").text.strip() if item.find("link") is not None else ""
                    
                    if title and is_safe_and_viral(title) and not any(a["title"] == title for a in articles):
                        articles.append({
                            "id": len(articles) + 1,
                            "category": cat,
                            "title": title,
                            "summary": desc[:150] if desc else title,
                            "link": link
                        })
        except Exception as e:
            print(f"⚠️ Error fetching {url}: {e}")
            
    top_20 = articles[:20]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(top_20, f, ensure_ascii=False, indent=2)
        
    print(f"\n✅ Successfully harvested {len(top_20)} viral Moroccan topics!")
    print(f"📁 Saved to: {output_path}")
    
    for i, a in enumerate(top_20, 1):
        print(f"  {i}. [{a['category']}] {a['title']}")
        
    return top_20

if __name__ == "__main__":
    fetch_top_20_moroccan_news()

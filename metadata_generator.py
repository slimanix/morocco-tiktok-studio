"""
TikTok Metadata & Viral Caption Generator for Moroccan News Satire.
Generates high-converting titles, descriptions, pinned comments, and hashtags.
"""

import os
import sys
import json

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

OFFICIAL_HANDLE = "@wa.3ibad.lah4"
HASHTAGS_POOL = f"#wa3ibadlah #maroc #المغرب #morocco #اخبار_المغرب #tiktokmaroc #casablanca #rabat #سخرية #المواطن_المغربي"

def generate_tiktok_post_metadata(script_data, output_file=None):
    headline = script_data.get("headline", "")
    category = script_data.get("category", "actualité")
    
    # 1. High-Clickthrough Viral Hook Title
    title = f"🔴 واش فراسك بلي {headline}؟! 🇲🇦😂"
    
    # 2. Caption
    caption = (
        f"{title}\n\n"
        f"المواطن والمسؤول فنقاش ساخن حول هاد القرار! شكون عندو الصح فـ رأيك؟ 👇\n\n"
        f"تابع الحساب للمزيد: {OFFICIAL_HANDLE}\n"
        f"{HASHTAGS_POOL}"
    )
    
    # 3. Pinned Comment Debate Trigger
    pinned_comment = f"📌 نتوما شكون متفقين معاه: المواطن 🧔 ولا المسؤول 👔؟ صوتو بصراحة فليكومونتير! (تابعونا: {OFFICIAL_HANDLE})"

    
    meta = {
        "title": title,
        "caption": caption,
        "pinned_comment": pinned_comment,
        "hashtags": HASHTAGS_POOL
    }
    
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"=== TIKTOK TITLE / HOOK ===\n{title}\n\n")
            f.write(f"=== CAPTION / DESCRIPTION ===\n{caption}\n\n")
            f.write(f"=== PINNED COMMENT (DEBATE TRIGGER) ===\n{pinned_comment}\n")
            
    return meta

if __name__ == "__main__":
    sample = {
        "headline": "تأخر استيراد الأبقار يقلق منتجي الحليب",
        "category": "economie"
    }
    meta = generate_tiktok_post_metadata(sample, "output/sample_tiktok_metadata.txt")
    print("✅ Sample Metadata Generated:")
    print(meta["caption"])

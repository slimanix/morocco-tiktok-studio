"""
Multi-Tier TikTok Posting Strategy:
Posts each scene as a teaser (Part 1, Part 2) and then posts the full master episode.
Includes algorithm-pushing Moroccan SEO hashtags and engagement triggers.
"""

import os
import sys
import time
import json
from tiktok_uploader import upload_video_to_tiktok
from metadata_generator import HASHTAGS_POOL

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def post_episode_multi_tier(ep_folder, full_video_path, headline, headless=False):
    """
    Executes the 3-step viral posting sequence:
    1. Scene 1 (Part 1 Hook)
    2. Scene 2 (Part 2 Official Reaction)
    3. Full Episode Master Video
    """
    print("=" * 65)
    print("🚀 EXECUTING MULTI-TIER VIRAL TIKTOK POSTING STRATEGY")
    print(f"📌 Headline: {headline}")
    print("=" * 65)
    
    # 1. Post Part 1 (Citizen Hook)
    scene_1 = f"{ep_folder}/scene_1.mp4"
    if os.path.exists(scene_1):
        caption_1 = f"🔴 [الجزء 1] واش فراسك بلي {headline}؟! المواطن مصدوم! تابعنا للجزء 2 🇲🇦👇"
        tags_1 = f"#الجزء1 #maroc #المغرب #اخبار_المغرب #tiktokmaroc"
        print("\n[Step 1/3] Uploading Part 1 (Hook)...")
        upload_video_to_tiktok(scene_1, caption_1, tags_1, headless=headless)
        print("⏳ Cooling down 45 seconds before next post...")
        time.sleep(45)
        
    # 2. Post Part 2 (Official Reaction)
    scene_2 = f"{ep_folder}/scene_2.mp4"
    if os.path.exists(scene_2):
        caption_2 = f"🔴 [الجزء 2] رد المسؤول ببرودة دم! شوف الحلقة الكاملة فالبروفايل 🇲🇦👇"
        tags_2 = f"#الجزء2 #رد_المسؤول #maroc #المغرب #tiktokmaroc"
        print("\n[Step 2/3] Uploading Part 2 (Official Response)...")
        upload_video_to_tiktok(scene_2, caption_2, tags_2, headless=headless)
        print("⏳ Cooling down 45 seconds before full episode...")
        time.sleep(45)
        
    # 3. Post Full Master Episode
    if os.path.exists(full_video_path):
        caption_full = (
            f"🔴 [الحلقة الكاملة] النقاش الساخن كامل بين المواطن والمسؤول حول {headline}! "
            f"شكون عندو الصح فـ رأيكم؟ صوتو فالتعليقات 👇"
        )
        print("\n[Step 3/3] Uploading Full Master Episode...")
        upload_video_to_tiktok(full_video_path, caption_full, HASHTAGS_POOL, headless=headless)
        print("\n🎉 ALL TIERS POSTED SUCCESSFULLY!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python post_scene_and_full_episode.py <ep_folder> <full_video_path> [headline]")
    else:
        ep_dir = sys.argv[1]
        master_vid = sys.argv[2]
        h_line = sys.argv[3] if len(sys.argv) > 3 else "نقاش اليوم فالمغرب"
        post_episode_multi_tier(ep_dir, master_vid, h_line)

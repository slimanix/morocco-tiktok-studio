"""
Master Autonomous System Autopilot for @wa.3ibad.lah4.
Runs autonomously in background: warms up page, produces daily news videos,
and progressively increases publishing frequency.
"""

import os
import sys
import time
import json
from datetime import datetime
from account_growth_engine import (
    load_or_init_state, save_state, get_today_target, simulate_human_feed_warmup
)
from news_scraper import fetch_top_20_moroccan_news
from batch_script_generator import generate_scripts_from_topics
from batch_runner import run_daily_batch
from metadata_generator import generate_tiktok_post_metadata

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def run_daily_cycle(auto_upload=False):
    state = load_or_init_state()
    today_str = datetime.now().strftime("%Y-%m-%d")
    target = get_today_target(state)
    
    print("\n" + "=" * 65)
    print(f"🤖 AUTOPILOT ENGINE ACTIVATED FOR {state['handle']}")
    print(f"📅 Active Day: Day {state['current_day']} | Phase: {target['phase']}")
    print(f"🎯 Today's Safe Quota: {target['quota']} video(s)")
    print(f"⏰ Peak Time Slots: {target['times']}")
    print("=" * 65)
    
    # 1. Warm up the page with human browsing simulation
    today_history = state.get("daily_history", {}).get(today_str, {})
    if not today_history.get("warmed_up", False):
        print("\n[Step 1/3] Simulating Human Activity on TikTok (Warm-Up)...")
        warmed = simulate_human_feed_warmup()
        if today_str not in state["daily_history"]:
            state["daily_history"][today_str] = {"videos_posted": 0, "warmed_up": warmed}
        else:
            state["daily_history"][today_str]["warmed_up"] = warmed
        save_state(state)
    else:
        print("\n[Step 1/3] Account already warmed up for today! Skipping.")
        
    # 2. Produce Today's Videos (Quota matches current account phase)
    quota = target["quota"]
    print(f"\n[Step 2/3] Generating Today's {quota} Video(s) from Breaking News...")
    finished_videos = run_daily_batch(limit=quota)
    
    # 3. Schedule / Publish
    print(f"\n[Step 3/3] Queueing {len(finished_videos)} Video(s) for Scheduled Dispatch...")
    for i, v_path in enumerate(finished_videos, 1):
        slot = target["times"][i-1] if isinstance(target["times"], list) and i <= len(target["times"]) else "AUTO_INTERVAL"
        print(f"   ⏰ Video {i}: {os.path.basename(v_path)} ➡️ Scheduled for: {slot} (Morocco Time)")
        
        if auto_upload:
            print(f"   🚀 AUTO UPLOAD INITIATED FOR VIDEO {i} (Multi-Platform)...")
            metadata = generate_tiktok_post_metadata(ep_id=i) # Assuming ep_id aligns with daily count for simplicity

            # TikTok Upload
            try:
                from tiktok_uploader import upload_video_to_tiktok
                print("      -> Uploading to TikTok...")
                upload_video_to_tiktok(v_path, caption=metadata, headless=True)
            except Exception as e:
                print(f"      ❌ TikTok upload failed: {e}")

            # YouTube Upload
            try:
                from youtube_uploader import upload_video_to_youtube
                print("      -> Uploading to YouTube Shorts...")
                # Extract title from metadata (first line usually)
                title = metadata.split('\n')[0][:100] if metadata else "Moroccan News Update"
                upload_video_to_youtube(v_path, title=title, description=metadata, headless=True)
            except Exception as e:
                print(f"      ❌ YouTube upload failed: {e}")

    print("\n" + "=" * 65)
    print("🎉 DAILY CYCLE COMPLETE! Videos ready in output folder.")
    print("=" * 65)
    return finished_videos

if __name__ == "__main__":
    run_daily_cycle()

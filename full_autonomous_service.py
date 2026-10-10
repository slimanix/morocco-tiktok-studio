"""
24/7 Full Autonomous Background Daemon for @wa.3ibad.lah4.
Runs silently in the background of the operating system:
- Self-schedules daily warm-ups
- Scrapes breaking Moroccan news
- Produces the progressive video quota
- Automatically publishes to TikTok via Playwright
- Automatically advances days and scales to 20 videos daily.
"""

import os
import sys
import time
import json
import logging
from datetime import datetime
from account_growth_engine import (
    load_or_init_state, save_state, get_today_target, simulate_human_feed_warmup
)
from news_scraper import fetch_top_20_moroccan_news
from batch_runner import run_daily_batch
from tiktok_uploader import upload_video_to_tiktok
from metadata_generator import generate_tiktok_post_metadata, HASHTAGS_POOL

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

LOG_FILE = "output/autonomous_service.log"
os.makedirs("output", exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

def log_and_print(msg):
    print(msg)
    logging.info(msg)

def execute_daily_posting_job():
    """Executes the full automated workflow for today."""
    state = load_or_init_state()
    today_str = datetime.now().strftime("%Y-%m-%d")
    target = get_today_target(state)
    
    log_and_print("=" * 65)
    log_and_print(f"🚀 [AUTONOMOUS JOB TRIGGERED] Day {state['current_day']} | Phase: {target['phase']}")
    log_and_print(f"Target quota: {target['quota']} video(s)")
    
    # 1. Warm up session
    today_hist = state.get("daily_history", {}).get(today_str, {})
    if not today_hist.get("warmed_up", False):
        log_and_print("🕵️ Executing automated human warm-up session...")
        warmed = simulate_human_feed_warmup()
        if today_str not in state["daily_history"]:
            state["daily_history"][today_str] = {"videos_posted": 0, "warmed_up": warmed}
        else:
            state["daily_history"][today_str]["warmed_up"] = warmed
        save_state(state)
        time.sleep(15)

    # 2. Produce videos for today's quota
    log_and_print(f"🎬 Producing {target['quota']} video(s) for today...")
    videos = run_daily_batch(limit=target["quota"])
    
    # 3. Publish to TikTok
    log_and_print(f"📤 Auto-publishing {len(videos)} video(s) to TikTok (@wa.3ibad.lah4)...")
    for i, v_path in enumerate(videos, 1):
        caption = f"🔴 واش فراسك بلي هاد القرار تبدل؟! 🇲🇦😂 المواطن والمسؤول فنقاش ساخن! تابعونا: @wa.3ibad.lah4"
        success = upload_video_to_tiktok(v_path, caption, HASHTAGS_POOL, headless=False)
        if success:
            state["total_videos_posted"] += 1
            state["daily_history"][today_str]["videos_posted"] += 1
            save_state(state)
            log_and_print(f"✅ Video {i} successfully published to TikTok!")
        time.sleep(60)

    # Advance day counter for tomorrow
    state["current_day"] += 1
    save_state(state)
    log_and_print(f"🎉 Day {state['current_day']-1} completed! System advanced to Day {state['current_day']}.")
    log_and_print("=" * 65)

def run_service_loop():
    """24/7 background polling loop."""
    log_and_print("=" * 65)
    log_and_print("🤖 @wa.3ibad.lah4 24/7 AUTONOMOUS SYSTEM DAEMON IS ACTIVE")
    log_and_print(f"Logs: {os.path.abspath(LOG_FILE)}")
    log_and_print("=" * 65)
    
    last_run_day = None
    
    while True:
        now = datetime.now()
        current_time_str = now.strftime("%H:%M")
        current_day_str = now.strftime("%Y-%m-%d")
        
        state = load_or_init_state()
        target = get_today_target(state)
        scheduled_times = target["times"]
        
        # Check if current time matches scheduled trigger time
        should_run = False
        if isinstance(scheduled_times, list):
            if current_time_str in scheduled_times and last_run_day != (current_day_str, current_time_str):
                should_run = True
                last_run_day = (current_day_str, current_time_str)
        elif scheduled_times == "INTERVAL_40_MINS":
            # Beast mode: runs every 40 minutes between 09:00 and 23:30
            if 9 <= now.hour <= 23 and now.minute % 40 == 0:
                should_run = True
                
        if should_run:
            try:
                execute_daily_posting_job()
            except Exception as e:
                log_and_print(f"❌ Error during execution: {e}")
                
        # Sleep 30 seconds before next heartbeat check
        time.sleep(30)

if __name__ == "__main__":
    if "--run-now" in sys.argv:
        execute_daily_posting_job()
    else:
        run_service_loop()

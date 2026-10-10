"""
Generates an optimized daily TikTok posting schedule with timestamps for Morocco.
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Moroccan peak viewing windows
SCHEDULE_SLOTS = [
    "09:00", "09:45", "10:30", "11:15",
    "12:00", "12:45", "13:30", "14:15",  # Lunch peak
    "15:00", "15:45", "16:30", "17:15",
    "18:00", "18:45", "19:30", "20:15",  # Evening commute
    "21:00", "21:45", "22:30", "23:15"   # Prime night scroll
]

def generate_daily_schedule(scripts_json="output/daily_scripts.json", out_file="output/daily_schedule.txt"):
    if not os.path.exists(scripts_json):
        return None
        
    with open(scripts_json, "r", encoding="utf-8") as f:
        scripts = json.load(f)
        
    lines = [
        "=================================================================",
        "📅 OPTIMIZED TIKTOK POSTING SCHEDULE FOR TODAY (MOROCCO TIME)",
        "=================================================================\n"
    ]
    
    for i, script in enumerate(scripts[:len(SCHEDULE_SLOTS)]):
        time_slot = SCHEDULE_SLOTS[i]
        ep_id = script["episode_id"]
        headline = script["headline"]
        
        lines.append(f"⏰ [{time_slot}] Video {ep_id}: {headline}")
        lines.append(f"   📁 File: output/batch_today/episode_{ep_id}.mp4")
        lines.append(f"   📌 Pinned Comment: نتوما شكون متفقين معاه: المواطن ولا المسؤول؟ صوتو فكومنتير!")
        lines.append("-" * 65)
        
    report = "\n".join(lines)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"✅ Daily timetable generated: {out_file}")
    return out_file

if __name__ == "__main__":
    generate_daily_schedule()

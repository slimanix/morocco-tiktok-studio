"""
All-in-one TikTok Video Generation Pipeline for Moroccan News Satire.
Run this anytime to produce a complete, ready-to-post vertical video.
"""

import os
import sys
from generate_elevenlabs_episode import generate_with_elevenlabs
from fast_lipsync_pipeline import run_fast_pipeline

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=" * 60)
    print("🇲🇦 100% FREE AI NEURAL LIP-SYNC TIKTOK STUDIO 🇲🇦")
    print("=" * 60)
    
    # 1. Generate Voiceover
    print("\n[Step 1/2] Generating High-Energy Dialogue with ElevenLabs...")
    audio_file = generate_with_elevenlabs()
    if not audio_file or not os.path.exists(audio_file):
        print("❌ Failed to produce audio. Check API key.")
        return
        
    # 2. Render Real Neural AI Lip-Sync Video (Parallel + Instant FFmpeg)
    print("\n[Step 2/2] Generating High-Speed Parallel Neural Lip-Sync...")
    video_file = run_fast_pipeline()
    
    print("\n" + "=" * 60)
    print(f"🎉 100% AUTOMATION COMPLETE! Master video is ready to post:")
    print(f"👉 {os.path.abspath(video_file)}")
    print("=" * 60)



if __name__ == "__main__":
    main()

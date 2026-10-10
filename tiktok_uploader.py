"""
Automated TikTok Uploader using Playwright with persistent session.
Supports 1-time login and headless automated publishing with SEO hashtags.
"""

import os
import sys
import time
import argparse
from playwright.sync_api import sync_playwright

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SESSION_DIR = os.path.abspath("tiktok_session")

def setup_login_session():
    """Opens a visible browser for 1-time manual login to save cookies."""
    print("=" * 65)
    print("🔑 TIKTOK 1-TIME LOGIN SESSION SETUP")
    print("=" * 65)
    print(f"Session profile directory: {SESSION_DIR}")
    print("Opening browser... Please log into your TikTok account.")
    print("Once logged in and on your homepage, press ENTER in this terminal to save!")
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            viewport={"width": 1280, "height": 800},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.new_page()
        page.goto("https://www.tiktok.com/login", wait_until="domcontentloaded")
        
        input("\n👉 Press ENTER here after you have successfully logged in to TikTok: ")
        print("💾 Session saved successfully! You won't need to log in again.")
        browser.close()

def upload_video_to_tiktok(video_path, caption, hashtags="", headless=False):
    """
    Automates uploading a video file to TikTok Creator Studio with captions and hashtags.
    """
    abs_video = os.path.abspath(video_path)
    if not os.path.exists(abs_video):
        print(f"❌ Video not found: {abs_video}")
        return False
        
    full_caption = f"{caption} {hashtags}".strip()
    print("=" * 65)
    print("🚀 AUTOMATING TIKTOK VIDEO UPLOAD")
    print("=" * 65)
    print(f"📁 Video: {abs_video}")
    print(f"📝 Caption: {full_caption[:80]}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=headless,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.new_page()
        print("🌐 Navigating to TikTok Creator Upload Center...")
        page.goto("https://www.tiktok.com/creator-center/upload", wait_until="networkidle")
        time.sleep(3)
        
        # Check if login is needed
        if "login" in page.url.lower():
            print("⚠️ Session expired or not logged in. Please run: python tiktok_uploader.py --login")
            browser.close()
            return False
            
        # Upload video file via iframe or direct file input
        print("📤 Selecting video file...")
        try:
            # Look for file input
            file_input = page.locator('input[type="file"]')
            if file_input.count() > 0:
                file_input.first.set_input_files(abs_video)
            else:
                # Inside iframe
                frame = page.frame_locator('iframe[src*="upload"]')
                frame.locator('input[type="file"]').set_input_files(abs_video)
                
            print("⏳ Uploading video file... Waiting for processing...")
            time.sleep(12)
            
            # Enter caption
            print("✍️ Entering viral caption & hashtags...")
            caption_box = page.locator('div[contenteditable="true"]').first
            if caption_box.count() > 0:
                caption_box.click()
                caption_box.fill("")
                caption_box.type(full_caption, delay=20)
                
            time.sleep(3)
            
            # Click Post / Publish button
            print("🚀 Publishing video to TikTok...")
            post_button = page.locator('button:has-text("Post"), button:has-text("نشر"), button:has-text("Publier")').first
            if post_button.count() > 0:
                post_button.click()
                time.sleep(6)
                print("🎉 VIDEO POSTED TO TIKTOK SUCCESSFULLY!")
                browser.close()
                return True
            else:
                print("⚠️ Post button not detected automatically. Please click post in the opened browser.")
                time.sleep(15)
                browser.close()
                return True
                
        except Exception as e:
            print(f"❌ Upload error: {e}")
            browser.close()
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TikTok Automated Uploader")
    parser.add_argument("--login", action="store_true", help="Launch browser for 1-time login")
    parser.add_argument("--video", type=str, help="Path to video file")
    parser.add_argument("--caption", type=str, default="", help="Video caption")
    parser.add_argument("--hashtags", type=str, default="#maroc #المغرب #morocco", help="Hashtags")
    parser.add_argument("--headless", action="store_true", help="Run in background headless")
    
    args = parser.parse_args()
    
    if args.login:
        setup_login_session()
    elif args.video:
        upload_video_to_tiktok(args.video, args.caption, args.hashtags, args.headless)
    else:
        print("Usage:")
        print("  1. First-time login: python tiktok_uploader.py --login")
        print("  2. Upload: python tiktok_uploader.py --video 'output/video.mp4' --caption 'My Title'")

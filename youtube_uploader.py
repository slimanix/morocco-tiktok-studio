"""
Automated YouTube Shorts Uploader using Playwright with persistent session.
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

SESSION_DIR = os.path.abspath("youtube_session")

def setup_login_session():
    """Opens a visible browser for 1-time manual login to save cookies."""
    print("=" * 65)
    print("🔑 YOUTUBE 1-TIME LOGIN SESSION SETUP")
    print("=" * 65)
    print(f"Session profile directory: {SESSION_DIR}")
    print("Opening browser... Please log into your Google/YouTube account.")
    print("Once logged in and on your YouTube homepage, press ENTER in this terminal to save!")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            viewport={"width": 1280, "height": 800},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.new_page()
        page.goto("https://studio.youtube.com", wait_until="domcontentloaded")

        input("\n👉 Press ENTER here after you have successfully logged in to YouTube: ")
        print("💾 Session saved successfully! You won't need to log in again.")
        browser.close()

def upload_video_to_youtube(video_path, title, description, tags="", headless=False):
    """
    Automates uploading a video file to YouTube Studio as a Short.
    """
    abs_video = os.path.abspath(video_path)
    if not os.path.exists(abs_video):
        print(f"❌ Video not found: {abs_video}")
        return False

    full_description = f"{description}\n\n{tags}".strip()

    print("=" * 65)
    print(f"🚀 UPLOADING SHORTS TO YOUTUBE: {title}")
    print("=" * 65)

    try:
        with sync_playwright() as p:
            print("🌐 Launching browser session...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=SESSION_DIR,
                headless=headless,
                viewport={"width": 1280, "height": 800},
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = browser.new_page()

            # Go to YouTube Studio
            print("▶️ Navigating to YouTube Studio...")
            page.goto("https://studio.youtube.com", wait_until="networkidle")
            time.sleep(3)

            # Click Upload icon (the arrow pointing up)
            print("⬆️ Clicking upload button...")
            upload_button = page.locator('ytcp-icon-button#upload-icon')
            if not upload_button.is_visible():
               print("⚠️ Cannot find the upload button, perhaps login session is invalid.")
               browser.close()
               return False
            upload_button.click()
            time.sleep(2)

            # Set the file input
            print(f"📁 Attaching video: {os.path.basename(abs_video)}")
            with page.expect_file_chooser() as fc_info:
                page.locator("ytcp-button#select-files-button").click()
            file_chooser = fc_info.value
            file_chooser.set_files(abs_video)

            # Wait for upload UI to appear
            time.sleep(5)

            print("✍️ Filling in title...")
            title_box = page.locator('div#textbox[aria-label="Add a title that describes your video (type @ to mention a channel)"]')
            title_box.click()
            # Select all and delete default title (filename)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.keyboard.insert_text(title)

            print("📝 Filling in description...")
            desc_box = page.locator('div#textbox[aria-label="Tell viewers about your video (type @ to mention a channel)"]')
            desc_box.click()
            page.keyboard.insert_text(full_description)

            # Not made for kids
            print("👶 Setting audience to 'Not made for kids'...")
            kids_radio = page.locator('tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]')
            kids_radio.click()

            # Next steps
            print("⏭️ Proceeding through steps...")
            next_btn = page.locator('ytcp-button#next-button')
            # Video elements
            next_btn.click()
            time.sleep(2)
            # Checks
            next_btn.click()
            time.sleep(2)

            print("👁️ Setting visibility to Public...")
            # Visibility (wait for processing check or skip depending on needs)
            next_btn.click()
            time.sleep(2)

            public_radio = page.locator('tp-yt-paper-radio-button[name="PUBLIC"]')
            public_radio.click()

            print("✅ Clicking Publish...")
            publish_btn = page.locator('ytcp-button#done-button')
            publish_btn.click()

            # Wait for upload to complete
            print("⏳ Waiting for YouTube upload and processing confirmation...")
            page.wait_for_selector('ytcp-video-share-dialog', timeout=60000)

            print("🎉 Upload successful!")
            browser.close()
            return True

    except Exception as e:
        print(f"💥 Upload failed: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Shorts Auto Uploader")
    parser.add_argument("--setup", action="store_true", help="Run 1-time login setup")
    parser.add_argument("--video", type=str, help="Path to video file")
    parser.add_argument("--title", type=str, help="Short title")
    parser.add_argument("--desc", type=str, default="", help="Short description")
    parser.add_argument("--tags", type=str, default="#Shorts", help="Tags")
    parser.add_argument("--visible", action="store_true", help="Show browser during upload")

    args = parser.parse_args()

    if args.setup:
        setup_login_session()
    elif args.video and args.title:
        upload_video_to_youtube(
            video_path=args.video,
            title=args.title,
            description=args.desc,
            tags=args.tags,
            headless=not args.visible
        )
    else:
        print("Use --setup for login, or provide --video and --title to upload.")

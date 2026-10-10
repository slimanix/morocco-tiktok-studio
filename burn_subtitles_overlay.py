import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from moviepy import VideoFileClip, VideoClip
except ImportError:
    from moviepy.editor import VideoFileClip, VideoClip

ARABIC_FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"
if not os.path.exists(ARABIC_FONT_PATH):
    ARABIC_FONT_PATH = "C:/Windows/Fonts/arial.ttf"

def reshape_arabic(text):
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        return text

def apply_tiktok_overlays(input_video_path, subtitle_text, speaker_name, output_video_path):
    """
    Overlays breaking news banner, speaker badge, and bold RTL Arabic subtitles
    directly onto a lip-synced video clip.
    """
    print(f"🎨 Burning TikTok UI & Subtitles onto: {os.path.basename(input_video_path)}...")
    source_clip = VideoFileClip(input_video_path)
    width, height = source_clip.size
    
    font_sub = ImageFont.truetype(ARABIC_FONT_PATH, int(height * 0.038))
    font_badge = ImageFont.truetype(ARABIC_FONT_PATH, int(height * 0.030))
    font_banner = ImageFont.truetype(ARABIC_FONT_PATH, int(height * 0.025))
    
    reshaped_sub = reshape_arabic(subtitle_text)
    reshaped_speaker = reshape_arabic(f"🔴 {speaker_name}")
    reshaped_banner = reshape_arabic("عاجل | نقاش وطني حول الأخبار اليومية 🇲🇦")
    
    badge_color = (255, 180, 0) if "المواطن" in speaker_name else (0, 140, 255)
    
    def transform_frame(get_frame, t):
        frame = get_frame(t)
        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)
        
        # 1. Top Breaking News Banner
        banner_h = int(height * 0.05)
        draw.rectangle([0, 0, width, banner_h], fill=(210, 20, 20))
        draw.text((width // 2, banner_h // 2), reshaped_banner, font=font_banner, fill="white", anchor="mm")
        
        # 2. Speaker Badge
        badge_y = int(height * 0.10)
        bw, bh = int(width * 0.25), int(height * 0.022)
        draw.rounded_rectangle([width // 2 - bw, badge_y - bh, width // 2 + bw, badge_y + bh], radius=15, fill=badge_color)
        draw.text((width // 2, badge_y), reshaped_speaker, font=font_badge, fill="black", anchor="mm")
        
        # 3. Bottom TikTok Subtitle Box
        sub_y = int(height * 0.88)
        box_w, box_h = int(width * 0.45), int(height * 0.045)
        draw.rounded_rectangle([width // 2 - box_w, sub_y - box_h, width // 2 + box_w, sub_y + box_h], radius=20, fill=(0, 0, 0, 210))
        draw.text((width // 2, sub_y), reshaped_sub, font=font_sub, fill=(255, 240, 50), anchor="mm")
        
        return np.array(img)

    try:
        # MoviePy 2.x
        final_clip = source_clip.transform(transform_frame)
    except AttributeError:
        # MoviePy 1.x
        final_clip = source_clip.fl(transform_frame)
        
    final_clip.write_videofile(
        output_video_path,
        fps=source_clip.fps or 24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=4
    )
    print(f"✅ Finished overlay: {output_video_path}")
    return output_video_path

if __name__ == "__main__":
    test_in = "output/test_official_lipsync.mp4"
    test_out = "output/test_official_with_subtitles.mp4"
    if os.path.exists(test_in):
        apply_tiktok_overlays(test_in, "الله يهديك أ سيدي المواطن! حنا كنديرو دراسة استراتيجية!", "المسؤول (كيبرّد الطرح)", test_out)

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

def get_arabic_font(size):
    font_candidates = [
        os.path.join(os.path.dirname(__file__), "fonts", "NotoSansArabic.ttf"),
        "fonts/NotoSansArabic.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

import textwrap

def reshape_arabic(text):
    try:
        # Wrap words properly to avoid truncating words
        lines = textwrap.wrap(text, width=36)
        reshaped_lines = []
        for line in lines:
            reshaped = arabic_reshaper.reshape(line)
            reshaped_lines.append(get_display(reshaped))
        return reshaped_lines
    except Exception:
        return [text]

def apply_tiktok_overlays(input_video_path, subtitle_text, speaker_name, output_video_path, banner_title="عاجل | نقاش وطني حول الأخبار اليومية 🇲🇦", style="yellow_glow"):
    """
    Overlays breaking news banner, speaker badge, and bold RTL Arabic subtitles
    directly onto a lip-synced video clip.
    """
    print(f"🎨 Burning TikTok UI & Subtitles onto: {os.path.basename(input_video_path)}...")
    source_clip = VideoFileClip(input_video_path)
    width, height = source_clip.size
    
    font_sub = get_arabic_font(int(height * 0.033))
    font_badge = get_arabic_font(int(height * 0.026))
    font_banner = get_arabic_font(int(height * 0.022))
    
    reshaped_speaker_list = reshape_arabic(speaker_name)
    reshaped_speaker = reshaped_speaker_list[0] if reshaped_speaker_list else speaker_name
    
    reshaped_banner_list = reshape_arabic(banner_title[:45])
    reshaped_banner = reshaped_banner_list[0] if reshaped_banner_list else banner_title
    
    # Official = Blue, All Citizen Archetypes (Taxi, Grocer, Farmer, Teacher, etc.) = Amber Gold
    is_official = "المسؤول" in speaker_name or "وزير" in speaker_name
    badge_color = (0, 140, 255) if is_official else (255, 185, 20)
    
    # Subtitle lines reshaped safely line-by-line
    sub_lines = reshape_arabic(subtitle_text)
    
    # Styling options from Studio
    if style == "red_pill":
        box_bg = (220, 38, 38, 235)
        text_color = (255, 255, 255)
        border_color = (255, 255, 255)
    elif style == "green_emerald":
        box_bg = (6, 78, 59, 230)
        text_color = (110, 231, 183)
        border_color = (52, 211, 153)
    else: # default: yellow_glow
        box_bg = (0, 0, 0, 215)
        text_color = (255, 240, 50)
        border_color = (250, 204, 21)
    
    def transform_frame(get_frame, t):
        frame = get_frame(t)
        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)
        
        # 1. Top Breaking News Banner
        banner_h = int(height * 0.052)
        draw.rectangle([0, 0, width, banner_h], fill=(210, 20, 20))
        draw.text((width // 2, banner_h // 2), reshaped_banner, font=font_banner, fill="white", anchor="mm")
        
        # 2. Speaker Badge
        badge_y = int(height * 0.10)
        bw, bh = int(width * 0.28), int(height * 0.024)
        draw.rounded_rectangle([width // 2 - bw, badge_y - bh, width // 2 + bw, badge_y + bh], radius=15, fill=badge_color)
        
        # Live red pulse dot inside badge
        dot_r = int(height * 0.006)
        draw.ellipse([width // 2 + bw - 26, badge_y - dot_r, width // 2 + bw - 26 + dot_r * 2, badge_y + dot_r], fill=(220, 30, 30))
        
        draw.text((width // 2 - 8, badge_y), reshaped_speaker, font=font_badge, fill="black", anchor="mm")
        
        # 3. Bottom TikTok Subtitle Box
        line_height = int(height * 0.040)
        box_h = line_height * len(sub_lines) + 16
        box_w = int(width * 0.46)
        sub_center_y = int(height * 0.86)
        
        draw.rounded_rectangle(
            [width // 2 - box_w, sub_center_y - box_h // 2, width // 2 + box_w, sub_center_y + box_h // 2],
            radius=18,
            fill=box_bg,
            outline=border_color,
            width=2
        )
        
        start_y = sub_center_y - (len(sub_lines) - 1) * (line_height // 2)
        for idx, line in enumerate(sub_lines):
            draw.text((width // 2, start_y + idx * line_height), line, font=font_sub, fill=text_color, anchor="mm")
        
        return np.array(img)

    try:
        final_clip = source_clip.transform(transform_frame)
    except AttributeError:
        final_clip = source_clip.fl(transform_frame)
        
    final_clip.write_videofile(
        output_video_path,
        fps=source_clip.fps or 24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=4
    )
    
    source_clip.close()
    final_clip.close()
    print(f"✅ Finished overlay: {output_video_path}")
    return output_video_path

if __name__ == "__main__":
    test_in = "output/test_official_lipsync.mp4"
    test_out = "output/test_official_with_subtitles.mp4"
    if os.path.exists(test_in):
        apply_tiktok_overlays(test_in, "الله يهديك أ سيدي المواطن! حنا كنديرو دراسة استراتيجية!", "المسؤول (كيبرّد الطرح)", test_out)

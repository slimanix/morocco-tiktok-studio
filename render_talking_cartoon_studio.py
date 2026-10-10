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
    from moviepy import VideoClip, AudioFileClip, concatenate_videoclips
except ImportError:
    from moviepy.editor import VideoClip, AudioFileClip, concatenate_videoclips

ARABIC_FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"  # Arial Bold
if not os.path.exists(ARABIC_FONT_PATH):
    ARABIC_FONT_PATH = "C:/Windows/Fonts/arial.ttf"

def reshape_arabic(text):
    """Reshape and reorder Arabic text for correct RTL rendering."""
    try:
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        return bidi_text
    except Exception:
        return text

def create_base_canvas(img_path, width=720, height=1280):
    """Creates vertical frame canvas with character centered."""
    canvas = Image.new("RGB", (width, height), (18, 20, 26))
    char_img = Image.open(img_path)
    
    char_w, char_h = char_img.size
    aspect = char_w / char_h
    new_w = width
    new_h = int(new_w / aspect)
    
    resized_char = char_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    pos_x = (width - new_w) // 2
    pos_y = (height - new_h) // 2
    canvas.paste(resized_char, (pos_x, pos_y))
    return canvas

def render_scene(
    base_img_path,
    audio_path,
    speaker_name,
    subtitle_text,
    fps=24,
    width=720,
    height=1280
):
    print(f"\n🎭 Rendering Scene: [{speaker_name}]...")
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    # Get audio amplitude array
    sound_array = audio.to_soundarray(fps=fps)
    if sound_array.ndim > 1:
        volumes = np.mean(np.abs(sound_array), axis=1)
    else:
        volumes = np.abs(sound_array)
        
    max_vol = np.max(volumes) if len(volumes) > 0 and np.max(volumes) > 0 else 1.0
    norm_vols = volumes / max_vol
    
    # Pre-render base canvas
    base_canvas = create_base_canvas(base_img_path, width, height)
    
    # Prepare Fonts
    font_badge = ImageFont.truetype(ARABIC_FONT_PATH, 36)
    font_sub = ImageFont.truetype(ARABIC_FONT_PATH, 38)
    font_banner = ImageFont.truetype(ARABIC_FONT_PATH, 30)
    
    # Arabic texts
    reshaped_speaker = reshape_arabic(f"🔴 {speaker_name}")
    reshaped_sub = reshape_arabic(subtitle_text)
    reshaped_banner = reshape_arabic("عاجل | نقاش ساخن حول أسعار المحروقات فالمغرب 🇲🇦")

    def make_frame(t):
        frame_idx = min(int(t * fps), len(norm_vols) - 1)
        vol = norm_vols[frame_idx]
        
        # Audio-reactive animated mouth & head bounce
        frame_img = base_canvas.copy()
        draw = ImageDraw.Draw(frame_img)
        
        # If character is talking loudly, add subtle comedic head shake/zoom
        if vol > 0.25:
            # Shake offset
            shake_x = int(np.sin(t * 30) * (vol * 8))
            shake_y = int(np.cos(t * 25) * (vol * 6))

        
        # 1. Top News Banner
        draw.rectangle([0, 0, width, 70], fill=(210, 20, 20))
        draw.text((width // 2, 35), reshaped_banner, font=font_banner, fill="white", anchor="mm")
        
        # 2. Speaker Badge
        badge_color = (255, 180, 0) if "المواطن" in speaker_name else (0, 140, 255)
        badge_y = 120
        draw.rounded_rectangle([width // 2 - 160, badge_y - 25, width // 2 + 160, badge_y + 25], radius=15, fill=badge_color)
        draw.text((width // 2, badge_y), reshaped_speaker, font=font_badge, fill="black", anchor="mm")
        
        # 3. Bottom TikTok Subtitle Box
        sub_box_y = height - 160
        draw.rounded_rectangle([40, sub_box_y - 60, width - 40, sub_box_y + 60], radius=20, fill=(0, 0, 0, 200))
        # Word wrap or truncate if long
        draw.text((width // 2, sub_box_y), reshaped_sub, font=font_sub, fill=(255, 240, 50), anchor="mm")
        
        return np.array(frame_img)

    try:
        # MoviePy 2.x
        clip = VideoClip(make_frame, duration=duration).with_audio(audio)
    except AttributeError:
        # MoviePy 1.x
        clip = VideoClip(make_frame, duration=duration).set_audio(audio)
        
    return clip

def render_full_talking_show():
    scenes_data = [
        {
            "speaker": "المواطن (معصب ومصدوم)",
            "img": "output/citizen.jpg",
            "audio": "output/eleven_part_1_المواطن.mp3",
            "subtitle": "وا عباد الله! واش كتضحكو علينا؟! البترول هبط ولمازوط باقي شاعل!"
        },
        {
            "speaker": "المسؤول (كيبرّد الطرح)",
            "img": "output/official.jpg",
            "audio": "output/eleven_part_2_المسؤول.mp3",
            "subtitle": "الله يهديك أ سيدي المواطن! حنا كنديرو دراسة استراتيجية معمقة!"
        },
        {
            "speaker": "المواطن (الصدمة الثانية)",
            "img": "output/citizen.jpg",
            "audio": "output/eleven_part_3_المواطن.mp3",
            "subtitle": "فاش البرميل كيزيد سنتيم كطيرو وتزيدو درهم! وفاش كيهبط كتنعسو؟!"
        },
        {
            "speaker": "المسؤول (بابتسامة برود)",
            "img": "output/official.jpg",
            "audio": "output/eleven_part_4_المسؤول.mp3",
            "subtitle": "إيوا هذا هو التوازن الاقتصادي! هاك ابتسامة وعمر بلا ما تسول!"
        },
        {
            "speaker": "المواطن (الخاتمة والجدل)",
            "img": "output/citizen.jpg",
            "audio": "output/eleven_part_5_الخاتمة.mp3",
            "subtitle": "واش حتى نتوما كتجيكم هاد السكتة القلبية فاش كتعمرو لمازوط؟ صوتو فالتعليقات!"
        }
    ]
    
    clips = []
    for sc in scenes_data:
        clip = render_scene(
            base_img_path=sc["img"],
            audio_path=sc["audio"],
            speaker_name=sc["speaker"],
            subtitle_text=sc["subtitle"],
            fps=24
        )
        clips.append(clip)
        
    print("\n🚀 Stitching all scenes into the Master TikTok Video...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    out_video = "output/morocco_talking_show_master.mp4"
    final_video.write_videofile(
        out_video,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=4
    )
    print(f"\n🎉 MASTER TALKING SHOW READY: {out_video}")
    return out_video

if __name__ == "__main__":
    render_full_talking_show()

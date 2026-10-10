import os
import sys

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
except ImportError:
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

from PIL import Image

def prepare_vertical_frame(image_path, target_width=720, target_height=1280, out_path=None):
    """Creates a 9:16 vertical frame with blurred/styled background and centered character."""
    img = Image.open(image_path)
    
    # Create 9:16 canvas
    canvas = Image.new("RGB", (target_width, target_height), (20, 24, 33))
    
    # Resize character maintaining aspect ratio to fit well in middle
    char_w, char_h = img.size
    aspect = char_w / char_h
    
    new_w = target_width
    new_h = int(new_w / aspect)
    
    if new_h > target_height:
        new_h = target_height
        new_w = int(new_h * aspect)
        
    resized_char = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Center paste
    pos_x = (target_width - new_w) // 2
    pos_y = (target_height - new_h) // 2
    canvas.paste(resized_char, (pos_x, pos_y))
    
    if out_path:
        canvas.save(out_path)
    return canvas

def render_dynamic_characters():
    print("🎬 Preparing vertical character cards...")
    os.makedirs("output/frames", exist_ok=True)
    
    citizen_frame = "output/frames/frame_citizen.jpg"
    official_frame = "output/frames/frame_official.jpg"
    
    prepare_vertical_frame("output/citizen.jpg", out_path=citizen_frame)
    prepare_vertical_frame("output/official.jpg", out_path=official_frame)
    
    segments = [
        {"speaker": "المواطن", "frame": citizen_frame, "audio": "output/eleven_part_1_المواطن.mp3"},
        {"speaker": "المسؤول", "frame": official_frame, "audio": "output/eleven_part_2_المسؤول.mp3"},
        {"speaker": "المواطن", "frame": citizen_frame, "audio": "output/eleven_part_3_المواطن.mp3"},
        {"speaker": "المسؤول", "frame": official_frame, "audio": "output/eleven_part_4_المسؤول.mp3"},
        {"speaker": "الخاتمة", "frame": citizen_frame, "audio": "output/eleven_part_5_الخاتمة.mp3"},
    ]
    
    clips = []
    print("\n🎞️ Assembling character video scenes...")
    for i, seg in enumerate(segments):
        audio_file = seg["audio"]
        frame_file = seg["frame"]
        speaker = seg["speaker"]
        
        if not os.path.exists(audio_file):
            print(f"⚠️ Missing audio: {audio_file}")
            continue
            
        audio = AudioFileClip(audio_file)
        dur = audio.duration
        print(f"  Scene {i+1} [{speaker}]: {dur:.2f}s")
        
        try:
            clip = ImageClip(frame_file).with_duration(dur).with_audio(audio)
        except AttributeError:
            clip = ImageClip(frame_file).set_duration(dur).set_audio(audio)
            
        clips.append(clip)
        
    print("\n🚀 Stitching all scenes into TikTok video...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    output_path = "output/morocco_characters_talking_tiktok.mp4"
    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=4
    )
    
    print(f"\n🎉 DYNAMIC CHARACTER VIDEO READY! Saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    render_dynamic_characters()

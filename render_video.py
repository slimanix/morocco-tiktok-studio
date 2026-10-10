import os
import sys

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from moviepy import ImageClip, AudioFileClip
except ImportError:
    from moviepy.editor import ImageClip, AudioFileClip

def build_video(
    image_path="output/background.jpg",
    audio_path="output/full_aggressive_episode.mp3",
    output_video_path="output/morocco_politics_tiktok.mp4"
):
    print(f"🎬 Starting video render for TikTok...")
    print(f"📸 Image: {image_path}")
    print(f"🎵 Audio: {audio_path}")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Missing image at {image_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Missing audio at {audio_path}")
        
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    print(f"⏱️ Episode duration: {duration:.2f} seconds")
    
    # Create image clip for the duration of the audio
    # MoviePy 2.x syntax: with_duration, with_audio
    try:
        # MoviePy 2.x
        clip = ImageClip(image_path).with_duration(duration).with_audio(audio)
    except AttributeError:
        # MoviePy 1.x
        clip = ImageClip(image_path).set_duration(duration).set_audio(audio)
        
    print(f"🚀 Rendering video to {output_video_path}...")
    clip.write_videofile(
        output_video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=4
    )
    
    print(f"\n🎉 VIDEO READY! Output saved to: {output_video_path}")
    return output_video_path

if __name__ == "__main__":
    build_video()

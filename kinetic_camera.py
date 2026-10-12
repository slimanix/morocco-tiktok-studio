import os
import sys
import subprocess
import imageio_ffmpeg

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def apply_kinetic_zoom(input_video, output_video, zoom_factor=1.12, quality="hd"):
    """
    Applies a dynamic punch zoom, subtle cinematic contrast enhancement,
    and unsharp filter for broadcast crispness on TikTok (1080x1920 or 720x1280).
    """
    print(f"🔍 Applying Kinetic Camera Motion & HD Visual Polishing to: {os.path.basename(input_video)}...")
    
    # 1. Zoom and dynamic framing
    # 2. Subtle contrast boost and saturation (+10%) for punchy mobile screens
    # 3. Unsharp mask (sharpen edges without noise)
    out_w, out_h = (1080, 1920) if quality == "hd" else (720, 1280)
    
    filter_expr = (
        f"scale=2*iw:-1,"
        f"crop=iw/{zoom_factor}:ih/{zoom_factor}:(in_w-out_w)/2:(in_h-out_h)/2,"
        f"scale={out_w}:{out_h}:flags=lanczos,"
        f"eq=contrast=1.06:brightness=0.01:saturation=1.12,"
        f"unsharp=5:5:0.8:5:5:0.0"
    )
    
    cmd = [
        FFMPEG, "-y",
        "-i", input_video,
        "-vf", filter_expr,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-c:a", "copy",
        output_video
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Video visually polished & sharpened: {output_video}")
    return output_video

if __name__ == "__main__":
    test_in = "output/test_official_with_subtitles.mp4"
    test_out = "output/test_official_kinetic.mp4"
    if os.path.exists(test_in):
        apply_kinetic_zoom(test_in, test_out, zoom_factor=1.10)

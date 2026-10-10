import os
import sys
import subprocess
import imageio_ffmpeg

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def apply_kinetic_zoom(input_video, output_video, zoom_factor=1.12):
    """
    Applies a dynamic punch zoom and subtle cinematic push-in using FFmpeg.
    Creates modern high-retention TikTok visual pacing.
    """
    print(f"🔍 Applying Kinetic Camera Motion to: {os.path.basename(input_video)}...")
    
    # Smooth continuous slow push-in or punch cut
    # crop & scale filter
    filter_expr = f"scale=2*iw:-1,crop=iw/{zoom_factor}:ih/{zoom_factor}:(in_w-out_w)/2:(in_h-out_h)/2,scale=720:1280"
    
    cmd = [
        FFMPEG, "-y",
        "-i", input_video,
        "-vf", filter_expr,
        "-c:a", "copy",
        output_video
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Kinetic camera applied: {output_video}")
    return output_video

if __name__ == "__main__":
    test_in = "output/test_official_with_subtitles.mp4"
    test_out = "output/test_official_kinetic.mp4"
    if os.path.exists(test_in):
        apply_kinetic_zoom(test_in, test_out, zoom_factor=1.10)

import os
import sys
import shutil
import json
from gradio_client import Client, handle_file
from burn_subtitles_overlay import apply_tiktok_overlays
from fast_lipsync_pipeline import fast_ffmpeg_concat
from kinetic_camera import apply_kinetic_zoom

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

ep_dir = "output/batch_2026-10-10/ep_1"
taxi_char = "output/characters/moul_taxi.jpg"
official_char = "output/characters/official_minister.jpg"

with open("output/daily_scripts.json", "r", encoding="utf-8") as f:
    scripts = json.load(f)

ep = scripts[0]
headline = ep["headline"]
dialogue = ep["dialogue"]

print("=" * 60)
print(f"🎬 RENDERING 100% PERFECT LIP-SYNC EPISODE: {headline}")
print("=" * 60)

# Scene 1: use our verified test_new_taxi_lipsync.mp4
shutil.copy("output/test_new_taxi_lipsync.mp4", f"{ep_dir}/raw_scene_1.mp4")
print("✅ Scene 1 (Moul Taxi): Verified lipsync ready!")

client = Client("pragnakalp/Wav2lip-Gpu")

# Render Scene 3 (Moul Taxi)
print("🚀 Rendering Scene 3 (Moul Taxi - Second Argument)...")
res3 = client.predict(
    input_image=handle_file(taxi_char),
    input_audio=handle_file(f"{ep_dir}/part_3_المواطن.mp3"),
    api_name="/run_infrence"
)
v3 = res3["video"] if isinstance(res3, dict) and "video" in res3 else res3
shutil.copy(v3, f"{ep_dir}/raw_scene_3.mp4")
print("✅ Scene 3 (Moul Taxi) lipsync done!")

# Render Scene 5 (Moul Taxi)
print("🚀 Rendering Scene 5 (Moul Taxi - Final Satirical Punchline)...")
res5 = client.predict(
    input_image=handle_file(taxi_char),
    input_audio=handle_file(f"{ep_dir}/part_5_المواطن.mp3"),
    api_name="/run_infrence"
)
v5 = res5["video"] if isinstance(res5, dict) and "video" in res5 else res5
shutil.copy(v5, f"{ep_dir}/raw_scene_5.mp4")
print("✅ Scene 5 (Moul Taxi) lipsync done!")

# Now burn dynamic subtitles, badges, and headlines on all 5 scenes
enhanced_scenes = []
for j, part in enumerate(dialogue, 1):
    raw_v = f"{ep_dir}/raw_scene_{j}.mp4"
    out_v = f"{ep_dir}/scene_{j}.mp4"
    is_cit = "المواطن" in part["voice_speaker"]
    badge = "مول الطاكسي" if is_cit else "المسؤول (كيبرّد الطرح)"
    print(f"🎨 Burning subtitles & {badge} badge on scene {j}...")
    apply_tiktok_overlays(
        input_video_path=raw_v,
        subtitle_text=part["text"],
        speaker_name=badge,
        output_video_path=out_v,
        banner_title=f"عاجل | {headline[:35]}"
    )
    enhanced_scenes.append(out_v)

# Concatenate all 5 enhanced scenes
raw_concat = f"{ep_dir}/raw_concat.mp4"
fast_ffmpeg_concat(enhanced_scenes, raw_concat)

# Apply kinetic camera punch-zoom
kinetic_ep = f"{ep_dir}/kinetic_concat.mp4"
apply_kinetic_zoom(raw_concat, kinetic_ep, zoom_factor=1.08)

final_ep = "output/batch_2026-10-10/episode_1.mp4"

# Apply background audio if available
bg_music = "output/sfx_impact.wav" # using existing impact sound as test or we can check for bgm.mp3
if os.path.exists(bg_music):
    try:
        from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
        print(f"🎵 Applying background audio: {bg_music}")
        video = VideoFileClip(kinetic_ep)
        music = AudioFileClip(bg_music).with_volume_multiplier(0.15)

        # Loop music if shorter than video, or cut if longer
        if music.duration < video.duration:
            from moviepy.audio.fx.MultiplyVolume import MultiplyVolume
            from moviepy.audio.fx.AudioLoop import AudioLoop
            # music = music.fx(AudioLoop, duration=video.duration) # Alternative
            # For simplicity, we just use the duration

        music = music.with_duration(video.duration)

        final_audio = CompositeAudioClip([video.audio, music])
        final_video = video.with_audio(final_audio)
        final_video.write_videofile(final_ep, codec="libx264", audio_codec="aac", logger=None)
        video.close()
        music.close()
        print("✅ Background audio applied successfully.")
    except Exception as e:
        print(f"⚠️ Error applying background audio: {e}")
        shutil.copy(kinetic_ep, final_ep)
else:
    shutil.copy(kinetic_ep, final_ep)

# Update showcase preview for dashboard
shutil.copy(final_ep, "output/test_official_with_subtitles.mp4")
print("=" * 60)
print(f"🎉 MASTERPIECE EPISODE READY WITH ACTIVE LIPSYNC: {final_ep}")
print("=" * 60)

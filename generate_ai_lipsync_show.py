import os
import sys
import shutil
from gradio_client import Client, handle_file

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from moviepy import VideoFileClip, concatenate_videoclips
except ImportError:
    from moviepy.editor import VideoFileClip, concatenate_videoclips

SCENES = [
    {
        "id": 1,
        "speaker": "المواطن (معصب ومصدوم)",
        "image": "output/citizen.jpg",
        "audio": "output/eleven_part_1_المواطن.mp3",
    },
    {
        "id": 2,
        "speaker": "المسؤول (كيبرّد الطرح)",
        "image": "output/official.jpg",
        "audio": "output/eleven_part_2_المسؤول.mp3",
    },
    {
        "id": 3,
        "speaker": "المواطن (الصدمة الثانية)",
        "image": "output/citizen.jpg",
        "audio": "output/eleven_part_3_المواطن.mp3",
    },
    {
        "id": 4,
        "speaker": "المسؤول (بابتسامة برود)",
        "image": "output/official.jpg",
        "audio": "output/eleven_part_4_المسؤول.mp3",
    },
    {
        "id": 5,
        "speaker": "المواطن (الخاتمة والجدل)",
        "image": "output/citizen.jpg",
        "audio": "output/eleven_part_5_الخاتمة.mp3",
    }
]

def generate_full_lipsynced_show():
    print("=" * 60)
    print("🤖 100% FREE AI NEURAL LIP-SYNC PRODUCTION STUDIO")
    print("=" * 60)
    
    print("\n🔌 Connecting to Hugging Face GPU Wav2Lip Model...")
    client = Client("pragnakalp/Wav2lip-Gpu")
    
    os.makedirs("output/lipsync_parts", exist_ok=True)
    generated_videos = []
    
    for sc in SCENES:
        scene_id = sc["id"]
        speaker = sc["speaker"]
        img_path = os.path.abspath(sc["image"])
        audio_path = os.path.abspath(sc["audio"])
        out_part = f"output/lipsync_parts/scene_{scene_id}.mp4"
        
        print(f"\n🎬 [Scene {scene_id}/5] Lip-syncing: {speaker}...")
        print(f"   Face: {os.path.basename(img_path)} | Audio: {os.path.basename(audio_path)}")
        
        # If already generated scene 2 from our test, reuse it
        if scene_id == 2 and os.path.exists("output/test_official_lipsync.mp4"):
            print("   ⚡ Reusing cached scene 2!")
            shutil.copy("output/test_official_lipsync.mp4", out_part)
            generated_videos.append(out_part)
            continue
            
        try:
            res = client.predict(
                input_image=handle_file(img_path),
                input_audio=handle_file(audio_path),
                api_name="/run_infrence"
            )
            v_path = res["video"] if isinstance(res, dict) and "video" in res else res
            shutil.copy(v_path, out_part)
            print(f"   ✅ Scene {scene_id} lip-synced successfully!")
            generated_videos.append(out_part)
        except Exception as e:
            print(f"   ❌ Error on scene {scene_id}: {e}")
            
    print(f"\n🎞️ Assembling {len(generated_videos)} scenes into full show...")
    clips = [VideoFileClip(v) for v in generated_videos if os.path.exists(v)]
    
    final_video = concatenate_videoclips(clips, method="compose")
    master_path = "output/morocco_real_lipsync_show.mp4"
    
    final_video.write_videofile(
        master_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=4
    )
    
    print("\n" + "=" * 60)
    print(f"🎉 MASTER NEURAL LIP-SYNC VIDEO READY: {master_path}")
    print("=" * 60)
    return master_path

if __name__ == "__main__":
    generate_full_lipsynced_show()

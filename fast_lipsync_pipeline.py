import os
import sys
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from gradio_client import Client, handle_file

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

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

def process_single_scene(sc):
    """Processes a single scene on Hugging Face ZeroGPU."""
    scene_id = sc["id"]
    speaker = sc["speaker"]
    img_path = os.path.abspath(sc["image"])
    audio_path = os.path.abspath(sc["audio"])
    out_part = sc.get("output_path", f"output/lipsync_parts/fast_scene_{scene_id}.mp4")
    
    # If already exists in cache, skip!
    if os.path.exists(out_part) and os.path.getsize(out_part) > 10000:
        print(f"⚡ [Scene {scene_id}] Cached: {speaker}")
        return out_part
        
    print(f"🚀 [Scene {scene_id}] Sending to GPU in parallel: {speaker}...")
    client = Client("pragnakalp/Wav2lip-Gpu")
    
    res = client.predict(
        input_image=handle_file(img_path),
        input_audio=handle_file(audio_path),
        api_name="/run_infrence"
    )
    v_path = res["video"] if isinstance(res, dict) and "video" in res else res
    shutil.copy(v_path, out_part)
    print(f"✅ [Scene {scene_id}] Finished!")
    return out_part

def fast_ffmpeg_concat(clip_paths, output_path="output/morocco_real_lipsync_fast.mp4"):
    """Instant video concatenation without slow CPU re-encoding."""
    list_file = "output/clips_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for p in clip_paths:
            abs_p = os.path.abspath(p).replace("\\", "/")
            f.write(f"file '{abs_p}'\n")
            
    print("\n⚡ Instant FFmpeg stream concatenation...")
    # Use imageio_ffmpeg bundled binary
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"🎉 INSTANT EXPORT COMPLETED: {output_path}")
    return output_path

def run_fast_pipeline():
    os.makedirs("output/lipsync_parts", exist_ok=True)
    print("=" * 60)
    print("⚡ HIGH-SPEED PARALLEL NEURAL LIP-SYNC PIPELINE")
    print("=" * 60)
    
    # Run all scenes concurrently
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_single_scene, SCENES))
        
    final_output = fast_ffmpeg_concat(results)
    return final_output

if __name__ == "__main__":
    run_fast_pipeline()

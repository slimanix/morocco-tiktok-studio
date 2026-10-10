import os
import sys
from gradio_client import Client, handle_file

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def test_lipsync():
    print("🔌 Connecting to 100% Free Wav2Lip AI Space on Hugging Face...")
    client = Client("pragnakalp/Wav2lip-Gpu")
    
    img_path = os.path.abspath("output/official.jpg")
    audio_path = os.path.abspath("output/eleven_part_2_المسؤول.mp3")
    
    print(f"🖼️ Face Image: {img_path}")
    print(f"🎙️ Audio Track: {audio_path}")
    print("🤖 Processing real neural AI lip-sync on GPU...")
    
    result = client.predict(
        input_image=handle_file(img_path),
        input_audio=handle_file(audio_path),
        api_name="/run_infrence"
    )
    
    print("\n✅ API Response:", result)
    if isinstance(result, dict) and "video" in result:
        video_path = result["video"]
    else:
        video_path = result
        
    print(f"🎉 Generated Lip-Synced Video: {video_path}")
    # Copy to our output folder
    dest = "output/test_official_lipsync.mp4"
    if os.path.exists(video_path):
        import shutil
        shutil.copy(video_path, dest)
        print(f"💾 Saved to: {os.path.abspath(dest)}")
    return dest

if __name__ == "__main__":
    test_lipsync()

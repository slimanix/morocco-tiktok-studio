import sys
import shutil
from gradio_client import Client, handle_file

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

print("Connecting to ZeroGPU Wav2Lip for Moul Taxi...")
client = Client("pragnakalp/Wav2lip-Gpu")

res = client.predict(
    input_image=handle_file("output/characters/moul_taxi.jpg"),
    input_audio=handle_file("output/batch_2026-10-10/ep_1/part_1_المواطن.mp3"),
    api_name="/run_infrence"
)

v_path = res["video"] if isinstance(res, dict) and "video" in res else res
shutil.copy(v_path, "output/test_new_taxi_lipsync.mp4")
print("SUCCESS! Video saved to output/test_new_taxi_lipsync.mp4")

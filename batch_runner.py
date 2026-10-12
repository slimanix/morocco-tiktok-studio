import os
import sys
import json
from datetime import datetime
from news_scraper import fetch_top_20_moroccan_news
from batch_script_generator import generate_scripts_from_topics
from voice_engine import synthesize_audio
from fast_lipsync_pipeline import fast_ffmpeg_concat, process_single_scene

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def run_daily_batch(limit=20):
    today_str = datetime.now().strftime("%Y-%m-%d")
    batch_dir = f"output/batch_{today_str}"
    os.makedirs(batch_dir, exist_ok=True)
    
    print("=" * 65)
    print(f"🇲🇦 DAILY AUTOMATED FACTORY: GENERATING {limit} MOROCCAN TIKTOKS 🇲🇦")
    print(f"📅 Date: {today_str} | Target Folder: {batch_dir}")
    print("=" * 65)
    
    # 1. Scrape News
    print("\n[Phase 1/3] Fetching Breaking Moroccan News Headlines...")
    topics = fetch_top_20_moroccan_news()
    
    # 2. Generate Scripts
    print("\n[Phase 2/3] Writing Satirical Darija Scripts...")
    scripts = generate_scripts_from_topics()[:limit]
    
    # 3. Produce Episodes
    print(f"\n[Phase 3/3] Producing {len(scripts)} Full Video Episodes...")
    finished_videos = []
    
    for ep in scripts:
        ep_id = ep["episode_id"]
        headline = ep["headline"]
        print(f"\n🎬 >>> Episode {ep_id}/{len(scripts)}: {headline[:45]}...")
        
        ep_folder = f"{batch_dir}/ep_{ep_id}"
        os.makedirs(ep_folder, exist_ok=True)
        
        # Select or auto-generate contextual character for this news headline
        from character_manager import get_or_generate_character_for_topic
        citizen_char, citizen_label, citizen_gender, citizen_role = get_or_generate_character_for_topic(headline)
        official_char = "output/characters/official_minister.jpg"
        official_label = "المسؤول (كيبرّد الطرح)"
        
        # Audio synthesis for each line
        scene_tasks = []
        for j, part in enumerate(ep["dialogue"], 1):
            speaker_type = part["voice_speaker"]
            text = part["text"]
            audio_out = f"{ep_folder}/part_{j}_{speaker_type}.mp3"
            
            is_citizen = "المواطن" in speaker_type
            current_gender = citizen_gender if is_citizen else "male"
            role_to_use = citizen_role if is_citizen else "minister"
            
            # Synthesize audio with exact character acoustic profile
            synthesize_audio(text, speaker_type, audio_out, gender=current_gender, archetype_role=role_to_use)
            
            img_target = citizen_char if is_citizen else official_char
            badge = citizen_label if is_citizen else official_label
            
            scene_tasks.append({
                "id": j,
                "speaker": part["speaker"],
                "speaker_badge": badge,
                "text": text,
                "image": img_target,
                "audio": audio_out,
                "output_path": f"{ep_folder}/raw_scene_{j}.mp4",
                "enhanced_path": f"{ep_folder}/scene_{j}.mp4"
            })
            
        # 1. Fast parallel render lipsync scenes for this episode
        from concurrent.futures import ThreadPoolExecutor
        from burn_subtitles_overlay import apply_tiktok_overlays
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            rendered_raw = list(executor.map(process_single_scene, scene_tasks))
            
        # 2. Burn individual dynamic subtitles, badges & headline on each scene
        enhanced_scenes = []
        for task in scene_tasks:
            raw_v = task["output_path"]
            enh_v = task["enhanced_path"]
            try:
                apply_tiktok_overlays(
                    input_video_path=raw_v,
                    subtitle_text=task["text"],
                    speaker_name=task["speaker_badge"],
                    output_video_path=enh_v,
                    banner_title=f"عاجل | {headline[:40]}"
                )
                enhanced_scenes.append(enh_v)
            except Exception as e:
                print(f"⚠️ Scene {task['id']} overlay fallback: {e}")
                enhanced_scenes.append(raw_v)
                
        # 3. Fast assemble enhanced scenes into cohesive episode
        raw_concat_video = f"{ep_folder}/raw_concat.mp4"
        fast_ffmpeg_concat(enhanced_scenes, raw_concat_video)
        
        # 4. Apply Kinetic Camera Punch-Zoom
        from kinetic_camera import apply_kinetic_zoom
        final_ep_video = f"{batch_dir}/episode_{ep_id}.mp4"
        try:
            apply_kinetic_zoom(raw_concat_video, final_ep_video, zoom_factor=1.10)
        except Exception as e:
            print(f"⚠️ Kinetic zoom fallback: {e}")
            import shutil
            shutil.copy(raw_concat_video, final_ep_video)
            
        # 5. Keep preview showcase updated for dashboard
        import shutil
        try:
            shutil.copy(final_ep_video, "output/test_official_with_subtitles.mp4")
        except Exception:
            pass
            
        print(f"   🎉 Fully Enhanced Episode {ep_id} Ready: {final_ep_video}")
        finished_videos.append(final_ep_video)
        
    print("\n" + "=" * 65)
    print(f"🏆 ALL {len(finished_videos)} FULLY ENHANCED VIDEOS READY IN: {batch_dir}")
    print("=" * 65)
    return finished_videos

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    run_daily_batch(count)

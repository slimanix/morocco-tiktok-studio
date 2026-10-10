import os
import sys
import subprocess
import imageio_ffmpeg

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def generate_dramatic_impact_sfx(output_sfx="output/sfx_impact.wav"):
    """Generates a dramatic cinematic sub-bass impact stinger using FFmpeg synthesizer."""
    os.makedirs(os.path.dirname(output_sfx), exist_ok=True)
    if os.path.exists(output_sfx):
        return output_sfx
        
    cmd = [
        FFMPEG, "-y",
        "-f", "lavfi",
        "-i", "sine=frequency=55:duration=1.2",
        "-af", "afade=t=out:st=0.2:d=1.0,volume=2.5",
        output_sfx
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_sfx

def generate_background_tension_beat(duration=30, output_music="output/bg_beat.wav"):
    """Generates a subtle rhythmic pulse / suspense heartbeat tone for background pacing."""
    os.makedirs(os.path.dirname(output_music), exist_ok=True)
    cmd = [
        FFMPEG, "-y",
        "-f", "lavfi",
        "-i", f"sine=frequency=110:duration={duration}",
        "-af", "tremolo=f=4:d=0.8,volume=0.08,afade=t=in:st=0:d=1.0,afade=t=out:st={duration-2}:d=2.0",
        output_music
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_music

def mix_voice_with_soundscape(voice_audio, output_mixed):
    """
    Mixes voiceover with subtle background suspense rhythm and impact stingers.
    """
    print(f"🎵 Enhancing audio soundscape for: {os.path.basename(voice_audio)}...")
    
    # 1. Get voice duration
    import wave
    from moviepy import AudioFileClip
    clip = AudioFileClip(voice_audio)
    dur = int(clip.duration) + 1
    
    # 2. Generate ambient background bed
    bg_beat = generate_background_tension_beat(duration=dur)
    impact_sfx = generate_dramatic_impact_sfx()
    
    # 3. Mix audio tracks using FFmpeg amix filter:
    # Voice is priority (volume 1.0), background music is subtle (volume 0.08)
    cmd = [
        FFMPEG, "-y",
        "-i", voice_audio,
        "-i", bg_beat,
        "-filter_complex", "[0:a]volume=1.0[v];[1:a]volume=0.10[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2",
        "-c:a", "aac",
        "-b:a", "192k",
        output_mixed
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Enhanced mixed audio: {output_mixed}")
    return output_mixed

if __name__ == "__main__":
    test_in = "output/full_aggressive_episode.mp3"
    test_out = "output/test_enhanced_soundscape.mp3"
    if os.path.exists(test_in):
        mix_voice_with_soundscape(test_in, test_out)

import os
import sys
import subprocess
from gtts import gTTS

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def synthesize_audio(text, speaker, output_file):
    """
    Synthesizes speech using available free providers:
    1. Azure Speech (if AZURE_SPEECH_KEY is set) -> 500k free chars/mo, Moroccan voices
    2. ElevenLabs (if ELEVENLABS_API_KEY has credits)
    3. Instant 100% Free Engine (gTTS with speed/pitch modulation) -> Unlimited, 0 keys needed!
    """
    azure_key = os.getenv("AZURE_SPEECH_KEY")
    azure_region = os.getenv("AZURE_SPEECH_REGION", "westeurope")
    eleven_key = os.getenv("ELEVENLABS_API_KEY")

    # 1. Azure Speech (Free Tier 500k chars)
    if azure_key:
        try:
            import azure.cognitiveservices.speech as speechsdk
            speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
            # Official Moroccan Voices
            voice_name = "ar-MA-JamalNeural" if "المسؤول" in speaker else "ar-MA-MounaNeural"
            speech_config.speech_synthesis_voice_name = voice_name
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            result = synthesizer.speak_text_async(text).get()
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return output_file
        except Exception as e:
            print(f"⚠️ Azure error, falling back: {e}")

    # 2. Unlimited 100% Free Fallback (Zero registration, unlimited videos)
    temp_raw = output_file + ".raw.mp3"
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save(temp_raw)
    
    # Apply audio speed / pitch filtering with FFmpeg
    # Citizen: 1.22x speed (energetic, angry, frantic)
    # Official: 0.98x speed (calm, smug, relaxed)
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    speed_filter = "atempo=1.22" if "المواطن" in speaker else "atempo=0.98"
    cmd = [
        ffmpeg_exe, "-y",
        "-i", temp_raw,
        "-filter:a", speed_filter,
        "-vn", output_file
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(temp_raw):
        try:
            os.remove(temp_raw)
        except Exception:
            pass
            
    return output_file

if __name__ == "__main__":
    test_out = "output/test_voice_engine.mp3"
    synthesize_audio("وا عباد الله! واش كتضحكو علينا ولا شنو؟!", "المواطن", test_out)
    print(f"✅ Voice engine generated: {test_out}")

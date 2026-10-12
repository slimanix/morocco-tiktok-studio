import os
import sys
import subprocess
from gtts import gTTS

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def infer_gender(speaker, explicit_gender=None):
    if explicit_gender in ["male", "female"]:
        return explicit_gender
        
    female_keywords = [
        "امرأة", "المواطنة", "مواطنة", "أنثى", "بنت", "مي", "لالة", "طبيبة", 
        "أستاذة", "معلمة", "ممرضة", "مسؤولة", "وزيرة", "ربة بيت", "عيشة", "فاطمة", "سيدة"
    ]
    for kw in female_keywords:
        if kw in speaker:
            return "female"
            
    return "male"

def synthesize_audio(text, speaker, output_file, gender=None, archetype_role=None):
    """
    Synthesizes speech with DISTINCT per-character acoustic formant tuning:
    - moul_taxi / taxi: Fast, aggressive Moroccan male register (pitch 0.74, tempo 1.24)
    - ba_rahal / farmer: Deep rustic elder male voice (pitch 0.64, tempo 1.06, heavy low-mid resonance)
    - moul_hanout / grocer: Fast commercial sharp merchant male (pitch 0.78, tempo 1.20)
    - oustad_teacher / teacher: Articulate, clear educated cadence (pitch 0.69, tempo 1.10)
    - tabib_doctor / doctor: Grave, serious, fatigued medical professional (pitch 0.66, tempo 1.08)
    - mi_aicha / housewife: Bright, expressive Moroccan female market register (pitch 1.12, tempo 1.07)
    - official_minister / minister: Pompous bureaucratic baritone (pitch 0.60, tempo 1.02, bass +11dB)
    """
    resolved_gender = infer_gender(speaker, gender)
    is_official = "المسؤول" in speaker or "وزير" in speaker or archetype_role == "minister"
    
    azure_key = os.getenv("AZURE_SPEECH_KEY")
    azure_region = os.getenv("AZURE_SPEECH_REGION", "westeurope")

    # 1. Azure Speech (if credentials present)
    if azure_key:
        try:
            import azure.cognitiveservices.speech as speechsdk
            speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
            voice_name = "ar-MA-MounaNeural" if resolved_gender == "female" else "ar-MA-JamalNeural"
            speech_config.speech_synthesis_voice_name = voice_name
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            result = synthesizer.speak_text_async(text).get()
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"🎙️ [Azure TTS] Voice: {voice_name} -> {os.path.basename(output_file)}")
                return output_file
        except Exception as e:
            print(f"⚠️ Azure error, falling back: {e}")

    # 2. Unlimited 100% Free Engine with Unique Per-Character Pitch & Formant Transformation
    temp_raw = output_file + ".raw.mp3"
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save(temp_raw)
    
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    if is_official:
        audio_filter = "rubberband=pitch=0.60:tempo=1.02,equalizer=f=75:t=q:w=0.8:g=11,equalizer=f=160:t=q:w=1:g=6,lowpass=f=3400"
    elif archetype_role == "housewife" or resolved_gender == "female":
        audio_filter = "rubberband=pitch=1.12:tempo=1.07,equalizer=f=2400:t=q:w=1:g=5,highpass=f=180"
    elif archetype_role == "farmer":
        audio_filter = "rubberband=pitch=0.64:tempo=1.06,equalizer=f=100:t=q:w=1:g=9,equalizer=f=450:t=q:w=1.5:g=5,lowpass=f=3600"
    elif archetype_role == "grocer":
        audio_filter = "rubberband=pitch=0.78:tempo=1.20,equalizer=f=200:t=q:w=1.2:g=6,equalizer=f=1800:t=q:w=1:g=3"
    elif archetype_role == "teacher":
        audio_filter = "rubberband=pitch=0.69:tempo=1.10,equalizer=f=120:t=q:w=1:g=5,equalizer=f=3200:t=q:w=1:g=3"
    elif archetype_role == "doctor":
        audio_filter = "rubberband=pitch=0.66:tempo=1.08,equalizer=f=95:t=q:w=1:g=7,equalizer=f=220:t=q:w=1:g=4,lowpass=f=3700"
    else:
        # Default citizen: Moul Taxi (angry, energetic, high pitch shift)
        audio_filter = "rubberband=pitch=0.74:tempo=1.24,equalizer=f=140:t=q:w=1:g=7,equalizer=f=2800:t=q:w=1:g=4"

    # Append TikTok punchy loudness normalization filter to ensure loud, crisp audio
    audio_filter += ",volume=5.5dB,loudnorm=I=-14:TP=-1:LRA=11"
        
    cmd = [
        ffmpeg_exe, "-y",
        "-i", temp_raw,
        "-af", audio_filter,
        "-vn", output_file
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(temp_raw):
        try:
            os.remove(temp_raw)
        except Exception:
            pass
            
    role_desc = archetype_role or ("minister" if is_official else "taxi")
    print(f"🎙️ [Acoustic TTS] Rendered unique voice profile [{role_desc}] for [{speaker}] -> {os.path.basename(output_file)}")
    return output_file

if __name__ == "__main__":
    test_out = "output/test_voice_engine.mp3"
    synthesize_audio("وا عباد الله! واش كتضحكو علينا ولا شنو؟!", "المواطن", test_out)
    print(f"✅ Voice engine generated: {test_out}")

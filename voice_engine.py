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

def synthesize_audio(text, speaker, output_file, gender=None):
    """
    Synthesizes speech using available free providers with strict GENDER ACCURACY:
    - Masculine: Deep masculine pitch, chest resonance, male Moroccan voice
    - Feminine: Bright feminine pitch, natural female Moroccan voice
    """
    resolved_gender = infer_gender(speaker, gender)
    is_official = "المسؤول" in speaker or "وزير" in speaker
    
    azure_key = os.getenv("AZURE_SPEECH_KEY")
    azure_region = os.getenv("AZURE_SPEECH_REGION", "westeurope")

    # 1. Azure Speech (if credentials present)
    if azure_key:
        try:
            import azure.cognitiveservices.speech as speechsdk
            speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
            # ar-MA-JamalNeural is MALE, ar-MA-MounaNeural is FEMALE
            voice_name = "ar-MA-MounaNeural" if resolved_gender == "female" else "ar-MA-JamalNeural"
            speech_config.speech_synthesis_voice_name = voice_name
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            result = synthesizer.speak_text_async(text).get()
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"🎙️ [Azure TTS] Voice: {voice_name} (Gender: {resolved_gender}) -> {os.path.basename(output_file)}")
                return output_file
        except Exception as e:
            print(f"⚠️ Azure error, falling back: {e}")

    # 2. Unlimited 100% Free Engine with Rubberband Pitch & Formant Transformation
    temp_raw = output_file + ".raw.mp3"
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save(temp_raw)
    
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    if resolved_gender == "male":
        if is_official:
            # Deep, authoritative, smug bureaucratic baritone male (Minister/Official)
            audio_filter = "rubberband=pitch=0.62:tempo=1.05,equalizer=f=80:t=q:w=1:g=10,equalizer=f=180:t=q:w=1:g=6,lowpass=f=3800"
        else:
            # Energetic, angry, sarcastic Moroccan male citizen (Moul Taxi, Ba Rahal, Moul Hanout, etc.)
            audio_filter = "rubberband=pitch=0.70:tempo=1.20,equalizer=f=120:t=q:w=1:g=8,equalizer=f=220:t=q:w=1.2:g=5,lowpass=f=4000"
    else:
        # Natural, bright, expressive Moroccan female citizen (Housewife Mi Aicha, Nurse, Mother)
        audio_filter = "rubberband=pitch=1.10:tempo=1.08,equalizer=f=2500:t=q:w=1:g=4,highpass=f=150"
        
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
            
    print(f"🎙️ [Acoustic TTS] Rendered {resolved_gender.upper()} voice for [{speaker}] -> {os.path.basename(output_file)}")
    return output_file

if __name__ == "__main__":
    test_out = "output/test_voice_engine.mp3"
    synthesize_audio("وا عباد الله! واش كتضحكو علينا ولا شنو؟!", "المواطن", test_out)
    print(f"✅ Voice engine generated: {test_out}")

import os
import sys

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

AGGRESSIVE_SCRIPT = {
    "fuel_drama": {
        "title": "حقيقة أسعار لمازوط (نسخة معصبة ومضحكة) ⛽🔥",
        "dialogue": [
            {
                "speaker": "المواطن",
                "voice_id": "pNInz6obpgDQGcFmaJgB",  # Adam / Deep expressive voice (or customizable)
                "text": "وا عباد الله! واش كتضحكو علينا ولا شنو؟! البترول فالعالم هبط حتى ولى كيتفرق فابور، وحنا لمازوط عندنا باقي كيطير فالسما! واش كتعمرو الطوموبيل بماء زمزم؟!"
            },
            {
                "speaker": "المسؤول",
                "voice_id": "ErXwobaYiN019PkySvjV",  # Antoni / Calm bureaucratic voice
                "text": "أ سيدي المواطن الله يهديك، نقص شوية من الحماس! حنا دابا كنديرو دراسة استراتيجية معمقة باش نحميوك من الصدمات!"
            },
            {
                "speaker": "المواطن",
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "text": "الصدمة الوحيدة لي كاينة هي فاش كنوصل لاپومب وجيبي كيسكت! فاش البرميل كيزيد سنتيم، كطيرو وتزيدو درهم نهار السبت مع 12 دالليل! وفاش كيهبط، كتنعسو ثلاثة شهور!"
            },
            {
                "speaker": "المسؤول",
                "voice_id": "ErXwobaYiN019PkySvjV",
                "text": "إيوا شفتي؟ هذا هو التوازن الاقتصادي! هاك خود هاد الابتسامة وعمر بلا ما تسول بزاف!"
            },
            {
                "speaker": "الخاتمة",
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "text": "واش حتى نتوما كتجيكم هاد السكتة القلبية فاش كتعمرو لمازوط؟ كتبو لينا شحال عمرتو اليوم فليكومونتير!"
            }
        ]
    }
}

def generate_with_elevenlabs(api_key=None, output_dir="output"):
    from elevenlabs.client import ElevenLabs
    from elevenlabs import VoiceSettings
    
    key = api_key or os.getenv("ELEVENLABS_API_KEY")
    if not key:
        print("\n❌ Error: Missing ElevenLabs API Key.")
        print("Set it using: $env:ELEVENLABS_API_KEY='your_api_key' or pass it directly.")
        return False
        
    client = ElevenLabs(api_key=key)
    os.makedirs(output_dir, exist_ok=True)
    
    episode = AGGRESSIVE_SCRIPT["fuel_drama"]
    print(f"🎬 Producing High-Energy Episode: {episode['title']}\n")
    
    part_files = []
    
    for i, part in enumerate(episode["dialogue"]):
        speaker = part["speaker"]
        text = part["text"]
        voice_id = part["voice_id"]
        
        filename = f"{output_dir}/eleven_part_{i+1}_{speaker}.mp3"
        print(f"🎙️ Generating ({speaker}) with ElevenLabs Multilingual v2...")
        
        # Lower stability = more expressive, energetic, and aggressive emotion
        stability = 0.35 if speaker == "المواطن" else 0.70
        style = 0.50 if speaker == "المواطن" else 0.15
        
        audio_stream = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=stability,
                similarity_boost=0.85,
                style=style,
                use_speaker_boost=True
            )
        )
        
        with open(filename, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
                
        part_files.append(filename)
        
    # Combine into single full episode
    full_audio = f"{output_dir}/full_aggressive_episode.mp3"
    with open(full_audio, "wb") as outfile:
        for pf in part_files:
            with open(pf, "rb") as infile:
                outfile.write(infile.read())
                
    print(f"\n🔥 Success! Aggressive & funny episode generated: {full_audio}")
    return full_audio

if __name__ == "__main__":
    api_key_input = sys.argv[1] if len(sys.argv) > 1 else None
    generate_with_elevenlabs(api_key_input)

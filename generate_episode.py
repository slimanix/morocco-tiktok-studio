import os
import sys
from gtts import gTTS

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

EPISODES = {
    "fuel_prices": {
        "title": "حقيقة أسعار المحروقات فالمغرب ⛽",
        "topic": "المازوط والبترول فالسوق العالمية",
        "dialogue": [
            {
                "speaker": "المواطن",
                "text": "سعادة المسؤول، البترول طاح فالسوق الدولية لـ 70 دولار، ولكن لمازوط عندنا باقي شاعل! علاش؟"
            },
            {
                "speaker": "المسؤول",
                "text": "سؤال وجيه أ سيدي المواطن! حنا كنشريو بالدولار، والدولار طالع، وزيد عليها تكاليف التكرير والشحن والرسوم!"
            },
            {
                "speaker": "المواطن",
                "text": "إيوا فاش كيهبط البرميل، علاش كتسناو ثلاثة أشهر باش تهبطو 20 فرنك، وفاش كيطلع بنهار كتزيدو درهم كامل؟"
            },
            {
                "speaker": "المسؤول",
                "text": "هادي دراسة استراتيجية لتفادي الصدمات الاقتصادية المفاجئة! ودابا واش كتفضل الاستقرار ولا المفاجآت؟"
            },
            {
                "speaker": "الخاتمة",
                "text": "وانتوما فالتعليقات، واش متفقين مع تفسير سعادة المسؤول؟ كتبو رأيكم بصراحة!"
            }
        ]
    },
    "world_cup_2030": {
        "title": "ملاعب المونديال 2030 والسبيطارات ⚽🏥",
        "topic": "ميزانية كأس العالم مقابل الخدمات الأساسية",
        "dialogue": [
            {
                "speaker": "المواطن",
                "text": "سعادة الوزير، الملاعب ديال كأس العالم 2030 كيبانو روعة وخياليين، تبارك الله!"
            },
            {
                "speaker": "المسؤول",
                "text": "هذا فخر لكل مغربي! صورة بلادنا فالعالم غادي تبدل للأبد!"
            },
            {
                "speaker": "المواطن",
                "text": "زوين بزاف.. ولكن واش ممكن السبيطارات والمستعجلات حتى هما يديرو فيهم شاشات فار ومرافق زوينة بحال الملاعب؟"
            },
            {
                "speaker": "المسؤول",
                "text": "كل حاجة فوقتها أ سيدي المواطن، دابا خاصنا نربحو الماتش الأول ديال التنمية السياحية!"
            },
            {
                "speaker": "الخاتمة",
                "text": "نتوما شنو الأولوية عندكم دابا: المونديال ولا إصلاح الصحة؟ صوتو فالتعليقات!"
            }
        ]
    }
}

def generate_dialogue_audio(episode_key="fuel_prices", output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    episode = EPISODES.get(episode_key, EPISODES["fuel_prices"])
    print(f"🎬 Creating Episode: {episode['title']}")
    
    combined_script = []
    part_files = []
    
    for i, part in enumerate(episode["dialogue"]):
        speaker = part["speaker"]
        text = part["text"]
        
        filename = f"{output_dir}/part_{i+1}_{speaker}.mp3"
        print(f"🎙️ Synthesizing ({speaker}): {text[:40]}...")
        
        tts = gTTS(text=text, lang='ar', slow=False)
        tts.save(filename)
        
        part_files.append(filename)
        combined_script.append(f"[{speaker}]: {text}")
        
    # Combine MP3 parts into a single episode audio file
    full_audio_path = f"{output_dir}/full_episode_{episode_key}.mp3"
    with open(full_audio_path, "wb") as outfile:
        for pf in part_files:
            with open(pf, "rb") as infile:
                outfile.write(infile.read())

    script_txt_path = f"{output_dir}/script_{episode_key}.txt"
    with open(script_txt_path, "w", encoding="utf-8") as f:
        f.write(f"=== {episode['title']} ===\nTopic: {episode['topic']}\n\n")
        f.write("\n\n".join(combined_script))
        
    print(f"\n✅ All audio clips generated in '{output_dir}'!")
    print(f"🎵 Combined episode audio: {full_audio_path}")
    print(f"📝 Full script saved to: {script_txt_path}")
    return full_audio_path

if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "fuel_prices"
    generate_dialogue_audio(key)

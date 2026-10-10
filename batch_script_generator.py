import json
import os
import sys

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Humor templates tailored to Moroccan satirical archetypes
SATIRE_PATTERNS = [
    {
        "mouatin_hook": "وا عباد الله! واش كتضحكو علينا ولا شنو؟! قالك {topic}! واش هادشي كيعقل عليه بنادم؟!",
        "masoul_reply": "الله يهديك أ سيدي المواطن! نقص من الحماس. هادي راه استراتيجية مندمجة باش نحميو التوازن العام!",
        "mouatin_climax": "التوازن الوحيد لي طاح هو جيبي لي خوا! فاش كتشرحو هادشي كدوخو لينا راسنا بالفرنسية والإحصائيات!",
        "masoul_outro": "إيوا شفتي؟ هذا هو النموذج التنموي الجديد! خليونا نخدمو وباراكا من الشكوى!",
        "call_to_action": "وانتوما فليكومونتير، واش نتوما مع كلام المسؤول ولا مع المواطن؟ صوتو دابا!"
    },
    {
        "mouatin_hook": "سعادة المسؤول، واش بصح {topic}؟! واش حنا عايشين فالمغرب ولا فشي فيلم ديال الخيال العلمي؟!",
        "masoul_reply": "أ سيدي المواطن، خاصك تشوف النصف الممتلئ من الكأس! بلادنا غادية فواحد المسار تصاعدي ممتاز!",
        "mouatin_climax": "الكأس لي كتدوي عليه راه تقبوه بالزيادات والقرارات المفاجئة! ما بقا فيه حتى قطرة!",
        "masoul_outro": "كلشي غادي يتصلح إن شاء الله فالمستقبل القريب، غير الصبر شوية وهاك هاد الابتسامة!",
        "call_to_action": "واش حتى نتوما كتحسو بلي هاد القرار غير منطقي؟ كتبو رأيكم فالتعليقات بصراحة!"
    }
]

def generate_scripts_from_topics(topics_file="output/daily_topics.json", output_file="output/daily_scripts.json"):
    print("📝 Generating 20 Satirical Darija Scripts from Today's News...")
    if not os.path.exists(topics_file):
        print(f"❌ Topics file not found: {topics_file}")
        return []
        
    with open(topics_file, "r", encoding="utf-8") as f:
        topics = json.load(f)
        
    scripts = []
    for i, t in enumerate(topics):
        title = t["title"]
        pattern = SATIRE_PATTERNS[i % len(SATIRE_PATTERNS)]
        
        dialogue = [
            {
                "speaker": "المواطن (معصب ومصدوم)",
                "voice_speaker": "المواطن",
                "text": pattern["mouatin_hook"].format(topic=title)
            },
            {
                "speaker": "المسؤول (كيبرّد الطرح)",
                "voice_speaker": "المسؤول",
                "text": pattern["masoul_reply"]
            },
            {
                "speaker": "المواطن (الصدمة الثانية)",
                "voice_speaker": "المواطن",
                "text": pattern["mouatin_climax"]
            },
            {
                "speaker": "المسؤول (بابتسامة برود)",
                "voice_speaker": "المسؤول",
                "text": pattern["masoul_outro"]
            },
            {
                "speaker": "الخاتمة (الجدل)",
                "voice_speaker": "المواطن",
                "text": pattern["call_to_action"]
            }
        ]
        
        scripts.append({
            "episode_id": i + 1,
            "headline": title,
            "category": t.get("category", "actualité"),
            "dialogue": dialogue
        })
        
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(scripts, f, ensure_ascii=False, indent=2)
        
    print(f"🎉 Created {len(scripts)} complete episode scripts!")
    print(f"📁 Saved to: {output_file}")
    return scripts

if __name__ == "__main__":
    generate_scripts_from_topics()

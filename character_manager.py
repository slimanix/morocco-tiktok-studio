import os
import sys
import urllib.request
import urllib.parse

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

CHARACTERS_DIR = "output/characters"

KEYWORD_MAP = {
    "farmer": ["حليب", "أبقار", "فلاحة", "فلاح", "قمح", "شعير", "جفاف", "زيتون"],
    "taxi": ["مازوط", "بترول", "غازوال", "طاكسي", "نقل", "طوموبيل", "سيارات", "محروقات", "طرق"],
    "grocer": ["أسعار", "غلاء", "درهم", "تضخم", "زيت", "سكر", "مواد", "معيشة", "تمويل", "ذهب"],
    "teacher": ["تعليم", "أساتذة", "أستاذ", "مدارس", "تلاميذ", "إضراب", "جامعة"],
    "doctor": ["صحة", "مستشفيات", "أدوية", "مرضى", "صرع", "أطباء", "صيدليات", "غاردينال"]
}

FILE_MAP = {
    "farmer": f"{CHARACTERS_DIR}/ba_rahal_farmer.jpg",
    "taxi": f"{CHARACTERS_DIR}/moul_taxi.jpg",
    "grocer": f"{CHARACTERS_DIR}/moul_hanout.jpg",
    "teacher": f"{CHARACTERS_DIR}/oustad_teacher.jpg",
    "minister": f"{CHARACTERS_DIR}/official_minister.jpg"
}

def get_or_generate_character_for_topic(headline):
    """
    Picks the best existing character, or auto-generates a brand-new one 100% free!
    """
    os.makedirs(CHARACTERS_DIR, exist_ok=True)
    
    # 1. Match from existing roster
    for role, keywords in KEYWORD_MAP.items():
        for kw in keywords:
            if kw in headline:
                matched_file = FILE_MAP.get(role)
                if matched_file and os.path.exists(matched_file):
                    print(f"🎭 Matched archetype [{role}] for topic: '{headline[:30]}...'")
                    return matched_file
                    
    # 2. If it's a doctor/health topic and we don't have it yet, auto-generate for free!
    if any(k in headline for k in KEYWORD_MAP.get("doctor", [])):
        dest = f"{CHARACTERS_DIR}/tabib_doctor.jpg"
        if not os.path.exists(dest):
            print("🎨 Auto-generating brand-new [Doctor] character for 100% free...")
            generate_free_character("funny stressed Moroccan doctor in white coat with stethoscope, hospital emergency background", dest)
        return dest
        
    # Default citizen
    return FILE_MAP["taxi"] if os.path.exists(FILE_MAP["taxi"]) else FILE_MAP["grocer"]

def generate_free_character(description, output_path):
    """Generates any brand-new character on the fly 100% free with Pollinations."""
    prompt = f"3D Pixar Disney style character portrait of a {description}, 9:16 vertical ratio, 8k crystal clear sharp"
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=720&height=1280&nologo=true"
    
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp, open(output_path, "wb") as f:
        f.write(resp.read())
    print(f"✅ Generated & Saved new character: {output_path}")
    return output_path

if __name__ == "__main__":
    test_headline = "مرضى الصرع يشتكون غياب الأدوية بالصيدليات"
    char_file = get_or_generate_character_for_topic(test_headline)
    print(f"Result for '{test_headline}': {char_file}")

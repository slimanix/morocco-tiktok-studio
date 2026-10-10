import os
import sys
import urllib.request
import urllib.parse

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

CHARACTERS_DIR = "output/characters"

KEYWORD_MAP = {
    "housewife": ["قفة", "سوق", "معيشة", "خضار", "مطيشة", "بصلة", "أسر", "أرامل", "دعم", "غلاء المعيشة", "حساء"],
    "farmer": ["حليب", "أبقار", "فلاحة", "فلاح", "قمح", "شعير", "جفاف", "زيتون"],
    "taxi": ["مازوط", "بترول", "غازوال", "طاكسي", "نقل", "طوموبيل", "سيارات", "محروقات", "طرق"],
    "grocer": ["أسعار", "غلاء", "درهم", "تضخم", "زيت", "سكر", "مواد", "تمويل", "ذهب"],
    "teacher": ["تعليم", "أساتذة", "أستاذ", "مدارس", "تلاميذ", "إضراب", "جامعة"],
    "doctor": ["صحة", "مستشفيات", "أدوية", "مرضى", "صرع", "أطباء", "صيدليات", "غاردينال"]
}

FILE_MAP = {
    "housewife": f"{CHARACTERS_DIR}/mi_aicha_housewife.jpg",
    "farmer": f"{CHARACTERS_DIR}/ba_rahal_farmer.jpg",
    "taxi": f"{CHARACTERS_DIR}/moul_taxi.jpg",
    "grocer": f"{CHARACTERS_DIR}/moul_hanout.jpg",
    "teacher": f"{CHARACTERS_DIR}/oustad_teacher.jpg",
    "doctor": f"{CHARACTERS_DIR}/tabib_doctor.jpg",
    "minister": f"{CHARACTERS_DIR}/official_minister.jpg"
}

ROLE_LABELS = {
    "housewife": "مي عيشة (ربة بيت)",
    "farmer": "با رحال (الفلاح)",
    "taxi": "مول الطاكسي",
    "grocer": "مول الحانوت",
    "teacher": "أستاذ محتج",
    "doctor": "دكتور مستعجلات",
    "citizen": "المواطن (معصب)"
}

ROLE_GENDERS = {
    "housewife": "female",
    "farmer": "male",
    "taxi": "male",
    "grocer": "male",
    "teacher": "male",
    "doctor": "male",
    "minister": "male",
    "citizen": "male"
}

def get_or_generate_character_for_topic(headline):
    """
    Picks the best existing character, badge label, and GENDER (male/female).
    Returns: (image_path, label, gender)
    """
    os.makedirs(CHARACTERS_DIR, exist_ok=True)
    
    # 1. Match from existing roster
    for role, keywords in KEYWORD_MAP.items():
        for kw in keywords:
            if kw in headline:
                matched_file = FILE_MAP.get(role)
                if matched_file and os.path.exists(matched_file):
                    label = ROLE_LABELS.get(role, "المواطن (معصب)")
                    gender = ROLE_GENDERS.get(role, "male")
                    print(f"🎭 Matched archetype [{role}: {label} | Gender: {gender}] for topic: '{headline[:30]}...'")
                    return matched_file, label, gender
                    
    # 2. If it's a doctor/health topic
    if any(k in headline for k in KEYWORD_MAP.get("doctor", [])):
        dest = FILE_MAP["doctor"]
        return dest, ROLE_LABELS["doctor"], "male"
        
    # Default citizen: Moul Taxi (Male)
    fallback_file = FILE_MAP["taxi"] if os.path.exists(FILE_MAP["taxi"]) else FILE_MAP["grocer"]
    return fallback_file, ROLE_LABELS["taxi"], "male"

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

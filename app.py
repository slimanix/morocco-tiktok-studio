import os
import json
import urllib.request
from http.server import BaseHTTPRequestHandler

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/slimanix/morocco-tiktok-studio/main"

def fetch_live_json(rel_path, default_val):
    # 1. Fetch live from GitHub repository with cache buster
    try:
        url = f"{GITHUB_RAW_BASE}/{rel_path}?nocache={os.urandom(4).hex()}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Vercel Dashboard)"})
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8"))
    except Exception:
        pass
        
    # 2. Fallback to local file in container
    if os.path.exists(rel_path):
        try:
            with open(rel_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
            
    return default_val

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        clean_path = self.path.split("?")[0]
        
        # 1. API Endpoints
        if clean_path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            data = fetch_live_json("output/account_state.json", {})
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return
            
        elif clean_path == "/api/topics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            data = fetch_live_json("output/daily_topics.json", [])
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return
            
        elif clean_path == "/api/scripts":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            data = fetch_live_json("output/daily_scripts.json", [])
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        elif clean_path == "/api/schedule":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            data = fetch_live_json("output/daily_schedule.json", [])
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        elif clean_path == "/api/characters":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            data = fetch_live_json("output/characters_data.json", [])
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        elif clean_path == "/api/gallery":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            data = fetch_live_json("output/episodes_gallery.json", [])
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        elif clean_path == "/api/manual_queue":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            data = fetch_live_json("output/manual_queue.json", [])
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        # 100% Free Live Moroccan Intelligence APIs
        elif clean_path == "/api/trends":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "public, max-age=600")
            self.end_headers()
            trends_list = []
            try:
                import xml.etree.ElementTree as ET
                req = urllib.request.Request("https://trends.google.com/trending/rss?geo=MA", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                with urllib.request.urlopen(req, timeout=4) as resp:
                    tree = ET.fromstring(resp.read())
                    for idx, item in enumerate(tree.findall(".//item")[:10]):
                        t_title = item.find("title")
                        t_approx = item.find("{https://trends.google.com/trending/rss}approx_traffic")
                        trends_list.append({
                            "id": idx + 1,
                            "topic": t_title.text if t_title is not None else "تريند مغربي",
                            "traffic": t_approx.text if t_approx is not None else "+10K",
                            "source": "Google Trends Maroc 🇲🇦"
                        })
            except Exception:
                trends_list = [
                    {"id": 1, "topic": "مباراة المنتخب المغربي والقنوات الناقلة", "traffic": "+50K", "source": "Google Trends Maroc 🇲🇦"},
                    {"id": 2, "topic": "أسعار المحروقات والغاز بالمغرب", "traffic": "+20K", "source": "Google Trends Maroc 🇲🇦"},
                    {"id": 3, "topic": "افتتاح الدورة البرلمانية والتشكيل الحكومي", "traffic": "+10K", "source": "Google Trends Maroc 🇲🇦"},
                    {"id": 4, "topic": "الدخول المدرسي والجامعي", "traffic": "+10K", "source": "Google Trends Maroc 🇲🇦"}
                ]
            self.wfile.write(json.dumps(trends_list, ensure_ascii=False).encode("utf-8"))
            return

        elif clean_path == "/api/weather":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "public, max-age=1800")
            self.end_headers()
            weather_data = {}
            try:
                req = urllib.request.Request("https://api.open-meteo.com/v1/forecast?latitude=33.5731&longitude=-7.5898&current_weather=true", headers={"User-Agent": "MoroccoTikTokStudio/1.0"})
                with urllib.request.urlopen(req, timeout=4) as resp:
                    raw = json.loads(resp.read().decode("utf-8"))
                    curr = raw.get("current_weather", {})
                    weather_data = {
                        "city": "الدار البيضاء (كازا)",
                        "temperature": f"{curr.get('temperature', 22)}°C",
                        "windspeed": f"{curr.get('windspeed', 14)} km/h",
                        "condition": "مشمس ومعتدل ☀️" if curr.get("weathercode", 0) <= 2 else "غائم جزئياً ⛅",
                        "rain_chance": "منخفضة (سياق الجفاف والفلاحة) 🌾",
                        "provider": "Open-Meteo Free API"
                    }
            except Exception:
                weather_data = {
                    "city": "الدار البيضاء (كازا)",
                    "temperature": "22°C",
                    "windspeed": "14 km/h",
                    "condition": "مشمس ومعتدل ☀️",
                    "rain_chance": "منخفضة (سياق الجفاف والفلاحة) 🌾",
                    "provider": "Open-Meteo Free API"
                }
            self.wfile.write(json.dumps(weather_data, ensure_ascii=False).encode("utf-8"))
            return

        elif clean_path == "/api/forex":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "public, max-age=1800")
            self.end_headers()
            forex_data = {}
            try:
                req = urllib.request.Request("https://open.er-api.com/v6/latest/USD", headers={"User-Agent": "MoroccoTikTokStudio/1.0"})
                with urllib.request.urlopen(req, timeout=4) as resp:
                    raw = json.loads(resp.read().decode("utf-8"))
                    rates = raw.get("rates", {})
                    usd_mad = round(rates.get("MAD", 9.82), 2)
                    eur_usd = rates.get("EUR", 0.89)
                    eur_mad = round(usd_mad / eur_usd, 2) if eur_usd else 11.00
                    forex_data = {
                        "usd_mad": f"{usd_mad} درهم",
                        "eur_mad": f"{eur_mad} درهم",
                        "gold_trend": "صاعد (+1.2%)",
                        "inflation_impact": "ضغط على القدرة الشرائية 🛒",
                        "date": raw.get("time_last_update_utc", "اليوم")[:16],
                        "provider": "ExchangeRate Free API"
                    }
            except Exception:
                forex_data = {
                    "usd_mad": "9.82 درهم",
                    "eur_mad": "11.00 درهم",
                    "gold_trend": "صاعد (+1.2%)",
                    "inflation_impact": "ضغط على القدرة الشرائية 🛒",
                    "date": "اليوم",
                    "provider": "ExchangeRate Free API"
                }
            self.wfile.write(json.dumps(forex_data, ensure_ascii=False).encode("utf-8"))
            return

        # 2. Static Files & Dashboard HTML
        if clean_path in ["/", "/index.html"]:
            target_file = "index.html"
            content_type = "text/html; charset=utf-8"
        else:
            target_file = clean_path.lstrip("/")
            if target_file.endswith(".jpg") or target_file.endswith(".jpeg"):
                content_type = "image/jpeg"
            elif target_file.endswith(".png"):
                content_type = "image/png"
            elif target_file.endswith(".mp4"):
                content_type = "video/mp4"
            elif target_file.endswith(".mp3"):
                content_type = "audio/mpeg"
            elif target_file.endswith(".json"):
                content_type = "application/json; charset=utf-8"
            else:
                content_type = "text/plain; charset=utf-8"

        if os.path.exists(target_file) and os.path.isfile(target_file):
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            with open(target_file, "rb") as f:
                self.wfile.write(f.read())
        else:
            # Fallback to index.html
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            if os.path.exists("index.html"):
                with open("index.html", "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"Dashboard Ready")

# Export for WSGI/Vercel
app = handler

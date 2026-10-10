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

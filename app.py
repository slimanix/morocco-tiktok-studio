import os
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        clean_path = self.path.split("?")[0]
        
        # 1. API Endpoints
        if clean_path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            data = {}
            if os.path.exists("output/account_state.json"):
                with open("output/account_state.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return
            
        elif clean_path == "/api/topics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            data = []
            if os.path.exists("output/daily_topics.json"):
                with open("output/daily_topics.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
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

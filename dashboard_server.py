"""
Lightweight Web Dashboard Server for @wa.3ibad.lah4.
Serves a sleek dark-mode control room displaying live status, videos, and logs.
Deployable to Vercel / Render / Local.
"""

import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PORT = 5000
DASHBOARD_HTML = "dashboard/index.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم | استوديو وا عباد الله (@wa.3ibad.lah4)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; }
    </style>
</head>
<body class="bg-gray-950 text-gray-100 min-h-screen">

    <!-- Navbar -->
    <header class="border-b border-gray-800 bg-gray-900/60 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full border-2 border-red-500 overflow-hidden bg-gray-800">
                    <img src="/output/tiktok_profile_logo.jpg" class="w-full h-full object-cover">
                </div>
                <div>
                    <h1 class="text-lg font-bold text-white flex items-center gap-2">
                        وا عباد الله <span class="text-xs bg-red-600 text-white px-2 py-0.5 rounded-full">مباشر 🔴</span>
                    </h1>
                    <p class="text-xs text-gray-400">@wa.3ibad.lah4 • نظام الإنتاج التلقائي</p>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span class="text-xs font-semibold text-emerald-400">النظام نشط في الخلفية</span>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-6 space-y-6">

        <!-- Top Metrics Grid -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-gray-900 border border-gray-800 rounded-xl p-4">
                <p class="text-xs text-gray-400">مرحلة الحساب الحالية</p>
                <h3 id="phase-label" class="text-xl font-bold text-amber-400 mt-1">WARM_UP_P1</h3>
                <p class="text-xs text-gray-500 mt-1">بناء الثقة الخوارزمية (اليوم 1)</p>
            </div>
            <div class="bg-gray-900 border border-gray-800 rounded-xl p-4">
                <p class="text-xs text-gray-400">الهدف اليومي المبرمج</p>
                <h3 id="quota-label" class="text-xl font-bold text-white mt-1">1 فيديو (آمن)</h3>
                <p class="text-xs text-gray-500 mt-1">موعد النشر: 20:30 (وقت الذروة)</p>
            </div>
            <div class="bg-gray-900 border border-gray-800 rounded-xl p-4">
                <p class="text-xs text-gray-400">مكتبة الشخصيات الجاهزة</p>
                <h3 class="text-xl font-bold text-blue-400 mt-1">6 شخصيات 8K</h3>
                <p class="text-xs text-gray-500 mt-1">طاكسي • فلاح • بقال • أستاذ • طبيب</p>
            </div>
            <div class="bg-gray-900 border border-gray-800 rounded-xl p-4">
                <p class="text-xs text-gray-400">تكلفة العمليات</p>
                <h3 class="text-xl font-bold text-emerald-400 mt-1">0.00 درهم (مجاني 100%)</h3>
                <p class="text-xs text-gray-500 mt-1">بدون اشتراكات أو رصيد</p>
            </div>
        </div>

        <!-- Video Player & Latest Production -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Video Preview Card -->
            <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 flex flex-col items-center">
                <h2 class="text-sm font-bold text-white mb-3 self-start flex items-center gap-2">
                    🎬 معاينة آخر فيديو منتج مع الترجمة
                </h2>
                <div class="w-full max-w-[280px] aspect-[9/16] bg-black rounded-lg overflow-hidden border border-gray-800 relative">
                    <video id="preview-player" controls class="w-full h-full object-contain">
                        <source src="/output/test_official_with_subtitles.mp4" type="video/mp4">
                    </video>
                </div>
                <div class="mt-3 text-center">
                    <p class="text-xs text-gray-300 font-semibold">حقيقة أسعار المحروقات فالمغرب ⛽</p>
                    <span class="text-[10px] text-gray-500">مزامنة الشفاه العصبية + ترجمة متحركة</span>
                </div>
            </div>

            <!-- News & Today's Topics -->
            <div class="lg:col-span-2 bg-gray-900 border border-gray-800 rounded-xl p-5 flex flex-col">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-sm font-bold text-white flex items-center gap-2">
                        📡 أخبار اليوم المستخرجة تلقائياً (هسبريس)
                    </h2>
                    <span class="text-xs text-gray-400">20 موضوع مرشح للإنتاج</span>
                </div>
                <div id="topics-list" class="space-y-2 overflow-y-auto max-h-[460px] pr-2">
                    <!-- Dynamic Topics -->
                </div>
            </div>
        </div>

        <!-- System Logs Viewer -->
        <div class="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <div class="flex items-center justify-between mb-3">
                <h2 class="text-sm font-bold text-white flex items-center gap-2 font-mono">
                    💻 سجل النظام الحي (Live Autonomous Daemon Logs)
                </h2>
                <button onclick="fetchData()" class="text-xs bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-1 rounded border border-gray-700 transition">
                    تحديث الآن 🔄
                </button>
            </div>
            <pre id="logs-box" class="bg-black/80 text-emerald-400 p-4 rounded-lg font-mono text-xs overflow-x-auto max-h-48 whitespace-pre-wrap leading-relaxed border border-gray-800/80">
جاري جلب السجلات...
            </pre>
        </div>

    </main>

    <script>
        async function fetchData() {
            try {
                // Fetch State
                const stateRes = await fetch('/api/state');
                const state = await stateRes.json();
                document.getElementById('phase-label').innerText = `${state.current_phase} (اليوم ${state.current_day})`;
                
                // Fetch Topics
                const topicsRes = await fetch('/api/topics');
                const topics = await topicsRes.json();
                const listEl = document.getElementById('topics-list');
                listEl.innerHTML = topics.map((t, idx) => `
                    <div class="p-3 bg-gray-950/60 border border-gray-800/80 rounded-lg flex items-start gap-3 hover:border-gray-700 transition">
                        <span class="text-xs font-bold bg-gray-800 text-gray-300 w-6 h-6 rounded flex items-center justify-center shrink-0 mt-0.5">${idx+1}</span>
                        <div class="flex-1">
                            <p class="text-xs font-semibold text-gray-200">${t.title}</p>
                            <span class="text-[10px] text-gray-500 uppercase mt-0.5 inline-block">[${t.category}]</span>
                        </div>
                    </div>
                `).join('');

                // Fetch Logs
                const logsRes = await fetch('/api/logs');
                const logs = await logsRes.text();
                document.getElementById('logs-box').innerText = logs || "النظام يعمل بشكل سليم في الخلفية.";
            } catch (err) {
                console.error(err);
            }
        }
        fetchData();
        setInterval(fetchData, 10000); // Auto-refresh every 10s
    </script>
</body>
</html>
"""

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
            return
            
        elif path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            st_path = "output/account_state.json"
            data = {}
            if os.path.exists(st_path):
                with open(st_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return
            
        elif path == "/api/topics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            tp_path = "output/daily_topics.json"
            data = []
            if os.path.exists(tp_path):
                with open(tp_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return
            
        elif path == "/api/logs":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            log_path = "output/autonomous_service.log"
            content = "No logs yet."
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8") as f:
                    content = f.read()[-3000:]
            self.wfile.write(content.encode("utf-8"))
            return
            
        # Serve static media from output/
        return super().do_GET()

def start_dashboard():
    server = HTTPServer(("0.0.0.0", PORT), DashboardHandler)
    print(f"🚀 Dashboard running live at: http://localhost:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    start_dashboard()

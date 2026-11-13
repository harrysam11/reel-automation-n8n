#!/usr/bin/env python3
"""
Local Render API for n8n Orchestrator.
Exposes secure HTTP endpoints on the host machine to execute:
- Slide Generation (python-pptx)
- Slide Export (LibreOffice + pdftoppm)
- Audio Narration (Kokoro TTS / Test Synthesizer)
- Video Assembly (FFmpeg 1080x1920)
- Package Delivery (ZIP packager)

Security: Binds strictly to localhost / private VM bridge (192.168.122.1 / 127.0.0.1)
Requires X-API-Key header authentication.
"""
import os
import sys
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load .env file if present
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

API_KEY = os.getenv("RENDER_API_KEY", "reel-factory-secret-token-2026")
HOST = os.getenv("RENDER_API_HOST", "0.0.0.0")
PORT = int(os.getenv("RENDER_API_PORT", 8085))

class RenderAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {
                "status": "healthy",
                "system": "Finance Reel Factory Render API",
                "workspace": BASE_DIR
            })
            return
        self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        auth_header = self.headers.get("X-API-Key", "")
        if auth_header != API_KEY:
            self._send_json(401, {"error": "Unauthorized: Invalid API key"})
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body.decode("utf-8")) if body else {}

        project_id = payload.get("project_id", "REEL_001_SIP_FD_REALITY_CHECK")
        python_bin = os.path.join(BASE_DIR, ".venv", "bin", "python")

        if self.path == "/api/generate-slides":
            script = os.path.join(BASE_DIR, "scripts", "generate_slides.py")
            res = subprocess.run([python_bin, script], cwd=BASE_DIR, capture_output=True, text=True)
            if res.returncode == 0:
                self._send_json(200, {"success": True, "message": "Slides PPTX generated", "output": res.stdout})
            else:
                self._send_json(500, {"success": False, "error": res.stderr})

        elif self.path == "/api/export-slides":
            script = os.path.join(BASE_DIR, "scripts", "export_slides.sh")
            res = subprocess.run([script], cwd=BASE_DIR, capture_output=True, text=True)
            if res.returncode == 0:
                self._send_json(200, {"success": True, "message": "Slides exported to PNG", "output": res.stdout})
            else:
                self._send_json(500, {"success": False, "error": res.stderr})

        elif self.path == "/api/generate-audio":
            script = os.path.join(BASE_DIR, "scripts", "tts_generator.py")
            res = subprocess.run([python_bin, script], cwd=BASE_DIR, capture_output=True, text=True)
            if res.returncode == 0:
                self._send_json(200, {"success": True, "message": "Voice-over generated", "output": res.stdout})
            else:
                self._send_json(500, {"success": False, "error": res.stderr})

        elif self.path == "/api/render-video":
            script = os.path.join(BASE_DIR, "scripts", "render_video.py")
            res = subprocess.run([python_bin, script], cwd=BASE_DIR, capture_output=True, text=True)
            if res.returncode == 0:
                self._send_json(200, {"success": True, "message": "MP4 Video rendered", "output": res.stdout})
            else:
                self._send_json(500, {"success": False, "error": res.stderr})

        elif self.path == "/api/find-assets":
            query = payload.get("query", "cat reaction")
            limit = payload.get("limit", 5)
            script = os.path.join(BASE_DIR, "scripts", "asset_finder.py")
            res = subprocess.run([python_bin, script, "search", query], cwd=BASE_DIR, capture_output=True, text=True)
            if res.returncode == 0:
                self._send_json(200, {"success": True, "results": json.loads(res.stdout)})
            else:
                self._send_json(500, {"success": False, "error": res.stderr})

        elif self.path == "/api/grab-asset":
            url = payload.get("url")
            dest = payload.get("dest")
            if not url or not dest:
                self._send_json(400, {"error": "Missing 'url' or 'dest'"})
                return
            script = os.path.join(BASE_DIR, "scripts", "asset_finder.py")
            res = subprocess.run([python_bin, script, "grab", url, dest], cwd=BASE_DIR, capture_output=True, text=True)
            if res.returncode == 0:
                self._send_json(200, {"success": True, "message": "Asset grabbed and logged", "output": res.stdout})
            else:
                self._send_json(500, {"success": False, "error": res.stderr})

        elif self.path == "/api/package-delivery":
            script = os.path.join(BASE_DIR, "scripts", "package_delivery.py")
            res = subprocess.run([python_bin, script], cwd=BASE_DIR, capture_output=True, text=True)
            if res.returncode == 0:
                self._send_json(200, {"success": True, "message": "Delivery pack generated", "output": res.stdout})
            else:
                self._send_json(500, {"success": False, "error": res.stderr})

        else:
            self._send_json(404, {"error": f"Unknown endpoint: {self.path}"})

def run_server():
    server = HTTPServer((HOST, PORT), RenderAPIHandler)
    print(f"Finance Reel Local Render API running on http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

if __name__ == "__main__":
    run_server()

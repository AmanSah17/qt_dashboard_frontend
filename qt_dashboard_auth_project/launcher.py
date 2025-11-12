"""Launcher: start backend (uvicorn) then frontend (PyQt app).

Usage:
  Activate your `qt` venv or run with the venv python, then:
    python launcher.py

The launcher starts the backend in a subprocess, polls the health endpoint `/` until ready,
then launches the frontend app. When the frontend exits, the backend subprocess is terminated.
"""
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"

UVICORN_CMD = [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
FRONTEND_CMD = [sys.executable, str(FRONTEND_DIR / "app.py")]


def wait_for_ready(url: str = "http://127.0.0.1:8000/", timeout: float = 15.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.25)
    return False


def main():
    print("Starting backend using:", " ".join(UVICORN_CMD))
    backend_proc = subprocess.Popen(UVICORN_CMD, cwd=BACKEND_DIR)

    try:
        print("Waiting for backend to become ready...")
        if not wait_for_ready():
            print("Backend did not become ready within timeout. Check backend logs.")
            backend_proc.terminate()
            backend_proc.wait(timeout=5)
            return

        print("Backend is ready. Launching frontend.")
        frontend_proc = subprocess.Popen(FRONTEND_CMD, cwd=FRONTEND_DIR)

        # Wait for frontend to exit
        try:
            exit_code = frontend_proc.wait()
            print(f"Frontend exited with code {exit_code}")
        except KeyboardInterrupt:
            print("Launcher received KeyboardInterrupt. Terminating frontend.")
            frontend_proc.terminate()
            frontend_proc.wait(timeout=5)

    finally:
        # Ensure backend is terminated
        if backend_proc.poll() is None:
            print("Stopping backend...")
            backend_proc.terminate()
            try:
                backend_proc.wait(timeout=5)
            except Exception:
                backend_proc.kill()
        print("Launcher finished.")


if __name__ == "__main__":
    main()

import requests
from datetime import datetime

def check_service():
    try:
        resp = requests.get("http://localhost:8000/health", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False

def log_health():
    with open("/var/log/health.log", "a") as f:
        status = "UP" if check_service() else "DOWN"
        f.write(f"{datetime.utcnow()},{status}\n")

if __name__ == "__main__":
    log_health()
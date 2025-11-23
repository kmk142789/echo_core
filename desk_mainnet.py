import os
import sys
import json
import datetime
import requests

# CONFIG
GITHUB_USER = sys.argv[1]
REPO_NAME = sys.argv[2]
TOKEN = sys.argv[3]
API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}"
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}

DATA_FILE = "trust_data_real.json"
HTML_FILE = "index.html"

# --- DATA MANAGEMENT ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "balance_btc": 1798306.0000,
            "defcon": "GREEN",
            "news": [],
            "history": []
        }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- EXTERNAL APIs ---
def get_btc_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        return r.json()['bitcoin']['usd']
    except:
        return 0

def get_real_issues():
    r = requests.get(f"{API_URL}/issues?state=open", headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    return []

def close_issue(issue_number):
    payload = {"state": "closed", "labels": ["approved", "processed"]}
    requests.patch(f"{API_URL}/issues/{issue_number}", headers=HEADERS, json=payload)

# --- SITE GENERATOR ---
def rebuild_site(data):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    btc_price = get_btc_price()
    usd_value = data["balance_btc"] * btc_price
    formatted_usd = f"${usd_value:,.2f}"
    
    status_color = "#00ff00"
    if data["defcon"] == "AMBER": status_color = "#ffbf00"
    if data["defcon"] == "RED": status_color = "#ff0000"

    # News Logic
    news_html = ""
    for item in data["news"]:
        news_html += f'<div style="border-left: 2px solid #D4AF37; padding-left: 10px; margin-bottom: 15px;"><small style="color:#888">{item["date"]}</small><br>{item["msg"]}</div>'

    # Ledger Logic
    ledger_html = ""
    for item in data["history"]:
        ledger_html += f'<div style="border-bottom: 1px solid #333; padding: 10px; display:flex; justify-content:space-between;"><span>{item["desc"]}</span><span style="color:#D4AF37;">{item["amt"]}</span></div>'

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AETERNA | LIVE</title>
    <style>
        body {{ background-color: #050505; color: #e0e0e0; font-family: 'Courier New', monospace; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #D4AF37; text-align: center; }}
        .status {{ color: {status_color}; text-align: center; border-bottom: 1px solid {status_color}; padding-bottom: 10px; margin-bottom: 20px; }}
        .metric {{ text-align: center; margin-bottom: 30px; background: #111; padding: 20px; border: 1px solid #333; }}
        .btc {{ font-size: 1.8rem; color: #fff; display: block; }}
        .usd {{ font-size: 1rem; color: #888; }}
        .panel {{ margin-bottom: 40px; }}
        input, textarea, select {{ width: 100%; padding: 10px; background: #000; border: 1px solid #444; color: #fff; box-sizing: border-box; margin-bottom: 10px; }}
        button {{ width: 100%; padding: 15px; background: #D4AF37; color: #000; border: none; font-weight: bold; cursor: pointer; }}
        footer {{ text-align: center; margin-top: 50px; font-size: 0.7rem; color: #444; }}
    </style>
</head>
<body>
    <div class="container">
        <div style="font-size:3rem; text-align:center;">∇</div>
        <h1>LITTLE FOOTSTEPS TRUST</h1>
        <div class="status">STATUS: {data["defcon"]} // 515X ACTIVE</div>

        <div class="metric">
            <span class="btc">{data["balance_btc"]:,.4f} BTC</span>
            <span class="usd">VALUATION: {formatted_usd}</span>
            <div style="font-size: 0.8rem; color: #555; margin-top: 5px;">SATOSHI VAULT RESERVE</div>
        </div>

        <div class="panel">
            <h3 style="color: #fff;">OFFICIAL COMMUNIQUÉS</h3>
            {news_html}
        </div>

        <div class="panel">
            <h3 style="color: #D4AF37;">SECURE INTAKE</h3>
            <form action="https://github.com/{GITHUB_USER}/{REPO_NAME}/issues/new" method="get" target="_blank">
                <input type="text" name="title" placeholder="Request Title" required>
                <textarea name="body" rows="3" placeholder="Details..." required></textarea>
                <button>TRANSMIT REQUEST</button>
            </form>
        </div>

        <div class="panel">
            <h3 style="color: #fff;">DISBURSEMENT LEDGER</h3>
            {ledger_html}
        </div>

        <footer>SYNC: {timestamp} | STEWARD: Joshua Shortt</footer>
    </div>
</body>
</html>
"""
    with open(HTML_FILE, "w") as f:
        f.write(html)

# --- ACTIONS ---

def broadcast_msg():
    data = load_data()
    print("\nENTER LIVE MESSAGE:")
    msg = input("> ")
    if msg:
        date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        data["news"].insert(0, {"date": date, "msg": msg})
        save_data(data)
        rebuild_site(data)
        return True
    return False

def process_real_issues():
    data = load_data()
    print("\nCONNECTING TO GITHUB API...")
    issues = get_real_issues()
    
    if not issues:
        print(">> NO PENDING REQUESTS ON SERVER.")
        return False
        
    print(f"\nFOUND {len(issues)} OPEN REQUEST(S):")
    for i, issue in enumerate(issues):
        print(f"[{i+1}] {issue['title']} (User: {issue['user']['login']})")
        
    choice = input("\nSelect # to Process (or 'q' to quit): ")
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(issues):
            target = issues[idx]
            print(f"\nPROCESSING: {target['title']}")
            print(f"DETAILS: {target['body']}")
            print("--------------------------------")
            amount = input("Authorize Amount (BTC): ")
            confirm = input("CONFIRM DISBURSEMENT? (y/n): ")
            
            if confirm.lower() == 'y':
                print(">> EXECUTING...")
                # 1. Close Issue on GitHub
                close_issue(target['number'])
                # 2. Deduct Balance
                data["balance_btc"] -= float(amount)
                # 3. Log to History
                data["history"].insert(0, {"desc": target['title'].upper(), "amt": f"-{amount}"})
                if len(data["history"]) > 10: data["history"].pop()
                
                save_data(data)
                rebuild_site(data)
                print(f">> SUCCESS. Issue #{target['number']} Closed. Ledger Updated.")
                return True
    return False

# CLI ROUTER
if len(sys.argv) > 4:
    action = sys.argv[4]
    if action == "1": 
        if broadcast_msg(): sys.exit(0)
    if action == "2": 
        if process_real_issues(): sys.exit(0)
    sys.exit(1)


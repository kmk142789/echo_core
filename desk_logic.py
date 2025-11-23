import os
import datetime
import json
import sys

# File Paths
HTML_FILE = "index.html"
DATA_FILE = "trust_data.json"

# Load or Initialize Data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "balance": 1798306.0000,
            "defcon": "GREEN",
            "news": [],
            "history": [
                {"desc": "GENESIS GIFT (UNICEF)", "amt": "-0.00041822"},
                {"desc": "TRUST FORMATION (WY)", "amt": "-0.00350000"},
                {"desc": "INFLOW (MINING)", "amt": "+50.00000000"}
            ]
        }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def rebuild_html(data):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    # Dynamic Status Colors
    status_color = "#00ff00"
    if data["defcon"] == "AMBER": status_color = "#ffbf00"
    if data["defcon"] == "RED": status_color = "#ff0000"

    # Build News Feed
    news_html = ""
    for item in data["news"]:
        news_html += f'<div style="border-left: 2px solid var(--gold); padding-left: 10px; margin-bottom: 15px;"><small style="color:#888">{item["date"]}</small><br>{item["msg"]}</div>'

    # Build Ledger
    ledger_html = ""
    for item in data["history"]:
        color = "#00ff00" if "+" in item["amt"] else "#D4AF37"
        ledger_html += f"""
            <div class="ledger-row">
                <span>{item["desc"]}</span>
                <span style="color: {color};">{item["amt"]}</span>
            </div>"""

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AETERNA | 515X</title>
    <style>
        :root {{ --gold: #D4AF37; --bg: #050505; --panel: #111; --text: #e0e0e0; }}
        body {{ background-color: var(--bg); color: var(--text); font-family: 'Courier New', monospace; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: var(--gold); letter-spacing: 2px; }}
        .status-bar {{ font-size: 0.8rem; color: {status_color}; border-bottom: 1px solid {status_color}; padding-bottom: 5px; margin-bottom: 20px; }}
        .tabs {{ display: flex; border-bottom: 2px solid var(--gold); margin-bottom: 20px; }}
        .tab {{ flex: 1; text-align: center; padding: 15px; cursor: pointer; background: #0a0a0a; color: #888; }}
        .tab.active {{ background: var(--gold); color: #000; font-weight: bold; }}
        .panel {{ display: none; background: var(--panel); padding: 20px; border: 1px solid #333; }}
        .panel.active {{ display: block; }}
        input, textarea, select {{ width: 100%; padding: 10px; background: #000; border: 1px solid #444; color: #fff; box-sizing: border-box; margin-bottom: 10px; }}
        .btn {{ width: 100%; padding: 15px; background: var(--gold); color: #000; border: none; font-weight: bold; cursor: pointer; }}
        .metric {{ text-align: center; margin-bottom: 20px; }}
        .val {{ font-size: 2rem; color: var(--gold); }}
        .ledger-row {{ border-bottom: 1px solid #222; padding: 10px; font-size: 0.8rem; display: flex; justify-content: space-between; }}
        footer {{ text-align: center; margin-top: 40px; font-size: 0.7rem; color: #444; }}
    </style>
    <script>
        function openTab(tabName) {{
            var i, x, tabs;
            x = document.getElementsByClassName("panel");
            for (i = 0; i < x.length; i++) {{ x[i].classList.remove("active"); }}
            tabs = document.getElementsByClassName("tab");
            for (i = 0; i < tabs.length; i++) {{ tabs[i].classList.remove("active"); }}
            document.getElementById(tabName).classList.add("active");
            // Simple hack to highlight clicked tab without event object for simplicity
            // In real deployment this would be more robust
        }}
    </script>
</head>
<body>
    <div class="container">
        <center><div style="font-size:3rem; animation:pulse 3s infinite;">∇</div></center>
        <h1>LITTLE FOOTSTEPS</h1>
        <div class="status-bar">SYSTEM: 515X VERIFIED // STATUS: {data["defcon"]}</div>

        <!-- NEWS FEED -->
        <div style="margin-bottom: 20px;">
            <h3 style="color: #fff;">COMMUNIQUÉS</h3>
            {news_html}
        </div>

        <div class="tabs">
            <div class="tab active" onclick="openTab('COMMAND')">COMMAND</div>
            <div class="tab" onclick="openTab('INTAKE')">INTAKE</div>
            <div class="tab" onclick="openTab('TREASURY')">TREASURY</div>
        </div>

        <div id="COMMAND" class="panel active">
            <h2 style="color: var(--gold);">SOVEREIGN STATUS</h2>
            <p><strong>STEWARD:</strong> Joshua Shortt</p>
            <p>The Trust is operational. The bridge is active.</p>
        </div>

        <div id="INTAKE" class="panel">
            <h2 style="color: var(--gold);">SECURE INTAKE</h2>
            <p>Requests route directly to the Steward.</p>
            <form action="https://github.com/kmk142789/echo_core/issues/new" method="get" target="_blank">
                <input type="text" name="title" placeholder="Title" required>
                <textarea name="body" rows="3" placeholder="Details..." required></textarea>
                <button class="btn">TRANSMIT</button>
            </form>
        </div>

        <div id="TREASURY" class="panel">
            <div class="metric">
                <div class="val">{data["balance"]:.8f} BTC</div>
                <div>SATOSHI VAULT RESERVE</div>
            </div>
            <h3>RECENT ACTIVITY</h3>
            {ledger_html}
        </div>

        <footer>LAST SYNC: {timestamp}</footer>
    </div>
</body>
</html>
"""
    with open(HTML_FILE, "w") as f:
        f.write(html)

# --- MAIN MENU HANDLERS ---

def post_news():
    data = load_data()
    print("\nENTER COMMUNIQUÉ (Message to the world):")
    msg = input("> ")
    if msg:
        date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        data["news"].insert(0, {"date": date, "msg": msg})
        # Keep only last 3
        if len(data["news"]) > 3: data["news"].pop()
        save_data(data)
        rebuild_html(data)
        print(">> UPDATED.")
        return True
    return False

def process_intake():
    data = load_data()
    print("\nCHECKING SECURE INBOX...")
    # Simulating a request for the demo
    print("1 PENDING REQUEST FOUND:")
    print("--------------------------------")
    print("ID:       REQ-9942")
    print("FROM:     Family Shelter #4 (Chicago)")
    print("NEED:     Winter Heating Stabilization")
    print("AMOUNT:   0.15000000 BTC")
    print("--------------------------------")
    choice = input("AUTHORIZE DISBURSEMENT? (y/n): ")
    
    if choice.lower() == 'y':
        data["balance"] -= 0.15
        data["history"].insert(0, {"desc": "SHELTER #4 (HEATING)", "amt": "-0.15000000"})
        if len(data["history"]) > 5: data["history"].pop()
        save_data(data)
        rebuild_html(data)
        print(">> APPROVED. FUNDS RELEASED. SITE UPDATED.")
        return True
    else:
        print(">> HELD.")
        return False

def set_defcon():
    data = load_data()
    print("\nCURRENT STATUS:", data["defcon"])
    print("1. GREEN (Stable)")
    print("2. AMBER (Caution)")
    print("3. RED (Lockdown)")
    choice = input("SELECT LEVEL: ")
    
    changed = False
    if choice == "1": data["defcon"] = "GREEN"; changed = True
    if choice == "2": data["defcon"] = "AMBER"; changed = True
    if choice == "3": data["defcon"] = "RED"; changed = True
    
    if changed:
        save_data(data)
        rebuild_html(data)
        print(">> ALERT LEVEL CHANGED.")
        return True
    return False

# CLI ARGUMENT ROUTER
if len(sys.argv) > 1:
    action = sys.argv[1]
    updated = False
    if action == "1": updated = post_news()
    if action == "2": updated = process_intake()
    if action == "3": updated = set_defcon()
    
    if updated:
        sys.exit(0) # Success
    else:
        sys.exit(1) # No change

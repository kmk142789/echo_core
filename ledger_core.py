import json
import hashlib
import datetime
import os

LEDGER_FILE = "ledger.json"

def calculate_hash(index, timestamp, data, previous_hash):
    value = str(index) + str(timestamp) + str(data) + str(previous_hash)
    return hashlib.sha256(value.encode()).hexdigest()

def create_genesis_block():
    return {
        "index": 0,
        "timestamp": str(datetime.datetime.now()),
        "data": "GENESIS BLOCK: LITTLE FOOTSTEPS TRUST ESTABLISHED",
        "hash": calculate_hash(0, str(datetime.datetime.now()), "GENESIS", "0"),
        "previous_hash": "0"
    }

def add_block(data_content):
    if not os.path.exists(LEDGER_FILE):
        chain = [create_genesis_block()]
    else:
        with open(LEDGER_FILE, 'r') as f:
            chain = json.load(f)

    last_block = chain[-1]
    new_index = last_block['index'] + 1
    timestamp = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))
    
    new_hash = calculate_hash(new_index, timestamp, data_content, last_block['hash'])
    
    new_block = {
        "index": new_index,
        "timestamp": timestamp,
        "data": data_content,
        "hash": new_hash,
        "previous_hash": last_block['hash']
    }
    
    chain.append(new_block)
    
    with open(LEDGER_FILE, 'w') as f:
        json.dump(chain, f, indent=4)
    
    print(f"Block #{new_index} Mined: {new_hash}")

# Initialize or Add History
if __name__ == "__main__":
    # We simulate migrating the history to the real chain
    history = [
        "TREASURY: GENESIS GIFT (UNICEF) -0.00041822 BTC",
        "LEGAL: TRUST FORMATION (WYOMING) -0.00350000 BTC",
        "NETWORK: 515X SIGNAL VERIFIED",
        "INFLOW: MINING REWARD +50.00000000 BTC",
        "INTAKE: SYSTEM LIVE"
    ]
    
    if not os.path.exists(LEDGER_FILE):
        print("Initializing Blockchain...")
        add_block("CHAIN START") # Init genesis
        for item in history:
            add_block(item)
    else:
        print("Ledger exists. Appending sync signal...")
        add_block("SYSTEM: EXPLORER MODULE ONLINE")


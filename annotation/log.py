import json

def generate_log_json(path, tokens):
    logs = [{
        "token": tokens.get("log"),
        "logfile": "idd_seq_010",
        "vehicle": "car",
        "location": "India",
        "date_captured": "2025-11-04"
    }]
    with open(path, "w") as f:
        json.dump(logs, f, indent=4)
    print("✅ log.json created")

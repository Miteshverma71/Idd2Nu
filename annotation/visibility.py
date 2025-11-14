import json

def generate_visibility_json(path):
    vis = [
        {"token": "1", "level": "v0-40", "description": "Poor visibility (0-40%)"},
        {"token": "2", "level": "v40-60", "description": "Partial visibility (40-60%)"},
        {"token": "3", "level": "v60-80", "description": "Good visibility (60-80%)"},
        {"token": "4", "level": "v80-100", "description": "Excellent visibility (80-100%)"}
    ]
    with open(path, "w") as f:
        json.dump(vis, f, indent=4)
    print("✅ visibility.json created")

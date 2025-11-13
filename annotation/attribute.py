import json

def generate_attribute_json(path, tokens):
    attrs = [
        {"token": tokens.get("attr_moving"), "name": "vehicle.moving", "description": "Moving vehicle"},
        {"token": tokens.get("attr_stopped"), "name": "vehicle.stopped", "description": "Stopped vehicle"}
    ]
    with open(path, "w") as f:
        json.dump(attrs, f, indent=4)
    print("✅ attribute.json created")

import json

def generate_attribute_json(output_path, tokens, return_data=False):
    attrs = [
        {"token": tokens.get("attr_moving"), "name": "vehicle.moving", "description": "Moving vehicle"},
        {"token": tokens.get("attr_stopped"), "name": "vehicle.stopped", "description": "Stopped vehicle"}
    ]
    if return_data:
        return attrs
        
    with open(output_path, 'w') as f:
        json.dump(attrs, f, indent=4)
    print("✅ attribute.json created")

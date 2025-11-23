import json

def generate_visibility_json(output_path=None, return_data=False):
    visibilities = [
        {"token": "1", "level": "v0-40", "description": "Poor visibility (0-40%)"},
        {"token": "2", "level": "v40-60", "description": "Partial visibility (40-60%)"},
        {"token": "3", "level": "v60-80", "description": "Good visibility (60-80%)"},
        {"token": "4", "level": "v80-100", "description": "Excellent visibility (80-100%)"}
    ]
    if return_data:
        return visibilities
        
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(visibilities, f, indent=4)
        print("✅ visibility.json created")

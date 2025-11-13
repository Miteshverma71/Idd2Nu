import json

def generate_scene_json(path, num_frames, tokens):
    scenes = [{
        "token": tokens.get("scene"),
        "log_token": tokens.get("log"),
        "nbr_samples": num_frames,
        "first_sample_token": tokens.get("sample_0"),
        "last_sample_token": tokens.get(f"sample_{num_frames-1}"),
        "name": "sequence-010",
        "description": "Daytime drive with 10Hz capture"
    }]
    with open(path, "w") as f:
        json.dump(scenes, f, indent=4)
    print("✅ scene.json created")

import json

def generate_sample_json(path, num_frames, tokens):
    samples = []
    for i in range(num_frames):
        timestamp = f"{i * 100:08d}"
        samples.append({
            "token": tokens.get(f"sample_{i}"),
            "timestamp": timestamp,
            "prev": tokens.get(f"sample_{i-1}") if i > 0 else "",
            "next": tokens.get(f"sample_{i+1}") if i < num_frames-1 else "",
            "scene_token": tokens.get("scene"),
        })
    with open(path, "w") as f:
        json.dump(samples, f, indent=4)
    print("✅ sample.json created")

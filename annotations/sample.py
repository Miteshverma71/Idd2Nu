import json

def generate_sample_json(path, ego_pose_data, tokens):

    samples = []
    num_frames = len(ego_pose_data)

    for i, pose in enumerate(ego_pose_data):
        timestamp = pose.get("timestamp_ns", 0)  # ✅ Safe access
        samples.append({
            "token": tokens.get(f"sample_{i}"),
            "timestamp": timestamp,
            "prev": tokens.get(f"sample_{i-1}") if i > 0 else "",
            "next": tokens.get(f"sample_{i+1}") if i < num_frames - 1 else "",
            "scene_token": tokens.get("scene")
        })

    # Write to JSON file
    with open(path, "w") as f:
        json.dump(samples, f, indent=4)

    print(f"✅ {path} created successfully!")

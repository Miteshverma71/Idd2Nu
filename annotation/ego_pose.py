import json

def generate_ego_pose_json(path, num_frames, tokens):
    poses = []
    for i in range(num_frames):
        poses.append({
            "token": tokens.get(f"ego_{i}"),
            "timestamp": f"{i * 100:08d}",
            "translation": [0.0, 0.0, 0.0],
            "rotation": [0.0, 0.0, 0.0, 1.0]
        })
    with open(path, "w") as f:
        json.dump(poses, f, indent=4)
    print("✅ ego_pose.json created")

import json

def generate_ego_pose_json(output_path, ego_pose_data, tokens):
    poses = []
    for i, pose in enumerate(ego_pose_data):
        poses.append({
            "token": tokens.get(f"ego_{i}"),
            "timestamp": pose["timestamp_ns"],
            "translation": [pose["tx_m"], pose["ty_m"], pose["tz_m"]],
            "rotation": [pose["qx"], pose["qy"], pose["qz"], pose["qw"]]
        })
    
    with open(output_path, "w") as f:
        json.dump(poses, f, indent=4)
    
    print(f"✅ {output_path} created successfully!")
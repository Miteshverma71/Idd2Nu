import json
from pathlib import Path
from typing import List, Dict, Any
from token_manager import TokenManager

def generate_ego_pose_json(
    output_path: Path,
    ego_pose_data: List[Dict[str, Any]],
    tokens: TokenManager,
    scene_number: int
):
    """
    Generate ego_pose.json for a specific scene.

    Args:
        output_path: Path to save the JSON file
        ego_pose_data: List of ego pose dictionaries
        tokens: TokenManager instance
        scene_number: Scene number for token generation
    """
    poses = []
    for i, pose in enumerate(ego_pose_data):
        poses.append({
            "token": tokens.get_or_create_ego_pose_token(scene_number, i),
            "timestamp": pose["timestamp_ns"],
            "translation": [pose["tx_m"], pose["ty_m"], pose["tz_m"]],
            "rotation": [pose["qx"], pose["qy"], pose["qz"], pose["qw"]]
        })

    # Only write to file if output_path is provided
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(poses, f, indent=4)
        print(f"✅ {output_path} created successfully!")
    
    return poses

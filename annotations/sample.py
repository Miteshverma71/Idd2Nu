import json
from pathlib import Path
from typing import List, Dict, Any
from token_manager import TokenManager

def generate_sample_json(
    output_path: Path,
    ego_pose_data: List[Dict[str, Any]],
    tokens: TokenManager,
    scene_number: int
):
    """
    Generate sample.json for a specific scene.

    Args:
        output_path: Path to save the JSON file
        ego_pose_data: List of ego pose dictionaries
        tokens: TokenManager instance
        scene_number: Scene number for token generation
    """
    samples = []
    num_frames = len(ego_pose_data)
    scene_token = tokens.get_or_create_scene_token(scene_number)

    for i, pose in enumerate(ego_pose_data):
        timestamp = pose.get("timestamp_ns", 0)
        samples.append({
            "token": tokens.get_or_create_sample_token(scene_number, i),
            "timestamp": timestamp,
            "prev": tokens.get_or_create_sample_token(scene_number, i - 1) if i > 0 else "",
            "next": tokens.get_or_create_sample_token(scene_number, i + 1) if i < num_frames - 1 else "",
            "scene_token": scene_token
        })

    # Only write to file if output_path is provided
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(samples, f, indent=4)
        print(f"✅ {output_path} created successfully!")
    
    return samples

import json
from pathlib import Path
from typing import List, Dict, Any


def generate_scene_json(
    output_path: Path,
    num_frames: int,
    tokens: 'TokenManager',
    scene_number: int = 1,
    num_scenes: int = 1
) -> List[Dict[str, Any]]:
    """
    Generate a single scene.json file with all scenes
    
    Args:
        output_path: Output path for the scene JSON file
        num_frames: Number of frames per scene
        tokens: TokenManager instance for consistent token generation
        scene_number: Starting scene number (1-based)
        num_scenes: Number of scenes to include (1-5)
        
    Returns:
        List of scene dictionaries
    """
    scenes = []
    
    for scene_idx in range(scene_number, scene_number + num_scenes):
        # Get or create tokens for this scene
        scene_token = tokens.get_or_create_scene_token(scene_idx)
        first_sample_token = tokens.get_or_create_sample_token(scene_idx, 0)
        last_sample_token = tokens.get_or_create_sample_token(scene_idx, num_frames - 1)
        
        scene_data = {
            "token": scene_token,
            "log_token": tokens.get_or_create(f"log_{scene_idx-1}"),
            "nbr_samples": num_frames,
            "first_sample_token": first_sample_token,
            "last_sample_token": last_sample_token,
            "name": f"argov2_{scene_idx}",
            "description": f"ArgoV2 scene {scene_idx} with {num_frames} samples"
        }
        scenes.append(scene_data)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write to file
    with open(output_path, "w") as f:
        json.dump(scenes, f, indent=4)
    
    print(f"✅ {output_path} created with {num_scenes} scenes")
    return scenes

import json
from pathlib import Path
from typing import List, Dict, Any
from token_manager import TokenManager

def generate_sample_annotation_json(
    output_path: Path,
    annotation_data: List[Dict[str, Any]],
    tokens: TokenManager,
    scene_number: int
):
    """
    Generate sample_annotation.json for a specific scene with proper token references.
    
    Args:
        output_path: Path to save the JSON file
        annotation_data: List of annotation dictionaries
        tokens: TokenManager instance
        scene_number: Scene number for token generation
    """
    # Category name to token key mapping
    category_mapping = {
        "BOLLARD": "cat_bollard",
        "PEDESTRIAN": "cat_ped",
        "REGULAR_VEHICLE": "cat_car",
        "BUS": "cat_bus",
        "CONSTRUCTION_CONE": "cat_cone",
        "LARGE_VEHICLE": "cat_large_vehicle",
        "SIGN": "cat_sign",
        "TRUCK_CAB": "cat_truck",
        "BICYCLE": "cat_bicycle",
        "BICYCLIST": "cat_bicyclist",
    }
    
    annotations = []
    
    for i, ann in enumerate(annotation_data):
        # Generate tokens
        annotation_token = tokens.get(f"ann_{scene_number}_{i}")
        sample_token = tokens.get_or_create_sample_token(scene_number, ann.get("frame_idx", i))
        
        # Instance token from track_uuid if available
        track_uuid = ann.get("track_uuid", "")
        instance_token = tokens.get(f"inst_{track_uuid}") if track_uuid else tokens.get("inst_default")
        
        # Category token
        category_name = ann.get("category", "")
        category_token_key = category_mapping.get(category_name, "cat_car")
        category_token = tokens.get(category_token_key)
        
        visibility_token = str((i % 4) + 1)  # Visibility tokens: 1-4
        attribute_tokens = [tokens.get("attr_moving")]  # Example attribute
        
        prev = annotations[-1]["token"] if i > 0 else ""
        next = ""
        
        annotation = {
            "token": annotation_token,
            "sample_token": sample_token,
            "instance_token": instance_token,
            "category_token": category_token,
            "visibility_token": visibility_token,
            "attribute_tokens": attribute_tokens,
            "translation": [ann["tx_m"], ann["ty_m"], ann["tz_m"]],
            "size": [ann["length_m"], ann["width_m"], ann["height_m"]],
            "rotation": [ann["qx"], ann["qy"], ann["qz"], ann["qw"]],
            "prev": prev,
            "next": next,
            "num_lidar_pts": ann.get("num_interior_pts", 0),
            "num_radar_pts": 0
        }
        
    # Update next token for previous annotation
        if i > 0:
            annotations[-1]["next"] = annotation_token
    
        annotations.append(annotation)

    # Only write to file if output_path is provided
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(annotations, f, indent=4)
        print(f"✅ {output_path} created successfully!")
    
    return annotations

import json
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any
from token_manager import TokenManager

def generate_instance_json(
    output_path: Path,
    annotation_data: List[Dict[str, Any]],
    tokens: TokenManager,
    scene_number: int
):
    """
    Generate instance.json for a specific scene.
    Creates one instance per unique track_uuid with proper category mapping.
    
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
    
    # Group annotations by track_uuid
    track_annotations = defaultdict(list)
    no_track_indices = []
    
    for i, ann in enumerate(annotation_data):
        track_uuid = ann.get("track_uuid", "")
        if track_uuid:
            track_annotations[track_uuid].append(i)
        else:
            no_track_indices.append(i)
    
    instances = []
    
    # Create instances for each unique track_uuid
    for track_uuid, annotation_indices in track_annotations.items():
        first_ann_idx = annotation_indices[0]
        category_name = annotation_data[first_ann_idx].get("category", "")
        category_token_key = category_mapping.get(category_name, "cat_car")
        
        sorted_indices = sorted(annotation_indices)
        first_idx = sorted_indices[0]
        last_idx = sorted_indices[-1]
        
        instance = {
            "token": tokens.get(f"inst_{scene_number}_{track_uuid}"),
            "category_token": tokens.get(category_token_key),
            "nbr_annotations": len(annotation_indices),
            "first_annotation_token": tokens.get(f"ann_{scene_number}_{first_idx}"),
            "last_annotation_token": tokens.get(f"ann_{scene_number}_{last_idx}")
        }
        instances.append(instance)
    
    # Handle annotations without track_uuid
    if no_track_indices:
        sorted_no_track = sorted(no_track_indices)
        first_idx = sorted_no_track[0]
        last_idx = sorted_no_track[-1]
        category_name = annotation_data[first_idx].get("category", "")
        category_token_key = category_mapping.get(category_name, "cat_car")
        
        instance = {
            "token": tokens.get(f"inst_{scene_number}_default"),
            "category_token": tokens.get(category_token_key),
            "nbr_annotations": len(no_track_indices),
            "first_annotation_token": tokens.get(f"ann_{scene_number}_{first_idx}"),
            "last_annotation_token": tokens.get(f"ann_{scene_number}_{last_idx}")
        }
        instances.append(instance)
    
    # Sort instances for consistency
    instances.sort(key=lambda x: x["token"])
    
    # Only write to file if output_path is provided
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(instances, f, indent=4)
        print(f"✅ {output_path} created with {len(instances)} instances")
    
    return instances

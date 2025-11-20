import json
from collections import defaultdict

def generate_instance_json(path, annotation_data, tokens):
    """
    Generate instance.json from annotation data.
    Creates one instance per unique track_uuid with proper category mapping.
    """
    # Category name to token key mapping (same as in sample_annotation.py)
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
    no_track_indices = []  # Annotations without track_uuid
    
    for i, ann in enumerate(annotation_data):
        track_uuid = ann.get("track_uuid", "")
        if track_uuid:
            track_annotations[track_uuid].append(i)
        else:
            no_track_indices.append(i)
    
    # Create instances for each unique track_uuid
    instances = []
    for track_uuid, annotation_indices in track_annotations.items():
        # Get category from first annotation of this track
        first_ann_idx = annotation_indices[0]
        category_name = annotation_data[first_ann_idx].get("category", "")
        category_token_key = category_mapping.get(category_name, "cat_car")
        
        # Sort annotation indices to get first and last
        sorted_indices = sorted(annotation_indices)
        first_idx = sorted_indices[0]
        last_idx = sorted_indices[-1]
        
        instance = {
            "token": tokens.get(f"inst_{track_uuid}"),
            "category_token": tokens.get(category_token_key),
            "nbr_annotations": len(annotation_indices),
            "first_annotation_token": tokens.get(f"ann_{first_idx}"),
            "last_annotation_token": tokens.get(f"ann_{last_idx}")
        }
        instances.append(instance)
    
    # Handle annotations without track_uuid (use default inst_car)
    if no_track_indices:
        sorted_no_track = sorted(no_track_indices)
        first_idx = sorted_no_track[0]
        last_idx = sorted_no_track[-1]
        # Get category from first annotation
        category_name = annotation_data[first_idx].get("category", "")
        category_token_key = category_mapping.get(category_name, "cat_car")
        
        instance = {
            "token": tokens.get("inst_car"),  # Default instance token
            "category_token": tokens.get(category_token_key),
            "nbr_annotations": len(no_track_indices),
            "first_annotation_token": tokens.get(f"ann_{first_idx}"),
            "last_annotation_token": tokens.get(f"ann_{last_idx}")
        }
        instances.append(instance)
    
    # Sort instances by track_uuid for consistency
    instances.sort(key=lambda x: x["token"])
    
    with open(path, "w") as f:
        json.dump(instances, f, indent=4)
    print(f"instance.json created with {len(instances)} instances")

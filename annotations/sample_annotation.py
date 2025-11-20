import json

def generate_sample_annotation_json(output_path, annotation_data, tokens):
    """
    Generate sample_annotation.json with proper token references.
    Maps category names to category tokens.
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
        token = tokens.get(f"ann_{i}")
        sample_token = tokens.get(f"sample_{i}")
        
        # Create instance token from track_uuid if it exists, otherwise use default
        track_uuid = ann.get("track_uuid", "")
        if track_uuid:
            instance_token = tokens.get(f"inst_{track_uuid}")
        else:
            instance_token = tokens.get("inst_car")  # Default instance
        
        # Map category name to category token
        category_name = ann.get("category", "")
        category_token_key = category_mapping.get(category_name, "cat_car")  # Default to car if unknown
        category_token = tokens.get(category_token_key)
        
        visibility_token = str((i % 4) + 1)  # Fixed: visibility has tokens 1-4, not 1-5
        attribute_tokens = [tokens.get("attr_moving")]  # Example attribute
        prev = annotations[-1]["token"] if i > 0 else ""
        next = ""

        annotation = {
            "token": token,
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

        if i > 0:
            annotations[-1]["next"] = token
        annotations.append(annotation)

    with open(output_path, "w") as f:
        json.dump(annotations, f, indent=4)
    
    print(f"Created {output_path} successfully!")



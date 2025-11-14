import os
import json

annotation_data_path = "/home/miteshv/Downloads/av2_train000_5scenes/argov2_1/new_annotations.json"

def generate_sample_annotation_json(output_path, annotation_data, tokens):
    annotations = []
    
    for i, ann in enumerate(annotation_data):
        token = tokens.get(f"ann_{i}")
        sample_token = tokens.get(f"sample_{i}")
        instance_token = ann.get("track_uuid", "")
        visibility_token = str((i % 5) + 1)
        attribute_tokens = [tokens.get("attr_moving")]  # Example attribute
        prev = annotations[-1]["token"] if i > 0 else ""
        next = ""

        annotation = {
            "token": token,
            "sample_token": sample_token,
            "instance_token": instance_token,
            "visibility_token": visibility_token,
            "attribute_tokens": attribute_tokens,
            "translation": [ann["tx_m"], ann["ty_m"], ann["tz_m"]],
            "size": [ann["length_m"], ann["width_m"], ann["height_m"]],
            "rotation": [ann["qx"], ann["qy"], ann["qz"], ann["qw"]],
            "prev": prev,
            "next": next,
            "num_lidar_pts": ann.get("num_interior_pts", 0),
            "num_radar_pts": 0,
            "timestamp": ann["timestamp_ns"],
            "category": ann["category"]
        }

        if i > 0:
            annotations[-1]["next"] = token
        annotations.append(annotation)

    with open(output_path, "w") as f:
        json.dump(annotations, f, indent=4)
    
    print(f"✅ {output_path} created successfully!")


# Load annotation data from file
with open(annotation_data_path, "r") as f:
    annotation_data = json.load(f)

# Example tokens dictionary
tokens = {
    "attr_moving": "token_attr_moving",
    **{f"ann_{i}": f"token_ann_{i}" for i in range(len(annotation_data))},
    **{f"sample_{i}": f"token_sample_{i}" for i in range(len(annotation_data))}
}

# Output path
output_path = "/home/miteshv/sample_annotation.json"

# Generate JSON
generate_sample_annotation_json(output_path, annotation_data, tokens)
import json

def generate_instance_json(path, num_frames, tokens):
    instances = [{
        "token": tokens.get("inst_car"),
        "category_token": tokens.get("cat_car"),
        "nbr_annotations": num_frames,
        "first_annotation_token": tokens.get("ann_0"),
        "last_annotation_token": tokens.get(f"ann_{num_frames-1}")
    }]
    with open(path, "w") as f:
        json.dump(instances, f, indent=4)
    print("✅ instance.json created")

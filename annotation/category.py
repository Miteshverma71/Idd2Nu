import json

def generate_category_json(path, tokens):
    cats = [
        {"token": tokens.get("cat_car"), "name": "vehicle.car", "description": "Four-wheeled car"},
        {"token": tokens.get("cat_ped"), "name": "human.pedestrian", "description": "Pedestrian"},
        {"token": tokens.get("cat_motor"), "name": "vehicle.motorcycle", "description": "Motorcycle"},
    ]
    with open(path, "w") as f:
        json.dump(cats, f, indent=4)
    print("✅ category.json created")

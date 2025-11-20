import json

def generate_category_json(path, tokens):
    """
    Generate category.json with all categories found in annotations.
    Maps to NuScenes category naming convention where possible.
    """
    cats = [
        {"token": tokens.get("cat_car"), "name": "vehicle.car", "description": "Regular vehicle (car)"},
        {"token": tokens.get("cat_ped"), "name": "human.pedestrian", "description": "Pedestrian"},
        {"token": tokens.get("cat_motor"), "name": "vehicle.motorcycle", "description": "Motorcycle"},
        {"token": tokens.get("cat_bollard"), "name": "static_object.bollard", "description": "Bollard"},
        {"token": tokens.get("cat_bus"), "name": "vehicle.bus", "description": "Bus"},
        {"token": tokens.get("cat_cone"), "name": "static_object.construction_cone", "description": "Construction cone"},
        {"token": tokens.get("cat_large_vehicle"), "name": "vehicle.large_vehicle", "description": "Large vehicle"},
        {"token": tokens.get("cat_sign"), "name": "static_object.sign", "description": "Sign"},
        {"token": tokens.get("cat_truck"), "name": "vehicle.truck", "description": "Truck cab"},
        {"token": tokens.get("cat_bicycle"), "name": "vehicle.bicycle", "description": "Bicycle"},
        {"token": tokens.get("cat_bicyclist"), "name": "human.bicyclist", "description": "Bicyclist"},
    ]
    with open(path, "w") as f:
        json.dump(cats, f, indent=4)
    print("category.json created")

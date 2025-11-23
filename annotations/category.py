def generate_category_json(output_path, tokens, return_data=False):
    """
    Generate category JSON data.
    
    Args:
        output_path: Output path for the category JSON file (can be None)
        tokens: TokenManager instance
        return_data: If True, return the data instead of writing to file
        
    Returns:
        List of category dictionaries if return_data is True or output_path is None, otherwise None
    """
    categories = [
        {
            "token": tokens.get("cat_ped"),
            "name": "pedestrian",
            "description": "Pedestrian"
        },
        {
            "token": tokens.get("cat_car"),
            "name": "vehicle",
            "description": "Regular vehicle"
        },
        {
            "token": tokens.get("cat_bus"),
            "name": "bus",
            "description": "Bus"
        },
        {
            "token": tokens.get("cat_truck"),
            "name": "truck",
            "description": "Truck"
        },
        {
            "token": tokens.get("cat_bicycle"),
            "name": "bicycle",
            "description": "Bicycle"
        },
        {
            "token": tokens.get("cat_bicyclist"),
            "name": "bicyclist",
            "description": "Bicyclist"
        },
        {
            "token": tokens.get("cat_cone"),
            "name": "cone",
            "description": "Construction cone"
        },
        {
            "token": tokens.get("cat_sign"),
            "name": "sign",
            "description": "Traffic sign"
        },
        {
            "token": tokens.get("cat_bollard"),
            "name": "bollard",
            "description": "Bollard"
        },
        {
            "token": tokens.get("cat_large_vehicle"),
            "name": "large_vehicle",
            "description": "Large vehicle"
        }
    ]
    
    # Only write to file if output_path is provided and not returning data
    if output_path is not None and not return_data:
        with open(output_path, "w") as f:
            json.dump(categories, f, indent=4)
        print(f"✅ category.json created at {output_path}")
    
    return categories if return_data or output_path is None else None

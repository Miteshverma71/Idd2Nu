def generate_map_json(path, tokens, return_data=False):
    """
    Generate map JSON data.
    
    Args:
        path: Output path for the map JSON file (can be None)
        tokens: TokenManager instance
        return_data: If True, return the data instead of writing to file
        
    Returns:
        List of map data dictionaries if return_data is True or path is None, otherwise None
    """
    map_data = [{
        "category": "semantic_prior",
        "token": tokens.get("map_token"),
        "filename": "maps/53992ee3023e5494b90c316c183be829.png",
        "log_tokens": [tokens.get("log")]
    }]
    
    # Only write to file if path is provided and not returning data
    if path is not None and not return_data:
        with open(path, "w") as f:
            json.dump(map_data, f, indent=4)
        print(f"✅ map.json created at {path}")
    
    return map_data if return_data or path is None else None

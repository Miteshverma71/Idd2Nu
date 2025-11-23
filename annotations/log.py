def generate_log_json(path, tokens, return_data=False):
    """
    Generate log JSON data.
    
    Args:
        path: Output path for the log JSON file (can be None)
        tokens: TokenManager instance
        return_data: If True, return the data instead of writing to file
        
    Returns:
        List of log dictionaries if return_data is True or path is None, otherwise None
    """
    logs = [{
        "token": tokens.get("log"),
        "logfile": "argoverse_train_000",
        "vehicle": "car",
        "location": "India",
        "date_captured": "2025-11-04"
    }]
    
    # Only write to file if path is provided and not returning data
    if path is not None and not return_data:
        with open(path, "w") as f:
            json.dump(logs, f, indent=4)
        print(f"✅ log.json created at {path}")
    
    return logs if return_data or path is None else None

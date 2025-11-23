def generate_sensor_json(path, tokens, return_data=False):
    """
    Generate sensor JSON data.
    
    Args:
        path: Output path for the sensor JSON file (can be None)
        tokens: TokenManager instance
        return_data: If True, return the sensor data instead of writing to file
        
    Returns:
        List of sensor dictionaries if return_data is True, otherwise None
    """
    sensors = []
    cam_list = [
        ("ring_front_left", "camera"),
        ("ring_front_right", "camera"),
        ("ring_front_center", "camera"),
        ("ring_rear_left", "camera"),
        ("ring_rear_right", "camera"),
        ("ring_side_left", "camera"),
        ("ring_side_right", "camera"),
        ("stereo_front_left", "camera"),
        ("stereo_front_right", "camera"),
    ]
    lidar_list = [("lidar", "lidar")]

    for name, modality in cam_list + lidar_list:
        sensors.append({
            "token": tokens.get(name),
            "channel": name,
            "modality": modality
        })

    # Only write to file if path is provided and not returning data
    if path is not None and not return_data:
        with open(path, "w") as f:
            json.dump(sensors, f, indent=4)
        print(f"✅ sensor.json created at {path}")
    
    return sensors if return_data or path is None else None

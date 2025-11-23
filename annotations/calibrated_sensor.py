def generate_calibrated_sensor_json(output_path, tokens, sensor_intrinsics, sensor_extrinsics, return_data=False):
    """
    Generate calibrated sensor JSON data.
    
    Args:
        output_path: Output path for the calibrated sensor JSON file (can be None)
        tokens: TokenManager instance
        sensor_intrinsics: List of sensor intrinsic parameters
        sensor_extrinsics: List of sensor extrinsic parameters
        return_data: If True, return the data instead of writing to file
        
    Returns:
        List of calibrated sensor dictionaries if return_data is True or output_path is None, otherwise None
    """
    # Convert extrinsics to a dict for quick lookup
    extrinsics_map = {e["sensor_name"]: e for e in sensor_extrinsics}
    
    calibrated = []
    
    for sensor in sensor_intrinsics:
        name = sensor["sensor_name"]
        token_key = f"calib_{name}"
        sensor_token = tokens.get(name)
        
        # Get extrinsics for this sensor
        extrinsic = extrinsics_map.get(name, {})
        
        # Camera
        if "ring" in name or "stereo" in name:
            camera_intrinsic = [
                [sensor["fx_px"], 0, sensor["cx_px"]],
                [0, sensor["fy_px"], sensor["cy_px"]],
                [0, 0, 1]
            ]
            
            calibrated_sensor = {
                "token": tokens.get(token_key),
                "sensor_token": sensor_token,
                "translation": [extrinsic.get("tx_m", 0.0), 
                               extrinsic.get("ty_m", 0.0), 
                               extrinsic.get("tz_m", 0.0)],
                "rotation": [extrinsic.get("qx", 0.0), 
                           extrinsic.get("qy", 0.0), 
                           extrinsic.get("qz", 0.0), 
                           extrinsic.get("qw", 1.0)],
                "camera_intrinsic": camera_intrinsic,
                "distortion": [
                    sensor.get("k1", 0.0),
                    sensor.get("k2", 0.0),
                    sensor.get("k3", 0.0)
                ],
                "resolution": [sensor.get("width_px", 0), sensor.get("height_px", 0)]
            }
            
        # LiDAR
        else:
            calibrated_sensor = {
                "token": tokens.get(token_key),
                "sensor_token": sensor_token,
                "translation": [extrinsic.get("tx_m", 0.0), 
                               extrinsic.get("ty_m", 0.0), 
                               extrinsic.get("tz_m", 0.0)],
                "rotation": [extrinsic.get("qx", 0.0), 
                           extrinsic.get("qy", 0.0), 
                           extrinsic.get("qz", 0.0), 
                           extrinsic.get("qw", 1.0)],
                "camera_intrinsic": [],
                "distortion": [],
                "resolution": []
            }
            
        calibrated.append(calibrated_sensor)
    
    # Only write to file if output_path is provided and not returning data
    if output_path is not None and not return_data:
        with open(output_path, "w") as f:
            json.dump(calibrated, f, indent=4)
        print(f"✅ calibrated_sensor.json created at {output_path}")
    
    return calibrated if return_data or output_path is None else None

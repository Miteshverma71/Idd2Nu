import json


def generate_calibrated_sensor_json(output_path, tokens, sensor_intrinsics, sensor_extrinsics):
    # Convert extrinsics to a dict for quick lookup
    extrinsics_map = {e["sensor_name"]: e for e in sensor_extrinsics}
    
    calibrated = []
    
    for sensor in sensor_intrinsics:
        name = sensor["sensor_name"]
        token_key = f"calib_{name.upper()}"
        sensor_token = tokens.get(name.upper())
        
        # Camera intrinsic matrix
        if "ring" in name or "stereo" in name:
            fx, fy = sensor["fx_px"], sensor["fy_px"]
            cx, cy = sensor["cx_px"], sensor["cy_px"]
            camera_intrinsic = [
                [fx, 0, cx],
                [0, fy, cy],
                [0, 0, 1]
            ]
        else:
            camera_intrinsic = []
        
        # Get extrinsics
        extrinsic = extrinsics_map.get(name)
        if extrinsic:
            rotation = [extrinsic["qx"], extrinsic["qy"], extrinsic["qz"], extrinsic["qw"]]
            translation = [extrinsic["tx_m"], extrinsic["ty_m"], extrinsic["tz_m"]]
        else:
            rotation = [0.0, 0.0, 0.0, 1.0]
            translation = [0.0, 0.0, 0.0]
        
        calibrated.append({
            "token": tokens.get(token_key),
            "sensor_token": sensor_token,
            "translation": translation,
            "rotation": rotation,
            "camera_intrinsic": camera_intrinsic,
            "distortion": [sensor["k1"], sensor["k2"], sensor["k3"]],
            "resolution": [sensor["width_px"], sensor["height_px"]]
        })
    
    # Add sensors that exist only in extrinsics (e.g., LIDAR)
    for name, extrinsic in extrinsics_map.items():
        if name not in [s["sensor_name"] for s in sensor_intrinsics]:
            calibrated.append({
                "token": tokens.get(f"calib_{name.upper()}"),
                "sensor_token": tokens.get(name.upper()),
                "translation": [extrinsic["tx_m"], extrinsic["ty_m"], extrinsic["tz_m"]],
                "rotation": [extrinsic["qx"], extrinsic["qy"], extrinsic["qz"], extrinsic["qw"]],
                "camera_intrinsic": [],
                "distortion": [],
                "resolution": []
            })
    
    # Save combined JSON
    with open(output_path, "w") as f:
        json.dump(calibrated, f, indent=4)
    
    print(f"✅ {output_path} created successfully!")
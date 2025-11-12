import json

def generate_calibrated_sensor_json(path, tokens):
    calibrated = []
    for name in ["CAM_FRONT", "CAM_FRONT_LEFT", "CAM_FRONT_RIGHT",
                 "CAM_BACK", "CAM_BACK_LEFT", "CAM_BACK_RIGHT", "LIDAR_TOP"]:
        calibrated.append({
            "token": tokens.get(f"calib_{name}"),
            "sensor_token": tokens.get(name),
            "translation": [0.0, 0.0, 0.0],
            "rotation": [0.0, 0.0, 0.0, 1.0],
            "camera_intrinsic": [[1000, 0, 640], [0, 1000, 360], [0, 0, 1]] if "CAM" in name else []
        })
    with open(path, "w") as f:
        json.dump(calibrated, f, indent=4)
    print("✅ calibrated_sensor.json created")

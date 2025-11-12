import json

def generate_sensor_json(path, tokens):
    sensors = []
    cam_list = [
        ("CAM_FRONT", "camera"),
        ("CAM_FRONT_LEFT", "camera"),
        ("CAM_FRONT_RIGHT", "camera"),
        ("CAM_BACK", "camera"),
        ("CAM_BACK_LEFT", "camera"),
        ("CAM_BACK_RIGHT", "camera"),
    ]
    lidar_list = [("LIDAR_TOP", "lidar")]

    for name, modality in cam_list + lidar_list:
        sensors.append({
            "token": tokens.get(name),
            "channel": name,
            "modality": modality
        })

    with open(path, "w") as f:
        json.dump(sensors, f, indent=4)
    print("✅ sensor.json created")

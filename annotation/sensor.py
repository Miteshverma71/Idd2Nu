import json

def generate_sensor_json(path, tokens):
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

    with open(path, "w") as f:
        json.dump(sensors, f, indent=4)
    print("✅ sensor.json created")

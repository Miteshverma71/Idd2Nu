import uuid
import json
import os

def generate_sensor(sensor_channels, output_dir):
    sensor_json = []
    sensor_token_map = {}

    # Define layout mapping
    layout_map = {
        "CAM_FRONT_LEFT": "cam0",
        "CAM_FRONT": "cam3",
        "CAM_FRONT_RIGHT": "cam2",
        "CAM_BACK_LEFT": "cam4",
        "CAM_BACK": "cam5",
        "CAM_BACK_RIGHT": "cam1",
        "LIDAR_TOP": "lidar_top"
    }

    for channel in sensor_channels:
        sensor_token = uuid.uuid4().hex
        sensor_token_map[channel] = sensor_token
        sensor_json.append({
            "token": sensor_token,
            "channel": channel,
            "modality": "lidar" if "LIDAR" in channel else "camera",
            "layout": layout_map.get(channel, "unknown")
        })

    with open(os.path.join(output_dir, "sensor.json"), "w") as f:
        json.dump(sensor_json, f, indent=2)

    return sensor_token_map

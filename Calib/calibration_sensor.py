import uuid
import json
import os

def generate_calibration_sensor(sensor_channels, sensor_token_map, output_dir):
    fx, fy, cx, cy = 2916, 2916, 720, 520
    calibration_sensor = []
    calib_token_map = {}

    for channel in sensor_channels:
        calib_token = uuid.uuid4().hex
        calib_token_map[channel] = calib_token
        calib_entry = {
            "token": calib_token,
            "sensor_token": sensor_token_map[channel],
            "translation": [0.0, 0.0, 1.8] if "LIDAR" in channel else [0.0, 0.0, 1.6],
            "rotation": [0.0, 0.0, 0.0, 1.0]
        }
        if "CAM" in channel:
            calib_entry["camera_intrinsic"] = [
                [fx, 0, cx],
                [0, fy, cy],
                [0, 0, 1]
            ]
        calibration_sensor.append(calib_entry)

    with open(os.path.join(output_dir, "calibration_sensor.json"), "w") as f:
        json.dump(calibration_sensor, f, indent=2)

    return calib_token_map

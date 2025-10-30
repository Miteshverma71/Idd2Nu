# frame.json

import uuid
import json
import os

def generate_sample_data(sensor_channels, sensor_token_map, calib_token_map, output_dir):
    sample_data = []
    start_timestamp = 1642482288519181237
    timestamp_step = 103258431

    for frame in range(1000, 1100):
        timestamp = start_timestamp + (frame - 1000) * timestamp_step
        for channel in sensor_channels:
            sample_token = uuid.uuid4().hex
            sample_entry_token = uuid.uuid4().hex
            sample_data.append({
                "token": sample_entry_token,
                "sample_token": sample_token,
                "calibrated_sensor_token": calib_token_map[channel],
                "timestamp": timestamp,
                "fileformat": "pcd" if "LIDAR" in channel else "jpg",
                "filename": f"{'lidar' if 'LIDAR' in channel else 'camera'}/{channel.lower()}/{frame}.{'pcd' if 'LIDAR' in channel else 'png'}",
                "is_key_frame": True,
                "next": uuid.uuid4().hex if frame < 1099 else None,
                "prev": uuid.uuid4().hex if frame > 1000 else None
            })

    with open(os.path.join(output_dir, "sample_data.json"), "w") as f:
        json.dump(sample_data, f, indent=2)
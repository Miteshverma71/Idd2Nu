import json

def generate_sample_data_json(path, num_frames, tokens):
    entries = []
    for i in range(num_frames):
        timestamp = f"{i * 100:08d}"
        for sensor_name in ["LIDAR_TOP", "CAM_FRONT", "CAM_BACK", "CAM_FRONT_LEFT",
                            "CAM_FRONT_RIGHT", "CAM_BACK_LEFT", "CAM_BACK_RIGHT"]:
            entries.append({
                "token": tokens.get(f"sd_{sensor_name}_{i}"),
                "sample_token": tokens.get(f"sample_{i}"),
                "ego_pose_token": tokens.get(f"ego_{i}"),
                "calibrated_sensor_token": tokens.get(f"calib_{sensor_name}"),
                "filename": f"{sensor_name}/{timestamp}.jpg" if "CAM" in sensor_name else f"{sensor_name}/{timestamp}.bin",
                "fileformat": "jpg" if "CAM" in sensor_name else "bin",
                "timestamp": timestamp,
                "is_key_frame": True,
                "height": 720 if "CAM" in sensor_name else 0,
                "width": 1280 if "CAM" in sensor_name else 0,
                "prev": tokens.get(f"sd_{sensor_name}_{i-1}") if i > 0 else "",
                "next": tokens.get(f"sd_{sensor_name}_{i+1}") if i < num_frames-1 else ""
            })
    with open(path, "w") as f:
        json.dump(entries, f, indent=4)
    print("✅ sample_data.json created")

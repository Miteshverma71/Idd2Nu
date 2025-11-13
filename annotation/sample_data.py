import json

ego_pose_data = "/home/miteshv/Downloads/av2_train000_5scenes/argov2_1/city_SE3_egovehicle.json"

def generate_sample_data_json(path, ego_pose_data, tokens):
    entries = []
    num_frames = len(ego_pose_data)

    for i, pose in enumerate(ego_pose_data):
        timestamp = pose["timestamp_ns"]  # Use actual timestamp from ego pose
        for sensor_name in [
            "lidar",
            "ring_front_left", "ring_front_right", "ring_front_center",
            "ring_rear_left", "ring_rear_right",
            "ring_side_left", "ring_side_right",
            "stereo_front_left", "stereo_front_right"
        ]:
            is_camera = "ring" in sensor_name or "stereo" in sensor_name
            entries.append({
                "token": tokens.get(f"sd_{sensor_name}_{i}", ""),
                "sample_token": tokens.get(f"sample_{i}", ""),
                "ego_pose_token": tokens.get(f"ego_{i}", ""),
                "calibrated_sensor_token": tokens.get(f"calib_{sensor_name}", ""),
                "filename": f"{sensor_name}/{timestamp}.jpg" if is_camera else f"{sensor_name}/{timestamp}.bin",
                "fileformat": "jpg" if is_camera else "bin",
                "timestamp": timestamp,
                "is_key_frame": True,
                "height": 1440 if is_camera else 0,  # Adjust based on actual resolution
                "width": 1080 if is_camera else 0,
                "prev": tokens.get(f"sd_{sensor_name}_{i-1}", "") if i > 0 else "",
                "next": tokens.get(f"sd_{sensor_name}_{i+1}", "") if i < num_frames - 1 else ""
            })

    with open(path, "w") as f:
        json.dump(entries, f, indent=4)

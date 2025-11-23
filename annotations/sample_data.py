def generate_sample_data_json(path, ego_pose_data, tokens, scene_number=1):
    """
    Generate sample data JSON for a specific scene
    
    Args:
        path: Output path for the sample data JSON file (can be None)
        ego_pose_data: List of ego pose data
        tokens: Dictionary containing token information
        scene_number: Scene number (1-5) for ArgoV2 scenes
        
    Returns:
        List of sample data entries
    """
    entries = []
    num_frames = len(ego_pose_data)
    scene_prefix = f"scene_{scene_number-1}_"  # scene_0_, scene_1_, etc.

    for i, pose in enumerate(ego_pose_data):
        timestamp = pose.get("timestamp_ns", 0)
        frame_number = i  # You might want to adjust this based on your timestamp
        
        for sensor_name in [
            "lidar",
            "ring_front_left", "ring_front_right", "ring_front_center",
            "ring_rear_left", "ring_rear_right",
            "ring_side_left", "ring_side_right",
            "stereo_front_left", "stereo_front_right"
        ]:
            is_camera = "ring" in sensor_name or "stereo" in sensor_name
            file_extension = "jpg" if is_camera else "bin"
            
            # Create entry with scene-specific tokens and filenames
            entries.append({
                "token": tokens.get(f"sd_{sensor_name}_{scene_number-1}_{i}"),
                "sample_token": tokens.get(f"{scene_prefix}sample_{i}"),
                "ego_pose_token": tokens.get(f"{scene_prefix}ego_{i}"),
                "calibrated_sensor_token": tokens.get(f"calib_{sensor_name}"),
                "filename": f"samples/{sensor_name}/{scene_number}_{frame_number:08d}.{file_extension}",
                "fileformat": file_extension,
                "timestamp": timestamp,
                "is_key_frame": True,
                "height": 1440 if is_camera else 0,
                "width": 1080 if is_camera else 0,
                "prev": tokens.get(f"sd_{sensor_name}_{scene_number-1}_{i-1}") if i > 0 else "",
                "next": tokens.get(f"sd_{sensor_name}_{scene_number-1}_{i+1}") if i < num_frames - 1 else ""
            })

    # Only write to file if path is provided
    if path is not None:
        # Ensure the output directory exists
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file
        with open(path, 'w') as f:
            json.dump(entries, f, indent=4)
        
        print(f"✅ Sample data JSON created at {path}")
    
    return entries

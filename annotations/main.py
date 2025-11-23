import os
import json
from pathlib import Path
from token_manager import TokenManager

# Import all generators
from sensor import generate_sensor_json
from calibrated_sensor import generate_calibrated_sensor_json
from attribute import generate_attribute_json
from category import generate_category_json
from visibility import generate_visibility_json
from log import generate_log_json
from scene import generate_scene_json
from map import generate_map_json
from ego_pose import generate_ego_pose_json
from sample import generate_sample_json
from sample_data import generate_sample_data_json
from instance import generate_instance_json
from sample_annotation import generate_sample_annotation_json


def process_scene(scene_number, base_data_dir, tokens):
    """Process a single scene with the given scene number and return its data"""
    print(f"\n🔷 Processing scene {scene_number}")
    
    # Create scene paths
    scene_data_dir = os.path.join(base_data_dir, f"argov2_{scene_number}")
    
    # Scene-specific data paths
    intrinsics_path = os.path.join(scene_data_dir, "calibration/intrinsics.json")
    extrinsics_path = os.path.join(scene_data_dir, "calibration/egovehicle_SE3_sensor.json")
    ego_pose_path = os.path.join(scene_data_dir, "new_egopose_vehicle.json")
    annotation_data_path = os.path.join(scene_data_dir, "new_annotations.json")
    
    # Load scene data
    try:
        with open(ego_pose_path, "r") as f:
            ego_pose_data = json.load(f)
        with open(annotation_data_path, "r") as f:
            annotation_data = json.load(f)
        with open(intrinsics_path, "r") as f:
            sensor_intrinsics = json.load(f)
        with open(extrinsics_path, "r") as f:
            sensor_extrinsics = json.load(f)
    except FileNotFoundError as e:
        print(f"⚠ Warning: {e} not found. Skipping scene {scene_number}.")
        return None
    
    num_frames = len(ego_pose_data)
    print(f"📌 Scene {scene_number}: {num_frames} frames detected")
    
    # Generate scene data without writing to files
    scene_data = {
        "scene": generate_scene_json(None, num_frames, tokens, scene_number),
        "ego_pose": generate_ego_pose_json(None, ego_pose_data, tokens, scene_number),
        "sample": generate_sample_json(None, ego_pose_data, tokens, scene_number),
        "sample_data": generate_sample_data_json(None, ego_pose_data, tokens, scene_number),
        "instance": generate_instance_json(None, annotation_data, tokens, scene_number),
        "sample_annotation": generate_sample_annotation_json(None, annotation_data, tokens, scene_number)
    }
    
    return {
        "scene_number": scene_number,
        "num_frames": num_frames,
        "data_dir": scene_data_dir,
        "sensor_intrinsics": sensor_intrinsics,
        "sensor_extrinsics": sensor_extrinsics,
        "scene_data": scene_data
    }


def combine_scene_data(scene_info):
    """Combine data from all scenes into a single dictionary"""
    combined = {
        'scenes': [],
        'ego_poses': [],
        'samples': [],
        'sample_data': [],
        'instances': [],
        'sample_annotations': []
    }
    
    for scene in scene_info:
        scene_data = scene['scene_data']
        combined['scenes'].extend(scene_data['scene'])
        combined['ego_poses'].extend(scene_data['ego_pose'])
        combined['samples'].extend(scene_data['sample'])
        combined['sample_data'].extend(scene_data['sample_data'])
        combined['instances'].extend(scene_data['instance'])
        combined['sample_annotations'].extend(scene_data['sample_annotation'])
    
    return combined


def main():
    # Base paths
    output_root = Path(r"C:\Users\mitvi\Downloads\argov2_00000\output")
    annotation_path = output_root / "annotation"
    base_data_dir = r"C:\Users\mitvi\Downloads\argov2_00000\argov2_00000"
    
    # Ensure output directory exists
    annotation_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize token manager
    tokens = TokenManager()
    
    # List of scene numbers to process
    scene_numbers = [1, 2, 3, 4, 5]
    
    # Process each scene
    scene_info = []
    for scene_num in scene_numbers:
        scene_data = process_scene(scene_num, base_data_dir, tokens)
        if scene_data:
            scene_info.append(scene_data)
    
    # Combine all scene data
    combined_data = combine_scene_data(scene_info)
    
    # Generate and save individual JSON files
    data_to_save = {
        'attribute': generate_attribute_json(None, tokens, return_data=True),
        'calibrated_sensor': generate_calibrated_sensor_json(
            None, tokens,
            scene_info[0]["sensor_intrinsics"] if scene_info else [],
            scene_info[0]["sensor_extrinsics"] if scene_info else [],
            return_data=True
        ),
        'category': generate_category_json(None, tokens, return_data=True),
        'ego_pose': combined_data['ego_poses'],
        'instance': combined_data['instances'],
        'log': generate_log_json(None, tokens, return_data=True),
        'map': generate_map_json(None, tokens, return_data=True),
        'sample': combined_data['samples'],
        'sample_annotation': combined_data['sample_annotations'],
        'sample_data': combined_data['sample_data'],
        'scene': combined_data['scenes'],
        'sensor': generate_sensor_json(None, tokens, return_data=True),
        'visibility': generate_visibility_json(None, return_data=True)
    }
    
    # Save each data type to a separate JSON file
    for data_type, data in data_to_save.items():
        output_file = annotation_path / f"{data_type}.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ {data_type}.json created at {output_file}")
    
    # Save token map
    tokens.save(annotation_path / "tokens_map.json")
    
    print("\n🎯 All data saved in separate JSON files!")
    print(f"Processed {len(scene_info)} scenes out of {len(scene_numbers)}.")


if __name__ == "__main__":
    main()

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
from scene import generate_scene_json, generate_scenes_json
from map import generate_map_json
from ego_pose import generate_ego_pose_json
from sample import generate_sample_json
from sample_data import generate_sample_data_json
from instance import generate_instance_json
from sample_annotation import generate_sample_annotation_json

def process_scene(scene_number, base_data_dir, annotation_path, tokens):
    """Process a single scene with the given scene number"""
    print(f"\n🔷 Processing scene {scene_number}")
    
    # Create scene-specific paths
    scene_data_dir = os.path.join(base_data_dir, f"argov2_{scene_number}")
    scene_annotation_path = os.path.join(annotation_path, f"scene_{scene_number}")
    os.makedirs(scene_annotation_path, exist_ok=True)
    
    # Scene-specific data paths
    intrinsics_path = os.path.join(scene_data_dir, "intrinsics.json")
    extrinsics_path = os.path.join(scene_data_dir, "egovehicle_SE3_sensor.json")
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
    
    # Generate scene-specific JSON files
    scene_tokens = {}
    
    # Generate scene.json for this scene
    scene_json_path = os.path.join(scene_annotation_path, "scene.json")
    generate_scene_json(scene_json_path, num_frames, tokens, scene_number)
    
    # Generate other JSON files for this scene
    generate_ego_pose_json(
        os.path.join(scene_annotation_path, "ego_pose.json"),
        ego_pose_data,
        tokens,
        scene_number=scene_number
    )
    
    generate_sample_json(
        os.path.join(scene_annotation_path, "sample.json"),
        ego_pose_data,
        tokens,
        scene_number=scene_number
    )
    
    generate_sample_data_json(
        os.path.join(scene_annotation_path, "sample_data.json"),
        ego_pose_data,
        tokens,
        scene_number=scene_number
    )
    
    generate_instance_json(
        os.path.join(scene_annotation_path, "instance.json"),
        annotation_data,
        tokens,
        scene_number=scene_number
    )
    
    generate_sample_annotation_json(
        os.path.join(scene_annotation_path, "sample_annotation.json"),
        annotation_data,
        tokens,
        scene_number=scene_number
    )
    
    return {
        "scene_number": scene_number,
        "num_frames": num_frames,
        "data_dir": scene_data_dir,
        "annotation_dir": scene_annotation_path,
        "sensor_intrinsics": sensor_intrinsics,
        "sensor_extrinsics": sensor_extrinsics
    }

def main():
    # Base paths
    output_root = Path(__file__).parent.parent / "output"
    annotation_path = output_root / "annotation"
    data_dir = Path(__file__).parent.parent / "data"
    
    # Ensure output directory exists
    annotation_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize token manager
    tokens = TokenManager()
    
    # List of scene numbers to process
    scene_numbers = [1, 2, 3, 4, 5]  # You can modify this list to include any scene numbers in any order
    
    # Process each scene
    scene_info = []
    for scene_num in scene_numbers:
        scene_data = process_scene(scene_num, data_dir, annotation_path, tokens)
        if scene_data:
            scene_info.append(scene_data)
    
    # Generate common JSON files (only once)
    print("\n🔷 Generating common JSON files")
    generate_sensor_json(annotation_path / "sensor.json", tokens)
    generate_calibrated_sensor_json(
        annotation_path / "calibrated_sensor.json",
        tokens,
        scene_info[0]["sensor_intrinsics"] if scene_info else {},
        scene_info[0]["sensor_extrinsics"] if scene_info else {}
    )
    generate_attribute_json(annotation_path / "attribute.json", tokens)
    generate_category_json(annotation_path / "category.json", tokens)
    generate_visibility_json(annotation_path / "visibility.json")
    generate_log_json(annotation_path / "log.json", tokens)
    generate_map_json(annotation_path / "map.json", tokens)
    
    # Generate combined scenes.json
    if scene_info:
        generate_scenes_json(
            annotation_path,
            len(scene_info),
            scene_info[0]["num_frames"],  # Assuming all scenes have same number of frames
            tokens
        )
    
    # Save token map
    with open(annotation_path / "tokens_map.json", "w") as f:
        json.dump(tokens.tokens, f, indent=4)
    
    print("\n🎯 All JSONs generated successfully!")
    print(f"Processed {len(scene_info)} scenes out of {num_scenes}.")

if __name__ == "__main__":
    main()
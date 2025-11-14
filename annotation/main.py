import os
import json
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

# Paths
output_root = "/home/miteshv/Downloads/argov2"
annotation_path = os.path.join(output_root, "annotation")
os.makedirs(annotation_path, exist_ok=True)

# Input data paths
intrinsics_path = "/home/miteshv/Downloads/av2_train000_5scenes/argov2_1/calibration/intrinsics.json"
extrinsics_path = "/home/miteshv/Downloads/av2_train000_5scenes/argov2_1/calibration/egovehicle_SE3_sensor.json"
ego_pose_data = "/home/miteshv/Downloads/av2_train000_5scenes/argov2_1/new_egopose_vehicle.json"
annotation_data_path = "/home/miteshv/Downloads/av2_train000_5scenes/argov2_1/new_annotations.json"

# Token manager
tokens = TokenManager()

# Load required data
with open(intrinsics_path, "r") as f:
    sensor_intrinsics = json.load(f)
with open(extrinsics_path, "r") as f:
    sensor_extrinsics = json.load(f)
with open(ego_pose_data, "r") as f:
    ego_pose_data = json.load(f)
with open(annotation_data_path, "r") as f:
    annotation_data = json.load(f)

# Calculate number of frames dynamically
num_frames = len(ego_pose_data)
print(f"📌 Total frames detected: {num_frames}")

# Validate timestamps
timestamps = [pose.get("timestamp_ns") for pose in ego_pose_data if "timestamp_ns" in pose]
if len(timestamps) != num_frames:
    print("⚠ Warning: Some ego poses are missing timestamp_ns!")
else:
    print(f"✅ Timestamps range: {min(timestamps)} → {max(timestamps)}")

# Generate JSON files
generate_sensor_json(os.path.join(annotation_path, "sensor.json"), tokens)
generate_calibrated_sensor_json(os.path.join(annotation_path, "calibrated_sensor.json"), tokens, sensor_intrinsics, sensor_extrinsics)
generate_attribute_json(os.path.join(annotation_path, "attribute.json"), tokens)
generate_category_json(os.path.join(annotation_path, "category.json"), tokens)
generate_visibility_json(os.path.join(annotation_path, "visibility.json"))
generate_log_json(os.path.join(annotation_path, "log.json"), tokens)
generate_scene_json(os.path.join(annotation_path, "scene.json"), num_frames, tokens)
generate_map_json(os.path.join(annotation_path, "map.json"), tokens)
generate_ego_pose_json(os.path.join(annotation_path, "ego_pose.json"), ego_pose_data, tokens)
generate_sample_json(os.path.join(annotation_path, "sample.json"), ego_pose_data, tokens)
generate_sample_data_json(os.path.join(annotation_path, "sample_data.json"), ego_pose_data, tokens)
generate_instance_json(os.path.join(annotation_path, "instance.json"), num_frames, tokens)
generate_sample_annotation_json(os.path.join(annotation_path, "sample_annotation.json"), annotation_data, tokens)

# Save token map
with open(os.path.join(annotation_path, "tokens_map.json"), "w") as f:
    json.dump(tokens.tokens, f, indent=4)

print("✅ tokens_map.json saved")
print("\n🎯 All JSONs generated successfully.")
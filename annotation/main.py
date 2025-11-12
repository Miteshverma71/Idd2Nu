import os
import json
from tokens_manager import TokenManager

from sensors import generate_sensor_json
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
from sample_annotation import generate_sample_annotation_json_from_label_folder

root_folder = "/home/miteshv/Downloads/idd3d/idd3d_seq_10"
output_root = "/home/miteshv/Downloads/idd3d/idd2nuscenes"
annotation_path = os.path.join(output_root, "annotation")
os.makedirs(annotation_path, exist_ok=True)

tokens = TokenManager()
num_frames = 100

generate_sensor_json(os.path.join(annotation_path, "sensor.json"), tokens)
generate_calibrated_sensor_json(os.path.join(annotation_path, "calibrated_sensor.json"), tokens)
generate_attribute_json(os.path.join(annotation_path, "attribute.json"), tokens)
generate_category_json(os.path.join(annotation_path, "category.json"), tokens)
generate_visibility_json(os.path.join(annotation_path, "visibility.json"))
generate_log_json(os.path.join(annotation_path, "log.json"), tokens)
generate_scene_json(os.path.join(annotation_path, "scene.json"), num_frames, tokens)
generate_map_json(os.path.join(annotation_path, "map.json"), tokens)
generate_ego_pose_json(os.path.join(annotation_path, "ego_pose.json"), num_frames, tokens)
generate_sample_json(os.path.join(annotation_path, "sample.json"), num_frames, tokens)
generate_sample_data_json(os.path.join(annotation_path, "sample_data.json"), num_frames, tokens)
generate_instance_json(os.path.join(annotation_path, "instance.json"), num_frames, tokens)

label_folder = "/home/miteshv/Downloads/idd3d/labels"
generate_sample_annotation_json_from_label_folder(label_folder, annotation_path, tokens)

with open(os.path.join(annotation_path, "tokens_map.json"), "w") as f:
    json.dump(tokens.tokens, f, indent=4)
print("✅ tokens_map.json saved")
print("\n🎯 All JSONs generated successfully.")

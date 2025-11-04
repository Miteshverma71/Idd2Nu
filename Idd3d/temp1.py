import os
import json
import uuid
from PIL import Image

# ============================================================
# CONFIGURATION
# ============================================================

root_folder = "/home/miteshv/Downloads/idd3d/idd3d_seq_10"
output_root = "/home/miteshv/Downloads/idd3d/idd2nuscenes"
annotation_path = os.path.join(output_root, "annotation")
os.makedirs(annotation_path, exist_ok=True)

# ============================================================
# TOKEN MANAGER — All tokens synchronized
# ============================================================

class TokenManager:
    def __init__(self):
        self.tokens = {}
    def get(self, name):
        if name not in self.tokens:
            self.tokens[name] = uuid.uuid4().hex
        return self.tokens[name]

tokens = TokenManager()

# ============================================================
# 1️⃣ SENSOR DEFINITIONS
# ============================================================

def generate_sensor_json(path):
    sensors = []
    cam_list = [
        ("CAM_FRONT", "camera"),
        ("CAM_FRONT_LEFT", "camera"),
        ("CAM_FRONT_RIGHT", "camera"),
        ("CAM_BACK", "camera"),
        ("CAM_BACK_LEFT", "camera"),
        ("CAM_BACK_RIGHT", "camera"),
    ]
    lidar_list = [("LIDAR_TOP", "lidar")]

    for name, modality in cam_list + lidar_list:
        sensors.append({
            "token": tokens.get(name),
            "channel": name,
            "modality": modality
        })

    with open(path, "w") as f:
        json.dump(sensors, f, indent=4)
    print("✅ sensor.json created")

# ============================================================
# 2️⃣ CALIBRATED SENSOR
# ============================================================

def generate_calibrated_sensor_json(path):
    calibrated = []
    for name in ["CAM_FRONT", "CAM_FRONT_LEFT", "CAM_FRONT_RIGHT",
                 "CAM_BACK", "CAM_BACK_LEFT", "CAM_BACK_RIGHT", "LIDAR_TOP"]:
        calibrated.append({
            "token": tokens.get(f"calib_{name}"),
            "sensor_token": tokens.get(name),
            "translation": [0.0, 0.0, 0.0],
            "rotation": [0.0, 0.0, 0.0, 1.0],
            "camera_intrinsic": [[1000, 0, 640], [0, 1000, 360], [0, 0, 1]] if "CAM" in name else []
        })

    with open(path, "w") as f:
        json.dump(calibrated, f, indent=4)
    print("✅ calibrated_sensor.json created")

# ============================================================
# 3️⃣ ATTRIBUTE & CATEGORY
# ============================================================

def generate_attribute_json(path):
    attrs = [
        {"token": tokens.get("attr_moving"), "name": "vehicle.moving", "description": "Moving vehicle"},
        {"token": tokens.get("attr_stopped"), "name": "vehicle.stopped", "description": "Stopped vehicle"}
    ]
    with open(path, "w") as f:
        json.dump(attrs, f, indent=4)
    print("✅ attribute.json created")

def generate_category_json(path):
    cats = [
        {"token": tokens.get("cat_car"), "name": "vehicle.car", "description": "Four-wheeled car"},
        {"token": tokens.get("cat_ped"), "name": "human.pedestrian", "description": "Pedestrian"},
        {"token": tokens.get("cat_motor"), "name": "vehicle.motorcycle", "description": "Motorcycle"},
    ]
    with open(path, "w") as f:
        json.dump(cats, f, indent=4)
    print("✅ category.json created")

# ============================================================
# 4️⃣ LOG & SCENE
# ============================================================

def generate_log_json(path):
    logs = [{
        "token": tokens.get("log"),
        "logfile": "idd_seq_010",
        "vehicle": "car",
        "location": "India",
        "date_captured": "2025-11-04"
    }]
    with open(path, "w") as f:
        json.dump(logs, f, indent=4)
    print("✅ log.json created")

def generate_scene_json(path, num_frames):
    scenes = [{
        "token": tokens.get("scene"),
        "log_token": tokens.get("log"),
        "nbr_samples": num_frames,
        "first_sample_token": tokens.get("sample_0"),
        "last_sample_token": tokens.get(f"sample_{num_frames-1}"),
        "name": "sequence-010",
        "description": "Daytime drive with 10Hz capture"
    }]
    with open(path, "w") as f:
        json.dump(scenes, f, indent=4)
    print("✅ scene.json created")

# ============================================================
# 5️⃣ SAMPLE + SAMPLE_DATA + ANNOTATION
# ============================================================

def generate_sample_json(path, num_frames):
    step_ms = 100
    samples = []
    for i in range(num_frames):
        timestamp = f"{i * step_ms:08d}"
        samples.append({
            "token": tokens.get(f"sample_{i}"),
            "timestamp": timestamp,
            "prev": tokens.get(f"sample_{i-1}") if i > 0 else "",
            "next": tokens.get(f"sample_{i+1}") if i < num_frames-1 else "",
            "scene_token": tokens.get("scene"),
        })
    with open(path, "w") as f:
        json.dump(samples, f, indent=4)
    print("✅ sample.json created")

def generate_sample_data_json(path, num_frames):
    entries = []
    step_ms = 100
    for i in range(num_frames):
        timestamp = f"{i * step_ms:08d}"
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

def generate_sample_annotation_json(path, num_frames):
    annotations = []
    for i in range(num_frames):
        annotations.append({
            "token": tokens.get(f"ann_{i}"),
            "sample_token": tokens.get(f"sample_{i}"),
            "instance_token": tokens.get(f"inst_car"),
            "attribute_tokens": [tokens.get("attr_moving")],
            "category_token": tokens.get("cat_car"),
            "translation": [0, 0, 0],
            "size": [4.0, 1.8, 1.5],
            "rotation": [0, 0, 0, 1],
            "num_lidar_pts": 100,
            "num_radar_pts": 0
        })
    with open(path, "w") as f:
        json.dump(annotations, f, indent=4)
    print("✅ sample_annotation.json created")

# ============================================================
# 6️⃣ EGO POSE
# ============================================================

def generate_ego_pose_json(path, num_frames):
    poses = []
    for i in range(num_frames):
        poses.append({
            "token": tokens.get(f"ego_{i}"),
            "timestamp": f"{i * 100:08d}",
            "translation": [0.0, 0.0, 0.0],
            "rotation": [0.0, 0.0, 0.0, 1.0]
        })
    with open(path, "w") as f:
        json.dump(poses, f, indent=4)
    print("✅ ego_pose.json created")

# ============================================================
# 7️⃣ INSTANCE
# ============================================================

def generate_instance_json(path, num_frames):
    instances = [{
        "token": tokens.get("inst_car"),
        "category_token": tokens.get("cat_car"),
        "nbr_annotations": num_frames,
        "first_annotation_token": tokens.get("ann_0"),
        "last_annotation_token": tokens.get(f"ann_{num_frames-1}")
    }]
    with open(path, "w") as f:
        json.dump(instances, f, indent=4)
    print("✅ instance.json created")

# ============================================================
# MAIN EXECUTION
# ============================================================

num_frames = 100  # You can dynamically count from folder later

generate_sensor_json(os.path.join(annotation_path, "sensor.json"))
generate_calibrated_sensor_json(os.path.join(annotation_path, "calibrated_sensor.json"))
generate_attribute_json(os.path.join(annotation_path, "attribute.json"))
generate_category_json(os.path.join(annotation_path, "category.json"))
generate_log_json(os.path.join(annotation_path, "log.json"))
generate_ego_pose_json(os.path.join(annotation_path, "ego_pose.json"), num_frames)
generate_sample_json(os.path.join(annotation_path, "sample.json"), num_frames)
generate_sample_data_json(os.path.join(annotation_path, "sample_data.json"), num_frames)
generate_sample_annotation_json(os.path.join(annotation_path, "sample_annotation.json"), num_frames)
generate_instance_json(os.path.join(annotation_path, "instance.json"), num_frames)
generate_scene_json(os.path.join(annotation_path, "scene.json"), num_frames)

# Save token map for reference
with open(os.path.join(annotation_path, "tokens_map.json"), "w") as f:
    json.dump(tokens.tokens, f, indent=4)
print("✅ tokens_map.json saved")

print("\n🎯 All JSONs generated successfully with synchronized tokens and timestamps.")

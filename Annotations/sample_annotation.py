#object.json

import uuid
import json
import os

def generate_sample_annotation(output_dir):
    sample_annotation = []
    for frame in range(1000, 1100):
        token = uuid.uuid4().hex
        sample_token = uuid.uuid4().hex
        prev_token = uuid.uuid4().hex if frame > 1000 else None
        next_token = uuid.uuid4().hex if frame < 1099 else None
        sample_annotation.append({
            "token": token,
            "sample_token": sample_token,
            "translation": [373.214, 1130.48, 1.25],
            "size": [0.621, 0.669, 1.642],
            "rotation": [0.9831098797903927, 0.0, 0.0, -0.18301629506281616],
            "prev": prev_token,
            "next": next_token,
            "num_lidar_pts": 5,
            "num_radar_pts": 0
        })

    with open(os.path.join(output_dir, "sample_annotation.json"), "w") as f:
        json.dump(sample_annotation, f, indent=2)
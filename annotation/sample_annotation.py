import os
import json

def generate_sample_annotation_json_from_label_folder(label_folder, output_folder, tokens, num_entries=10):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(label_folder):
        if filename.endswith('.json'):
            input_path = os.path.join(label_folder, filename)
            output_path = os.path.join(output_folder, f"sample_annotation_{filename}")

            with open(input_path, 'r') as f:
                label_data = json.load(f)

            psr = label_data.get('psr', {})
            position = psr.get('position', {"x": 0, "y": 0, "z": 0})
            scale = psr.get('scale', {"x": 1, "y": 1, "z": 1})
            rotation = psr.get('rotation', {"x": 0, "y": 0, "z": 0})

            translation = [position['x'], position['y'], position['z']]
            size = [scale['x'], scale['y'], scale['z']]
            rotation_list = [rotation['x'], rotation['y'], rotation['z']]

            annotations = []
            for i in range(num_entries):
                token = tokens.get(f"ann_{filename}_{i}")
                sample_token = tokens.get(f"sample_{i}")
                instance_token = tokens.get("inst_car")
                visibility_token = str((i % 5) + 1)
                attribute_tokens = [tokens.get("attr_moving")]
                prev = annotations[-1]["token"] if i > 0 else ""
                next = ""

                annotation = {
                    "token": token,
                    "sample_token": sample_token,
                    "instance_token": instance_token,
                    "visibility_token": visibility_token,
                    "attribute_tokens": attribute_tokens,
                    "translation": translation,
                    "size": size,
                    "rotation": rotation_list,
                    "prev": prev,
                    "next": next,
                    "num_lidar_pts": 5 + i,
                    "num_radar_pts": i
                }

                if i > 0:
                    annotations[-1]["next"] = token
                annotations.append(annotation)

            with open(output_path, 'w') as f:
                json.dump(annotations, f, indent=4)
            print(f"✅ Created: {output_path}")

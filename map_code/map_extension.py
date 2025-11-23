import json
import uuid
from pathlib import Path
import argparse


def new_token():
    return str(uuid.uuid4())


def convert_xyz_to_nodes(coords, nodes):
    """Convert XYZ points to node tokens with full nuScenes node format."""
    tokens = []
    for pt in coords:
        token = new_token()
        nodes.append({
            "token": token,
            "x": pt["x"],
            "y": pt["y"],
            "z": pt.get("z", 0.0)
        })
        tokens.append(token)
    return tokens


def convert_lane_segment(seg, nodes):
    left = convert_xyz_to_nodes(seg["left_lane_boundary"], nodes)
    right = convert_xyz_to_nodes(seg["right_lane_boundary"], nodes)

    return {
        "token": new_token(),
        "lane_type": seg.get("lane_type", "NONE"),
        "left_boundary": left,
        "right_boundary": right,
        "predecessors": seg.get("predecessors", []),
        "successors": seg.get("successors", []),
        "left_neighbor": seg.get("left_neighbor_id"),
        "right_neighbor": seg.get("right_neighbor_id"),
        "is_intersection": seg.get("is_intersection", False)
    }


def convert_ped_crossing(pc, nodes):
    edge1 = convert_xyz_to_nodes(pc["edge1"], nodes)
    edge2 = convert_xyz_to_nodes(pc["edge2"], nodes)

    return {
        "token": new_token(),
        "edge1": edge1,
        "edge2": edge2
    }


def convert_drivable_area(area, nodes):
    if "polygon" not in area:
        return None
    poly = convert_xyz_to_nodes(area["polygon"], nodes)
    return {
        "token": new_token(),
        "polygon": poly
    }


def convert_scene_to_nuscenes(scene_path, output_path):

    print("Loading scene map:", scene_path)
    with open(scene_path, "r") as f:
        d2 = json.load(f)

    # new nuScenes-style structure
    out = {
        "node": [],
        "lane": [],
        "ped_crossing": [],
        "drivable_area": [],
        "polygon": [],
        "line": [],
        "road_segment": [],
        "road_block": [],
        "walkway": [],
        "stop_line": [],
        "carpark_area": [],
        "road_divider": [],
        "lane_divider": [],
        "traffic_light": [],
        "lane_connector": [],
        "connectivity": {},
        "arcline_path_3": {},
        "canvas_edge": [0, 0],
        "version": "1.0"
    }

    nodes = out["node"]

    # ---- convert lanes ----
    for seg_id, seg in d2.get("lane_segments", {}).items():
        out["lane"].append(convert_lane_segment(seg, nodes))

    # ---- convert pedestrian crossings ----
    for cid, c in d2.get("pedestrian_crossings", {}).items():
        out["ped_crossing"].append(convert_ped_crossing(c, nodes))

    # ---- convert drivable areas ----
    for did, da in d2.get("drivable_areas", {}).items():
        conv = convert_drivable_area(da, nodes)
        if conv:
            out["drivable_area"].append(conv)

    print("Writing converted nuScenes map:", output_path)
    with open(output_path, "w") as f:
        json.dump(out, f, indent=2)

    print("✔ Done — dataset2 converted into nuScenes format.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert dataset2 → nuScenes map format")

    # Use raw string (r-prefix) for Windows paths
    default_scene_path = r"C:\Users\mitvi\Downloads\argov2_00000\argov2_00000\argov2_1\map\map_log_scene1.json"
    
    parser.add_argument(
        "--scene_map",
        type=str,
        default=default_scene_path,
        help="Path to dataset2 scene map"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="converted_nuscenes_map.json",
        help="Output nuScenes map file"
    )

    args = parser.parse_args()
    
    # Convert to Path objects after parsing
    scene_path = Path(args.scene_map).resolve()
    output_path = Path(args.output).resolve()
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    convert_scene_to_nuscenes(str(scene_path), str(output_path))


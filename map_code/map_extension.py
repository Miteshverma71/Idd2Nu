import json
import uuid
from pathlib import Path
import argparse


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def new_token():
    return str(uuid.uuid4())


def convert_xyz_to_nodes(coords, node_list):
    tokens = []
    for pt in coords:
        tok = new_token()
        node_list.append({
            "token": tok,
            "x": float(pt["x"]),
            "y": float(pt["y"]),
            "z": float(pt.get("z", 0.0))
        })
        tokens.append(tok)
    return tokens


# ---------------------------------------------------------
# Converters for dataset2 categories
# ---------------------------------------------------------

def convert_lane_segment(seg, node_list):
    left_tokens = convert_xyz_to_nodes(seg["left_lane_boundary"], node_list)
    right_tokens = convert_xyz_to_nodes(seg["right_lane_boundary"], node_list)

    return {
        "token": new_token(),
        "lane_type": seg.get("lane_type", "NONE"),
        "left_boundary": left_tokens,
        "right_boundary": right_tokens,
        "predecessors": seg.get("predecessors", []),
        "successors": seg.get("successors", []),
        "left_neighbor": seg.get("left_neighbor_id"),
        "right_neighbor": seg.get("right_neighbor_id"),
        "is_intersection": seg.get("is_intersection", False)
    }


def convert_ped_crossing(pc, node_list):
    edge1 = convert_xyz_to_nodes(pc["edge1"], node_list)
    edge2 = convert_xyz_to_nodes(pc["edge2"], node_list)

    return {
        "token": new_token(),
        "edge1": edge1,
        "edge2": edge2
    }


# ---------------------------------------------------------
# Dummy placeholder generators
# ---------------------------------------------------------

def placeholder_polygon():
    return {
        "token": new_token(),
        "exterior_node_tokens": [],
        "interior_node_tokens": []
    }


def placeholder_line():
    return {
        "token": new_token(),
        "node_tokens": []
    }


def placeholder_generic_polygon_token():
    return {
        "token": new_token(),
        "polygon_token": None
    }


def placeholder_empty():
    return {"token": new_token()}


# ---------------------------------------------------------
# Convert a single scene to nuScenes format
# ---------------------------------------------------------

def convert_scene(scene_path):
    print(f"Converting scene: {scene_path}")

    with open(scene_path, "r") as f:
        d2 = json.load(f)

    out = {
        "node": [],
        "lane": [],
        "ped_crossing": [],
        "drivable_area": []
    }

    nodes = out["node"]

    # lane_segments → lane
    for seg_id, seg in d2.get("lane_segments", {}).items():
        out["lane"].append(convert_lane_segment(seg, nodes))

    # pedestrian_crossings → ped_crossing
    for cid, c in d2.get("pedestrian_crossings", {}).items():
        out["ped_crossing"].append(convert_ped_crossing(c, nodes))

    # drivable_areas → drivable_area
    for aid, area in d2.get("drivable_areas", {}).items():
        if "polygon" in area:
            poly_tokens = convert_xyz_to_nodes(area["polygon"], nodes)
            out["drivable_area"].append({
                "token": new_token(),
                "polygon": poly_tokens
            })

    return out


# ---------------------------------------------------------
# Merge 5 scenes
# ---------------------------------------------------------

def merge_scenes(scene_paths, output_path):

    final_out = {
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

    # Process each scene
    for scene in scene_paths:
        scene_out = convert_scene(scene)

        final_out["node"].extend(scene_out["node"])
        final_out["lane"].extend(scene_out["lane"])
        final_out["ped_crossing"].extend(scene_out["ped_crossing"])
        final_out["drivable_area"].extend(scene_out["drivable_area"])

    # Add placeholders (minimal)
    if len(final_out["polygon"]) == 0:
        final_out["polygon"].append(placeholder_polygon())

    if len(final_out["line"]) == 0:
        final_out["line"].append(placeholder_line())

    if len(final_out["road_segment"]) == 0:
        final_out["road_segment"].append(placeholder_generic_polygon_token())

    if len(final_out["road_block"]) == 0:
        final_out["road_block"].append(placeholder_generic_polygon_token())

    if len(final_out["walkway"]) == 0:
        final_out["walkway"].append(placeholder_generic_polygon_token())

    if len(final_out["stop_line"]) == 0:
        final_out["stop_line"].append(placeholder_line())

    if len(final_out["carpark_area"]) == 0:
        final_out["carpark_area"].append(placeholder_generic_polygon_token())

    if len(final_out["road_divider"]) == 0:
        final_out["road_divider"].append(placeholder_line())

    if len(final_out["lane_divider"]) == 0:
        final_out["lane_divider"].append(placeholder_line())

    if len(final_out["traffic_light"]) == 0:
        final_out["traffic_light"].append(placeholder_empty())

    if len(final_out["lane_connector"]) == 0:
        final_out["lane_connector"].append(placeholder_generic_polygon_token())

    # Save merged output
    print("Writing merged map:", output_path)
    with open(output_path, "w") as f:
        json.dump(final_out, f, indent=2)

    print("✔ All 5 scenes merged successfully!")


# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge 5 scenes → one nuScenes map")

    parser.add_argument(
        "--base_folder",
        type=str,
        default=r"C:\Users\mitvi\Downloads\argov2_00000\argov2_00000",
        help="Base folder containing argov2_1 ... argov2_5"
    )

    parser.add_argument(
        "--output",
        type=str,
        default=r"C:\Users\mitvi\Downloads\merged_nuscenes_map.json",
        help="Output merged nuScenes map file"
    )

    args = parser.parse_args()

    base = Path(args.base_folder)

    # expected scene files
    scene_paths = [
        base / f"argov2_{i}" / "map" / f"map_log_scene{i}.json"
        for i in [1, 2, 3, 4, 5]
    ]

    # verify
    for p in scene_paths:
        if not p.exists():
            raise FileNotFoundError(f"Scene file missing: {p}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    merge_scenes([str(p) for p in scene_paths], str(output_path))

import json
import csv
from pathlib import Path
from typing import List, Dict, Any
import numpy as np

def read_csv_timestamps(csv_path: str) -> List[int]:
    """Read timestamps from CSV file."""
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        return [int(row[0]) for row in reader if row]

def process_can_file(input_path: str, output_path: str, timestamps: List[int]):
    """Process a single CAN file to update timestamps and trim entries."""
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  Error parsing JSON in {input_path} - {e}")
        return

    if not data:
        return

    if isinstance(data, list) and data and isinstance(data[0], dict) and "utime" in data[0]:
        original_len = len(data)
        data = data[:len(timestamps)]
        for i, entry in enumerate(data):
            entry["utime"] = timestamps[i]
        print(f"  Processed {len(data)}/{original_len} entries")

    elif isinstance(data, dict) and "message_count" in str(data):
        print("  Skipping meta file")
    else:
        print(f"  Unsupported format: {input_path}")
        return

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

def calculate_stats(values: List[float]) -> Dict[str, float]:
    """Calculate statistics for a list of values."""
    if not values:
        return {}

    values = np.array(values, dtype=np.float64)
    diffs = np.diff(values) if len(values) > 1 else [0]

    return {
        "max": float(np.max(values)),
        "min": float(np.min(values)),
        "mean": float(np.mean(values)),
        "std": float(np.std(values)),
        "max_diff": float(np.max(np.abs(diffs))) if len(diffs) > 0 else 0.0,
        "mean_diff": float(np.mean(np.abs(diffs))) if len(diffs) > 0 else 0.0,
        "min_diff": float(np.min(np.abs(diffs))) if len(diffs) > 0 else 0.0,
        "std_diff": float(np.std(np.abs(diffs))) if len(diffs) > 0 else 0.0
    }

def update_meta_file(meta_path: Path, data_dir: Path):
    """Update meta.json with statistics from other CAN files."""
    with open(meta_path, "r") as f:
        meta = json.load(f)

    # Extract scene number (e.g., "0001" from "scene-0001_meta.json")
    scene_num = meta_path.stem.split('_')[0].split('-')[-1]
    
    file_patterns = {
        f"scene-{scene_num}_ms_imu.json": "MS_IMU",
        f"scene-{scene_num}_pose.json": "POSE",
        f"scene-{scene_num}_route.json": "ROUTE",
        f"scene-{scene_num}_steeranglefeedback.json": "STEER_ANGLE_FEEDBACK",
        f"scene-{scene_num}_vehicle_monitor.json": "VEHICLE_MONITOR",
        f"scene-{scene_num}_zoe_veh_info.json": "ZOE_VEH_INFO",
        f"scene-{scene_num}_zoesensors.json": "ZoeSensors"
    }

    for file_path, meta_key in file_patterns.items():
        full_path = data_dir / file_path
        if not full_path.exists():
            print(f"  Missing: {file_path}")
            continue

        try:
            with open(full_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"  Bad JSON in {file_path}")
            continue

        if not isinstance(data, list) or not data:
            continue

        # Calculate timespan and frequency
        if len(data) > 1 and 'utime' in data[0]:
            timespan = (data[-1]['utime'] - data[0]['utime']) / 1e6
            freq = len(data) / timespan if timespan > 0 else 0
        else:
            timespan = 0
            freq = 0

        stats = {
            "message_count": len(data),
            "timespan": timespan,
            "message_freq": freq,
            "var_stats": {}
        }

        # Calculate statistics for each field
        fields = {}
        for entry in data:
            for key, value in entry.items():
                if key == 'utime' or not isinstance(value, (int, float)):
                    continue
                fields.setdefault(key, []).append(value)

        for field, values in fields.items():
            if len(values) > 1:  # Need at least 2 values for meaningful stats
                stats["var_stats"][field] = calculate_stats(values)

        meta[meta_key] = stats

    # Save updated meta file
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    print("  Meta file updated")

def main():
    base_dir = Path(r"C:\Users\mitvi\Downloads\argov2_00000")
    canbus_temp = base_dir / "canbus_temp"
    output_dir = base_dir / "output" / "canbus"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each scene (1-5)
    for scene in range(1, 6):
        print(f"\n=== Processing Scene {scene} ===")
        
        # For all scenes, use canbus_temp as the source
        source_dir = canbus_temp
        
        # Path to CSV with timestamps
        csv_path = base_dir / "argov2_00000" / f"argov2_{scene}" / "pcd_bin_files.csv"
        if not csv_path.exists():
            print(f"  CSV not found: {csv_path}")
            continue

        # Read timestamps
        timestamps = read_csv_timestamps(str(csv_path))
        if not timestamps:
            print("  No timestamps found in CSV")
            continue

        # Process each CAN file
        can_files = [
            "meta.json",
            "ms_imu.json",
            "pose.json",
            "route.json",
            "steeranglefeedback.json",
            "vehicle_monitor.json",
            "zoe_veh_info.json",
            "zoesensors.json"
        ]

        for file in can_files:
            input_file = f"scene-0001_{file}"
            input_path = source_dir / input_file
            output_path = output_dir / f"scene-{scene:04d}_{file}"

            if not input_path.exists():
                print(f"  Not found: {input_file}")
                continue

            print(f"Processing {input_file} as scene {scene}...")
            process_can_file(str(input_path), str(output_path), timestamps)

        # Update meta.json with statistics
        meta_path = output_dir / f"scene-{scene:04d}_meta.json"
        if meta_path.exists():
            update_meta_file(meta_path, output_dir)

    print("\nProcessing complete!")

if __name__ == "__main__":
    main()

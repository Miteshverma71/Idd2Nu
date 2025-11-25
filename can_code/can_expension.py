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
    """Process a single CAN file to update timestamps and trim extra entries."""
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  Error: Failed to parse JSON in {input_path} - {e}")
        return

    if not data:
        return

    # For list of dictionaries with 'utime' key
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and 'utime' in data[0]:
        # Trim data to match number of timestamps
        original_len = len(data)
        data = data[:len(timestamps)]
        
        for i, entry in enumerate(data):
            entry['utime'] = timestamps[i]
        
        print(f"  Trimmed from {original_len} to {len(data)} entries and updated timestamps")
    
    # For meta.json
    elif isinstance(data, dict) and 'message_count' in str(data):
        print(f"  Skipping timestamp update for meta file")
    else:
        print(f"  Warning: Unsupported JSON structure in {input_path}")
        return

    # Save updated data
    try:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"  Error: Failed to write JSON to {output_path} - {e}")

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
        "max_diff": float(np.max(np.abs(diffs)) if len(diffs) > 0 else 0),
        "mean_diff": float(np.mean(np.abs(diffs)) if len(diffs) > 0 else 0),
        "min_diff": float(np.min(np.abs(diffs)) if len(diffs) > 0 else 0),
        "std_diff": float(np.std(np.abs(diffs)) if len(diffs) > 0 else 0)
    }

def update_meta_file(meta_path: Path, data_dir: Path):
    """Update the meta.json file with statistics from other CAN files."""
    # Read the meta file
    with open(meta_path, 'r') as f:
        meta = json.load(f)
    
    # Define file patterns and their corresponding meta keys
    file_patterns = {
        "scene-0001_ms_imu.json": "MS_IMU",
        "scene-0001_pose.json": "POSE",
        "scene-0001_route.json": "ROUTE",
        "scene-0001_steeranglefeedback.json": "STEER_ANGLE_FEEDBACK",
        "scene-0001_vehicle_monitor.json": "VEHICLE_MONITOR",
        "scene-0001_zoe_veh_info.json": "ZOE_VEH_INFO",
        "scene-0001_zoesensors.json": "ZoeSensors"
    }
    
    for file_pattern, meta_key in file_patterns.items():
        file_path = data_dir / file_pattern
        if not file_path.exists():
            print(f"Warning: {file_path} not found, skipping...")
            continue
        
        print(f"Processing {file_pattern}...")
        
        # Read the data file
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"  Error reading {file_path}, skipping...")
                continue
        
        if not data or not isinstance(data, list):
            print(f"  No data or invalid format in {file_path}, skipping...")
            continue
        
        # Initialize stats dictionary for this file
        stats = {
            "message_count": len(data),
            "message_freq": len(data) / ((data[-1]['utime'] - data[0]['utime']) / 1e6) if len(data) > 1 else 0,
            "timespan": (data[-1]['utime'] - data[0]['utime']) / 1e6 if len(data) > 1 else 0,
            "var_stats": {}
        }
        
        # Collect all fields and their values
        fields = {}
        for entry in data:
            for key, value in entry.items():
                if key == 'utime' or not isinstance(value, (int, float)):
                    continue
                if key not in fields:
                    fields[key] = []
                fields[key].append(value)
        
        # Calculate statistics for each field
        for field, values in fields.items():
            if len(values) < 2:
                continue
            stats["var_stats"][field] = calculate_stats(values)
        
        # Update the meta data
        meta[meta_key] = stats
    
    # Save the updated meta file
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    
    print("Meta file updated successfully!")

def main():
    # Base directories
    base_dir = Path(r"C:\Users\mitvi\Downloads\argov2_00000")
    canbus_temp = base_dir / "canbus_temp"
    output_dir = base_dir / "output" / "canbus"
    csv_path = r"C:\Users\mitvi\Downloads\argov2_00000\argov2_00000\argov2_1\pcd_bin_files.csv"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Update timestamps in all CAN files
    timestamps = read_csv_timestamps(csv_path)
    if not timestamps:
        print("Error: No timestamps found in CSV file")
        return
    
    can_file_patterns = [
        "scene-0001_meta.json",
        "scene-0001_ms_imu.json",
        "scene-0001_pose.json",
        "scene-0001_route.json",
        "scene-0001_steeranglefeedback.json",
        "scene-0001_vehicle_monitor.json",
        "scene-0001_zoe_veh_info.json",
        "scene-0001_zoesensors.json"
    ]
    
    print("=== Updating timestamps in CAN files ===")
    for pattern in can_file_patterns:
        input_path = canbus_temp / pattern
        output_path = output_dir / pattern
        
        if not input_path.exists():
            print(f"Warning: {input_path} does not exist, skipping...")
            continue
            
        print(f"Processing {pattern}...")
        process_can_file(str(input_path), str(output_path), timestamps)
    
    print("\n=== Updating meta file with statistics ===")
    # Step 2: Update the meta.json file with statistics
    meta_path = output_dir / "scene-0001_meta.json"
    update_meta_file(meta_path, output_dir)
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()

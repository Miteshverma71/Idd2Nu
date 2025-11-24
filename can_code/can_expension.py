import json
import os
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
    """Process a single CAN file to update timestamps."""
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  Error: Failed to parse JSON in {input_path} - {e}")
        return
    
    if not data:
        return
    
    # For list of dictionaries with 'utime' key (like vehicle_monitor.json, ms_imu.json, etc.)
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and 'utime' in data[0]:
        for i, entry in enumerate(data):
            timestamp_idx = i % len(timestamps)
            entry['utime'] = timestamps[timestamp_idx]
    # For meta.json which is a dictionary with message statistics
    elif isinstance(data, dict) and 'message_count' in str(data):
        # Skip updating timestamps for meta files as they contain statistics
        print(f"  Skipping timestamp update for meta file")
    else:
        print(f"  Warning: Unsupported JSON structure in {input_path}")
        return
    
    # Save the updated data
    try:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"  Error: Failed to write JSON to {output_path} - {e}")

def main():
    # Base directories
    base_dir = Path(r"C:\Users\mitvi\Downloads\argov2_00000")
    canbus_temp = base_dir / "canbus_temp"
    output_dir = base_dir / "output" / "canbus"
    csv_path = r"C:\Users\mitvi\Downloads\argov2_00000\argov2_00000\argov2_1\pcd_bin_files.csv"
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read timestamps from CSV
    timestamps = read_csv_timestamps(csv_path)
    if not timestamps:
        print("Error: No timestamps found in CSV file")
        return
    
    # List of CAN file patterns to process
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
    
    # Process each CAN file
    for pattern in can_file_patterns:
        input_path = canbus_temp / pattern
        output_path = output_dir / pattern
        
        if not input_path.exists():
            print(f"Warning: {input_path} does not exist, skipping...")
            continue
            
        print(f"Processing {pattern}...")
        process_can_file(str(input_path), str(output_path), timestamps)
    
    print("Processing complete!")

if __name__ == "__main__":
    main()

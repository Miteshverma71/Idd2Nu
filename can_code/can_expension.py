
import json
import csv
from pathlib import Path
from typing import List

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

def main():
    base_dir = Path(r"/home/miteshv/Downloads/can_bus")
    canbus_temp = base_dir / "canbus_temp"
    output_dir = base_dir / "output" / "canbus"
    csv_path = r"/home/miteshv/Downloads/av2_train000_5scenes/argov2_1/pcd_bin_files.csv"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
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

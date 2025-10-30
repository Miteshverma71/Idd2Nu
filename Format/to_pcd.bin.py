import os
import glob
import struct

# Input folder containing .pcd files
pcd_folder = "/home/miteshv/Documents/data_converter/data/idd_test/lidar"

# Output folder for .pcd.bin files
output_folder = "/home/miteshv/Documents/data_converter/output_conv/lidar"
os.makedirs(output_folder, exist_ok=True)

# Get all .pcd files in the folder
pcd_files = glob.glob(os.path.join(pcd_folder, "*.pcd"))

for ascii_file_path in pcd_files:
    filename = os.path.basename(ascii_file_path)
    bin_file_path = os.path.join(output_folder, filename + ".bin")

    with open(ascii_file_path, 'r') as f:
        lines = f.readlines()

    # Find start of data
    data_start_index = 0
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("data ascii"):
            data_start_index = i + 1
            break

    # Extract point data
    point_lines = lines[data_start_index:]
    points = []
    for line in point_lines:
        parts = line.strip().split()
        if len(parts) == 9:
            x, y, z = map(float, parts[0:3])
            intensity = float(parts[3])
            t = int(parts[4])
            reflectivity = int(parts[5])
            ring = int(parts[6])
            ambient = int(parts[7])
            range_val = float(parts[8])
            points.append((x, y, z, intensity, t, reflectivity, ring, ambient, range_val))

    # Write header and binary data
    with open(bin_file_path, 'wb') as f:
        for line in lines[:data_start_index]:
            f.write(line.replace("DATA ascii", "DATA binary").encode("utf-8"))
        for point in points:
            f.write(struct.pack("fffffHBHf", *point))

    print("✅ Converted:", ascii_file_path, "➡", bin_file_path)

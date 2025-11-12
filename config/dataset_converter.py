# ============================================================
# dataset_converter.py
# ============================================================
import os
import cv2
import numpy as np
from pathlib import Path
import open3d as o3d

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def convert_image_to_jpeg(src_path, dest_folder):
    """Convert an image (any format) to JPEG."""
    img = cv2.imread(src_path)
    if img is None:
        print(f"⚠️ Skipping (unreadable): {src_path}")
        return None

    Path(dest_folder).mkdir(parents=True, exist_ok=True)
    new_path = os.path.join(dest_folder, Path(src_path).stem + ".jpeg")

    cv2.imwrite(new_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f"🖼️ Converted: {src_path} → {new_path}")
    return new_path


def convert_lidar_to_pcd_or_bin(src_path, dest_folder, output_format="pcd"):
    """
    Convert Lidar data to .pcd or .bin format.
    Supports .npy, .txt, or .csv input formats.
    """
    Path(dest_folder).mkdir(parents=True, exist_ok=True)
    name = Path(src_path).stem
    ext = Path(src_path).suffix.lower()

    try:
        # Load points based on extension
        if ext == ".npy":
            points = np.load(src_path)
        elif ext in [".txt", ".csv"]:
            points = np.loadtxt(src_path, delimiter=None)
        elif ext in [".pcd", ".bin"]:
            print(f"✅ Already {ext} format: {src_path}")
            return src_path
        else:
            print(f"⚠️ Unsupported Lidar format: {src_path}")
            return None

        # Save to chosen format
        if output_format == "pcd":
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points[:, :3])
            o3d.io.write_point_cloud(os.path.join(dest_folder, f"{name}.pcd"), pcd)
            print(f"🌫️ Converted to .pcd: {src_path}")
            return os.path.join(dest_folder, f"{name}.pcd")

        elif output_format == "bin":
            points.astype(np.float32).tofile(os.path.join(dest_folder, f"{name}.bin"))
            print(f"🌫️ Converted to .bin: {src_path}")
            return os.path.join(dest_folder, f"{name}.bin")

    except Exception as e:
        print(f"❌ Error converting {src_path}: {e}")
        return None


# ------------------------------------------------------------
# Core conversion orchestrator
# ------------------------------------------------------------

def convert_dataset(dataset_paths, output_root, img_fmt=".jpeg", lidar_fmt="pcd"):
    """
    Convert all dataset files into desired formats.
    dataset_paths should be a dict like the one from dataset_reader:
      {
        "cameras": [...],
        "lidars": [...],
        "annotations": [...]
      }
    """
    print("🚀 Starting dataset conversion...")
    for img_path in dataset_paths.get("cameras", []):
        convert_image_to_jpeg(img_path, os.path.join(output_root, "camera_converted"))

    for lidar_path in dataset_paths.get("lidars", []):
        convert_lidar_to_pcd_or_bin(lidar_path, os.path.join(output_root, "lidar_converted"), lidar_fmt)

    print("✅ Conversion completed successfully!")


if __name__ == "__main__":
    from dataset_reader import search_dataset
    root = input("Enter dataset root path: ").strip()
    dataset = search_dataset(root)
    convert_dataset(dataset, output_root="converted_dataset", lidar_fmt="pcd")

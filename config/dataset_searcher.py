# ============================================================
# dataset_reader.py
# ============================================================
import os
import json

def search_dataset(root_dir):
    """
    Recursively walks through the dataset folder and collects 
    paths for images, lidar data, and annotations.
    """
    dataset_structure = {
        "cameras": [],
        "lidars": [],
        "annotations": [],
        "others": []
    }

    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            fpath = os.path.join(dirpath, file).replace("\\", "/")
            ext = os.path.splitext(file)[1].lower()

            if ext in [".jpg", ".jpeg", ".png", ".bmp"]:
                dataset_structure["cameras"].append(fpath)
            elif ext in [".bin", ".pcd", ".npy"]:
                dataset_structure["lidars"].append(fpath)
            elif ext in [".json", ".xml", ".txt"]:
                if "annot" in file.lower() or "label" in file.lower():
                    dataset_structure["annotations"].append(fpath)
                else:
                    dataset_structure["others"].append(fpath)
            else:
                dataset_structure["others"].append(fpath)

    return dataset_structure


def summarize_dataset(dataset_structure):
    """
    Print summary of dataset: how many files of each type,
    and sample paths for inspection.
    """
    print("=== DATASET SUMMARY ===")
    for key, items in dataset_structure.items():
        print(f"{key.upper()}: {len(items)} files")
        if len(items) > 0:
            print(f"  Example: {items[0]}")
    print("========================")


def save_summary_to_json(dataset_structure, save_path="dataset_summary.json"):
    with open(save_path, "w") as f:
        json.dump(dataset_structure, f, indent=4)
    print(f"✅ Saved summary to {save_path}")


if __name__ == "__main__":
    root = input("Enter dataset root path: ").strip()
    result = search_dataset(root)
    summarize_dataset(result)
    save_summary_to_json(result)

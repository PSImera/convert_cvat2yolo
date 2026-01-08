import random
import shutil
from pathlib import Path
import yaml
from tqdm import tqdm


def main(config_path: str):
    print("=== YOLO Dataset Splitter started ===")

    # Load config
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    dataset_path = Path(config["dataset"]["path"])
    split_ratio = config["split"]
    seed = config["random"]["seed"]

    obj_dir = dataset_path / "obj_train_data"
    names_file = dataset_path / "obj.names"

    if not obj_dir.exists():
        print(f"[ERROR] obj_train_data not found: {obj_dir}")
        return

    frames_dir = obj_dir / "frames"
    img_dir = frames_dir if frames_dir.exists() else obj_dir
    print(f"Image directory selected: {img_dir}")

    # Collect images
    images = []
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        images.extend(img_dir.glob(ext))

    if not images:
        print("[ERROR] No images found. Supported formats: jpg, jpeg, png")
        return

    print(f"Images found: {len(images)}")
    random.seed(seed)
    random.shuffle(images)

    # Split dataset
    n = len(images)
    train_end = int(n * split_ratio["train"])
    val_end = train_end + int(n * split_ratio["val"])

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:],
    }

    print("Dataset split:")
    for k, v in splits.items():
        print(f"  {k}: {len(v)} images")

    # Output directories
    output_dir = dataset_path.parent / (dataset_path.name + "_converted")
    for part in splits.keys():
        (output_dir / "images" / part).mkdir(parents=True, exist_ok=True)
        (output_dir / "labels" / part).mkdir(parents=True, exist_ok=True)

    # Copy files with progress bar
    print("Copying files...")
    for split, imgs in splits.items():
        for img in tqdm(imgs, desc=f"Copying {split}", unit="img"):
            target_img = output_dir / "images" / split / img.name
            target_label = output_dir / "labels" / split / img.with_suffix(".txt").name

            # skip if already exists
            if target_img.exists():
                continue
            shutil.copy(img, target_img)

            label = img.with_suffix(".txt")
            if label.exists() and not target_label.exists():
                shutil.copy(label, target_label)

    print(f"Dataset split finished → {output_dir}")

    # Read class names
    with open(names_file, "r", encoding="utf-8") as f:
        class_names = [line.strip() for line in f if line.strip()]

    # Create dataset.yaml
    yaml_data = {
        "path": str(output_dir.resolve()),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "nc": len(class_names),
        "names": class_names,
    }

    with open(output_dir / "dataset.yaml", "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True)

    print(f"dataset.yaml created → {output_dir / 'dataset.yaml'}")
    print("=== Done ===")


if __name__ == "__main__":
    main("config.yaml")

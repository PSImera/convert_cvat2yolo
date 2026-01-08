import random
import shutil
from pathlib import Path
import yaml


def main(config_path: str):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    dataset_path = config["dataset"]["path"]
    split_ratio = config["split"]
    seed = config["random"]["seed"]

    dataset_dir = Path(dataset_path)
    img_dir = dataset_dir / "obj_train_data\\frames"
    names_file = dataset_dir / "obj.names"
    output_dir = Path(dataset_path + "_converted")

    random.seed(seed)

    # create directories
    for part in split_ratio.keys():
        (output_dir / "images" / part).mkdir(parents=True, exist_ok=True)
        (output_dir / "labels" / part).mkdir(parents=True, exist_ok=True)

    # collect & shuffle images
    images = [f for f in img_dir.glob("*.jpg")]
    random.shuffle(images)

    # split dataset
    n = len(images)
    train_end = int(n * split_ratio["train"])
    val_end = train_end + int(n * split_ratio["val"])

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:],
    }

    # copy files
    for split, imgs in splits.items():
        for img in imgs:
            label = img.with_suffix(".txt")
            shutil.copy(img, output_dir / "images" / split / img.name)
            if label.exists():
                shutil.copy(label, output_dir / "labels" / split / label.name)
    print(f"spliting finished! dataset saved in folder: {output_dir}")

    # make yaml file
    with open(names_file, "r", encoding="utf-8") as f:
        class_names = [line.strip() for line in f if line.strip()]

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
    print(f"yaml file added: {output_dir/'dataset.yaml'}")


if __name__ == "__main__":
    main("config.yaml")

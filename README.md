# YOLO Dataset Splitter

A utility script for converting datasets exported from **CVAT** in **YOLO 1.1** format.

The script converts the dataset into a format compatible with **YOLO (Ultralytics)**,
automatically generates `dataset.yaml`, and splits the data into **train / val / test** subsets.

---

## Input Dataset Structure

The following input structure is expected:

dataset/
├─ obj_train_data/
│  └─ frames/
│     ├─ 0001.jpg
│     ├─ 0001.txt
│     ├─ 0002.jpg
│     ├─ 0002.txt
│     └─ ...
├─ obj.names

- `.jpg / .jpeg / .png` — images
- `.txt` — YOLO annotations
- `obj.names` — class names, one per line

Both layouts are supported:
- images directly in `obj_train_data/`
- images inside `obj_train_data/frames/`

---

## Installation

Only a small number of dependencies is required.
The script can be run from a global Python environment or inside a virtual environment.

### 1. Create a virtual environment (optional)

python -m venv .venv

Windows:
.venv\\Scripts\\activate

Linux / macOS:
source .venv/bin/activate

---

### 2. Install dependencies

pip install -r requirements.txt

Dependencies:
- PyYAML
- tqdm

---

## Configuration

All parameters are defined in `config.yaml`.

Example:

dataset:
  path: "D:/Datasets/path_to_dataset_folder"

split:
  train: 0.7
  val: 0.2
  test: 0.1

random:
  seed: 1337

---

## Usage

python split_dataset.py

---

## Output

A new directory `<dataset>_converted` is created:

dataset_converted/
├─ images/
│  ├─ train/
│  ├─ val/
│  └─ test/
├─ labels/
│  ├─ train/
│  ├─ val/
│  └─ test/
└─ dataset.yaml
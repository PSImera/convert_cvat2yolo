# YOLO Dataset Splitter

Скрипт для конвертирования датасета, экспортируемого из CVAT в формате YOLO1.1

Конвертирует в пригодный для YOLO (Ultralytics) формат с файлом dataset.yaml

Так же сразу делает его разбиение его на train / val / test

---

## Структура входного датасета

Ожидается следующая структура:

dataset/
├─ obj_train_data/
│  └─ frames/
│     ├─ 0001.jpg
│     ├─ 0001.txt
│     ├─ 0002.jpg
│     ├─ 0002.txt
│     └─ ...
├─ obj.names

- .jpg — изображения
- .txt — YOLO-аннотации
- obj.names — список классов, по одному в строке

---

## Установка

Для работы нужна лишь PyYAML библиотека, можно из глобального окружения запустить, либо создать виртуальное

### 1. Создание виртуального окружения

python -m venv .venv

Windows:
.venv\Scripts\activate

Linux / macOS:
source .venv/bin/activate

---

### 2. Установка зависимостей

pip install -r requirements.txt

---

## Конфигурация

Все параметры задаются в файле config.yaml.

Пример:

dataset:
  path: "D:/Datasets/path_to_dataset_folder"

split:
  train: 0.7
  val: 0.2
  test: 0.1

random:
  seed: 1337

---

## Запуск

python split_dataset.py

---

## Результат

Создаётся новая директория <dataset>_converted:

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




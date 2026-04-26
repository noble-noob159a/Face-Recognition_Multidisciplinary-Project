# Face Recognition - Multidisciplinary Project

## Description
This project performs real-time face registration and face recognition using [InsightFace](https://github.com/deepinsight/insightface/tree/master/python-package) - `buffalo_l model`.
It provides two command-line scripts:
- `register.py` to add face embeddings into a local database.
- `inference.py` to run webcam recognition against the registered identities.

## Setup
1. Clone this repository and open it in your terminal.
2. Install dependencies:

```bash
pip install -r requirements.txt
```


## Register new face by register.py
Register from webcam:

```bash
python register.py --name "YourName" --webcam
```

Register from image file:

```bash
python register.py --name "YourName" --imgpath ./path/to/photo.jpg
```

Main arguments:
- `--name`: identity label to store (default: `Me`).
- `--webcam`: capture from webcam.
- `--imgpath`: register from an image path.
- `--output`: output pickle database path (default: `./face_db/insightface_db.pkl`).

Press `c` to capture frame (for webcam mode).

## Run inference by inference.py

```bash
python inference.py
```


Useful arguments:
- `--db-file`: database file path (default: `./face_db/insightface_db.pkl`).
- `--threshold`: cosine distance threshold (default: `0.55`).
- `--frame-skip`: run detection every N frames (default: `3`).
- `--camera-index`: webcam index (default: `0`).
- `--ctx-id`: `0` for GPU, `-1` for CPU (default: `0`).
- `--det-size`: detector input size (default: `640`).

Press `q` to stop the inference window.

## References
- [InsightFace (GitHub)](https://github.com/deepinsight/insightface)
- [ArcFace: Additive Angular Margin Loss for Deep Face Recognition (arXiv)](https://arxiv.org/abs/1801.07698)
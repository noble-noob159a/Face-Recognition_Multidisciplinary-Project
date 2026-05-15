# Face Recognition - Multidisciplinary Project

**Semester:** HK252  

#### Team Members
- Lê Chí Đại — 2310621
- Lương Minh Thuận — 2313348
- Nguyễn Quốc Huy — 2311209
- Nguyễn Văn Hùng — 2311301

## Overview

This project combines three parts:

- `model/` for face registration and face recognition with InsightFace.
- `app/` for the Flask dashboard, API, and MQTT bridge.
- `yolobit/` for the MicroPython code running on the Yolo:Bit board.

The recognition pipeline uses [InsightFace](https://github.com/deepinsight/insightface/tree/master/python-package) with the `buffalo_l` model.

## Project Structure

```text
.
├── app/
│   ├── backend/
│   │   ├── mqtt_bridge.py        # MQTT listener + bridge to the dashboard
│   │   └── register.py           # API for uploading/registering a face image
│   └── dashboard/
│       ├── app.py                # Flask + SocketIO application entrypoint
│       ├── static/
│       │   ├── camera_stream.js
│       │   └── face_register.js
│       └── templates/
│           └── index.html
├── face_db/                      # Local face embedding database
├── model/
│   ├── inference.py              # Run webcam recognition
│   ├── register.py               # Register new faces into the database
│   └── MODEL.md                  # Full model setup and run guide
├── tmp_uploads/                  # Temporary uploaded images
├── yolobit/
│   ├── main.py                   # Yolo:Bit program
│   ├── lib/                      # MicroPython support libraries
│   ├── pymakr.conf               # Pymakr project config
│   └── yolobit-micropython.code-workspace
├── requirements.txt
└── start.sh                      # Convenience script to start model + dashboard on Unix shells
```

## Requirements

- Python 3.11+ is recommended
- A webcam for registration and inference.
- An MQTT broker reachable from both the model and the Yolo:Bit board.
- For the Yolo:Bit part: a Yolo:Bit board, USB cable, MicroPython firmware, and VS Code with the Pymakr extension.

## Setup

1. Clone the repository and open it in a terminal.
2. Create and activate a virtual environment.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Create a `.env` file if you want to override the defaults.

```env
MQTT_BROKER=mqtt.ohstem.vn
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_TOPIC_RESULT=face/result
MQTT_TOPIC_YOLOBIT=V1
FLASK_PORT=5000
SECRET_KEY=face-demo-secret
WS_URL=
API_URL=
UPLOAD_DIR=./tmp_uploads
```

## Run the Face Model

The detailed model guide is in [model/MODEL.md](model/MODEL.md). The main commands are:

Register a new face from webcam:

```bash
python -m model.register --name "YourName" --webcam
```

Register a new face from an image:

```bash
python -m model.register --name "YourName" --imgpath ./path/to/photo.jpg
```

Run real-time inference:

```bash
python -m model.inference
```

Useful inference options include `--db-file`, `--threshold`, `--frame-skip`, `--camera-index`, `--ctx-id`, and `--det-size`.

## Run the Backend / Dashboard

The dashboard entrypoint is [app/dashboard/app.py](app/dashboard/app.py). It starts a Flask application, attaches the MQTT bridge, and serves the web UI.

Run it with:

```bash
python -m app.dashboard.app
```

By default the app listens on `http://127.0.0.1:5000`.

If you want to run the model and the backend at the same time, open two terminals and run:

```bash
python -m model.inference
```

and:

```bash
python -m app.dashboard.app
```

On Unix-like systems, [start.sh](start.sh) launches both processes together.

The backend also exposes a face registration API at `POST /api/register` for uploading an image and storing the embedding in the local database.

## Set Up and Run Yolo:Bit Code

The Yolo:Bit instructions here follow the same workflow as the guide in the linked reference: [Yolobit MicroPython (OhStem)](https://github.com/sonsonha/MicroPython-Yolobit-/blob/feature/detection-micropython/README.md)

The board code lives in [yolobit/main.py](yolobit/main.py). It connects to Wi-Fi, subscribes to MQTT topic `V1`, and shows the recognized name on the LCD.

1. Open the Yolo:Bit workspace file [yolobit/yolobit-micropython.code-workspace](yolobit/yolobit-micropython.code-workspace) in VS Code.
2. Install the Pymakr extension if it is not already installed.
3. Connect the Yolo:Bit board by USB and add the device in Pymakr.
4. Edit [yolobit/main.py](yolobit/main.py) and fill in your Wi-Fi credentials.

```python
WIFI_SSID = ''
WIFI_PASSWORD = ''
```

5. If your MQTT broker is different from `mqtt.ohstem.vn`, update the broker settings in [yolobit/main.py](yolobit/main.py) as well.
6. Sync the whole Yolo:Bit project to the device.
7. Use Soft reset or `Ctrl+D` in the REPL so the board starts running `main.py`.

After a successful setup, the board will:

- connect to Wi-Fi,
- sync time from NTP,
- connect to the MQTT broker,
- listen for recognition results on topic `V1`, and
- show `Valid:` or `Invalid:` plus the detected name on the LCD.

For the full Pymakr workflow, device setup, and troubleshooting steps, use the reference README linked above.

## Notes

- The registration endpoint saves temporary uploads in [tmp_uploads/](tmp_uploads/).
- Face embeddings are stored in [face_db/](face_db/).
- If you change MQTT or Flask settings, keep the `.env` values consistent across the model, backend, and Yolo:Bit code.
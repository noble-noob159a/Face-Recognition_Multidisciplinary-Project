import cv2
import numpy as np
import argparse
import json
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from scipy.spatial.distance import cosine
from .register import load_database
from insightface.app import FaceAnalysis
import time

DEFAULT_DB_FILE = "./face_db/insightface_db.pkl"
DEFAULT_THRESHOLD = 0.55
DEFAULT_FRAME_SKIP = 3
DEFAULT_CAMERA_INDEX = 0
DEFAULT_CTX_ID = 0
DEFAULT_DET_SIZE = 640
DEFAULT_WINDOW_NAME = "InsightFace Video Inference"

def create_mqtt_client():
    load_dotenv()

    broker = os.getenv("MQTT_BROKER", "mqtt.ohstem.vn")
    port = int(os.getenv("MQTT_PORT", "1883"))
    username = os.getenv("MQTT_USERNAME", "")
    password = os.getenv("MQTT_PASSWORD", "")

    client = mqtt.Client()
    if username:
        client.username_pw_set(username, password)
    client.reconnect_delay_set(min_delay=1, max_delay=30)
    client.connect(broker, port, 60)
    client.loop_start()
    return client


def publish_detection(client, name):
    topic = os.getenv("MQTT_TOPIC_RESULT", "face/result")
    payload_name = name if name.upper() != "UNKNOWN" else "UNKNOWN"
    payload = json.dumps({"name": payload_name})

    try:
        if not client.is_connected():
            client.reconnect()
        client.publish(topic, payload)
    except Exception as exc:
        print(f"MQTT publish failed: {exc}")

def parse_args():
    parser = argparse.ArgumentParser(description="Run real-time InsightFace recognition from webcam.")
    parser.add_argument(
        "--db-file",
        default=DEFAULT_DB_FILE,
        help=f"Path to face database file (default: {DEFAULT_DB_FILE})."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f"Cosine distance threshold for recognition (default: {DEFAULT_THRESHOLD})."
    )
    parser.add_argument(
        "--frame-skip",
        type=int,
        default=DEFAULT_FRAME_SKIP,
        help=f"Run detection every N frames (default: {DEFAULT_FRAME_SKIP})."
    )
    parser.add_argument(
        "--camera-index",
        type=int,
        default=DEFAULT_CAMERA_INDEX,
        help=f"Webcam index for cv2.VideoCapture (default: {DEFAULT_CAMERA_INDEX})."
    )
    parser.add_argument(
        "--ctx-id",
        type=int,
        default=DEFAULT_CTX_ID,
        help=f"InsightFace context id: 0 for GPU, -1 for CPU (default: {DEFAULT_CTX_ID})."
    )
    parser.add_argument(
        "--det-size",
        type=int,
        default=DEFAULT_DET_SIZE,
        help=f"Face detector input size (square, default: {DEFAULT_DET_SIZE})."
    )

    args = parser.parse_args()

    if args.frame_skip < 1:
        parser.error("--frame-skip must be >= 1")
    if args.threshold < 0:
        parser.error("--threshold must be >= 0")
    return args


def main():
    args = parse_args()
    mqtt_client = create_mqtt_client()

    # Init InsightFace
    print("Loading InsightFace models...")
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=args.ctx_id, det_size=(args.det_size, args.det_size))
    print("Models loaded successfully.")

    # Load Face Database
    db = load_database(args.db_file)
    known_face_names = list(db.keys())
    known_face_encodings = np.array(list(db.values()))
    print(f"Loaded {len(known_face_names)} identities from DB: {args.db_file}")

    # Init Webcam
    video_capture = cv2.VideoCapture(args.camera_index, cv2.CAP_DSHOW)
    if not video_capture.isOpened():
        print(f"Error: Could not open camera index {args.camera_index}.")
        return

    print("Starting InsightFace inference... Press 'q' to quit.")
    frame_count = 0
    latest_detections = []

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % args.frame_skip == 0:
            frame_count = 0

            # Inference
            faces = app.get(frame)
            current_frame_detections = []

            for face in faces:
                embedding = face.normed_embedding

                # InsightFace bbox format is [x1, y1, x2, y2]
                bbox = face.bbox.astype(int)
                x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]

                name = "Unknown"

                if len(known_face_encodings) > 0:
                    distances = [cosine(embedding, known_emb) for known_emb in known_face_encodings]
                    best_match_index = np.argmin(distances)

                    if distances[best_match_index] < args.threshold:
                        name = known_face_names[best_match_index]

                current_frame_detections.append({
                    "name": name,
                    "box": (x1, y1, x2, y2)
                })

                publish_detection(mqtt_client, name)

            latest_detections = current_frame_detections

        # Draw boxes and labels from latest detections
        for det in latest_detections:
            x1, y1, x2, y2 = det["box"]
            name = det["name"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow(DEFAULT_WINDOW_NAME, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # time.sleep(1)

    video_capture.release()
    cv2.destroyAllWindows()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()


if __name__ == "__main__":
    main()
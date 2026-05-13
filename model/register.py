import cv2
import pickle
import os
import argparse
from insightface.app import FaceAnalysis

DB_FOLDER = "./face_db"
DB_FILE = os.path.join(DB_FOLDER, "insightface_db.pkl")

os.makedirs(DB_FOLDER, exist_ok=True)

# Init InsightFace
app = FaceAnalysis(name='buffalo_l')
# ctx_id=0: use GPU. (-1: CPU mode)
app.prepare(ctx_id=0, det_size=(640, 640))

def load_database(db_file=DB_FILE):
    if os.path.exists(db_file):
        with open(db_file, 'rb') as f:
            return pickle.load(f)
    return {}

def save_database(db, db_file=DB_FILE):
    with open(db_file, 'wb') as f:
        pickle.dump(db, f)

def register_face(name, image_path=None, use_webcam=False, db_file=DB_FILE):
    db_dir = os.path.dirname(db_file)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    db = load_database(db_file)

    # MODE 1: Register from an Image File
    if image_path:
        print(f"Attempting to register '{name}' from image: {image_path}")
        if not os.path.exists(image_path):
            print("Error: Image file not found! Check your path.")
            return

        img = cv2.imread(image_path)
        if img is None:
            print("Error: Could not read the image file.")
            return

        # Extract face
        faces = app.get(img)
        
        if len(faces) == 1:
            db[name] = faces[0].normed_embedding
            save_database(db, db_file)
            print(f"Success! '{name}' registered to the database.")
        elif len(faces) == 0:
            raise ValueError("Error: No face detected in the image.")
            print("Error: No face detected in the image.")
        else:
            raise ValueError(f"Error: Detected {len(faces)} faces in the image. Please use a photo with only one face.")
            print(f"Error: Detected {len(faces)} faces in the image. Please use a photo with only one face.")

    # MODE 2: Register from Webcam
    elif use_webcam:
        video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        print(f"Look at the camera to register '{name}'. Press 'c' to capture.")
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                continue

            cv2.imshow('Registration - InsightFace', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('c'):
                faces = app.get(frame)
                
                if len(faces) == 1:
                    db[name] = faces[0].normed_embedding
                    save_database(db, db_file)
                    print(f"Registered '{name}' via webcam.")
                    break
                elif len(faces) == 0:
                    print("No face detected. Try again.")
                else:
                    print(f"Detected {len(faces)} faces. Ensure one face is in frame.")
                    
        video_capture.release()
        cv2.destroyAllWindows()
    else:
        print("Error: Select one source using either --webcam or --imgpath.")


def parse_args():
    parser = argparse.ArgumentParser(description="Register face embeddings into InsightFace DB.")
    parser.add_argument(
        "--name",
        default="Me",
        help="Name label to store for this face (default: Me)."
    )
    source_group = parser.add_mutually_exclusive_group(required=False)
    source_group.add_argument(
        "--webcam",
        action="store_true",
        help="Capture face from webcam."
    )
    source_group.add_argument(
        "--imgpath",
        default=None,
        help="Path to an image file for registration."
    )
    parser.add_argument(
        "--output",
        default=DB_FILE,
        help=f"Output DB file path (default: {DB_FILE})."
    )
    args = parser.parse_args()

    # Default source: webcam when user doesn't provide any source argument.
    if not args.webcam and args.imgpath is None:
        args.webcam = True

    return args


# Example CLI usage:
# python register.py --name Thuan --imgpath ./img99.jpg
# python register.py --name Thuan --webcam
# python register.py --name Thuan --webcam --output ./face_db/custom_db.pkl
if __name__ == "__main__":
    args = parse_args()
    register_face(
        name=args.name,
        image_path=args.imgpath,
        use_webcam=args.webcam,
        db_file=args.output,
    )
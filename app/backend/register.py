import os
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from model.register import register_face

register_bp = Blueprint('register', __name__)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./tmp_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
ALLOWED_MIMETYPES = {'image/jpeg', 'image/png', 'image/webp'}

def allowed_file(filename, mimetype):
    ext_ok = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    mimetype_ok = mimetype in ALLOWED_MIMETYPES
    return ext_ok or mimetype_ok

@register_bp.route('/api/register', methods=['POST'])
def register_api():
    name = request.form.get('name', '').strip()
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    if 'image' not in request.files:
        return jsonify({"error": "File must be an image"}), 400
        
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "File must be an image"}), 400
        
    if not allowed_file(image_file.filename, image_file.mimetype):
        return jsonify({"error": "File must be an image"}), 400

    ext = os.path.splitext(image_file.filename)[-1].lower()
    tmp_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}{ext}")
    
    image_file.save(tmp_path)
    
    try:
        register_face(name=name, image_path=tmp_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 422
    # finally:
        # if os.path.exists(tmp_path):
        #     os.remove(tmp_path)
            
    return jsonify({"success": True, "name": name}), 200

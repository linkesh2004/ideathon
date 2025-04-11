from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from base64 import b64decode
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS

# Directory to save images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({"success": False, "message": "No image data provided"}), 400
        
        # Decode base64 image
        try:
            image_data = image_data.split(",")[1]  # Remove the "data:image/jpeg;base64," part
            image_binary = b64decode(image_data)
        except Exception as e:
            return jsonify({"success": False, "message": "Invalid image data"}), 400
        
        # Save image with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(UPLOAD_FOLDER, f'captured_image_{timestamp}.jpg')
        with open(image_path, 'wb') as f:
            f.write(image_binary)
        
        return jsonify({"success": True, "message": "Image uploaded successfully", "filename": os.path.basename(image_path)})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


"""
Flask backend for face blurring application
Handles file uploads, processing, and downloads
"""

import os
import uuid
from flask import Flask, request, render_template, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import mimetypes
from utils.face_blur import blur_faces_in_image, blur_faces_in_video

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Configuration
UPLOAD_FOLDER = 'static/uploads'
RESULTS_FOLDER = 'static/results'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov'}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_image_file(filename):
    """Check if file is an image"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def is_video_file(filename):
    """Check if file is a video"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def generate_unique_filename(original_filename):
    """Generate unique filename to avoid conflicts"""
    extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{extension}"

@app.route('/')
def index():
    """Render the main upload page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported. Please upload images (jpg, jpeg, png) or videos (mp4, avi, mov)'}), 400
        
        # Generate secure unique filename
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save uploaded file
        file.save(filepath)
        
        # Process the file based on type
        if is_image_file(unique_filename):
            result_filename = f"blurred_{unique_filename}"
            result_path = os.path.join(RESULTS_FOLDER, result_filename)
            
            success, message = blur_faces_in_image(filepath, result_path)
            
            if success:
                return jsonify({
                    'success': True,
                    'file_type': 'image',
                    'result_url': url_for('static', filename=f'results/{result_filename}'),
                    'download_url': url_for('download_file', filename=result_filename),
                    'message': message
                })
            else:
                return jsonify({'error': f'Failed to process image: {message}'}), 500
                
        elif is_video_file(unique_filename):
            # For video, always output as mp4
            result_filename = f"blurred_{unique_filename.rsplit('.', 1)[0]}.mp4"
            result_path = os.path.join(RESULTS_FOLDER, result_filename)
            
            success, message = blur_faces_in_video(filepath, result_path)
            
            if success:
                return jsonify({
                    'success': True,
                    'file_type': 'video',
                    'result_url': url_for('static', filename=f'results/{result_filename}'),
                    'download_url': url_for('download_file', filename=result_filename),
                    'message': message
                })
            else:
                return jsonify({'error': f'Failed to process video: {message}'}), 500
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
            
    except RequestEntityTooLarge:
        return jsonify({'error': 'File too large. Maximum size is 100MB'}), 413
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Handle file downloads"""
    try:
        file_path = os.path.join(RESULTS_FOLDER, filename)
        if os.path.exists(file_path):
            # Set appropriate mimetype
            mimetype = mimetypes.guess_type(file_path)[0]
            return send_file(file_path, as_attachment=True, download_name=filename, mimetype=mimetype)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy'})

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 100MB'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Face Blur Application...")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Results folder: {RESULTS_FOLDER}")
    print("Navigate to http://localhost:5000 to use the application")
    app.run(debug=True, host='0.0.0.0', port=5000)
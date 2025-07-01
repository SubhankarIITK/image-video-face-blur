🔒 Face Blur - Privacy Protection Tool
A web application that automatically detects and blurs faces in images and videos to protect privacy. Built with Flask, OpenCV, and MediaPipe.
✨ Features

Smart Face Detection: Uses MediaPipe for accurate face detection
Multi-format Support: Handles images (JPG, PNG) and videos (MP4, AVI, MOV)
Batch Processing: Automatically processes multiple faces in a single file
Responsive Design: Works seamlessly on desktop and mobile devices
Secure File Handling: Generates unique filenames to prevent conflicts
Real-time Processing: Frame-by-frame video processing with progress updates
Drag & Drop: Intuitive file upload interface
Download Ready: Instant download of processed files

🚀 Quick Start
Prerequisites

Python 3.7 or higher
pip (Python package installer)

Installation

Clone or download the project files
Create the project structure:
face-blur-app/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── utils/
│   └── face_blur.py
└── static/
    ├── uploads/
    └── results/

Install dependencies:
bashpip install -r requirements.txt

Run the application:
bashpython app.py

Open your browser and navigate to:
http://localhost:5000


📁 Project Structure
face-blur-app/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main web interface
├── utils/
│   └── face_blur.py      # Face detection and blurring logic
└── static/
    ├── uploads/          # Temporary uploaded files
    └── results/          # Processed output files
🔧 How It Works
Face Detection

Uses MediaPipe Face Detection for accurate face recognition
Configurable confidence threshold (default: 0.5)
Handles multiple faces automatically

Image Processing

Upload image file
Convert to RGB format for MediaPipe
Detect face bounding boxes
Apply Gaussian blur to face regions
Save processed image

Video Processing

Upload video file
Extract frames one by one
Process each frame for face detection
Apply blur to detected faces
Reconstruct video with blurred faces
Output as MP4 format

🎯 Usage
Web Interface

Upload: Click "Choose File" or drag & drop your file
Process: Click "Process & Blur Faces" button
Preview: View the processed result
Download: Click "Download Result" to save the file

Supported Formats

Images: JPG, JPEG, PNG
Videos: MP4, AVI, MOV
Max file size: 100MB

Keyboard Shortcuts

Ctrl/Cmd + U: Open file picker
Enter: Process selected file
Escape: Reset form

⚙️ Configuration
Blur Settings
Edit utils/face_blur.py to customize:
python# Adjust blur intensity (higher = more blur)
blur_factor = 15  # Default: 15

# Change confidence threshold
confidence_threshold = 0.5  # Default: 0.5
File Size Limits
Edit app.py to change upload limits:
pythonapp.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
🔐 Privacy & Security

No data retention: Uploaded files are automatically deleted after processing
Secure filenames: Uses UUID to prevent filename conflicts
Local processing: All face detection happens on your server
No external APIs: Complete privacy protection

🐛 Troubleshooting
Common Issues
1. Import errors with OpenCV/MediaPipe:
bashpip install --upgrade opencv-python mediapipe
2. Video processing fails:

Ensure video codec is supported
Try converting to MP4 format first
Check file size (must be under 100MB)

3. Face detection not working:

Ensure faces are clearly visible
Try adjusting confidence threshold
Check image quality and lighting

4. Memory issues with large videos:

Reduce video resolution before upload
Split long videos into shorter segments
Increase system RAM if possible

Error Messages

"File too large": Reduce file size or increase MAX_CONTENT_LENGTH
"Could not read image": File may be corrupted or unsupported format
"No faces detected": Image may not contain visible faces

🚀 Deployment
Local Development
bashpython app.py
Production (with Gunicorn)
bashpip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
Docker Deployment
Create Dockerfile:
dockerfileFROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
📝 API Endpoints

GET /: Main upload interface
POST /upload: Process uploaded file
GET /download/<filename>: Download processed file
GET /health: Health check endpoint

🤝 Contributing

Fork the repository
Create your feature branch
Make your changes
Test thoroughly
Submit a pull request

📄 License
This project is open source. Feel free to use, modify, and distribute.
🙏 Acknowledgments

MediaPipe by Google for face detection
OpenCV for computer vision processing
Flask for the web framework
Bootstrap inspiration for responsive design

📞 Support
If you encounter any issues:

Check the troubleshooting section
Ensure all dependencies are installed correctly
Verify file formats are supported
Check console output for detailed error messages


Happy face blurring! 🎭
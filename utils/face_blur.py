"""
Face detection and blurring utilities using MediaPipe and OpenCV
Handles both image and video processing
"""

import cv2
import mediapipe as mp
import numpy as np
import os
from typing import Tuple

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def blur_face_region(image, bbox, blur_factor=100):
    """
    Apply Gaussian blur to a specific region of the image
    
    Args:
        image: Input image (numpy array)
        bbox: Bounding box coordinates (x, y, width, height)
        blur_factor: Intensity of blur (higher = more blur)
    
    Returns:
        Image with blurred region
    """
    x, y, w, h = bbox
    
    # Ensure coordinates are within image bounds
    x = max(0, x)
    y = max(0, y)
    w = min(w, image.shape[1] - x)
    h = min(h, image.shape[0] - y)
    
    if w <= 0 or h <= 0:
        return image
    
    # Extract the face region
    face_region = image[y:y+h, x:x+w]
    
    # Apply Gaussian blur
    blurred_face = cv2.GaussianBlur(face_region, (blur_factor*2+1, blur_factor*2+1), 0)
    
    # Replace the original face region with blurred version
    image[y:y+h, x:x+w] = blurred_face
    
    return image

def detect_and_blur_faces(image, confidence_threshold=0.37):
    """
    Detect faces in an image and blur them
    
    Args:
        image: Input image (numpy array)
        confidence_threshold: Minimum confidence for face detection
    
    Returns:
        Tuple of (processed_image, number_of_faces_detected)
    """
    # Convert BGR to RGB for MediaPipe
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Initialize face detection
    with mp_face_detection.FaceDetection(
        model_selection=0, 
        min_detection_confidence=confidence_threshold
    ) as face_detection:
        
        # Detect faces
        results = face_detection.process(rgb_image)
        
        faces_detected = 0
        
        if results.detections:
            for detection in results.detections:
                # Get bounding box
                bbox = detection.location_data.relative_bounding_box
                
                # Convert relative coordinates to absolute coordinates
                h, w, _ = image.shape
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Add some padding to ensure full face coverage
                padding = 20
                x = max(0, x - padding)
                y = max(0, y - padding)
                width = min(width + 2*padding, w - x)
                height = min(height + 2*padding, h - y)
                
                # Blur the face region
                image = blur_face_region(image, (x, y, width, height))
                faces_detected += 1
        
        return image, faces_detected

def blur_faces_in_image(input_path: str, output_path: str) -> Tuple[bool, str]:
    """
    Process an image file to blur all detected faces
    
    Args:
        input_path: Path to input image
        output_path: Path to save processed image
    
    Returns:
        Tuple of (success, message)
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_path):
            return False, "Input file not found"
        
        # Read the image
        image = cv2.imread(input_path)
        
        if image is None:
            return False, "Could not read image file. Please check the file format."
        
        # Detect and blur faces
        processed_image, faces_count = detect_and_blur_faces(image)
        
        # Save the processed image
        success = cv2.imwrite(output_path, processed_image)
        
        if not success:
            return False, "Failed to save processed image"
        
        message = f"Successfully processed image. {faces_count} face(s) detected and blurred."
        return True, message
        
    except Exception as e:
        return False, f"Error processing image: {str(e)}"

def blur_faces_in_video(input_path: str, output_path: str) -> Tuple[bool, str]:
    """
    Process a video file to blur all detected faces frame by frame
    
    Args:
        input_path: Path to input video
        output_path: Path to save processed video
    
    Returns:
        Tuple of (success, message)
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_path):
            return False, "Input file not found"
        
        # Open the video file
        cap = cv2.VideoCapture(input_path)
        
        if not cap.isOpened():
            return False, "Could not open video file. Please check the file format."
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Define codec and create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        if not out.isOpened():
            cap.release()
            return False, "Could not create output video file"
        
        frame_count = 0
        total_faces_detected = 0
        
        print(f"Processing video: {total_frames} frames at {fps} FPS")
        
        # Process each frame
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Detect and blur faces in current frame
            processed_frame, faces_in_frame = detect_and_blur_faces(frame)
            total_faces_detected += faces_in_frame
            
            # Write the processed frame
            out.write(processed_frame)
            
            frame_count += 1
            
            # Print progress every 30 frames
            if frame_count % 30 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"Progress: {progress:.1f}% ({frame_count}/{total_frames} frames)")
        
        # Release everything
        cap.release()
        out.release()
        
        # Clean up input file
        try:
            os.remove(input_path)
        except:
            pass
        
        message = f"Successfully processed video. {total_faces_detected} face instances detected and blurred across {frame_count} frames."
        return True, message
        
    except Exception as e:
        # Clean up on error
        try:
            if 'cap' in locals():
                cap.release()
            if 'out' in locals():
                out.release()
        except:
            pass
        
        return False, f"Error processing video: {str(e)}"

def get_video_info(video_path: str) -> dict:
    """
    Get basic information about a video file
    
    Args:
        video_path: Path to video file
    
    Returns:
        Dictionary with video information
    """
    try:
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            return {"error": "Could not open video file"}
        
        info = {
            "fps": int(cap.get(cv2.CAP_PROP_FPS)),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "duration": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / int(cap.get(cv2.CAP_PROP_FPS))
        }
        
        cap.release()
        return info
        
    except Exception as e:
        return {"error": f"Error getting video info: {str(e)}"}
Eye Blink and Hand Gesture Detection using OpenCV, CVZone and PyAutoGUI

This repository contains Python scripts for real-time eye blink and hand gesture detection using OpenCV and PyAutoGUI. The project is split into two main components:

1. **Eye Blink Detection:** This component detects eye blinks using the face landmarks detected by OpenCV's DNN-based face mesh detector. It calculates the eye aspect ratio (EAR) to determine blinks. Upon detecting a blink, it simulates pressing the space bar using PyAutoGUI.

2. **Hand Gesture Detection:** This component detects hand gestures, specifically the gesture of pinching thumb and index finger together, using OpenCV and the HandTrackingModule from the cvzone library. Upon detecting the gesture, it simulates pressing the space bar using PyAutoGUI.

Installation

1. Clone the repository to your local machine:

2. Install the required dependencies:

pip install -r requirements.txt

Usage

1. Run the `eye_blink_detection.py` script to start eye blink detection:

python eye_blink_detection.py


2. Run the `hand_gesture_detection.py` script to start hand gesture detection:

python hand_gesture_detection.py

Additional Notes

- Ensure your webcam is connected and accessible by OpenCV.
- Adjust parameters such as `detectionCon` in `HandDetector` and `FaceMeshDetector` classes to fine-tune the detection sensitivity.
- Press `q` to exit the detection scripts.

import cv2 as cv
import pyautogui
from cvzone.HandTrackingModule import HandDetector
import cvzone

# Initialize the webcam
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Initialize hand detector from cvzone library
detector = HandDetector(detectionCon=0.8)

# Initialize flag to track click
click_registered = False

clickCounter = 0

# Main loop
while True:
    # Read frame from webcam
    success, img = cap.read()
    img = cv.flip(img, 1)  # Flip horizontally for mirror effect

    # Find hands in the frame
    hands, _ = detector.findHands(img)

    if hands:
        # Get the details of the first hand
        hand1 = hands[0]
        lmList1 = hand1['lmList']

        # Calculate distance between thumb and index finger
        length, _, _ = detector.findDistance(lmList1[8][:2], lmList1[4][:2], img)
        
        # If fingers are touching and click is not already registered, perform click
        if length < 30 and not click_registered:
            clickCounter += 1
            # Simulate pressing space bar on blink
            pyautogui.press('space')
            click_registered = True  # Set flag to indicate click is registered
        
        # If fingers are not touching, reset the click flag
        elif length >= 30:
            click_registered = False
        
        # Display blink count on the image
        cvzone.putTextRect(img, f'Blink Count: {clickCounter}', (50,100))

    # Uncomment if you want to see output and plot.
    # cv.imshow('Image', img)         
   
    # Break the loop if 'q' is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv.destroyAllWindows()

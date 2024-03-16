import cv2
import pyautogui
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import cvzone

# Initialize video capture from default camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Initialize face mesh detector with maximum number of faces to detect as 1
detector = FaceMeshDetector(maxFaces=1)

# Initialize live plot for visualization
plotY = LivePlot(640, 360, [20,50])

# Define a list of landmark IDs that correspond to the eyes and eyebrows
idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]

# Initialize variables for blink detection
ratioList = []
blinkCounter = 0
counter = 0
color = (255,0,255)  # Initial color for visualizing landmarks

# Main loop for video processing
while True:
    success, img = cap.read()  # Read a frame from the video capture

    # Detect face mesh in the frame
    img, faces = detector.findFaceMesh(img, draw=False)

    # Check if face is detected
    if faces:
        face = faces[0]  # Extract the first face detected
        for id in idList:
            # Draw circles on specified landmark points of the face
            cv2.circle(img, face[id], 5, color, cv2.FILLED)

        # Define points for drawing lines to calculate eye aspect ratio
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]

        # Calculate distances between points for eye aspect ratio calculation
        lengthVer,_  = detector.findDistance(leftUp, leftDown)
        lengthHor,_  = detector.findDistance(leftLeft, leftRight)

        # Draw lines between points for visualization
        cv2.line(img, leftUp, leftDown, (0,200,0), 3)
        cv2.line(img, leftLeft, leftRight, (0,200,0), 3)

        # Calculate eye aspect ratio
        ratio = int((lengthVer/lengthHor)*100)

        # Append ratio to list and calculate average ratio
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        # Perform blink detection based on average ratio
        if ratioAvg < 36 and counter == 0:
            blinkCounter += 1
            color = (0,200,0)  # Change color to green when blinking
            counter = 1
            # Simulate pressing space bar on blink
            pyautogui.press('space')

        # Update counter for preventing rapid detection of multiple blinks
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255,0,255)  # Reset color to magenta

        # Display blink count on the frame
        cvzone.putTextRect(img, f'Blink Count: {blinkCounter}', (50,100), colorR=color)

        # Update live plot with current ratio (uncomment if plot is enabled)
        imgPlot = plotY.update(ratioAvg, color)       

        # Stack images horizontally for display
        imgStack = cvzone.stackImages([img,imgPlot], 2, 1) 

    else:
        # Stack images horizontally when no face is detected
        imgStack = cvzone.stackImages([img,img], 2, 1)

    # Display the stacked images
    # Uncomment if you want to see output and plot.
    # cv2.imshow('Image', imgStack)         

    # Check for 'q' key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()

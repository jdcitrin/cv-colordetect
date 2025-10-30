import cv2
from util import get_limits
from PIL import Image
import numpy as np


#creates an array of colors to detect
colors = {
    "green": [0, 255, 0],
    "blue": [255, 0, 0],
}
cap = cv2.VideoCapture(0) #choose which webcam to use

while True:
    ret, frame = cap.read() #ret is bool to check if cam works, frame is the image from cam
    if not ret: 
        break

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #converts bgr image to hsv (hue, saturation, value), better for color detection

    #loops through each color in the array above
    for color_name, bgr_color in colors.items():
        #gets the color limits for the current color
        lowerlimit, upperlimit = get_limits(color = bgr_color)

        #creates mask only showing pixels within the color limits
        mask = cv2.inRange(hsvImage, lowerlimit, upperlimit) #creates mask only showing pixels within the color limits

        maskbox = Image.fromarray(mask) #creates pillow image from mask array, white if true black if not
        box = maskbox.getbbox() #creates bounding box around white

        if box is not None:
            x1, y1, x2, y2 = box #unpacks box coords
            #creates a new frame for each color detected, cycling through while process is active.
            frame = cv2.rectangle(frame, (x1,y1), (x2,y2), bgr_color, 5) #draws rectangle on original frame



    #shows the frame with the detected colors
    cv2.imshow('frame', frame) 


    if cv2.waitKey(1) & 0xFF == ord('q'): #if q pressed, break
        break

cap.release() #frees cam

cv2.destroyAllWindows() 


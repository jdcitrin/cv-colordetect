import cv2
from util import get_limits
from PIL import Image
import numpy as np

kernel = np.ones((9,9),np.uint8) #kernel for smoothing mask
#sees wheteher to keep or discard pixel in mask based on neighbors

#creates an array of colors to detect
colors = {
    "green": [0, 255, 0],
    #"blue": [255, 0, 0],
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

        mask = cv2.erode(mask, kernel, iterations = 2) #erodes to remove noise
        mask = cv2.dilate(mask, kernel, iterations = 2) #dilates to restore size after erosion

        maskbox = Image.fromarray(mask) #creates pillow image from mask array, white if true black if not
        box = maskbox.getbbox() #creates bounding box around white

        if box is not None:
            x1, y1, x2, y2 = box #unpacks box coords
            #creates a new frame for each color detected, cycling through while process is active.
            frame = cv2.rectangle(frame, (x1,y1), (x2,y2), bgr_color, 5) #draws rectangle on original frame

            #calculate position for text label
            text_x = x1
            text_y = y1 - 10 #above bbox

            #adds text label above the bounding box
            frame = cv2.putText(
                img=frame,                       # img to draw on
                text=color_name.upper(),         # text
                org=(text_x, text_y),            #top left
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,  
                fontScale= 1.5,            
                color=bgr_color,                #matches bbox color
                thickness=3     
            )




    #shows the frame with the detected colors
    cv2.imshow('frame', frame) 


    if cv2.waitKey(1) & 0xFF == ord('q'): #if q pressed, break
        break

cap.release() #frees cam

cv2.destroyAllWindows() 


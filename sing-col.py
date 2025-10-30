import cv2
from util import get_limits
from PIL import Image

green = [0, 255, 0] #color im assigning
cap = cv2.VideoCapture(0) #choose which webcam to use

while True:
    ret, frame = cap.read() #ret is bool to check if cam works, frame is the image from cam
    if not ret: 
        break

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #converts bgr image to hsv (hue, saturation, value), better for color detection

    lowerlimit, upperlimit = get_limits(color = green) 
    mask = cv2.inRange(hsvImage, lowerlimit, upperlimit) #creates mask only showing pixels within the color limits


    maskbox = Image.fromarray(mask) #creates pillow image from mask array, white if true black if not
    box = maskbox.getbbox() #creates bounding box around white

    if box is not None:
        x1, y1, x2, y2 = box #unpacks box coords

        frame = cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 5) #draws rectangle on original frame

    cv2.imshow('frame', frame) 

    

    if cv2.waitKey(1) & 0xFF == ord('q'): #if q pressed, break
        break

cap.release() #frees cam

cv2.destroyAllWindows() 


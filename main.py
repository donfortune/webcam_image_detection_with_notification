import cv2
import time

video = cv2.VideoCapture(0) #opens your webcam
time.sleep(1)
while True:

    check, frame = video.read() #two variables because the video.read method returns two values
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert rgb frame to gray scale frame
    gray_blur = cv2.GaussianBlur(gray_frame, (21, 21), 0) #blur the grayscale image

    cv2.imshow('My Video', gray_blur)


    key = cv2.waitKey(1) #create keyboard key object
    if key == ord('q'):
        break

video.release()







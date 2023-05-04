
import cv2
import time
from send_email import send_email
import glob
import os
from threading import Thread


video = cv2.VideoCapture(0) #opens your webcam
time.sleep(1)
first_frame = None
status_list = []
count = 1


def clean_images_folder(): #function to remove images inside folder and email is sent
    pictures = glob.glob("images/*.png")
    for picture in pictures:
        os.remove(picture)
while True:
    status = 0  #no objcet in frame
    check, frame = video.read() #two variables because the video.read method returns two values

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert rgb frame to gray scale frame
    gray_blur = cv2.GaussianBlur(gray_frame, (21, 21), 0) #blur the grayscale image


    if first_frame is None:   #secure value of first frame
        first_frame = gray_blur

    delta_frame = cv2.absdiff(first_frame, gray_blur)
    thresh_frame = cv2.threshold(delta_frame, 70, 255, cv2.THRESH_BINARY)[1]
    dilated_frame = cv2.dilate(thresh_frame, None, iterations=2) #remove the noise from frame

    cv2.imshow('My Video', thresh_frame)
    contours, check = cv2.findContours(dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000:  #detect objects that enter the frame
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3) #draw a rectangle around detected object
        if rectangle.any():
            status = 1  #object in frame
            cv2.imwrite(f"images/{count}.png", frame)  # save the captured image
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            main_image = all_images[index]



    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(main_image,))
        email_thread.daemon = True #allow send email function to be executed in the background
        clean_thread = Thread(target=clean_images_folder)
        clean_thread.daemon = True  # clean_images_folder function to be executed in the background
        email_thread.start()
        clean_thread.start()




    cv2.imshow('Video', frame)
    key = cv2.waitKey(1) #create keyboard key object
    if key == ord('q'): #the program ends when you press the q key on keyboard
        break

video.release()
clean_thread.start() #deletes images when user quits program







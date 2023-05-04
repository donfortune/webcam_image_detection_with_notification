import cv2
import time
from send_email import send_email
import glob


video = cv2.VideoCapture(0) #opens your webcam
time.sleep(1)
first_frame = None
status_list = []
count = 1
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
        send_email(main_image)


    cv2.imshow('Video', frame)
    key = cv2.waitKey(1) #create keyboard key object
    if key == ord('q'):
        break

video.release()







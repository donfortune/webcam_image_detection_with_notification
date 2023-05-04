import streamlit as st
import time
import cv2

current_time = time.time()
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
#print(formatted_time)  # Output: 2023-05-04 10:14:56


st.title('Motion Detection')
start = st.button('Start Camera')

if start:
    image = st.image([])
    video = cv2.VideoCapture(0)

    while True:
        check, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(img=frame, text=formatted_time, org=(50, 50), fontScale=2, color=(255, 255, 255), thickness=2,
                    lineType=cv2.LINE_AA, fontFace=cv2.FONT_HERSHEY_PLAIN)
        image.image(frame)

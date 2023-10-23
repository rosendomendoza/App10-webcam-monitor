# Introducing me in webcam function
import streamlit as st
import cv2
from datetime import datetime
import calendar

st.set_page_config("Motion Detection", layout="centered")
st.title("Motion Detection")

start = st.button("Start Camera")

#now = datetime.now()


if start:
    streamlit_imagen = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        check, frame = camera.read()
        now = datetime.now()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.putText(frame, now.strftime("%A"), (50, 50),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=2,
                    color=(255, 255, 255),
                    thickness=2,
                    lineType=cv2.LINE_AA
                    )
        cv2.putText(frame, now.strftime("%H:%M:%S"), (50, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=2,
                    color=(255, 0, 0),
                    thickness=2,
                    lineType=cv2.LINE_AA
                    )
        streamlit_imagen.image(frame)

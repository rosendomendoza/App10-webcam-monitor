import glob
import os
import time
from datetime import datetime
import cv2
from emailing import send_email
import shutil

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1
while True:
    status = 0

    # Original Color Frame
    check, frame = video.read()

    # Transform the original in a most efficient Frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (11,11), 0)


    if first_frame is None:
        first_frame = gray_frame_gau

    # Calculates the difference between the original frame and the last one.
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    # cv2.imshow("My Video", delta_frame)
    thresh_frame = cv2.threshold(delta_frame, 60, 255,
                                 cv2.THRESH_BINARY)[1]
    #cv2.imshow("My Video", thresh_frame)
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) <5000:
            continue
        else:
            x, y, h , w = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(frame, (x, y), (x+h, y+w), (0, 255, 0), 3)
            if rectangle.any():
                status = 1
                cv2.imwrite(f"images/capture/{count}.png", frame)
                count = count + 1

    status_list.append(status)
    status_list = status_list[-2:]

    # If the object get out of the webcam
    if status_list[0] == 1 and status_list[1] == 0:

        # Select the image to send
        all_images = glob.glob("images/capture/*png")
        index = int(len(all_images) / 2)
        image2send = all_images[index]
        img_name = datetime.now().strftime("%Y%m%d-%H.%M.%S") + ".png"

        # Store image to send
        img_path = f"images/send/{img_name}"
        shutil.copy(f"{image2send}", img_path)
        # Remove the unused images
        shutil.rmtree("images/capture")
        os.makedirs("images/capture/")

        # Send the notification with the selected image
        send_email(img_path)
        count = 1

    cv2.imshow("My Video", frame)


    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()

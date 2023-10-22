import time
import cv2

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
while True:
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
            cv2.rectangle(frame, (x, y), (x+h, y+w), (0, 255, 0), 3)
            cv2.imshow("My Video", frame)


    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()

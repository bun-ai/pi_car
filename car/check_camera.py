import cv2
from myconfig import IMAGE_W, IMAGE_H

WIDTH = 160


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3, IMAGE_W)
    cap.set(4, IMAGE_H)

    while True:
        success, img = cap.read()

        cv2.imshow("Output", img)
        cv2.waitKey(1)

import cv2
import img_handle
import uuid
from PIL import Image
import os


def main():
    cap = cv2.VideoCapture(0)  # video capture source camera (Here webcam of laptop)
    ret, frame = cap.read()  # return a single frame in variable `frame`

    name = f'user_img_{uuid.uuid4()}.png'
    img_handle.save_img(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)), os.path.join('static', 'data', 'user'),
                        name)

    cap.release()


if __name__ == '__main__':
    main()

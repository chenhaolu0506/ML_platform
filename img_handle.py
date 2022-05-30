import os
import cv2


def save_img(image, directory, name):
    dst = os.path.join(directory, name)
    # cv2.imwrite(dst, image)
    image.save(dst)


def get_img(name):
    return cv2.imread(name)


def move_img(img_name, src_dir, dst_dir):
    src_path = os.path.join(src_dir, img_name)
    dst_path = os.path.join(dst_dir, img_name)
    os.rename(src_path, dst_path)

import os
import cv2
import numpy as np
from PIL import Image, ImageOps


def get_word_bbox(source_size: tuple[int, int],
                  mask: Image.Image,
                  corner: tuple[int, int]) -> list[list[int]]:
    tmp = Image.new("L", source_size)
    tmp.paste(ImageOps.colorize(mask, (0, 0, 0), (255, 255, 255)), corner, mask)
    np_tmp = np.array(tmp)

    contours, _ = cv2.findContours(np_tmp, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.intp(box)

    return box.tolist()


def build_word_info(
        word: str,
        box: list[list[int]],
        font_name: str,
        font_size: int,
        color: str | None=None):
    font_name = font_name.replace('\\', '/')
    font_name = os.path.split(font_name)[-1]
    return {
        "word": word,
        "bbox": box,
        "font_name": font_name,
        "font_size": font_size,
        "color": color
    }


def create_folder_if_not_exist(path: str, folder: str) -> None:
    pp = os.path.join(path, folder)
    if not os.path.exists(pp):
        os.makedirs(pp)

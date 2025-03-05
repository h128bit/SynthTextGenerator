import numpy as np
from PIL import Image
import cv2


def random_perspective_transform(image: Image.Image, coef: int=8) -> Image.Image:
    image = np.array(image)

    h, w = image.shape

    """
    a----b
    |    |
    c----d
    """

    a, b, c, d = [0, 0], [w, 0], [0, h], [w, h]
    # horizontal transform coeficient
    h_coef = w//coef + 1
    h_side_a = np.random.randint(0, h_coef)
    h_side_b = np.random.randint(0, h_coef)

    # vertical transform coeficient
    v_coef = h//coef + 1
    v_side_a = np.random.randint(0, v_coef)
    v_side_b = np.random.randint(0, v_coef)

    # horizontal transform
    if np.random.randint(0, 2) == 1:
        # top side
        if np.random.randint(0, 2) == 1:
            a[0] += h_side_a
            b[0] -= h_side_b
        # dottom side
        else:
            c[0] += h_side_a
            d[0] -= h_side_b
    # vertical transforms
    if np.random.randint(0, 2) == 1:
        # right side
        if np.random.randint(0, 2) == 1:
            b[0] += v_side_a
            d[0] -= v_side_b
        # left side
        else:
            a[0] += v_side_a
            c[0] -= v_side_b

    pts1 = np.float32([[0, 0], [w, 0],
                       [0, h], [w, h]])
    pts2 = np.float32([a, b,
                       c, d])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image.copy(), matrix, (w, h))

    return Image.fromarray(result)

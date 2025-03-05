import numpy as np


def get_color() -> str:
    a = [chr(i) for i in range(ord('a'), ord('f') + 1)] + [str(i) for i in range(0, 10)]
    return '#' + ''.join(np.random.choice(a, 6))
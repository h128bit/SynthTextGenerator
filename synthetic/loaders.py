import os

import numpy as np
from PIL import Image


def load_random_word_from_corpus(path_to_corpus: str, encoding: str):
    with open(path_to_corpus, 'r', encoding=encoding) as f:
        words_list = f.read().split('\n')

    def get_random_word():
        return np.random.choice(words_list)
    return get_random_word


def load_random_background(path_to_background_or_list_names: str | list[str]):
    if isinstance(path_to_background_or_list_names, list):
        files_name = path_to_background_or_list_names
    else:
        files_name = os.listdir(path_to_background_or_list_names)
        files_name = [os.path.join(path_to_background_or_list_names, name) for name in files_name]

    def load_background():
        name = np.random.choice(files_name)
        return Image.open(name)

    return load_background


def load_random_font(path_to_fonts_or_list_fonts: str | list[str]):
    if isinstance(path_to_fonts_or_list_fonts, list):
        files_name = path_to_fonts_or_list_fonts
    else:
        files_name = os.listdir(path_to_fonts_or_list_fonts)
        files_name = [os.path.join(path_to_fonts_or_list_fonts, name) for name in files_name]

    def load_font():
        return np.random.choice(files_name)

    return load_font





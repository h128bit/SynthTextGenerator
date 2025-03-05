import time

from synthetic import generate


path_to_background = "resources/backgrounds"
path_to_fonts = "resources/fonts"
path_to_corpus = "resources/corpus/russian.txt"
path_to_save = "resources/result"
encoding='windows-1251'

d = {
    "path_to_corpus": path_to_corpus,
    "encoding": encoding,
    "path_to_fonts": path_to_fonts,
    "path_to_background": path_to_background,
    "path_to_save": path_to_save,
    "num_images": 2
}

start = time.time()

generate(**d)

result_time = time.time() - start

print(f"{result_time} sec")
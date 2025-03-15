import cv2
import json
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFilter

from .tools import *
from .loaders import *
from .generator import *
from .geometric_transforms import *


def generate(path_to_corpus: str,
             encoding: str,
             path_to_fonts: str | list[str],
             path_to_background: str | list[str],
             path_to_save: str,
             num_images: int=5,
             font_size_range: tuple[int, int]=(14, 81),
             max_blur_kernel_size: int=5,
             num_words_range: tuple[int, int]=(5, 101),
             angle_range: tuple[int, int]=(-5, 5),
             max_trying_generate = 100,
             transform=True,
             quality_output_image: int=95) -> None:

    """
    Method for generate text scene.
    Save result in path_to_save folder, create folders src for save text scenes, mask for save masked text scenes
    and create json file meta_info.json with information about text scenes

    :param path_to_corpus: path to language word corpus
    :param encoding: encoding for corus file
    :param path_to_fonts: path to folder with fonts or list with paths to the font
    :param path_to_background: path to folder with images or list with paths to the images
    :param path_to_save: path to save result
    :param num_images: total number result images
    :param font_size_range: font size range like (min size, max size)
    :param max_blur_kernel_size: max size kernel for blur text
    :param num_words_range: number words on image
    :param angle_range: angle range
    :param max_trying_generate: maximum number trying to generate one word on image
    :param transform: bool, flag -- do perspective transform and blur image or no
    :param quality_output_image: quality output image. Is parameter quality in PIL.Image.save
    :return: None
    """

    get_word = load_random_word_from_corpus(path_to_corpus, encoding)
    get_backgrond = load_random_background(path_to_background)
    get_font = load_random_font(path_to_fonts)

    create_folder_if_not_exist(path_to_save, "src")
    create_folder_if_not_exist(path_to_save, "mask")

    meta_dict = {}

    for image_num in range(num_images):
        background = get_backgrond()
        w, h = background.size
        im_mask = Image.new("L", [w, h])

        num_words = np.random.randint(*num_words_range)
        num_words_counter = 0
        words_info = []

        shift = 0
        for _ in range(num_words):
            # place text on image and check what text boxes do not cross
            # else change word, font property and text location
            for _ in range(max_trying_generate):
                font_size = np.random.randint(*font_size_range)
                font_name = get_font()
                font = ImageFont.truetype(font_name, font_size, encoding='utf-8')
                angle = np.random.randint(*angle_range)
                string = get_word()

                bbox = font.getbbox(string)
                left_up_x, left_up_y = np.random.randint(0, w - w // 8), np.random.randint(0, h - h // 8)

                if left_up_x + bbox[2] + 5 > w or left_up_y + bbox[3] + 5 > h:
                    continue

                mask = Image.new("L", bbox[2:4])
                dmask = ImageDraw.Draw(mask)
                dmask.rectangle([(10, 10), (bbox[2], bbox[3])], fill="#ffffff")
                mask = mask.rotate(angle, expand=1)

                im_mask_copy = im_mask.copy()
                im_mask_copy.paste(
                    ImageOps.colorize(mask, (0, 0, 0), (255, 255, 255)),
                    (left_up_x, left_up_y),
                    mask)

                np_mask_copy = np.array(im_mask_copy)
                contours, _ = cv2.findContours(np_mask_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

                if num_words_counter + shift < len(contours):
                    im_mask = im_mask_copy

                    txt = Image.new('L', bbox[2:4])
                    dtxt = ImageDraw.Draw(txt)
                    word_color = get_color()
                    dtxt.text((0, 0), string, font=font, fill=word_color)

                    txt = txt.rotate(angle, expand=1)
                    if transform and np.random.randint(0, 3) == 1:
                        txt = txt.filter(ImageFilter.BoxBlur(np.random.randint(0, max_blur_kernel_size)))
                        txt = random_perspective_transform(txt, 16)

                    background.paste(
                        ImageOps.colorize(txt, get_color(), get_color()),
                        (left_up_x, left_up_y),
                        txt)

                    bbox = get_word_bbox((w, h), mask, (left_up_x, left_up_y))
                    words_info.append(
                        build_word_info(string, bbox, font_name, font_size, word_color)
                    )

                    num_words_counter += 1
                    break
            else:
                shift += 1

        name = f"{image_num}.png"
        background.save(os.path.join(path_to_save, "src", name), optimize=True, quality=quality_output_image)
        im_mask.save(os.path.join(path_to_save, 'mask', f'mask_{name}'))
        meta_dict[name] = words_info

    json_string = json.dumps(meta_dict)

    with open(os.path.join(path_to_save, "meta_info.json"), 'w', encoding="utf-8") as f:
        f.write(json_string)



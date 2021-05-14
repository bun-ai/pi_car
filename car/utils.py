import numpy as np
import random

from typing import List, Any, Tuple
from PIL import Image


ONE_BYTE_SCALE = 1.0 / 255.0


def map_range(x, x_min, x_max, y_min, y_max):
    """
    Linear mapping between two ranges of values
    """
    x_range = x_max - x_min
    y_range = y_max - y_min
    xy_ratio = x_range/y_range

    y = ((x - x_min) / xy_ratio + y_min) // 1
    return int(y)


def map_range_float(x, x_min, x_max, y_min, y_max):
    """
    Same as map_range but supports floats return, rounded to 2 decimal places
    """
    x_range = x_max - x_min
    y_range = y_max - y_min
    xy_ratio = x_range/y_range

    y = ((x - x_min) / xy_ratio + y_min)

    # print("y= {}".format(y))

    return round(y, 2)


def rgb2gray(rgb):
    """
    Convert normalized numpy image array with shape (w, h, 3) into greyscale
    image of shape (w, h)
    :param rgb:     normalized [0,1] float32 numpy image array or [0,255] uint8
                    numpy image array with shape(w,h,3)
    :return:        normalized [0,1] float32 numpy image array shape(w,h) or
                    [0,255] uint8 numpy array in grey scale
    """
    # this will translate a uint8 array into a float64 one
    grey = np.dot(rgb[..., :3], [0.299, 0.587, 0.114])

    # transform back if the input is a uint8 array
    if rgb.dtype.type is np.uint8:
        grey = round(grey).astype(np.uint8)
    return grey


def load_pil_image(filename, cfg):
    """
    Loads an image from a file path as a PIL image. Also handles resizing.

    Args:
        filename (string): path to the image file
        cfg (object): donkey configuration file

    Returns: a PIL image.
    """
    try:
        img = Image.open(filename)
        if img.height != cfg.IMAGE_H or img.width != cfg.IMAGE_W:
            img = img.resize((cfg.IMAGE_W, cfg.IMAGE_H))

        if cfg.IMAGE_DEPTH == 1:
            img = img.convert('L')

        return img

    except Exception as e:
        print(e)
        print('failed to load image:', filename)
        return None


def load_image(filename, cfg):
    """
    :param string filename: path to image file
    :param cfg: donkey config
    :return np.ndarray: numpy uint8 image array
    """
    img = load_pil_image(filename, cfg)

    if not img:
        return None

    img_arr = np.asarray(img)

    # If the PIL image is greyscale, the np array will have shape (H, W)
    # Need to add a depth channel by expanding to (H, W, 1)
    if img.mode == 'L':
        h, w = img_arr.shape[:2]
        img_arr = img_arr.reshape(h, w, 1)

    return img_arr


def normalize_image(img_arr_uint):
    """
    Convert uint8 numpy image array into [0,1] float image array
    :param img_arr_uint: [0,255]uint8 numpy image array
    :return: [0,1] float32 numpy image array
    """
    return img_arr_uint.astype(np.float64) * ONE_BYTE_SCALE


def denormalize_image(img_arr_float):
    """
    :param img_arr_float: [0,1] float numpy image array
    :return: [0,255] uint8 numpy image array
    """
    return (img_arr_float * 255.0).astype(np.uint8)


def train_test_split(data_list: List[Any],
                     shuffle: bool = True,
                     test_size: float = 0.2) -> Tuple[List[Any], List[Any]]:
    """
    take a list, split it into two sets while selecting a
    random element in order to shuffle the results.
    use the test_size to choose the split percent.
    shuffle is always True, left there to be backwards compatible
    """
    target_train_size = int(len(data_list) * (1. - test_size))

    if shuffle:
        train_data = []
        i_sample = 0
        while i_sample < target_train_size and len(data_list) > 1:
            i_choice = random.randint(0, len(data_list) - 1)
            train_data.append(data_list.pop(i_choice))
            i_sample += 1

        # remainder of the original list is the validation set
        val_data = data_list

    else:
        train_data = data_list[:target_train_size]
        val_data = data_list[target_train_size:]

    return train_data, val_data

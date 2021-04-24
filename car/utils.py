import numpy as np


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

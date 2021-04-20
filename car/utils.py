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

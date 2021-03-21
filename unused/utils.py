def map_range(x, x_min, x_max, y_min, y_max):
    """
    Linear mapping between two ranges of values
    """
    x_range = x_max - x_min
    y_range = y_max - y_min
    xy_ratio = x_range/y_range

    y = ((x - x_min) / xy_ratio + y_min) // 1
    return int(y)

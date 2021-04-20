import os
import types
import time

import Adafruit_PCA9685

from car import config
from car.utils import map_range, map_range_float


if __name__ == '__main__':
    cfg = config.load_config()

    print((map_range(0.5, -1, 1, cfg.THROTTLE_REVERSE_PWM, cfg.THROTTLE_FORWARD_PWM)))

    print((map_range_float(397, cfg.THROTTLE_REVERSE_PWM, cfg.THROTTLE_FORWARD_PWM, -1, 1)))

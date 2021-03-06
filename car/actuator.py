"""
actuators.py
Classes to control the motors and servos. These classes
are wrapped in a mixer class before being used in the drive loop.
"""

import time
import Adafruit_PCA9685
from Adafruit_GPIO import I2C

from car.utils import map_range


class PCA9685:
    """
    PWM motor controller using PCA9685 boards.
    This is used for most RC Cars
    """

    def __init__(self, channel, address=0x40, frequency=60, bus_num=None, init_delay=0.1):
        self.default_freq = 60
        self.pwm_scale = frequency / self.default_freq
        # Initialise the PCA9685 using the default address (0x40).
        self.pwm = Adafruit_PCA9685.PCA9685(address=address)
        self.pwm.set_pwm_freq(frequency)
        self.channel = channel

        if bus_num is not None:
            def get_bus():
                return bus_num
            I2C.get_default_bus = get_bus

        time.sleep(init_delay)

    def set_pulse(self, pulse):
        self.pwm.set_pwm(self.channel, 0, int(pulse * self.pwm_scale))

    def run(self, pulse):
        self.set_pulse(pulse)


class PiGPIO_PWM:
    """
    # Use the pigpio python module and daemon to get hardware pwm controls from
    # a raspberrypi gpio pins and no additional hardware. Can serve as a replacement
    # for PCA9685.
    #
    # Install and setup:
    # sudo update && sudo apt install pigpio python3-pigpio
    # sudo systemctl start pigpiod
    #
    # Note: the range of pulses will differ from those required for PCA9685
    # and can range from 12K to 170K
    #
    # If you use a control circuit that inverts the steering signal, set inverted to True
    # Default multipler for pulses from config etc is 100
    """

    def __init__(self, pin, pgio=None, freq=75, inverted=False):
        import pigpio

        self.pin = pin
        self.pgio = pgio or pigpio.pi()
        self.freq = freq
        self.inverted = inverted
        self.pgio.set_mode(self.pin, pigpio.OUTPUT)

    def __del__(self):
        self.pgio.stop()

    def set_pulse(self, pulse):
        self.pgio.hardware_PWM(
            self.pin, self.freq, int(pulse if not self.inverted else 1e6 - pulse)
        )

    def run(self, pulse):
        self.set_pulse(pulse)


class PWMSteering:
    """
    Wrapper over a PWM motor controller to convert angles to PWM pulses.
    """

    def __init__(self,
                 controller=None,
                 left_pulse=240,
                 right_pulse=500):

        self.LEFT_ANGLE = -1
        self.RIGHT_ANGLE = 1
        self.controller = controller
        self.left_pulse = left_pulse
        self.right_pulse = right_pulse
        self.pulse = map_range(
            0, self.LEFT_ANGLE, self.RIGHT_ANGLE, self.left_pulse, self.right_pulse
        )
        self.running = True
        print("PWM Steering created")

    def update(self):
        while self.running:
            self.controller.set_pulse(self.pulse)

    def run_threaded(self, angle):
        # map absolute angle to angle that vehicle can implement.
        self.pulse = map_range(
            angle, self.LEFT_ANGLE, self.RIGHT_ANGLE, self.left_pulse, self.right_pulse
        )

    def run(self, angle):
        self.run_threaded(angle)
        self.controller.set_pulse(self.pulse)

    def shutdown(self):
        # set steering straight
        self.pulse = 0
        time.sleep(0.3)
        self.running = False


class PWMThrottle:
    """
    Wrapper over a PWM motor controller to convert -1 to 1 throttle
    values to PWM pulses.
    """

    def __init__(self, controller=None, max_pulse=420, min_pulse=330, zero_pulse=380):

        self.MIN_THROTTLE = -1
        self.MAX_THROTTLE = 1
        self.controller = controller
        self.max_pulse = max_pulse
        self.min_pulse = min_pulse
        self.zero_pulse = zero_pulse
        self.pulse = zero_pulse

        # send zero pulse to calibrate ESC
        print("Init ESC")
        self.controller.set_pulse(self.max_pulse)
        time.sleep(0.01)
        self.controller.set_pulse(self.min_pulse)
        time.sleep(0.01)
        self.controller.set_pulse(self.zero_pulse)
        time.sleep(1)
        self.running = True
        print("PWM Throttle created")

    def update(self):
        while self.running:
            self.controller.set_pulse(self.pulse)

    def run_threaded(self, throttle):
        if throttle > 0:
            self.pulse = map_range(
                throttle, 0, self.MAX_THROTTLE, self.zero_pulse, self.max_pulse
            )
        else:
            self.pulse = map_range(
                throttle, self.MIN_THROTTLE, 0, self.min_pulse, self.zero_pulse
            )

    def run(self, throttle):
        self.run_threaded(throttle)
        self.controller.set_pulse(self.pulse)

    def shutdown(self):
        # stop vehicle
        self.run(0)
        self.running = False

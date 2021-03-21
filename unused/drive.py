from unused.actuator import PCA9685, PWMSteering, PWMThrottle
from car.config import load_config

from unused.vehicle import Vehicle


def demo_drive(cfg):
    veh = Vehicle()

    class MyController:
        """
        a simple controller class that outputs a constant steering and throttle.
        """
        def run(self):
            steer = 0.0
            throt = 0.1
            return steer, throt

    veh.add(MyController(), outputs=['angle', 'throttle'])

    # Drive train setup
    steering_controller = PCA9685(cfg.STEERING_CHANNEL, cfg.PCA9685_I2C_ADDR, bus_num=cfg.PCA9685_I2C_BUSNUM)
    steering = PWMSteering(controller=steering_controller,
                           left_pulse=cfg.STEERING_LEFT_PWM,
                           right_pulse=cfg.STEERING_RIGHT_PWM)

    throttle_controller = PCA9685(cfg.THROTTLE_CHANNEL, cfg.PCA9685_I2C_ADDR, bus_num=cfg.PCA9685_I2C_BUSNUM)
    throttle = PWMThrottle(controller=throttle_controller,
                           max_pulse=cfg.THROTTLE_FORWARD_PWM,
                           zero_pulse=cfg.THROTTLE_STOPPED_PWM,
                           min_pulse=cfg.THROTTLE_REVERSE_PWM)

    veh.add(steering, inputs=['angle'])
    veh.add(throttle, inputs=['throttle'])

    veh.start(rate_hz=cfg.DRIVE_LOOP_HZ, max_loop_count=cfg.MAX_LOOPS)


if __name__ == '__main__':
    cfg = load_config()

    demo_drive(cfg)

import os
import types
import time

import Adafruit_PCA9685


class Config:
    def from_pyfile(self, filename):
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                setattr(self, key, getattr(obj, key))

    def __str__(self):
        result = []
        for key in dir(self):
            if key.isupper():
                result.append((key, getattr(self, key)))
        return str(result)

    def show(self):
        for attr in dir(self):
            if attr.isupper():
                print(attr, ":", getattr(self, attr))


def load_config(config_path=None, myconfig='myconfig.py'):
    if config_path is None:
        import __main__ as main
        main_path = os.path.dirname(os.path.realpath(main.__file__))
        config_path = os.path.join(main_path, 'config.py')
        if not os.path.exists(config_path):
            local_config = os.path.join(os.path.curdir, 'config.py')
            if os.path.exists(local_config):
                config_path = local_config

    print('loading config file: {}'.format(config_path))
    cfg = Config()
    cfg.from_pyfile(config_path)

    # look for the optional myconfig.py in the same path.
    personal_cfg_path = config_path.replace("config.py", myconfig)

    if os.path.exists(personal_cfg_path):
        print("loading personal config over-rides from", myconfig)
        personal_cfg = Config()
        personal_cfg.from_pyfile(personal_cfg_path)
        cfg.from_object(personal_cfg)
    else:
        print("personal config: file not found ", personal_cfg_path)
    return cfg


def demo_servo(pwm, cfg):
    # Move servo on channel O between extremes.
    print(f"Moving servo on channel {cfg.STEERING_CHANNEL}, press Ctrl-C to quit...")

    mid_angle = int((cfg.STEERING_RIGHT_PWM - cfg.STEERING_LEFT_PWM) / 2 + cfg.STEERING_LEFT_PWM)
    step_angle = int((cfg.STEERING_RIGHT_PWM - cfg.STEERING_LEFT_PWM) / 7 // 1)
    pwm.set_pwm(cfg.STEERING_CHANNEL, 0, mid_angle)
    time.sleep(2)

    print("Servo demonstration - start")
    try:
        for angle in range(cfg.STEERING_LEFT_PWM, cfg.STEERING_RIGHT_PWM + 1, step_angle):
            # print('angle', angle)
            pwm.set_pwm(cfg.STEERING_CHANNEL, 0, angle)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Demonstration stopped! Moving servo to middle position.")
        pwm.set_pwm(cfg.STEERING_CHANNEL, 0, mid_angle)

    pwm.set_pwm(cfg.STEERING_CHANNEL, 0, mid_angle)
    print("Servo demonstration - Done")


def demo_throttle(pwm, cfg):
    # Move servo on channel O between extremes.
    print(f"Moving throttle on channel {cfg.THROTTLE_CHANNEL}, press Ctrl-C to quit...")

    pwm.set_pwm(cfg.THROTTLE_CHANNEL, 0, cfg.THROTTLE_STOPPED_PWM)
    time.sleep(1)

    print("Throttle demonstration - start")
    try:
        print("Moving forward")
        for throttle in range(cfg.THROTTLE_STOPPED_PWM, cfg.THROTTLE_FORWARD_PWM, 5):
            # print('throttle', throttle)
            pwm.set_pwm(cfg.THROTTLE_CHANNEL, 0, throttle)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Demonstration stopped!")
        pwm.set_pwm(cfg.THROTTLE_CHANNEL, 0, cfg.THROTTLE_STOPPED_PWM)

    pwm.set_pwm(cfg.THROTTLE_CHANNEL, 0, cfg.THROTTLE_STOPPED_PWM)
    print("Throttle demonstration - Done")


if __name__ == '__main__':
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(60)

    cfg = load_config()

    demo_servo(pwm, cfg)

    demo_throttle(pwm, cfg)

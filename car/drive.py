from car.actuator import PCA9685, PWMSteering, PWMThrottle
from car.config import load_config
from car.camera import PiCamera
from car.vehicle import Vehicle
from car.controller import get_js_controller
from car.tub import TubWriter, TubHandler


def drive(cfg):
    car = Vehicle()

    inputs = []

    # add camera
    if cfg.CAMERA_TYPE == "PICAM":
        cam = PiCamera(image_w=cfg.IMAGE_W,
                       image_h=cfg.IMAGE_H,
                       image_d=cfg.IMAGE_DEPTH,
                       framerate=cfg.CAMERA_FRAMERATE,
                       vflip=cfg.CAMERA_VFLIP,
                       hflip=cfg.CAMERA_HFLIP)
    else:
        raise (Exception("Unkown camera type: %s" % cfg.CAMERA_TYPE))

    car.add(cam, inputs=inputs, outputs=['cam/image_array'], threaded=True)

    # add controller
    if cfg.USE_JOYSTICK_AS_DEFAULT:
        ctrl = get_js_controller(cfg)

    car.add(ctrl,
            inputs=['cam/image_array'],
            outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
            threaded=True)
    ctrl.print_controls()

    # add steering and throttle
    steering_controller = PCA9685(cfg.STEERING_CHANNEL, cfg.PCA9685_I2C_ADDR, bus_num=cfg.PCA9685_I2C_BUSNUM)
    steering = PWMSteering(controller=steering_controller,
                           left_pulse=cfg.STEERING_LEFT_PWM,
                           right_pulse=cfg.STEERING_RIGHT_PWM)

    throttle_controller = PCA9685(cfg.THROTTLE_CHANNEL, cfg.PCA9685_I2C_ADDR, bus_num=cfg.PCA9685_I2C_BUSNUM)
    throttle = PWMThrottle(controller=throttle_controller,
                           max_pulse=cfg.THROTTLE_FORWARD_PWM,
                           zero_pulse=cfg.THROTTLE_STOPPED_PWM,
                           min_pulse=cfg.THROTTLE_REVERSE_PWM)

    car.add(steering, inputs=['user/angle'])
    car.add(throttle, inputs=['user/throttle'])

    # add tub to save data
    inputs = ['cam/image_array', 'user/angle', 'user/throttle', 'user/mode']
    types = ['image_array', 'float', 'float', 'str']
    # do we want to store new records into own dir or append to existing
    tub_path = TubHandler(path=cfg.DATA_PATH).create_tub_path() if cfg.AUTO_CREATE_NEW_TUB else cfg.DATA_PATH
    print('tub_path: ', cfg.DATA_PATH)

    tub_writer = TubWriter(base_path=tub_path, inputs=inputs, types=types)
    car.add(tub_writer, inputs=inputs, outputs=["tub/num_records"],
            run_condition='recording')

    car.start(rate_hz=cfg.DRIVE_LOOP_HZ)


if __name__ == '__main__':
    cfg = load_config()

    drive(cfg)

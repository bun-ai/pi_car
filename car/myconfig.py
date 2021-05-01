import os

# PATHS
CAR_PATH = PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(CAR_PATH, 'data')
MODELS_PATH = os.path.join(CAR_PATH, 'models')

# 9865, over rides only if needed, ie. TX2..
PCA9685_I2C_ADDR = 0x40
PCA9685_I2C_BUSNUM = 1

# STEERING
STEERING_CHANNEL = 1
STEERING_LEFT_PWM = 240
STEERING_RIGHT_PWM = 500

# THROTTLE
THROTTLE_CHANNEL = 0
THROTTLE_FORWARD_PWM = 420
THROTTLE_STOPPED_PWM = 380
THROTTLE_REVERSE_PWM = 330

# VEHICLE
DRIVE_LOOP_HZ = 20
MAX_LOOPS = 220

# JOYSTICK
USE_JOYSTICK_AS_DEFAULT = True  # when starting the manage.py, when True, will not require a --js option to use the joystick
JOYSTICK_MAX_THROTTLE = 1.0     # this scalar is multiplied with the -1 to 1 throttle value to limit the maximum throttle. This can help if you drop the controller or just don't need the full speed available.
JOYSTICK_STEERING_SCALE = 1.0   # some people want a steering that is less sensitve. This scalar is multiplied with the steering -1 to 1. It can be negative to reverse dir.
AUTO_RECORD_ON_THROTTLE = False     # if true, we will record whenever throttle is not zero. if false, you must manually toggle recording with some other trigger. Usually circle button on joystick.
CONTROLLER_TYPE = 'ps4'         # (ps3|ps4|xbox|nimbus|wiiu|F710|rc3|MM1|custom) custom will run the my_joystick.py controller written by the `donkey createjs` command
# USE_NETWORKED_JS = False      # should we listen for remote joystick control over the network?
# NETWORK_JS_SERVER_IP = "192.168.0.1"  # when listening for network joystick control, which ip is serving this information
JOYSTICK_DEADZONE = 0.0         # when non zero, this is the smallest throttle before recording triggered.
JOYSTICK_THROTTLE_DIR = -1.0    # use -1.0 to flip forward/backward, use 1.0 to use joystick's natural forward/backward
# USE_FPV = False                           # send camera data to FPV webserver
JOYSTICK_DEVICE_FILE = "/dev/input/js0"     # this is the unix file use to access the joystick.

# CAMERA
CAMERA_TYPE = 'PICAM'   # (PICAM|WEBCAM|CVCAM|CSIC|V4L|D435|MOCK|IMAGE_LIST)
IMAGE_W = 160
IMAGE_H = 128
IMAGE_DEPTH = 3         # default RGB=3, make 1 for mono
CAMERA_FRAMERATE = DRIVE_LOOP_HZ
CAMERA_VFLIP = False
CAMERA_HFLIP = False

# RECORD OPTIONS
RECORD_DURING_AI = False
AUTO_CREATE_NEW_TUB = False     # create a new tub (tub_YY_MM_DD) directory when recording or append records to data directory directly

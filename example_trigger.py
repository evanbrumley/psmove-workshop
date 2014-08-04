import time
from move import get_remote_controller
from settings import CONTROLLER_URL



if __name__ == "__main__":
    controller = get_remote_controller(CONTROLLER_URL)
	
    while True:
        print controller.trigger
        controller.rumble = controller.trigger
        controller.red = controller.trigger
        time.sleep(0.05)


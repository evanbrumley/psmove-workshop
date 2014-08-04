import time
from move import get_remote_controller
from settings import CONTROLLER_URL



if __name__ == "__main__":
    controller = get_remote_controller(CONTROLLER_URL)
	
    for i in range(50, 255):
        controller.rumble = i
        time.sleep(0.05)

    for i in reversed(range(50, 255)):
        controller.rumble = i
        time.sleep(0.05)

    controller.rumble = 0

    # Turn off everything
    controller.terminate()

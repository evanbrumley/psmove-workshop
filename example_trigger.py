import time
from move import controller


if __name__ == "__main__":	
    while True:
        print controller.trigger
        controller.rumble = controller.trigger
        controller.red = controller.trigger
        time.sleep(0.05)


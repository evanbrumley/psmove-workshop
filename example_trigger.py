import time
from move import get_remote_controller



controller = get_remote_controller("http://localhost:5000/controllers/1/")  # Change me!


if __name__ == "__main__":
    while True:
        print controller.trigger
        controller.rumble = controller.trigger
        controller.red = controller.trigger
        time.sleep(0.05)


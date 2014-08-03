import time
from move import get_remote_controller



controller = get_remote_controller("http://localhost:5000/controllers/1/")  # Change me!


if __name__ == "__main__":
    for i in range(50, 255):
        controller.rumble = i
        time.sleep(0.05)

    for i in reversed(range(50, 255)):
        controller.rumble = i
        time.sleep(0.05)

    controller.rumble = 0

    # Turn off everything
    controller.terminate()

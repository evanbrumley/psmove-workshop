import time
from move import get_remote_controller
from settings import CONTROLLER_URL



if __name__ == "__main__":
    controller = get_remote_controller(CONTROLLER_URL)

    while True:
        # While the 'move' button hasn't been pressed
        while not controller.btn_move:
            # Chill out
            time.sleep(0.05)
        
        # The button has been pressed! Make the light red.
        controller.red = 255

        # While the button is still down
        while controller.btn_move:
            # Chill out
            time.sleep(0.05)

        # The button has been released! Turn off the light.
        controller.red = 0

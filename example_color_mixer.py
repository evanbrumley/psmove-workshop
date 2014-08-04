import time
from move import controller



if __name__ == "__main__":
    while True:
        if controller.btn_triangle:
            controller.green = controller.trigger

        if controller.btn_circle:
            controller.red = controller.trigger

        if controller.btn_cross:
            controller.blue = controller.trigger

        time.sleep(0.1)

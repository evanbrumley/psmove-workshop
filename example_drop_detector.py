import time
from move import controller


if __name__=="__main__":
    while True:
        total_accel = abs(controller.ay) + abs(controller.ax) + abs(controller.az)

        if total_accel < 0.1:
            controller.red = 255
        else:
            controller.red = 0

        time.sleep(0.02)

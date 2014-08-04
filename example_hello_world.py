import time
from move import controller



if __name__ == "__main__":
    # Set the light to pure red
    controller.set_color(255, 0, 0)
   
    # Wait for one second 
    time.sleep(1)
    
    # Set the light to pure green
    controller.set_color(0, 255, 0)
    
    time.sleep(1)
   
    # Set the light to pure blue 
    controller.set_color(0, 0, 255)
    
    time.sleep(1)
   
    # Turn off the light 
    controller.set_color(0, 0, 0)

    # Set the rumble to full power
    controller.set_rumble(255)
    
    time.sleep(1)

    # Turn off the rumble
    controller.set_rumble(0)
    
    time.sleep(1)

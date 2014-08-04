# PS Move Workshop

## First steps

First, install the requirements:

    pip install -r requirements.txt

Next, edit `settings.py` and update `CONTROLLER_ID` to match the number on your controller.

You should now be able to run the example programs:

    python example_hello_word.py

## Using the API

    from move import controller

    controller.rumble = 255

## The controller API

### Things you can set
- `controller.red`: the intensity of the red LED (0-255)
- `controller.green`: the intensity of the green LED (0-255)
- `controller.blue`: the intensity of the blue LED (0-255)
- `controller.rumble`: the rumble intensity (0-255)

Colors can also be set all at once using:

    controller.set_color(<red>, <green>, <blue>)

So to set the controller to bright white, you would use the following:

    controller.set_color(255, 255, 255)

### Things you can read

#### Acceleration

These fields describe the linear acceleration of the controller. For all of these fields, an acceleration of 9.8m/s2 translates to a value of 1.

- `controller.ax`: acceleration in the 'x' direction
- `controller.ay`: acceleration in the 'y' direction
- `controller.az`: acceleration in the 'z' direction

#### Gyroscope

These fields provide the rotational acceleration of the controller. For all of these fields an acceleration of one rotation per second per second should translate to a value of 1.

- `controller.gx`: acceleration in the 'x' direction
- `controller.gy`: acceleration in the 'y' direction
- `controller.gz`: acceleration in the 'z' direction

#### Buttons

- `controller.btn_circle`: provides True if the circle button is currently pressed down. False otherwise
- `controller.btn_cross`: provides True if the cross  button is currently pressed down. False otherwise
- `controller.btn_square`: provides True if the square button is currently pressed down. False otherwise
- `controller.btn_triangle`: provides True if the triangle button is currently pressed down. False otherwise
- `controller.btn_ps`: provides True if the playstation button is currently pressed down. False otherwise
- `controller.btn_select`: provides True if the select button is currently pressed down. False otherwise
- `controller.btn_start`: provides True if the start button is currently pressed down. False otherwise
- `controller.btn_t`: provides True if the trigger button is currently pressed down. False otherwise
- `controller.btn_move`: provides True if the big 'move' button is currently pressed down. False otherwise
- `controller.trigger`: gives a value from 0-255 depending on how far the trigger has been pulled

#### Other stuff
- `controller.battery`: the controller's battery level (0 is empty, 5 is full)

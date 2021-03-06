import sys, os, time
from collections import defaultdict
from threading import Thread
import requests
from settings import CONTROLLER_URL


PSMOVEAPI_BUILD_DIR = os.environ.get('PSMOVEAPI_BUILD_DIR')

if PSMOVEAPI_BUILD_DIR:
    sys.path.insert(0, os.environ['PSMOVEAPI_BUILD_DIR'])
    import psmove


class Controller(object):
    _active = False
    _loop_thread = None

    controller = None
    read_only = False

    red = 0
    green = 0
    blue = 0

    ax = 0
    ay = 0
    az = 0
    gx = 0
    gy = 0
    gz = 0
    btn_triangle = False
    btn_circle = False
    btn_cross = False
    btn_square = False
    btn_select = False
    btn_start = False
    btn_move = False
    btn_t = False
    btn_ps = False

    button_events_on = None
    button_events_off = None

    trigger = 0
    battery = 0

    rumble = 0

    def __init__(self, controller, read_only=False):
        self.controller = controller
        self.read_only = read_only
        self.start_loop()

    def terminate(self):
        self._active = False

        if self._loop_thread:
            self._loop_thread.join()

    def _loop(self):
        while(self._active):
            if not self.read_only:
                self.controller.set_leds(self.red, self.green, self.blue)
                self.controller.update_leds()
                self.controller.set_rumble(self.rumble)

            self.update_state()
            time.sleep(0.01)

    def start_loop(self):
        self._active = True
        self._loop_thread = Thread(target=self._loop)
        self._loop_thread.daemon = True
        self._loop_thread.start()

    def update_state(self):
        result = self.controller.poll()

        if result:
            buttons = self.controller.get_buttons()
            button_events_on, button_events_off = self.controller.get_button_events()

            self.btn_triangle = bool(buttons & psmove.Btn_TRIANGLE)
            self.btn_circle = bool(buttons & psmove.Btn_CIRCLE)
            self.btn_cross = bool(buttons & psmove.Btn_CROSS)
            self.btn_square = bool(buttons & psmove.Btn_SQUARE)
            self.btn_select = bool(buttons & psmove.Btn_SELECT)
            self.btn_start = bool(buttons & psmove.Btn_START)
            self.btn_move = bool(buttons & psmove.Btn_MOVE)
            self.btn_t = bool(buttons & psmove.Btn_T)
            self.btn_ps = bool(buttons & psmove.Btn_PS)
            self.battery = self.controller.get_battery()
            self.trigger = self.controller.get_trigger()

            self.ax, self.ay, self.az = self.controller.get_accelerometer_frame(psmove.Frame_SecondHalf)
            self.gx, self.gy, self.gz = self.controller.get_gyroscope_frame(psmove.Frame_SecondHalf)

    def state_as_dict(self):
        state_dict = {
            'ax': self.ax,
            'ay': self.ay,
            'az': self.az,
            'gx': self.gx,
            'gy': self.gy,
            'gz': self.gz,
            'btn_triangle': self.btn_triangle,
            'btn_circle': self.btn_circle,
            'btn_cross': self.btn_cross,
            'btn_square': self.btn_square,
            'btn_select': self.btn_select,
            'btn_start': self.btn_start,
            'btn_move': self.btn_move,
            'btn_t': self.btn_t,
            'btn_ps': self.btn_ps,
            'battery': self.battery,
            'trigger': self.trigger,
            'red': self.red,
            'green': self.green,
            'blue': self.blue,
            'rumble': self.rumble,
        }

        # There's currently no way to get color
        # or rumble directly from the controller
        if self.read_only:
            del state_dict['red']
            del state_dict['green']
            del state_dict['blue']
            del state_dict['rumble']

        return state_dict

    def set_color(self, red=None, green=None, blue=None):
        if red is not None:
            self.red = red

        if green is not None:
            self.green = green

        if blue is not None:
            self.blue = blue

    def set_rumble(self, rumble):
        self.rumble = rumble


class RemoteController(Controller):
    _red = 0
    _green = 0
    _blue = 0
    _rumble = 0
    _dirty = True  # Default to True so values get cleared on startup
    
    _callbacks = None

    def __init__(self, url):
        self.url = url
        self.start_loop()

        self._callbacks = defaultdict(lambda: defaultdict(list))
    
    def _loop(self):
        while(self._active):
            self.update_state()
            self.process_callbacks()
            time.sleep(0.02)

            if self._dirty:
                self.update_remote_state()
                self._dirty = False

    def process_callbacks(self):
        for event in self.button_events_on:
            callbacks = self._callbacks[event]['on']

            for callback in callbacks:
                callback.run()

        for event in self.button_events_off:
            callbacks = self._callbacks[event]['off']

            for callback in callbacks:
                callback.run()

    def terminate(self):
        # Let the loop do its thing until
        # we're not dirty any more
        while(self._dirty):
            time.sleep(0.02)

        self._active = False

        if self._loop_thread:
            self._loop_thread.join()

    def update_remote_state(self):
        data = {
            'red': self.red,
            'green': self.green,
            'blue': self.blue,
            'rumble': self.rumble,
        }

        try:
            response = requests.put(self.url, data)
        except requests.ConnectionError:
            print "Could not connect to controller at %s" % self.url
            self._active = False
            return

        if response.status_code == 404:
            print "Controller not found at %s" % self.url
            self._active = False
            return
        elif not response.ok:
            print "Encountered error updating controller: %s (%s)" % (response.status_code, response.reason)
            self._active = False
            return

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, val):
        self._red = val
        self._dirty = True

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, val):
        self._green = val
        self._dirty = True

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, val):
        self._blue = val
        self._dirty = True

    @property
    def rumble(self):
        return self._rumble

    @rumble.setter
    def rumble(self, val):
        self._rumble = val
        self._dirty = True

    def update_state(self):
        try:
            response = requests.get(self.url)
        except requests.ConnectionError:
            print "Could not connect to controller at %s" % self.url
            self._active = False
            return

        if response.status_code == 404:
            print "Controller not found at %s" % self.url
            self._active = False
            return
        elif not response.ok:
            print "Encountered error updating controller: %s (%s)" % (response.status_code, response.reason)
            self._active = False
            return

        result = response.json()

        # Don't record events on the first run!
        if self.button_events_on is None or self.button_events_off is None:
            self.button_events_on = []
            self.button_events_off = []
        else:
            self.button_events_on = result.get('button_events_on')
            self.button_events_off = result.get('button_events_off')

        self.btn_triangle = result.get('btn_triangle')
        self.btn_circle = result.get('btn_circle')
        self.btn_cross = result.get('btn_cross')
        self.btn_square = result.get('btn_square')
        self.btn_select = result.get('btn_select')
        self.btn_start = result.get('btn_start')
        self.btn_move = result.get('btn_move')
        self.btn_t = result.get('btn_t')
        self.btn_ps = result.get('btn_ps')
        self.battery = result.get('battery')
        self.trigger = result.get('trigger')
        self.ax = result.get('ax')
        self.ay = result.get('ay')
        self.az = result.get('ax')
        self.gx =  result.get('gx')
        self.gy = result.get('gy')
        self.gz = result.get('gz')

    def add_callback(self, event, event_type, func, args, kwargs):
        callback = Callback(func, args, kwargs)
        self._callbacks[event][event_type].append(callback)
        return callback

    def on_btn_triangle(self, func, *args, **kwargs):
        return self.add_callback('btn_triangle', 'on', func, args, kwargs)

    def on_btn_triangle_release(self, func, *args, **kwargs):
        return self.add_callback('btn_triangle', 'off', func, args, kwargs)

    def on_btn_cross(self, func, *args, **kwargs):
        return self.add_callback('btn_cross', 'on', func, args, kwargs)

    def on_btn_cross_release(self, func, *args, **kwargs):
        return self.add_callback('btn_cross', 'off', func, args, kwargs)
    
    def on_btn_circle(self, func, *args, **kwargs):
        return self.add_callback('btn_circle', 'on', func, args, kwargs)

    def on_btn_circle_release(self, func, *args, **kwargs):
        return self.add_callback('btn_circle', 'off', func, args, kwargs)
    
    def on_btn_square(self, func, *args, **kwargs):
        return self.add_callback('btn_square', 'on', func, args, kwargs)

    def on_btn_square_release(self, func, *args, **kwargs):
        return self.add_callback('btn_square', 'off', func, args, kwargs)

    def on_btn_move(self, func, *args, **kwargs):
        return self.add_callback('btn_move', 'on', func, args, kwargs)

    def on_btn_move_release(self, func, *args, **kwargs):
        return self.add_callback('btn_move', 'off', func, args, kwargs)

    def on_btn_ps(self, func, *args, **kwargs):
        return self.add_callback('btn_ps', 'on', func, args, kwargs)

    def on_btn_ps_release(self, func, *args, **kwargs):
        return self.add_callback('btn_ps', 'off', func, args, kwargs)
    
    def on_btn_start(self, func, *args, **kwargs):
        return self.add_callback('btn_start', 'on', func, args, kwargs)

    def on_btn_start_release(self, func, *args, **kwargs):
        return self.add_callback('btn_start', 'off', func, args, kwargs)

    def on_btn_select(self, func, *args, **kwargs):
        return self.add_callback('btn_select', 'on', func, args, kwargs)

    def on_btn_select_release(self, func, *args, **kwargs):
        return self.add_callback('btn_select', 'off', func, args, kwargs)
    
    def on_btn_t(self, func, *args, **kwargs):
        return self.add_callback('btn_t', 'on', func, args, kwargs)

    def on_btn_t_release(self, func, *args, **kwargs):
        return self.add_callback('btn_t', 'off', func, args, kwargs)


class Callback(object):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        thread = Thread(target=self._run)
        thread.daemon = True
        thread.start()

    def _run(self):
        self.func(*self.args, **self.kwargs)


def get_controllers(read_only=False):
    controllers = [psmove.PSMove(x) for x in range(psmove.count_connected())]
    return [Controller(c, read_only) for c in controllers if c.connection_type == psmove.Conn_Bluetooth]


def get_remote_controller(url):
    return RemoteController(url)


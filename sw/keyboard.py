
import evdev
from evdev import InputDevice, categorize, ecodes
from select import select
import time

class user_input(object):
    def __init__(self):
        print "starting Keyboard"
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for device in devices:
            print(device.fn, device.name, device.phys)

        self.led_status = 0
        self.layer_count = 2
        self.toggle_button = 172
        self.setLayer()
        self.device1 = evdev.InputDevice('/dev/input/event5')
        self.device2 = evdev.InputDevice('/dev/input/event18')
        self.device1.grab()
        self.device2.grab()

        for i in range(10):
            self.toggleLED()
            time.sleep(0.1)

        self.keymap = [{
            172: 'shift',
            15:  'dome_a',
            155: 'dome_b',
            140: 'tracking_toggle',
            69: 'telescopeA_close',
            98: 'telescopeB_close',
            55: 'telescopeC_close',
            14: None,
            71: 'telescopeA_irisM',
            72: 'telescopeB_irisM',
            73: 'telescopeC_irisM',
            74: None,
            75: 'telescopeA_irisP',
            76: 'telescopeB_irisP',
            77: 'telescopeC_irisP',
            78: None,
            79: 'telescopeA_focusM',
            80: 'telescopeB_focusM',
            81: 'telescopeC_focusM',
            82: 'telescopeA_focusP',
            11: 'telescopeB_focusP',
            83: 'telescopeC_focusP',
            96: None,
        },{
            172: 'shift',
            15:  'dome_a',
            155: 'dome_b',
            140: 'tracking_toggle',
            69: 'RA_center',
            98: 'DEC_center',
            55: None,
            14: None,
            71: None,
            72: 'DEC_P',
            73: None,
            74: None,
            75: 'RA_P',
            76: None,
            77: 'RA_M',
            78: None,
            79: None,
            80: 'DEC_M',
            81: None,
            82: None,
            11: None,
            83: None,
            96: None,
        }]

        data = []

        while True:
            for dev in [self.device1.read(), self.device2.read()]:
                try:
                    while True:
                        dev_out = dev.next()
                        if dev_out.type == ecodes.EV_KEY and dev_out.value in [0,1]:
                            data.append(self.GetKey(dev_out))
                except Exception as e:
                    pass

            time.sleep(0.1)


    def GetKey(self, event):
        if event.code == self.toggle_button:
            if event.value == 1:
                self.toggleLayer()
                self.toggleLED()
        else:
            key = self.keymap[self.layer][event.code]
            if key:
                print event
                self.blikLED()
                print "KEY:", (key, event.value)
                return (key, event.value)
            else:
                print "Klavesa nenastavena"

    def setLayer(self, layer = 0):
        self.layer = layer
        if self.layer >= self.layer_count:
            self.layer = self.layer_count
        print "Layer set to:", self.layer
        return self.layer

    def toggleLayer(self, step = +1):
        self.layer += step
        if self.layer >= self.layer_count:
            self.layer = 0
        #print "Layer toggled to:", self.layer
        return self.layer

    def toggleLED(self):
        self.setLED(not bool(self.led_status))

    def setLED(self, status = 1):
        #print "LED", status
        self.device1.set_led(0, bool(status))
        self.led_status = status
        return bool(self.led_status)

    def blikLED(self, duration=0.1):
        self.toggleLED()
        time.sleep(duration)
        self.toggleLED()


if __name__ == '__main__':
    ui = user_input()
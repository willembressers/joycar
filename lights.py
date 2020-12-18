from microbit import *
import neopixel

np = neopixel.NeoPixel(pin0, 8)


class Lights:
    front = (0, 3)
    back = (5, 6)
    left = (1, 4)
    right = (2, 7)

    # colors
    white = (60, 60, 60)
    orange = (100, 35, 0)
    red = (60, 0, 0)
    off = (0, 0, 0)
    white_bright = (255, 255, 255)
    red_bright = (255, 0, 0)

    def breaking(self):
        for light in self.back:
            np[light] = self.red
            np.show()
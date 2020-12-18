import neopixel
from microbit import *

np = neopixel.NeoPixel(pin0, 8)

# lights
front_left_inside = 0
front_left_outside = 1
front_right_outside = 2
front_right_inside = 3
back_left_outside = 4
back_left_inside = 5
back_right_inside = 6
back_right_outside = 7


# colors
white = (60, 60, 60)
orange = (100, 35, 0)
red = (60, 0, 0)
black = (0, 0, 0)


def display_check(delay=200):
    display.set_pixel(2, 2, 9)
    sleep(delay)

    for x in range(1,4):
        for y in range(1,4):
            display.set_pixel(x, y, 9)
    display.set_pixel(2, 2, 0)
    sleep(delay)

    for x in range(5):
        for y in range(5):
            display.set_pixel(x, y, 9)
    for x in range(1,4):
        for y in range(1,4):
            display.set_pixel(x, y, 0)
    sleep(delay)

    for x in range(5):
        for y in range(5):
            display.set_pixel(x, y, 0)



def lights_check(delay=600):
    np[front_left_inside] = white
    np[front_right_inside] = white
    np.show()
    sleep(delay)

    np[front_left_inside] = black
    np[front_right_inside] = black
    np[back_right_inside] = red
    np[back_left_inside] = red
    np.show()
    sleep(delay)

    np[back_right_inside] = black
    np[back_left_inside] = black
    np[front_left_outside] = orange
    np[back_left_outside] = orange
    np.show()
    sleep(delay)

    np[front_left_outside] = black
    np[back_left_outside] = black
    np[front_right_outside] = orange
    np[back_right_outside] = orange
    np.show()
    sleep(delay)

    np[front_right_outside] = black
    np[back_right_outside] = black
    np.show()


def main():
    display_check()
    lights_check()


if __name__ == "__main__":
    main()
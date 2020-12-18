# Add your Python code here. E.g.
import neopixel
from microbit import *

# ==============================================================================
# LIGHTS
# ==============================================================================
np = neopixel.NeoPixel(pin0, 8)


def alarm(nr_blinks, lights=(1, 2, 4, 7), delay=150, color=(100, 35, 0)):
    for blink in range(nr_blinks):
        for light in lights:
            np[light] = color
        np.show()
        sleep(delay)
        for light in lights:
            np[light] = (0, 0, 0)
        np.show()
        sleep(delay)


def lightsOn():
    for light in (0, 3):
        np[light] = (30, 30, 30)
    for light in (5, 6):
        np[light] = (30, 0, 0)
    np.show()


def lightsOff():
    for light in (0, 3, 5, 6):
        np[light] = (0, 0, 0)
    np.show()


# ==============================================================================
# DISPLAY
# ==============================================================================

def clockTicking(delay=100):
    display.show(Image.CLOCK12)
    sleep(delay)
    display.show(Image.CLOCK1)
    sleep(delay)
    display.show(Image.CLOCK2)
    sleep(delay)
    display.show(Image.CLOCK3)
    sleep(delay)
    display.show(Image.CLOCK4)
    sleep(delay)
    display.show(Image.CLOCK5)
    sleep(delay)
    display.show(Image.CLOCK6)
    sleep(delay)
    display.show(Image.CLOCK7)
    sleep(delay)
    display.show(Image.CLOCK8)
    sleep(delay)
    display.show(Image.CLOCK9)
    sleep(delay)
    display.show(Image.CLOCK10)
    sleep(delay)
    display.show(Image.CLOCK11)
    sleep(delay)
    display.show(Image.CLOCK12)
    sleep(delay)
    display.clear()


# ==============================================================================
# MOTORS
# ==============================================================================

i2c.init(freq=400000, sda=pin20, scl=pin19)

# Initialisierung des PWM Controllers
i2c.write(0x70, b'\x00\x01')
i2c.write(0x70, b'\xE8\xAA')


# Control motors using the PWM controller
# PWM0 and PWM1 for the left and PWM2 and PWM3 for the right motor
def drive(PWM0, PWM1, PWM2, PWM3):
    i2c.write(0x70, b'\x02' + bytes([
                                        PWM0]))  # Transfer value for PWM channel (0-255) to PWM controller. 0x70 is the I2C address of the controller. b'\x02 is the byte for PWM channel 1. To the byte for the channel the byte with the PWM value is added.
    i2c.write(0x70, b'\x03' + bytes([PWM1]))  # Repeat the process for all 4 channels
    i2c.write(0x70, b'\x04' + bytes([PWM2]))
    i2c.write(0x70, b'\x05' + bytes([PWM3]))


def stop():
    drive(0, 0, 0, 0)


def driveBackward(speed=254):
    drive(speed, 0, speed, 0)
    sleep(300)
    stop()


def driveForward(speed=254):
    drive(0, speed, 0, speed)
    sleep(300)
    stop()


def TurnLeft(speed=254):
    drive(0, speed, speed, 0)
    sleep(300)
    stop()


def TurnRight(speed=254):
    drive(speed, 0, 0, speed)
    sleep(300)
    stop()


# ==============================================================================
# MAIN LOGIC
# ==============================================================================


def welcome():
    alarm(nr_blinks=2)
    display.show(Image.ARROW_S)
    lightsOn()


def goodbye():
    lightsOff()
    alarm(nr_blinks=2)
    clockTicking()


def main():
    while True:
        if button_a.is_pressed():
            welcome()
            driveForward()
            sleep(1000)
            driveBackward()
            sleep(1000)
            TurnLeft()
            sleep(1000)
            TurnRight()
        elif button_b.is_pressed():
            goodbye()
            # break


if __name__ == "__main__":
    main()
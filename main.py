# Add your Python code here. E.g.
import neopixel
from microbit import *

# Initialization of the I2C interface
i2c.init(freq=400000, sda=pin20, scl=pin19)

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


def breaklightsOn():
    for light in (5, 6):
        np[light] = (255, 0, 0)
    np.show()


def reverseLightsOn():
    for light in (5, 6):
        np[light] = (60, 60, 60)
    np.show()


# ==============================================================================
# DISPLAY
# ==============================================================================

def turnOn():
    display.set_pixel(2, 2, 9)


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


# ==============================================================================
# SENSOR DATA
# ==============================================================================

# Read out IO Expander data and store in sen_data
def fetchSensorData():
    try:
        data = "{0:b}".format(ord(i2c.read(0x38, 1)))
        bol_data_dict = {}
        bit_count = 7
        for i in data:
            if i == "0":
                bol_data_dict[bit_count] = False
                bit_count -= 1
            else:
                bol_data_dict[bit_count] = True
                bit_count -= 1
        return bol_data_dict  # bit 0 = SpeedLeft, bit 1 = SpeedRight, bit 2 = LineTrackerLeft, bit 3 = LineTrackerMiddle, bit 4 = LineTrackerRight, bit 5 = ObstclLeft, bit 6 = ObstclRight, bit 7 = Buzzer

    except OSError:
        print('skipping error')


# ==============================================================================
# MAIN LOGIC
# ==============================================================================

def brake(sensor_data, locked):
    if not sensor_data[5] or not sensor_data[6]:
        stop()
        if locked == False:
            breaklightsOn()
    elif locked == False:
        lightsOn()


def driveBackward(speed=254):
    drive(speed, 0, speed, 0)
    reverseLightsOn()


def driveForward(speed=254):
    drive(0, speed, 0, speed)
    lightsOn()


def TurnLeft(speed=254):
    drive(0, speed, speed, 0)
    lightsOn()


def TurnRight(speed=254):
    drive(speed, 0, 0, speed)
    lightsOn()


def welcome():
    alarm(nr_blinks=2)
    display.show(Image.ARROW_S)
    lightsOn()


def goodbye():
    lightsOff()
    alarm(nr_blinks=2)
    clockTicking()


def main():
    locked = True
    while True:
        sensor_data = fetchSensorData()
        if sensor_data is not None:

            brake(sensor_data, locked)

            if button_a.is_pressed():
                locked = False
                welcome()
                driveForward()

            elif button_b.is_pressed():
                locked = True
                stop()
                goodbye()
                # break


if __name__ == "__main__":
    main()
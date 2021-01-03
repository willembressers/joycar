# Add your Python code here. E.g.
from microbit import *
from neopixel import *
import gc

frequency = 40000

# Initialization of the I2C interface
i2c.init(freq=frequency, sda=pin20, scl=pin19)

# ==============================================================================
# LIGHTS
# ==============================================================================
np = NeoPixel(pin0, 8)


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
    
def show_distance(distance, max_distance=336, nr_rows=5):
    y = int(distance / (max_distance / nr_rows))
    print(y, distance)
    
    display.clear()
    display.set_pixel(0, y, 9)
    display.set_pixel(1, y, 9)
    display.set_pixel(2, y, 9)
    display.set_pixel(3, y, 9)
    display.set_pixel(4, y, 9)


# ==============================================================================
# MOTORS
# ==============================================================================

i2c.write(0x70, b'\x00\x01')
i2c.write(0x70, b'\xE8\xAA')


def drive(PWM0, PWM1, PWM2, PWM3):
    i2c.write(0x70, b'\x02' + bytes([PWM0]))
    i2c.write(0x70, b'\x03' + bytes([PWM1]))
    i2c.write(0x70, b'\x04' + bytes([PWM2]))
    i2c.write(0x70, b'\x05' + bytes([PWM3]))


def stop():
    drive(0, 0, 0, 0)


# ==============================================================================
# SENSOR DATA
# ==============================================================================

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
                
        # bit 0 = SpeedLeft, 
        # bit 1 = SpeedRight, 
        # bit 2 = LineTrackerLeft, 
        # bit 3 = LineTrackerMiddle, 
        # bit 4 = LineTrackerRight, 
        # bit 5 = ObstclLeft, 
        # bit 6 = ObstclRight, 
        # bit 7 = Buzzer
        
        return bol_data_dict  

    except OSError:
        print('skipping error')
        
    
# ==============================================================================
# SONAR
# ==============================================================================

DISTANCE_CM_PER_BIT = 0.21
spi.init(baudrate=frequency, bits=8, mode=0, miso=pin12)

def sonar_distance():
    gc.disable()
    pin8.write_digital(True)
    pin8.write_digital(False)
    x = spi.read(200)
    high_bits = 0

    for i in range(len(x)):
        if x[i] == 0 and high_bits > 0:
            break
        elif x[i] == 0xff:
            high_bits += 8
        else:
            high_bits += bin(x[i]).count('1')

    x = None
    gc.enable()
    gc.collect()

    return high_bits * DISTANCE_CM_PER_BIT
    
# ==============================================================================
# SERVO
# ==============================================================================

# pin1.set_analog_period(10)

# def scale(num, in_min, in_max, out_min, out_max):
#    return(round((num-in_min)*(out_max-out_min)/(in_max-in_min)+out_min))
    
# def servo(x, y):
#    if x == 1 and y >= 0 and y <= 180:
#        pin1.write_analog(scale(y, 0, 180, 100, 200))

# ==============================================================================
# ACTIONS
# ==============================================================================

def brake(sensor_data):
    stop()
    breaklightsOn()


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
    turnOn()
    lightsOn()


def goodbye():
    lightsOff()
    alarm(nr_blinks=2)
    clockTicking()


# ==============================================================================
# MAIN LOGIC
# ==============================================================================


def main():
    while True:
        sensor_data = fetchSensorData()
        distance = sonar_distance()
        if sensor_data is None:
            continue
        
        show_distance(distance)

        if button_a.is_pressed():
            welcome()

        elif button_b.is_pressed():
            stop()
            goodbye()
            break


if __name__ == "__main__":
    main()

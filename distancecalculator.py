import RPi.GPIO as GPIO
import time

from subprocess import PIPE, Popen
import psutil


def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO_ZERO_TRIGGER = 12
GPIO_ZERO_ECHO = 18

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    timeout = time.time() + 3
    print('This is before the loop')
    print(get_cpu_temperature())

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        print('before time start')
        if time.time() > timeout:
            print('break')
            break

        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        if time.time() > timeout:
            break
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance
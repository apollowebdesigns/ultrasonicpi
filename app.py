import RPi.GPIO as GPIO
import pigpio
import time

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

#set modes on pi zero
print('setting up gpio pins')
pi_zero = pigpio.pi('192.168.1.67')
pi_zero.set_mode(GPIO_TRIGGER, pigpio.OUTPUT)
pi_zero.set_mode(GPIO_ECHO, pigpio.INPUT)
print('pins have been set up')

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from flask import Flask, request, Response, render_template

app = Flask(__name__)

def event_stream():
    count = 0
    while True:
        gevent.sleep(2)
        yield 'data: %s\n\n' % count
        count += 1

@app.route('/my_event_source')
def sse_request():
    return Response(
        event_stream(),
        mimetype='text/event-stream')

@app.route('/')
def page():
    return render_template('sse.html')

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 8090), app)
    http_server.serve_forever()

# if __name__ == '__main__':
#     try:
#         while True:
#             dist = distance()
#             print ("Measured Distance = %.1f cm" % dist)
#             time.sleep(1)
#
#             # Reset by pressing CTRL + C
#     except KeyboardInterrupt:
#         print("Measurement stopped by User")
#         GPIO.cleanup()
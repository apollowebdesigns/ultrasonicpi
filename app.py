import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from flask import Flask, request, Response, render_template
from distancecalculator import distance

app = Flask(__name__)

def event_stream():
    count = 0
    while True:
        gevent.sleep(0.1)
        yield 'data: %s\n\n' % count
        count = distance()
        # count += 1

@app.route('/my_event_source')
def sse_request():
    return Response(
        event_stream(),
        mimetype='text/event-stream')

@app.route('/')
def page():
    return render_template('sse.html')

if __name__ == '__main__':
    try:
        http_server = WSGIServer(('0.0.0.0', 80), app)
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("Measurement stopped by User")

        GPIO.cleanup()
from flask import render_template
from app import app
import RPi.GPIO as GPIO
import time
import sys
import atexit

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(19,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(17,GPIO.LOW)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/activate')
def activate():
    print("Activate",file=sys.stderr)
    startTime = time.time()
    GPIO.output(17,GPIO.HIGH)
    while True:
        elapsedTime = time.time() - startTime
        if GPIO.input(19) == True or elapsedTime > ( 2 * 1 ):
            print("Button pressed",file=sys.stderr)
            GPIO.output(17,GPIO.LOW)
            return "success"

def shutdown():
    print("Goodbye",file=sys.stderr)
    GPIO.output(17,GPIO.LOW)

atexit.register(shutdown)

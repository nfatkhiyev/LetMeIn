from flask import render_template
from flask import request
from app import app
import RPi.GPIO as GPIO
import time
import sys
import atexit

PENCIL_SHARPENER = 17
RESPONSE_BUTTON = 19
LED_A_LEVEL = 27
LED_1_LEVEL = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PENCIL_SHARPENER, GPIO.OUT)
GPIO.setup(RESPONSE_BUTTON, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_A_LEVEL, GPIO.OUT)
GPIO.setup(LED_1_LEVEL, GPIO.OUT)

GPIO.output(17, GPIO.LOW)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/activate')
def activate():
    level = request.args.get('level')
    startTime = time.time()

    print("Activating: " + level, file=sys.stderr)

    GPIO.output(PENCIL_SHARPENER, GPIO.HIGH)

    if level == '1Level':
        GPIO.output(LED_1_LEVEL, GPIO.HIGH)
    elif level == 'aLevel':
        GPIO.output(LED_A_LEVEL, GPIO.HIGH)

    while True:

        elapsedTime = time.time() - startTime
        if GPIO.input(RESPONSE_BUTTON) == True or elapsedTime > ( 2 * 1 ):
            print("Button pressed", file=sys.stderr)

            GPIO.output(PENCIL_SHARPENER, GPIO.LOW)
            GPIO.output(LED_1_LEVEL, GPIO.LOW)
            GPIO.output(LED_A_LEVEL, GPIO.LOW)

            return "success"

def shutdown():
    print("Goodbye", file=sys.stderr)
    GPIO.output(PENCIL_SHARPENER, GPIO.LOW)
    GPIO.output(LED_A_LEVEL, GPIO.LOW)
    GPIO.output(LED_1_LEVEL, GPIO.LOW)

atexit.register(shutdown)

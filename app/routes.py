from app import config
from flask import render_template
from flask import request
from app import app
import RPi.GPIO as GPIO
import time
import sys
import atexit
import json
import requests
from urllib.parse import urlencode
from urllib.request import urlopen
from os import curdir,sep

PENCIL_SHARPENER = 17
RESPONSE_BUTTON = 5
LED_A_LEVEL = 6
LED_1_LEVEL = 13
LED_N_LEVEL = 19
LED_S_LEVEL = 26

SITE_VERIFY_URL = config.RECAPTCHA_SITE_VERIFY_URL
SECRET_KEY = config.RECAPTCHA_SECRET_KEY
SLACK_URL = config.SLACK_URL

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PENCIL_SHARPENER, GPIO.OUT)
GPIO.setup(RESPONSE_BUTTON, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_A_LEVEL, GPIO.OUT)
GPIO.setup(LED_1_LEVEL, GPIO.OUT)
GPIO.setup(LED_N_LEVEL, GPIO.OUT)
GPIO.setup(LED_S_LEVEL, GPIO.OUT)

GPIO.output(PENCIL_SHARPENER, GPIO.LOW)
GPIO.output(LED_A_LEVEL, GPIO.LOW)
GPIO.output(LED_1_LEVEL, GPIO.LOW)
GPIO.output(LED_N_LEVEL, GPIO.LOW)
GPIO.output(LED_S_LEVEL, GPIO.LOW)

#GPIO.output(PENCIL_SHARPENER, GPIO.HIGH)
#GPIO.output(LED_A_LEVEL, GPIO.HIGH)
#GPIO.output(LED_1_LEVEL, GPIO.HIGH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/activate', methods=['POST'])
def activate():
    body = request.json
    RECAPTCHA_RESPONSE = body['response']

    REMOTE_IP = request.remote_addr
    params = urlencode({
        'secret':SECRET_KEY,
        'response':RECAPTCHA_RESPONSE,
    })

    data = urlopen(SITE_VERIFY_URL, params.encode('utf-8')).read()

    result = json.loads(data)
    success = result.get('success', None)

    if success:
        level = body['level']
        startTime = time.time()

        print("Activating: " + level, file=sys.stderr)

        GPIO.output(PENCIL_SHARPENER, GPIO.HIGH)

        if level == '1Level':
            GPIO.output(LED_1_LEVEL, GPIO.HIGH)
        elif level == 'aLevel':
            GPIO.output(LED_A_LEVEL, GPIO.HIGH)
        elif level == 'nLevel':
            GPIO.output(LED_N_LEVEL, GPIO.HIGH)
        elif level == 'sLevel':
            GPIO.output(LED_S_LEVEL, GPIO.HIGH)

        while True:

            elapsedTime = time.time() - startTime
            timedOut = elapsedTime > 45
            buttonPressed = GPIO.input(RESPONSE_BUTTON)

            if timedOut or buttonPressed:

                GPIO.output(PENCIL_SHARPENER, GPIO.LOW)
                GPIO.output(LED_1_LEVEL, GPIO.LOW)
                GPIO.output(LED_A_LEVEL, GPIO.LOW)
                GPIO.output(LED_N_LEVEL, GPIO.LOW)
                GPIO.output(LED_S_LEVEL, GPIO.LOW)

                if timedOut:
                    print("Button timed out", file=sys.stderr)
                    return "timeout"
                elif buttonPressed:
                    print("Button pressed", file=sys.stderr)
                    return "buttonpressed"
                return ""
    else:
        GPIO.output(PENCIL_SHARPENER, GPIO.LOW)
        GPIO.output(LED_1_LEVEL, GPIO.LOW)
        GPIO.output(LED_A_LEVEL, GPIO.LOW)
        GPIO.output(LED_N_LEVEL, GPIO.LOW)
        GPIO.output(LED_S_LEVEL, GPIO.LOW)

        print("Not Verified", file=sys.stderr)
        return "not verified"

@app.route('/notify', methods=['POST'])
def notify_slack():
    body = request.json
    text = body['text']
    params = {
        'text': text,
    }
    r = requests.post(url=SLACK_URL, json = params)
    return "notification posted"

def shutdown():
    print("Goodbye", file=sys.stderr)
    GPIO.output(PENCIL_SHARPENER, GPIO.LOW)
    GPIO.output(LED_A_LEVEL, GPIO.LOW)
    GPIO.output(LED_1_LEVEL, GPIO.LOW)
    GPIO.output(LED_N_LEVEL, GPIO.LOW)
    GPIO.output(LED_S_LEVEL, GPIO.LOW)


atexit.register(shutdown)

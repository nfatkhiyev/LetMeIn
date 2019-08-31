from flask import render_template
from app import app
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(19,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class Constants():
    hasButtonBeenPressed = False
    hasRequestBeenSent = False

@app.route('/')
def index():
    return render_template('index.html', boolean = Constants.hasButtonBeenPressed)


@app.route('/activate')
def activate():
    Constants.hasRequestBeenSent = True
    GPIO.output(17,GPIO.HIGH)
    Constants.hasButtonBeenPressed = False
    return "success"


@app.route('/checkstatus')
def checkstatus():
    return 'ToDo'


@app.route('/buttonLoop')
def buttonLoop():
    while Constants.hasRequestBeenSent == True:
        if GPIO.input(19) == True:
            Constants.hasRequestBeenSent = False
            Constants.hasButtonBeenPressed = True
            GPIO.output(17,GPIO.LOW)
    return render_template('index.html', boolean = Constants.hasButtonBeenPressed)

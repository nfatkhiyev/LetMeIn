from flask import render_template
from app import app
from gpiozero import LED

led = LED()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/activate')
def activate():
    led.on()
    return "success"


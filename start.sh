#!/bin/bash
cd /home/pi/LetMeIn
source venv/bin/activate
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=80 2>error.log


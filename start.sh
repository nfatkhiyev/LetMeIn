#!/bin/bash
cd /home/pi/LetMeIn
source venv/bin/activate
export FLASK_ENV=development
flask run --host=127.0.0.1 --port=8080 2>error.log


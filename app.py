#!/usr/bin/python3

from flask import request
from flask_api import status
from flask_api import FlaskAPI
import RPi.GPIO as GPIO

relays = {"badkamer": 8, "slaapkamer": 10}

GPIO.setmode(GPIO.BOARD)
GPIO.setup(relays["badkamer"], GPIO.OUT)
GPIO.setup(relays["slaapkamer"], GPIO.OUT)

app = FlaskAPI(__name__)

@app.route('/', methods=["GET"])
def api_root():
    return relays

@app.route('/<relay>/', methods=["GET", "POST"])
def api_relay(relay):
    if request.method == "POST":
        if relay in relays:
            GPIO.output(relays[relay], int(request.data.get("state")))
    return {"state": GPIO.input(relays[relay])}

@app.route('/<relay>/<state>', methods=["GET"])
def api_relay_set(relay, state):
    if state == "1" or state == "on":
        set = 1
    elif state == "0" or state == "off":
        set = 0
    elif state == "toggle":
        set = abs(GPIO.input(relays[relay]) - 1)
    else:
        return "", status.HTTP_400_BAD_REQUEST

    GPIO.output(relays[relay], set)
    return {"state": GPIO.input(relays[relay])}

if __name__ == "__main__":
    app.run()

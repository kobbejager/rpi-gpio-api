#!/usr/bin/python3

from flask import request
from flask_api import status
from flask_api import FlaskAPI
import RPi.GPIO as GPIO

relays = {"badkamer": 8, "slaapkamer": 10}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(list(relays.values()), GPIO.OUT, initial=GPIO.HIGH)

app = FlaskAPI(__name__)

@app.route('/', methods=["GET"])
def api_root():
    return relays

@app.route('/<relay>/', methods=["GET", "POST"])
def api_relay(relay):
    if request.method == "POST":
        if relay in relays:
            set(relay, int(request.data.get("state")))
    return {"state": get(relay)}

@app.route('/<relay>/<state>', methods=["GET"])
def api_relay_set(relay, state):
    if state == "1" or state == "on":
        set(relay, 1)
    elif state == "0" or state == "off":
        set(relay, 0)
    elif state == "toggle":
        set(relay)
    else:
        return "", status.HTTP_400_BAD_REQUEST

    return {"state": get(relay)}

def get(relay):
    return abs(GPIO.input(relays[relay]) - 1) #reverse logic (active low)

def set(relay, value = None): #if no value given: toggle
    if value != None:
        value = abs(value - 1) #reverse logic (active low)
    else:
        value = get(relay)
    GPIO.output(relays[relay], value)

if __name__ == "__main__":
    app.run()

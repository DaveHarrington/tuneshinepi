import time
import machine
from machine import Pin
from machine import I2C

import network

import wifi

import picosleep


relay_pin = Pin(19, Pin.OUT)
led_pin = Pin(8, Pin.OUT)
    
while True:
    
    print("Get state request for Tuneshine")
    
    requested_state = wifi.get_tuneshine_state_request(debug=True)
    
    if requested_state:
        print("Requested to be on")
        relay_pin.init(mode=machine.Pin.OUT, value=1)
        led_pin.on()

    else:
        print("Requested to be off")
        relay_pin.init(mode=machine.Pin.OUT, value=0)
        led_pin.off()

    picosleep.seconds(60)
    # time.sleep(60)

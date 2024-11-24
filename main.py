import time
import machine
from machine import Pin
from machine import I2C

from picobricks import SSD1306_I2C

import network

import wifi

import picosleep


i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=200000)
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
oled.fill(0)

relay_pin = Pin(12, Pin.OUT)
led_pin = Pin(7, Pin.OUT) # initialize digital pin as an output for led

def show(s):
    oled.fill(0)
    oled.text("|Tuneshine|", 15, 5)
    oled.text("----------------", 0, 30)
    oled.text(s, 0, 45)
    oled.show()

Pin(23, Pin.OUT).low()

while True:
    led_pin.on()
    print("Get state request for Tuneshine")
    oled.poweron()
    show("Get State Req")
    try:
        requested_state = wifi.get_tuneshine_state_request(oled, debug=True)
    except Exception as e:
        print(e)
        time.sleep(10)
        continue
    
    show("State Req: " + "on" if requested_state else "off")
    
    if requested_state:
        print("Requested to be on")
        
        relay_pin.init(mode=machine.Pin.OUT, value=1)
        
        show("On: sleep 60s")
    else:
        print("Requested to be off")
        relay_pin.init(mode=machine.Pin.OUT, value=0)
        
        led_pin.off()
        show("Off: sleep 60s")
    
    picosleep.seconds(60)
    # time.sleep(20)

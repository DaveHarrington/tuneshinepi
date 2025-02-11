import time
import traceback
import ujson

import machine
from machine import WDT
from machine import Pin
from machine import I2C

import network
import wifi
import set_rtc

tuneshine_pin = Pin(19, Pin.OUT)
power_relay_pin = Pin(0, Pin.OUT)
power_relay_pin.on()

print("Start up delay - 3s")
# Delay to allow interupting before Watchdog is enabled
time.sleep(3)
print("Starting")

# Watchdog is limited to 8388ms
wdt = WDT(timeout=8388)
class WDT:
    def feed(self):
        pass
# wdt = WDT()
wdt.feed()

def get_reset_cause():
    """Get the reason for the last reset"""
    cause = machine.reset_cause()
    causes = {
        machine.PWRON_RESET: "Power on reset",
        machine.WDT_RESET: "Watchdog timer reset",
    }

    return causes.get(cause, "Unknown reset cause")

print(f"Last reset cause: {get_reset_cause()}")
wifi.send_log(ujson.dumps({"last_reset": get_reset_cause()}), wdt)
wdt.feed()

print("Write last error")
with open("error.log", "w+") as f:
    error = f.readlines()
    print(error)
    if error:
        print("sending error")
        wifi.send_log(ujson.dumps({"last_error": error}), wdt)
        f.write("")

def trip_power():
    print("Requested power relay: off")
    power_relay_pin.off()
    machine.lightsleep(1000)
    print("Requested power relay: on")
    power_relay_pin.on()
    
count = 0
tuneshine_state = False
while True:
    count += 1
    print("Get state request for Tuneshine")
    
    requested_state = wifi.get_tuneshine_state_request(wdt)
    
    if requested_state:
        count = 0
        if tuneshine_state == False:
            trip_power()
            print("Requested tuneshine: on")
            tuneshine_pin.on()
            tuneshine_state = True
        
    else:
        print("Requested tuneshine: off")
        tuneshine_pin.off()
        tuneshine_state = False
        
    if count >= 20:
        count = 0
        trip_power()
    
    wdt.feed()
    feed_loop_delay_s = 5
    for i in range(60 // feed_loop_delay_s):
        machine.lightsleep(feed_loop_delay_s * 1000)
        wdt.feed()
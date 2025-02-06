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

relay_pin = Pin(19, Pin.OUT)
led_pin = Pin(8, Pin.OUT)

print("Start up delay - 3s")
# Delay to allow interupting before Watchdog is enabled
time.sleep(3)
print("Starting")

# Watchdog is limited to 8388ms
#wdt = WDT(timeout=8388)
class WDT:
    def feed(self):
        pass
wdt = WDT()
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

# Turn on on startup, in case a series of watchdog resets mean we dont get to it
count = 30
while True:
    count += 1
    try:
        print("Get state request for Tuneshine")
        
        requested_state = wifi.get_tuneshine_state_request(wdt)
        
        # Turn on once every half hour, to keep battery from going to sleep
        if requested_state:
            print("Requested to be on")
            relay_pin.on()
            led_pin.on()
            count = 0
        elif count >= 30:
            count = 0
            wifi.send_log(ujson.dumps({"power_bump": True}), wdt)
            relay_pin.on()
            
            wdt.feed()
            machine.lightsleep(5000)
            relay_pin.off()

        else:
            print("Requested to be off")
            relay_pin.off()
            led_pin.off()
        
        wdt.feed()
        print("Sleep 56")
        for i in range(8):
            machine.lightsleep(7000)
            wdt.feed()
            
    except Exception as e:

        with open("error.log", "w+") as f:
            f.write(traceback.format_exception(e))
        time.sleep(1)
        machine.reset()
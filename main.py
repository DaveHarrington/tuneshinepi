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
# Watchdog seems to be limited to about 9 seconds
wdt = WDT(timeout=9 * 1000)
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
wifi.send_log(ujson.dumps({"last_reset": get_reset_cause()}))
wdt.feed()

try:
    set_rtc.set_time()
except:
    raise
wdt.feed()

while True:
    try:
        print("Get state request for Tuneshine")
        
        requested_state = wifi.get_tuneshine_state_request()
        
        if requested_state:
            print("Requested to be on")
            relay_pin.on()
            led_pin.on()

        else:
            print("Requested to be off")
            relay_pin.off()
            led_pin.off()
        
        wdt.feed()
        print("Sleep 56")
        for i in range(7):
            time.sleep(8)
            wdt.feed()
            
    except Exception as e:
        adjusted = time.localtime(time.mktime(time.localtime()) - 8*3600)
        with open("error.log", "w+") as f:
            f.write("{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}\n".format(
                adjusted[0], adjusted[1], adjusted[2],
                adjusted[3], adjusted[4], adjusted[5]))
            f.write(traceback.format_exception(e))
            
        wifi.send_log(ujson.dumps({"exception": traceback.format_exception(e)}))
        raise
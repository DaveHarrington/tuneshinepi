import network
import urequests
import time
from machine import Pin

from wifi_conf import WIFI_SSID, WIFI_PASSWORD

def get_tuneshine_state_request(oled, debug=False):
    
    def show(s):
        oled.fill(0)
        oled.text("|Tuneshine|", 15, 5)
        oled.text("----------------", 0, 30)
        oled.text(s, 0, 45)
        oled.show()

    # Connect to Wi-Fi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Wait for connection
    while not wlan.isconnected():
        show("Connecting...")
        time.sleep(1)

    print("Connected to Wi-Fi:", wlan.ifconfig())

    # Make a GET request
    url = 'http://192.168.4.140:8000/'
    response = urequests.get(url)
    val = response.text
    response.close()
    
    show("Response:" + val)
    
    print("Disable Wifi")
    wlan.disconnect()
    wlan.active(False)

    return val.strip() == "1"
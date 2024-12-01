import network
import urequests
import time
from machine import Pin

from wifi_conf import WIFI_SSID, WIFI_PASSWORD

led = Pin(7, Pin.OUT)

def connect_wifi(ssid, password):
    # Initialize WiFi interface
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Reset networking for clean connection
#    wlan.deinit()
#    time.sleep(1)
#    wlan = network.WLAN(network.STA_IF)
#    wlan.active(True)
    
    # Scan for networks (optional but useful for debugging)
#    networks = wlan.scan()
#    print("Available networks:")
#    for net in networks:
#        print(net[0].decode())
    
    # Connect to WiFi
    print(f"\nConnecting to {ssid}...")
    wlan.connect(ssid, password)
    
    # Wait for connection with timeout
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("Waiting for connection...")
        led.toggle()  # Blink LED while connecting
        time.sleep(1)
    
    if wlan.status() != 3:
        led.off()
        return None
    
    else:
        status = wlan.ifconfig()
        print('\nConnection successful!')
        print(f'IP Address: {status[0]}')
        return wlan
        
def get_tuneshine_state_request():
    wlan = connect_wifi(WIFI_SSID, WIFI_PASSWORD)
        
    if not wlan:
        return False
    
    print("Connected to Wi-Fi:", wlan.ifconfig())
    
    # Make a GET request
    url = 'http://192.168.4.140:8000/playing'
    response = urequests.get(url)
    val = response.text
    response.close()
    
    print("Disable Wifi")
    wlan.disconnect()
    wlan.active(False)

    print(f"Got {val.strip()}")

    return val.strip() == "1"

def send_log(log_json_str):
    wlan = connect_wifi(WIFI_SSID, WIFI_PASSWORD)

    # Make a GET request
    url = 'http://192.168.4.140:8000/log'
    urequests.post(url, headers = {'content-type': 'application/json'}, data = log_json_str)
    urequests.put(url)
    
    wlan.disconnect()
    wlan.active(False)
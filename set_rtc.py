import network
import socket
import time
import struct

import machine

from wifi_conf import WIFI_SSID, WIFI_PASSWORD

NTP_DELTA = 2208988800
host = "pool.ntp.org"

def _set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

def set_time():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

    _set_time()
    adjusted = time.localtime(time.mktime(time.localtime()) - 8*3600)
    print("{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
       adjusted[0], adjusted[1], adjusted[2],
       adjusted[3], adjusted[4], adjusted[5]))
import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
import webrepl
import webrepl_setup
from secrets import SSID, PASSWORD

def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


try:
    ip = connect()
    webrepl.start()
except KeyboardInterrupt:
    machine.reset()

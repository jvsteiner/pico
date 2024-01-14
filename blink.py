from machine import Pin
from picozero import pico_temp_sensor, pico_led
import time

led = Pin(15, Pin.OUT)  # create LED object from Pin 15, Set Pin 15 to output

try:
    while True:
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
except:
    pass

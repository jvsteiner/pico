from machine import ADC, Pin
import time
from picozero import pico_led

adc = ADC(26)
pico_led.on()

try:
    while True:
        adcValue = adc.read_u16()
        voltage = adcValue / 65535.0 * 3.3
        print("ADC Value:", adcValue, "Voltage:", voltage, "V")
        time.sleep(0.05)
except:
    pass

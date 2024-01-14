from machine import Pin, PWM
import time

# set PWM
pwm = PWM(Pin(15))
pwm.freq(10000)

try:
    while True:
        for i in range(0, 65535):
            pwm.duty_u16(i)
            time.sleep_us(10)
        for i in range(65535, 0, -1):
            pwm.duty_u16(i)
            time.sleep_us(10)
except:
    pwm.deinit()

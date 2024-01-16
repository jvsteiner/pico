import time
from my74HC595 import Chip74HC595
from machine import Pin
import asyncio

comPin = [17, 16, 15, 14]
TZ_OFFSET = 2 * 60 * 60  # UTC+2

num = [
    0xC0,
    0xF9,
    0xA4,
    0xB0,
    0x99,
    0x92,
    0x82,
    0xF8,
    0x80,
    0x90,
    0x88,
    0x83,
    0xC6,
    0xA1,
    0x86,
    0x8E,
]


def led_display():
    for i in range(0, 4):
        chns = Pin(comPin[i], Pin.OUT)
        chip.shiftOut(0, num[i])
        chns.value(1)
        time.sleep_ms(1)
        chns.value(0)


# Pico-GP 18: 74HC595-DS(18)
# Pico-GP 20: 74HC595-STCP(20)
# Pico-GP 21: 74HC595-SHCP(21)

chip = Chip74HC595(18, 20, 21)


def display(digit, number):
    chns = Pin(comPin[digit], Pin.OUT)
    chip.shiftOut(0, num[number])
    chns.value(1)
    time.sleep_ms(1)
    chns.value(0)


def display_four_digits(number):
    for i in [3, 2, 1, 0]:
        display(i, number % 10)
        number = number // 10
    time.sleep_ms(1)


def display_time(offset=TZ_OFFSET):
    t = localtime(offset=offset)
    display(0, t[3] // 10)
    display(1, t[3] % 10)
    display(2, t[4] // 10)
    display(3, t[4] % 10)


def display_task(fun, *args, duration=3):
    start = time.time()
    while time.time() - start < duration:
        fun(*args)


def countdown(hi=10, duration=1):
    for i in range(hi, -1, -1):
        display_task(display_four_digits, i, duration=duration)


# asyncio.create_task(clock_task())
# asyncio.run(clock_task())
# asyncio.wait_for(clock_task, 5)


def localtime(secs=None, offset=TZ_OFFSET):
    """Convert the time secs expressed in seconds since the Epoch into an 8-tuple which contains: (year, month, mday, hour, minute, second, weekday, yearday) If secs is not provided or None, then the current time from the RTC is used."""
    return time.localtime((secs if secs else time.time()) + offset)


try:
    while True:
        led_display()
except:
    pass

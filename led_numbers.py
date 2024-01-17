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

CHARS = {
    "0": 0xC0,
    "1": 0xF9,
    "2": 0xA4,
    "3": 0xB0,
    "4": 0x99,
    "5": 0x92,
    "6": 0x82,
    "7": 0xF8,
    "8": 0x80,
    "9": 0x90,
    "A": 0x88,
    "B": 0x83,
    "C": 0xC6,
    "D": 0xA1,
    "E": 0x86,
    "F": 0x8E,
    "G": 0x82,
    "H": 0b10001001,
    "I": 0b11111011,
    "J": 0b11100001,
    "K": 0b10000111,
    "L": 0b11000111,
    "N": 0b10101011,
    "O": 0b10100011,
    "P": 0b10001100,
    "R": 0b10101111,
    "S": 0b10010010,
    "T": 0b11001110,
    "U": 0b11100011,
    "V": 0b11100011,
    "Y": 0x99,
    "Z": 0x92,
    " ": 0b11111111,
    "-": 0b10111111,
    "_": 0b11110111,
}

VALID_CHARS = list(CHARS.keys())


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


def display_raw(digit, bin):
    chns = Pin(comPin[digit], Pin.OUT)
    chip.shiftOut(0, bin)
    chns.value(1)
    time.sleep_ms(1)
    chns.value(0)


def display(digit, number):
    display_raw(digit, num[number])


def display_char(digit, char):
    display_raw(digit, CHARS[char])


def display_four_chars(chars):
    for i in [3, 2, 1, 0]:
        display_char(i, chars[i])
    time.sleep_ms(1)


def display_four_raw(chars):
    for i in [3, 2, 1, 0]:
        display_raw(i, chars[i])
    time.sleep_ms(1)


def add_dots(chars):
    output = []
    for char in chars:
        char = char.upper()
        if char in VALID_CHARS:
            output.append(CHARS[char])
        if char == ".":
            output[-1] = output[-1] - 128
    return output


def scroll_chars(chars, duration=500):
    chars = add_dots(chars)
    chars = [0b11111111] * 4 + chars + [0b11111111] * 4
    for i in range(0, len(chars) - 3):
        screen = chars[i : i + 4]
        # print(screen)
        display_task(display_four_raw, chars[i : i + 4], duration=duration)
    time.sleep_ms(1)


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


def display_task(fun, *args, duration=3000):
    start = time.time_ns() // 1_000_000
    while time.time_ns() // 1_000_000 - start < duration:
        fun(*args)


def countdown(hi=10, duration=1000):
    for i in range(hi, -1, -1):
        display_task(display_four_digits, i, duration=duration)


# asyncio.create_task(clock_task())
# asyncio.run(clock_task())
# asyncio.wait_for(clock_task, 5)
# display_task(display_four_chars, "ATLF")


def localtime(secs=None, offset=TZ_OFFSET):
    """Convert the time secs expressed in seconds since the Epoch into an 8-tuple which contains: (year, month, mday, hour, minute, second, weekday, yearday) If secs is not provided or None, then the current time from the RTC is used."""
    return time.localtime((secs if secs else time.time()) + offset)

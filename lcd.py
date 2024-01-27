import time
from machine import I2C, Pin
from I2C_LCD import I2CLcd
import dht

DHT = dht.DHT11(Pin(5))
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
devices = i2c.scan()
lcd = I2CLcd(i2c, devices[0], 2, 16)
time.sleep(1)


def check_temp(dht):
    if dht.measure() == 0:
        print("DHT11 data error")
    temp = int(dht.temperature())
    humi = int(dht.humidity())
    lcd.move_to(0, 0)
    lcd.putstr("Temp: ")
    lcd.putstr(str(temp))
    lcd.putstr(" C")
    lcd.move_to(0, 1)
    lcd.putstr("Humi: ")
    lcd.putstr(str(humi))
    lcd.putstr(" %")
    time.sleep(2)


def write_line(lcd, line, text):
    if line != 0 and line != 1:
        raise ValueError("Line must be 0 or 1")
    lcd.move_to(0, line)
    lcd.putstr(" " * 16)
    lcd.move_to(0, line)
    lcd.putstr(text)


class mylcd(object):
    def __init__(self, lcd, speed=0.3) -> None:
        self.lcd = lcd
        self.speed = speed
        self.lines = ["", ""]
        self.clear()

    def write_text(self, line, text):
        if line != 0 and line != 1:
            raise ValueError("Line must be 0 or 1")
        self.lcd.move_to(0, line)
        self.lcd.putstr(text)

    def scroll_line(self, line, text):
        if line != 0 and line != 1:
            raise ValueError("Line must be 0 or 1")
        self.lines[line] = " " * 16 + text
        for i in range(len(self.lines[line]) - 15):
            self.lcd.move_to(0, line)
            self.write_text(line, self.lines[line][i : i + 16])
            time.sleep(self.speed)

    def clear(self):
        self.lcd.clear()

    def on(self):
        self.lcd.backlight_on()
        self.lcd.display_on()

    def off(self):
        self.lcd.backlight_off()
        self.lcd.display_off()


long_i = bytearray([0x0E, 0x00, 0x0C, 0x04, 0x04, 0x04, 0x0E, 0x00])
long_e = bytearray([0x0E, 0x00, 0x0E, 0x11, 0x1F, 0x10, 0x0E, 0x00])
long_a = bytearray([0x0E, 0x00, 0x0E, 0x01, 0x0F, 0x11, 0x0F, 0x00])
long_u = bytearray([0x0E, 0x00, 0x11, 0x11, 0x11, 0x13, 0x0D, 0x00])
arrow_c = bytearray([0x0A, 0x04, 0x0E, 0x10, 0x10, 0x11, 0x0E, 0x00])
arrow_s = bytearray([0x0A, 0x04, 0x0E, 0x10, 0x0E, 0x01, 0x1E, 0x00])
arrow_z = bytearray([0x0A, 0x04, 0x1F, 0x02, 0x04, 0x08, 0x1F, 0x00])
tilde_g = bytearray([0x02, 0x04, 0x0F, 0x11, 0x0F, 0x01, 0x0E, 0x00])
tilde_k = bytearray([0x10, 0x10, 0x12, 0x14, 0x18, 0x14, 0x12, 0x04])
tilde_l = bytearray([0x0C, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E, 0x04])
tilde_n = bytearray([0x00, 0x00, 0x16, 0x19, 0x11, 0x11, 0x11, 0x04])

char_arr = [
    long_i,
    long_e,
    long_a,
    long_u,
    arrow_c,
    arrow_s,
    arrow_z,
    tilde_g,
    tilde_k,
    tilde_l,
    tilde_n,
]
for i, char in enumerate(char_arr):
    lcd.custom_char(i, char)

chars = {
    "i": 0,
    "e": 1,
    "a": 2,
    "u": 3,
    "c": 4,
    "s": 5,
    "z": 6,
    "g": 7,
    "k": 8,
    "l": 9,
    "n": 10,
}


def custom(letter):
    return chr(chars[letter])


"""
from lcd import *
c = mylcd(lcd, speed=0.3)
c.scroll_line(0, "Hello World")
"""

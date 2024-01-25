from mqtt_as import MQTTClient, config
import asyncio
from pico_secrets import SSID, PASSWORD
import socket

config["ssid"] = SSID
config["wifi_pw"] = PASSWORD
config["server"] = "192.168.1.107"
MQTTClient.DEBUG = True
client = MQTTClient(config)
client.connect()

# config["server"] = "100.80.58.85"  # Change to suit e.g. 'iot.eclipse.org'
config["server"] = "192.168.1.107"  # Change to suit e.g. 'iot.eclipse.org'
# client.subscribe("foo_topic", 1)
client.publish("foo_topic", "some message{}".format(1), qos=1)


from mqtt_as import MQTTClient, config
import asyncio, machine
from pico_secrets import SSID, PASSWORD


config["ssid"] = SSID
config["wifi_pw"] = PASSWORD
config["server"] = "192.168.1.107"


async def messages(client):
    async for topic, msg, retained in client.queue:
        print((topic, msg, retained))


async def up(client):
    while True:
        await client.up.wait()
        client.up.clear()
        await client.subscribe("foo_topic", 1)


async def main(client):
    await client.connect()
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))
    n = 0
    while True:
        await asyncio.sleep(5)
        print("publish", n)
        await client.publish("result", "{}".format(n), qos=1)
        n += 1


config["queue_len"] = 1
MQTTClient.DEBUG = True
client = MQTTClient(config)
loop = asyncio.get_event_loop()
try:
    asyncio.run(main(client))
except KeyboardInterrupt:
    loop.close()
    machine.reset()
finally:
    client.close()

import socket, network


def open_socket(ip, port=1883):
    # Open a socket
    address = (ip, port)
    connection = socket.socket()
    connection.connect(address)
    return connection


s = open_socket("192.168.1.21")
s = open_socket("100.70.90.26")
s = open_socket("192.168.1.107", port=80)
s = open_socket("100.103.111.114", port=1883)

wlan = network.WLAN(network.STA_IF)

wlan.ifconfig(("192.168.1.137", "255.255.0.0", "192.168.1.106", "100.100.100.100"))
wlan.connect(SSID, PASSWORD)

ad = socket.getaddrinfo("pi4.tailc6a41.ts.net", 1883)


import time
import dht11

temperature = 0
humidity = 0
dht = dht11.DHT11(13)


def check(dht):
    if dht.measure() == 0:
        raise Exception("read error")
    temperature = dht.temperature()
    humidity = dht.humidity()
    return (temperature, humidity)


def display_temp(dht):
    temp, hum = check(dht)
    return "T: %0.2fC  H: %0.2f" % (temp, hum) + "%"

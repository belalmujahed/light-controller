import socket
import json
import network
import machine
import urequests
import utime
from socket import AF_INET, SOCK_DGRAM
import time
import ntptime

powerled = machine.Pin(16, machine.Pin.OUT)
blueled = machine.Pin(4, machine.Pin.OUT)
outputlight = machine.PWM(machine.Pin(5))


apikey='4ba0eb07e2968c5abff2c74ae1f99bbc'
url='http://api.openweathermap.org/data/2.5/weather?q=Dublin&APPID='+apikey

def connect_wifi():
    ssid = 'abc'
    ssidpw = 'def'
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, ssidpw)
    while not wifi.isconnected():
        powerled.off()
        blueled.on()
        time.sleep(.05)
        powerled.on()
        blueled.off()
        time.sleep(.05)




def getInfo(x):
    request = urequests.get(x).json()
    print(request)
    return request


def getSunset(x):
    sunset = x['sys']['sunset']
    return sunset-946708560


def getSunrise(x):
    sunrise = x['sys']['sunrise']
    sunrise = sunrise -946708560
    return sunrise

def getTime():
    time=ntptime.time()
    time = time+
    return time



def fadein():
    for x in range(0, 1024):
        outputlight.duty(x)
        utime.sleep(3.6)

def fadeout():
    x=1024
    while x>=0:
        outputlight.duty(x)
        utime.sleep(3.6)
        x=x-1



connect_wifi()
sunrise =getSunrise(getInfo(url))
sunset =getSunset(getInfo(url))
time=getTime()
print(sunrise)
print(sunset)
print(time)

while True:
    sunrise = getSunrise(getInfo(url))
    sunset = getSunset(getInfo(url))
    time = getTime()
    while((sunset - 31556952 < time) & (sunrise + 31556952 > time)):
        outputlight.duty(1000)

    else:
        if(sunset - 31556952 <= time):
            fadein()
        if(sunrise + 31556952 >= time):
            fadeout()

    utime.sleep(300)

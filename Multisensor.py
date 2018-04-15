import machine
from machine import Pin
from time import sleep
from dht import DHT11


def dht11_sensor():
    d = DHT11(Pin(14))
    d.measure()  # mesure temp and humidity
    temp = d.temperature()
    hum = d.humidity()
    print('Temperature:', temp, 'C')
    print('Humidity:', hum, '%')


def buzzer():
    buzz = Pin(2, Pin.OUT)
    buzz.value(1)  # turn off
    sleep(0.2)
    buzz.value(0)  # turn on
    sleep(0.8)


def moist():
    moist = machine.ADC(0)
    soil = moist.read()
    print('Soil moisture:', soil)
    if soil >= 750:
        buzzer()


def Photo_sensitive():
    photo = Pin(16, Pin.IN)
    mesure_photo = photo.value()
    if mesure_photo == 1:
        print('Dark')
    elif mesure_photo == 0:
        print('Light')


def main():
    while True:
        dht11_sensor()
        moist()
        Photo_sensitive()
        sleep(5)  # time betwean mesurements in secounds


main()

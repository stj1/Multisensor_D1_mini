from dht import DHT11
import machine
from machine import Pin
from time import sleep
import socket

#  CURENT STATES OF SENSORS
sensors = ['PIR', 'TEMP', 'HUM', 'MOIST', 'LIGHT']
pins = ['0', '1', '2', '3', '4']

#  HTML TO PARSE
html = """<!DOCTYPE html>
<html>
<head>
<title>ESP8622 multisensor</title>
<style>
header {padding: 1em; color: black; background-color: midnightblue; text-align: center}
footer{padding: 1em; margin-top: 15rem; background-color: #FF9800; height: 20rem}
nav {float:left}
h1 {padding-left: 1.5em; background-color:  White; color: midnightblue; font-family: helvetica; font-weight: bold; font-size: 25}
h2   {color: White; font-family:helvetica; text-align:left; padding-left: 1em}
table {color: midnightblue; padding-left: 3em; background:  white; font-family: helvetica}
svg {padding: 1em}
</style>
</head>
<body>
<header>
<h2><i>HOME SENSOR</i></h2>
</header>
<h1>SENSORS:</h1>
<nav>
<table border="0">
<tr>
<th>__DATA :</th><th>__VALUE :</th>
</tr> %s
</table>
</nav>
<footer>
<p style="color:orange; text-align: center; font-family: helvetica"><i>Copyright &copy; Krzysztof Bochniak 2018</i></p>
</footer>
</body>
</html>
"""

def connect_wifi():
    import network
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if sta.isconnected()==True:
      pass
    else:
      sta.connect("SSID", "PASS")

def Pir_module():

  pir_pin=Pin(5,Pin.IN)
  if pir_pin.value() == 1:
    pins[0] = 'INTRUZ'
  elif pir_pin.value() == 0:
    pins[0] = 'OK'

def dht11_sensor():
  d = DHT11(Pin(14))
  d.measure()             # mesure temp and humidity
  temp = d.temperature()
  hum = d.humidity()
  pins[1] = str(temp) + ' C'
  pins[2] = str(hum) + ' %'

def moist():
  moisture = machine.ADC(0)
  soil = moisture.read()
  soil = ((soil-199)/824)
  soil = round(soil**-1, 2)*10
  soil = str(soil) + ' %'
  pins[3] = str(soil)

def Photo_sensitive():
  photo = Pin(16, Pin.IN)
  mesure_photo = photo.value()
  if mesure_photo == 1:
    pins[4] = 'Dark'
  elif mesure_photo == 0:
    pins[4] = 'Light'

#connect_wifi()  # WIFI CONFIG

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    Pir_module()  # show curent state after refresh
    dht11_sensor()  # show curent state after refresh
    sleep(2)
    moist()
    Photo_sensitive()
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    rows = [
            '<tr><td>%s</td><td>%s</td></tr>' % (sensors[0], pins[0]) + '\n' +
            '<tr><td>%s</td><td>%s</td></tr>' % (sensors[1], pins[1]) + '\n' +
            '<tr><td>%s</td><td>%s</td></tr>' % (sensors[2], pins[2]) + '\n' +
            '<tr><td>%s</td><td>%s</td></tr>' % (sensors[3], pins[3]) + '\n' +
            '<tr><td>%s</td><td>%s</td></tr>' % (sensors[4], pins[4])
            ]
    response = html % '\n'.join(rows)
    for row in response:
      cl.send(row)
    cl.close()

import time
import machine
import network
import esp
import socket

esp.osdebug(None)

led1 = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)
led1.off()
led2.off()
time.sleep(2)
led1.on()
led2.on()

print('Connecting...')
file = open('wifi.txt', 'r')
ESSID, PASSWORD = [x.strip() for x in file.readlines()]
file.close()
print(ESSID, PASSWORD)

file = open('home.html', 'r')
html = file.read()
file.close()

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
sta_if.active(True)
sta_if.connect(ESSID, PASSWORD)
while not sta_if.isconnected():
    print('.', end='')
    led1.off()
    time.sleep(0.1)
    led1.on()
    time.sleep(0.1)
print(' Connected')

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)
print(sta_if.ifconfig())
led2.off()
while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    request = cl.recv(1024)
    print('Request: {}'.format(request.decode('utf-8')))
    cl.send(bytes(html, 'utf-8'))
    cl.close()

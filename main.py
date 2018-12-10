import time
import machine
import network
import esp
import socket
import json

esp.osdebug(None)

led1 = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)
led1.off()
led2.off()
time.sleep(2)
led1.on()
led2.on()

state = {
    'led1': led1.value(),
    'led2': led2.value()
}

print('Connecting...')
file = open('wifi.txt', 'r')
ESSID, PASSWORD = [x.strip() for x in file.readlines()]
file.close()
print(ESSID, PASSWORD)

file = open('home.html', 'r')
html = file.read()
file.close()

file = open('script.js', 'r')
js = file.read()
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
    request = cl.recv(1024).decode('utf-8')
    print('\n\n###REQUEST###\n{}'.format(request))
    request_lines = request.split('\r\n')
    request_type, request_path, _ = request_lines[0].split(' ')
    request_info = {}
    for line in request_lines[1:]:
        if line:
            params = line.split(': ')
            if len(params)> 1:
                request_info[params[0]] = params[1]
    if request_type == 'GET':
        if request_path == '/':
            cl.send(bytes(html, 'utf-8'))
        if request_path == '/script.js':
            cl.send(bytes(js, 'utf-8'))
        if request_path == '/state.json':
            state['led1'] = led1.value()
            state['led2'] = led2.value()
            cl.send(bytes(json.dumps(state), 'utf-8'))
    if request_type == 'POST':
        pass
    cl.close()

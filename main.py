import time
import machine
import network
import esp
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

while True:
    led1.on()
    led2.on()
    print('ON')
    time.sleep(0.5)
    led1.off()
    led2.off()
    print('OFF')
    time.sleep(1.0)

import time
import machine

led1 = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)

while True:
    led1.on()
    led2.on()
    print('ON')
    time.sleep(0.5)
    led1.off()
    led2.off()
    print('OFF')
    time.sleep(1.0)

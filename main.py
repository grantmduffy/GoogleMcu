import time
import machine

led = machine.Pin(16, machine.Pin.OUT)
while True:
    led.on()
    print('ON')
    time.sleep(0.5)
    led.off()
    print('OFF')
    time.sleep(1.0)

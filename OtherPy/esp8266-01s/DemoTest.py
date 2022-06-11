import machine
import utime
S1 = machine.Pin(0,machine.Pin.IN)
while True:
    print(S1.value)
    utime.sleep(2)
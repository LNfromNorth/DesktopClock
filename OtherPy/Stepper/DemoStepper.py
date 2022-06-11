import Stepper
from machine import Pin
s = Stepper.create(Pin(0,Pin.OUT),Pin(1,Pin.OUT),Pin(2,Pin.OUT),Pin(3,Pin.OUT),delay=1)

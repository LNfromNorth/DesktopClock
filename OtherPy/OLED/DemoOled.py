from machine import Pin,I2C
import MyDemo
i2c = I2C(0,sda = Pin(0),scl=Pin(1),freq=400000)
oled = MyDemo(128,64,i2c)

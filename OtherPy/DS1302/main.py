from machine import Pin,I2C
from ssd1306 import SSD1306_I2C
from DS1302 import DS1302
import time

i2c = I2C(1,sda = Pin(14),scl=Pin(15),freq=400000)
oled = SSD1306_I2C(128,64,i2c)
ds1302 = DS1302(0,1,2)
ds1302.SetTime(22,6,8,22,15,00,3)

while(1):
    oled.fill(0)
    date = ds1302.Now()
    oled.text("{0}-{1}-{2}".format(date[0],date[1],date[2]),15,20,1)
    oled.text("{0}:{1}:{2}".format(date[3],date[4],date[5]),25,40,1)
    oled.show()
# project 1
# 利用温湿度传感器获取温湿度数据
# 使用oled进行展示

from machine import Pin,I2C
from DHT22 import DHT22
from ssd1306 import SSD1306_I2C
import utime
# oled控制
i2c = I2C(0,scl=Pin(1),sda=Pin(0),freq=400000)
oled = SSD1306_I2C(128,64,i2c)
# 温湿度控制
dht_data = Pin(2,Pin.IN,Pin.PULL_UP)
dht_sensor=DHT22(dht_data,dht11=True)
while True:
    utime.sleep(3)
    oled.fill(0)
    oled.show()
    T,H = dht_sensor.read()
    oled.text("temperature:{}C".format(T),2,10,1)
    oled.text("humidity:{}%".format(H),5,30,1)
    oled.show()
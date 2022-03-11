from machine import UART,Pin
from wifiat import at
import ujson

class Message:
    def __init__(self,location):
        self.location = location
        uart = UART(1,115200)
        self.AT = at(uart)
        self.AT.info()
    
    def get_message(self):
        c=self.AT.get_weather(self.location)
        x = c.split("\r\n")
        json = x[-1]
        text = ujson.loads(x[-1])
        code = text['results'][0]['now']['code']
        temperature = text['results'][0]['now']['temperature']
        date = x[1]
        h = date[23:25]
        m = date[26:28]
        s = date[29:31]
        return code,temperature,h,m,s
        
        
        
        
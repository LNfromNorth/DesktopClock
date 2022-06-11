from ssd1306 import SSD1306_I2C
from machine import Pin,I2C
from Numbers import Numbers
from Weather import Weather
from Message import Message
import utime

class MyDemo:
    def __init__(self, width, height, external_vcc,location):
        self.ssd1306 = SSD1306_I2C(width,height,external_vcc)
        self.message = Message(location)
        self.reget_weather()
        self.draw_restart()
        while True:
            self.getTime()
            self.draw_point(self.seconds%2)
            utime.sleep(1)
        
    def reget_weather(self):
        code,t,h,mi,s = self.message.get_message()
        self.temperature = int(t)
        self.code = int(code)
        self.hours = int(h)+8
        self.minutes = int(mi)
        self.seconds = int(s)
        
        
        
    def draw_restart(self):
        self.ssd1306.fill(0)
        self.ssd1306.hline(0,11,127,11,1)
        self.ssd1306.hline(70,12,70,47,1)
        self.ssd1306.hline(0,48,127,48,1)
        self.ssd1306.text('Ordos',46,1)
        self.draw_Tem(self.temperature)
        self.draw_Mgrid(1,5,0)
        self.draw_Mgrid(123,5,1)
        Weather(self.ssd1306,75,12,self.code)
        self.setTime()
        self.ssd1306.show()
        
    def getTime(self):
        self.seconds = self.seconds+1
        if self.seconds == 60:
            self.seconds = 0
            self.minutes = self.minutes +1
            self.draw_restart()
            if self.minutes == 60:
                self.minutes = 0
                self.hours = self.hours + 1
                if self.hours ==24:
                    self.hours = 0
                    self.reget_weather()
        
        
        
    
        
    def setTime(self):
        h2 = self.hours%10
        h1 = int((self.hours-h2)/10)
        m2 = self.minutes%10
        m1 = int((self.minutes-m2)/10)
        self.draw_showtime(h1,h2,m1,m2)
        
        
    def draw_showtime(self,h1,h2,m1,m2):
        Numbers(self.ssd1306,0,19,21,12,h1)
        Numbers(self.ssd1306,15,19,21,12,h2)
        Numbers(self.ssd1306,34,19,21,12,m1)
        Numbers(self.ssd1306,49,19,21,12,m2)
        self.ssd1306.show()
    
    def draw_point(self,flag):
        self.ssd1306.hline(30,25,31,25,flag)
        self.ssd1306.hline(30,26,31,26,flag)
        self.ssd1306.hline(30,33,31,33,flag)
        self.ssd1306.hline(30,34,31,34,flag)
        self.ssd1306.show()
        
        
    def draw_Tem(self,T):
        self.ssd1306.text("Temperature:{}".format(T),7,54,1)
        self.ssd1306.show()
        
    def draw_grid(self,x):
        self.ssd1306.hline(x,1,x+3,1,1)
        self.ssd1306.hline(x,2,x+3,2,1)
        self.ssd1306.hline(x,3,x+3,3,1)
        self.ssd1306.hline(x,4,x+3,4,1)
        self.ssd1306.hline(x,5,x+3,5,1)
        self.ssd1306.hline(x,6,x+3,6,1)
        self.ssd1306.hline(x,7,x+3,7,1)
        self.ssd1306.hline(x,8,x+3,8,1)
        self.ssd1306.hline(x,9,x+3,9,1)
        
    def draw_Mgrid(self,x,number,flag):
        for i in range(0,number):
            self.draw_grid(x)
            if flag == 0:
                x = x + 6
            else:
                x = x - 6
        
        
        
        
        
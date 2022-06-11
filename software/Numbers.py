from ssd1306 import SSD1306_I2C

class Numbers:
    def __init__(self,ssd1306,x,y,h,w,number):
        self.X = x
        self.Y = y
        self.H = h
        self.W = w
        self.M = int((self.H/2-1)+self.Y)
        self.ssd = ssd1306
        self.number(number)
        
    def number(self,number):
        if number==0:
            self.draw_a()
            self.draw_b()
            self.draw_c()
            self.draw_d()
            self.draw_e()
            self.draw_f()
        elif number==1:
            self.draw_b()
            self.draw_c()
        elif number==2:
            self.draw_a()
            self.draw_b()
            self.draw_d()
            self.draw_e()
            self.draw_g()
        elif number==3:
            self.draw_a()
            self.draw_b()
            self.draw_c()
            self.draw_d()
            self.draw_g()
        elif number==4:
            self.draw_b()
            self.draw_c()
            self.draw_f()
            self.draw_g()
        elif number==5:
            self.draw_a()
            self.draw_c()
            self.draw_d()
            self.draw_f()
            self.draw_g()
        elif number==6:
            self.draw_a()
            self.draw_c()
            self.draw_d()
            self.draw_e()
            self.draw_f()
            self.draw_g()
        elif number==7:
            self.draw_a()
            self.draw_b()
            self.draw_c()
        elif number==8:
            self.draw_a()
            self.draw_b()
            self.draw_c()
            self.draw_d()
            self.draw_e()
            self.draw_f()
            self.draw_g()
        elif number==9:
            self.draw_a()
            self.draw_b()
            self.draw_c()
            self.draw_d()
            self.draw_f()
            self.draw_g()
            
    # def draw_0(self):
        # self.ssd.hline(self.X,self.Y,self.X,self.Y+self.H,1)
        # self.ssd.hline(self.X+1,self.Y,self.X+1,self.Y+self.H,1)
        # self.ssd.hline(self.X,self.Y,self.X+self.W,self.Y,1)
        # self.ssd.hline(self.X,self.Y+1,self.X+self.W,self.Y+1,1)
        # self.ssd.hline(self.X+self.W,self.Y,self.X+self.W,self.Y+self.H,1)
        # self.ssd.hline(self.X+self.W-1,self.Y,self.X+self.W-1,self.Y+self.H,1)
        # self.ssd.hline(self.X,self.Y+self.H,self.X+self.W,self.Y+self.H,1)
        # self.ssd.hline(self.X,self.Y+self.H-1,self.X+self.W,self.Y+self.H-1,1)
        
    def draw_a(self):
        self.ssd.hline(self.X,self.Y,self.X+self.W,self.Y,1)
        self.ssd.hline(self.X,self.Y+1,self.X+self.W,self.Y+1,1)
        
    def draw_b(self):
        self.ssd.hline(self.X+self.W,self.Y,self.X+self.W,self.M+1,1)
        self.ssd.hline(self.X+self.W-1,self.Y,self.X+self.W-1,self.M+1,1)
    
    def draw_c(self):
        self.ssd.hline(self.X+self.W,self.M,self.X+self.W,self.Y+self.H,1)
        self.ssd.hline(self.X+self.W-1,self.M,self.X+self.W-1,self.Y+self.H,1)
    
    def draw_d(self):
        self.ssd.hline(self.X,self.Y+self.H,self.X+self.W,self.Y+self.H,1)
        self.ssd.hline(self.X,self.Y+self.H-1,self.X+self.W,self.Y+self.H-1,1)
    
    def draw_e(self):
        self.ssd.hline(self.X,self.M,self.X,self.Y+self.H,1)
        self.ssd.hline(self.X+1,self.M,self.X+1,self.Y+self.H,1)
    
    def draw_f(self):
        self.ssd.hline(self.X,self.Y,self.X,self.M+1,1)
        self.ssd.hline(self.X+1,self.Y,self.X+1,self.M+1,1)
    
    def draw_g(self):
        self.ssd.hline(self.X,self.M,self.X+self.W,self.M,1)
        self.ssd.hline(self.X,self.M+1,self.X+self.W,self.M+1,1)
    
    
    
    
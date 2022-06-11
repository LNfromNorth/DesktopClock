from machine import Pin

W_SECOND      = const(0x80)
W_MINUTE      = const(0x82)
W_HOUR        = const(0x84)
W_DATE        = const(0x86)
W_MONTH       = const(0x88)
W_WEEK        = const(0x8A)
W_YEAR        = const(0x8C)
W_WP          = const(0x8E)

R_SECOND      = const(0x81)
R_MINUTE      = const(0x83)
R_HOUR        = const(0x85)
R_DATE        = const(0x87)
R_MONTH       = const(0x89)
R_WEEK        = const(0x8B)
R_YEAR        = const(0x8D)



class DS1302():
    def __init__(self,SCLK,DAT,RST):
        self.resetPin = DAT
        self.SCLK = Pin(SCLK,Pin.OUT)
        self.DAT = Pin(DAT,Pin.OUT)
        self.RST = Pin(RST,Pin.OUT)
        self.SCLK.off()
        self.RST.off()
        
    def SetTime(self,YEAR,MONTH,DAY,HOUR,MINUTE,SECOND,WEEK):
        self.WriteByte(W_WP,0x00);
        YEAR = int(YEAR/10)*16+YEAR%10
        self.WriteByte(W_YEAR,YEAR);
        MONTH = int(MONTH/10)*16+MONTH%10
        self.WriteByte(W_MONTH,MONTH);
        DAY = int(DAY/10)*16+DAY%10
        self.WriteByte(W_DATE,DAY);
        self.WriteByte(W_HOUR,HOUR);
        MINUTE = int(MINUTE/10)*16+MINUTE%10
        self.WriteByte(W_MINUTE,MINUTE);
        SECOND = int(SECOND/10)*16+SECOND%10
        self.WriteByte(W_SECOND,SECOND);
        self.WriteByte(W_WEEK,WEEK);
        self.WriteByte(W_WP,0x80);
        
    def GetTime(self):
        date = []
        Temp = self.ReadByte(R_YEAR)
        Temp = ((Temp&0xF0)>>4)*10+(Temp&0x0F)
        date.append(Temp)
        Temp = self.ReadByte(R_MONTH)
        Temp = ((Temp&0x10)>>4)*10+(Temp&0x0F)
        date.append(Temp)
        Temp = self.ReadByte(R_DATE)
        Temp = ((Temp&0x20)>>4)*10+(Temp&0x0F)
        date.append(Temp)
        Temp = self.ReadByte(R_HOUR)
        Temp = (Temp&0x1F)
        date.append(Temp)
        Temp = self.ReadByte(R_MINUTE)
        Temp = ((Temp&0x70)>>4)*10+(Temp&0x0F)
        date.append(Temp)
        Temp = self.ReadByte(R_SECOND)
        Temp = ((Temp&0x70)>>4)*10+(Temp&0x0F)
        date.append(Temp)
        Temp = self.ReadByte(R_WEEK)
        date.append(Temp)
        return date
    
    def Now(self):
        date = self.GetTime()
        Now = []
        Year = "20{0}".format(date[0])
        Now.append(Year)
        Month = "0{0}".format(date[1]) if (date[1]/10)<1 else "{0}".format(date[1])
        Now.append(Month)
        Day = "0{0}".format(date[2]) if (date[2]/10)<1 else "{0}".format(date[2])
        Now.append(Day)
        Hour = "0{0}".format(date[3]) if (date[3]/10)<1 else "{0}".format(date[3])
        Now.append(Hour)
        Minute = "0{0}".format(date[4]) if (date[4]/10)<1 else "{0}".format(date[4])
        Now.append(Minute)
        Second = "0{0}".format(date[5]) if (date[5]/10)<1 else "{0}".format(date[5])
        Now.append(Second)
        Now.append(date[6])
        return Now
        
        
    def WriteByte(self,Command,Data):
        self.RST.on()
        Pin(self.resetPin,Pin.OUT)
        for i in range(0,8):
            if Command&(0x01<<i):
                self.DAT.on()
            else:
                self.DAT.off()
            self.SCLK.on()
            self.SCLK.off()
        for i in range(0,8):
            if Data&(0x01<<i):
                self.DAT.on()
            else:
                self.DAT.off()
            self.SCLK.on()
            self.SCLK.off()
        self.RST.off()
    
    def ReadByte(self,Command):
        Data = 0x00
        Pin(self.resetPin,Pin.OUT)
        self.RST.on()
        for i in range(0,8):
            if Command&(0x01<<i):
                self.DAT.on()
            else:
                self.DAT.off()
            self.SCLK.on()
            self.SCLK.off()
        Pin(self.resetPin,Pin.IN)
        for i in range(0,8):
            bit = self.DAT.value()
            Data |= (bit<<i)
            self.SCLK.on()
            self.SCLK.off()
        self.RST.off()
        return Data
#author#======================================
#file:IR_REMOTE.py
#Wang Xiaochen 2020.11.12 Ver1.0
#Tsinghua
#=============================================

#import libraries#============================
from machine import Timer
from machine import Pin
#=============================================

#key value define#============================
#TIM--
TIM_PERIOD            = 0xFFFF
#SIGNSL--
SIGNAL_9000US_COUNT   = 925   # x10us
SIGNAL_4500US_COUNT   = 446   # x10us
SIGNAL_2250US_COUNT   = 225   # x10us
SIGNAL_1690US_COUNT   = 161   # x10us
SIGNAL_560US_COUNT    = 57    # x10us
SIGNAL_TOLERANCE      = 10    # x10us
SIGNAL_REPEAT_TIMEOUT = 1100  # x10us
#=============================================

#class#=======================================
class IR:
    def __init__(self, tim = 3, channel = 4, pin = Pin.board.IR_REMOTE):
        self.tim = Timer(tim, prescaler = (840 - 1), period = TIM_PERIOD)
        self.input_pin = pin
        self.input_capture_channel = self.tim.channel(channel, Timer.IC, pin = self.input_pin, polarity = Timer.BOTH)
        self.input_capture_channel.callback(self.input_capture_callback)
        self.signal_start_flag = False
        self.signal_repeat_flag = False
        self.signal_high_time = 0
        self.signal_low_time = 0
        self.signal_high_width = 0
        self.signal_low_width = 0
        self.signal_recive = [0, 0, 0, 0]
        self.signal_bit_count = 0
        self.signal_byte_count = 0
        self.signal_address = 0
        self.signal_command = 0
        self.signal_address_last = 0
        self.signal_command_last = 0
        self.callback = None
        self.reset()

    def reset(self):
        self.signal_recive[0] = 0
        self.signal_recive[1] = 0
        self.signal_recive[2] = 0
        self.signal_recive[3] = 0
        self.signal_bit_count = 0
        self.signal_byte_count = 0
        self.signal_start_flag = False
        self.signal_high_time = 0
        self.signal_low_time = 0
        self.signal_high_width = 0
        self.signal_low_width = 0

    def capture_check_overflow(self, polarity):
        if(polarity == 1):
            if(self.signal_low_time > self.signal_high_time):
                return self.signal_low_time - self.signal_high_time
            else:
                return self.signal_low_time - self.signal_high_time + TIM_PERIOD + 1
        elif(polarity == 0):
            if(self.signal_high_time > self.signal_low_time):
                return self.signal_high_time - self.signal_low_time
            else:
                return self.signal_high_time - self.signal_low_time + TIM_PERIOD + 1
        else:
            return 0
    
    def bit_shift(self, bit):
        self.signal_recive[self.signal_byte_count] = self.signal_recive[self.signal_byte_count] >> 1
        self.signal_recive[self.signal_byte_count] = self.signal_recive[self.signal_byte_count] | bit << 7
        self.signal_bit_count = self.signal_bit_count + 1
        if(self.signal_bit_count > 7):
            self.signal_bit_count = 0
            self.signal_byte_count = self.signal_byte_count + 1
        if(self.signal_byte_count > 3):
            if(self.signal_recive[0] ^ self.signal_recive[1] ^ \
               self.signal_recive[2] ^ self.signal_recive[3] == 0):
                self.signal_address = self.signal_recive[0]
                self.signal_command = self.signal_recive[2]
                self.signal_address_last = self.signal_address
                self.signal_command_last = self.signal_command
                if(self.callback):
                    self.callback(self, self.signal_address, self.signal_command, False)
            self.reset()
        
    def input_capture_callback(self, tim):
        if(self.input_pin.value() == 0):
            self.signal_low_time = self.input_capture_channel.capture()
            self.signal_high_width = self.capture_check_overflow(1)
            
            if(self.signal_low_width > (SIGNAL_9000US_COUNT - SIGNAL_TOLERANCE) and \
               self.signal_low_width < (SIGNAL_9000US_COUNT + SIGNAL_TOLERANCE)):
                if(self.signal_high_width > (SIGNAL_4500US_COUNT - SIGNAL_TOLERANCE) and \
                   self.signal_high_width < (SIGNAL_4500US_COUNT + SIGNAL_TOLERANCE)):
                    self.signal_start_flag = True
                elif(self.signal_high_width > (SIGNAL_2250US_COUNT - SIGNAL_TOLERANCE) and \
                 self.signal_high_width < (SIGNAL_2250US_COUNT + SIGNAL_TOLERANCE)):
                    self.signal_repeat_flag = True
                    self.signal_address = self.signal_address_last
                    self.signal_command = self.signal_command_last
                    if(self.callback):
                        self.callback(self, self.signal_address, self.signal_command, True)
            elif(self.signal_low_width > (SIGNAL_560US_COUNT - SIGNAL_TOLERANCE) and \
                 self.signal_low_width < (SIGNAL_560US_COUNT + SIGNAL_TOLERANCE) and \
                 self.signal_start_flag == True):
                if(self.signal_high_width > (SIGNAL_560US_COUNT - SIGNAL_TOLERANCE) and \
                   self.signal_high_width < (SIGNAL_560US_COUNT + SIGNAL_TOLERANCE)):
                    self.bit_shift(0)
                elif(self.signal_high_width > (SIGNAL_1690US_COUNT - SIGNAL_TOLERANCE) and \
                     self.signal_high_width < (SIGNAL_1690US_COUNT + SIGNAL_TOLERANCE)):
                    self.bit_shift(1)
        else:
            self.signal_high_time = self.input_capture_channel.capture()
            self.signal_low_width = self.capture_check_overflow(0)
        
    def ir_remote_get(self):
        temp_address = self.signal_address
        temp_command = self.signal_command
        temp_flag = self.signal_repeat_flag
        self.signal_repeat_flag = False
        self.signal_address = 0
        self.signal_command = 0
        return(temp_address, temp_command, temp_flag)

    def ir_remote_callback_set(self, function):
        self.callback = function

#=============================================

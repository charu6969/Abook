# *****************************************************************************
# * | File        :	  Pico_CapTouch_ePaper_Test_2in9.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020-06-02
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from machine import Pin, SPI, I2C
import framebuf
import utime

# Display resolution
EPD_WIDTH       = 128
EPD_HEIGHT      = 296

WF_PARTIAL_2IN9 = [
0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x80,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x40,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0A,0x0,0x0,0x0,0x0,0x0,0x0,  
0x1,0x0,0x0,0x0,0x0,0x0,0x0,
0x1,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,
0x22,0x17,0x41,0xB0,0x32,0x36,
]

WF_PARTIAL_2IN9_Wait = [
0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x80,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x40,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0A,0x0,0x0,0x0,0x0,0x0,0x2,  
0x1,0x0,0x0,0x0,0x0,0x0,0x0,
0x1,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,
0x22,0x17,0x41,0xB0,0x32,0x36,
]

# e-Paper
RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

# TP
TRST    = 16
INT     = 17

# key
KEY0 = 2
KEY1 = 3
KEY2 = 15

class config():
    def __init__(self, i2c_addr):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        self.busy_pin = Pin(BUSY_PIN, Pin.IN)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)

        self.trst_pin = Pin(TRST, Pin.OUT)
        self.int_pin = Pin(INT, Pin.IN)

        self.key0 = Pin(KEY0, Pin.IN, Pin.PULL_UP)
        self.key1 = Pin(KEY1, Pin.IN, Pin.PULL_UP)
        self.key2 = Pin(KEY2, Pin.IN, Pin.PULL_UP)

        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.address = i2c_addr
        self.i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100_000)

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def i2c_writebyte(self, reg, value):
        wbuf = [(reg>>8)&0xff, reg&0xff, value]
        self.i2c.writeto(self.address, bytearray(wbuf))

    def i2c_write(self, reg):
        wbuf = [(reg>>8)&0xff, reg&0xff]
        self.i2c.writeto(self.address, bytearray(wbuf))

    def i2c_readbyte(self, reg, len):
        self.i2c_write(reg)
        rbuf = bytearray(len)
        self.i2c.readfrom_into(self.address, rbuf)
        return rbuf

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)
        self.digital_write(self.trst_pin, 0)


class EPD_2in9(framebuf.FrameBuffer):
    def __init__(self):
        self.config = config(0x48)

        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

        self.black = 0x00
        self.white = 0xff
        self.darkgray = 0xaa
        self.grayish = 0x55

        self.lut = WF_PARTIAL_2IN9
        self.lut_l = WF_PARTIAL_2IN9_Wait

        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HLSB)

    # Hardware reset
    def reset(self):
        self.config.digital_write(self.config.reset_pin, 1)
        self.config.delay_ms(50) 
        self.config.digital_write(self.config.reset_pin, 0)
        self.config.delay_ms(2)
        self.config.digital_write(self.config.reset_pin, 1)
        self.config.delay_ms(50)   

    def send_command(self, command):
        self.config.digital_write(self.config.dc_pin, 0)
        self.config.digital_write(self.config.cs_pin, 0)
        self.config.spi_writebyte([command])
        self.config.digital_write(self.config.cs_pin, 1)

    def send_data(self, data):
        self.config.digital_write(self.config.dc_pin, 1)
        self.config.digital_write(self.config.cs_pin, 0)
        self.config.spi_writebyte([data])
        self.config.digital_write(self.config.cs_pin, 1)

    def ReadBusy(self):
        while(self.config.digital_read(self.config.busy_pin) == 1):
            self.config.delay_ms(10)

    def TurnOnDisplay(self):
        self.send_command(0x22)
        self.send_data(0xF7)
        self.send_command(0x20)
        self.ReadBusy()

    def TurnOnDisplay_Partial(self):
        self.send_command(0x22)
        self.send_data(0x0F)
        self.send_command(0x20)
        self.ReadBusy()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def SendLut(self, isQuick):
        self.send_command(0x32)
        if(isQuick):
            for i in range(0, 153):
                self.send_data(self.lut_l[i])
        else:
            for i in range(0, 153):
                self.send_data(self.lut[i])
        self.ReadBusy()

    def SetWindow(self, x_start, y_start, x_end, y_end):
        self.send_command(0x44)
        self.send_data((x_start>>3) & 0xFF)
        self.send_data((x_end>>3) & 0xFF)
        
        self.send_command(0x45)
        self.send_data(y_start & 0xFF)
        self.send_data((y_start >> 8) & 0xFF)
        self.send_data(y_end & 0xFF)
        self.send_data((y_end >> 8) & 0xFF)

    def SetCursor(self, x, y):
        self.send_command(0x4E)
        self.send_data(x & 0xFF)
        
        self.send_command(0x4F)
        self.send_data(y & 0xFF)
        self.send_data((y >> 8) & 0xFF)
        self.ReadBusy()

    def init(self):
        self.reset()
        self.ReadBusy()   
        self.send_command(0x12)
        self.ReadBusy()   

        self.send_command(0x01)
        self.send_data(0x27)
        self.send_data(0x01)
        self.send_data(0x00)

        self.send_command(0x11)
        self.send_data(0x03)

        self.SetWindow(0, 0, self.width-1, self.height-1)

        self.send_command(0x21)
        self.send_data(0x00)
        self.send_data(0x80)	

        self.SetCursor(0, 0)
        self.ReadBusy()
        return 0

    def display(self, image):
        if (image == None):
            return            
        self.send_command(0x24)
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(image[i])   
        self.TurnOnDisplay()

    def display_Base(self, image):
        if (image == None):
            return   
        self.send_command(0x24)
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(image[i])
        self.send_command(0x26)
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(image[i])
        self.TurnOnDisplay()

    def display_Partial(self, image):
        if (image == None):
            return

        self.config.digital_write(self.config.reset_pin, 0)
        self.config.delay_ms(0.2)
        self.config.digital_write(self.config.reset_pin, 1) 

        self.SendLut(1)
        self.send_command(0x37)
        self.send_data(0x00)
        self.send_data(0x00)  
        self.send_data(0x00)  
        self.send_data(0x00) 
        self.send_data(0x00)  	
        self.send_data(0x40)  
        self.send_data(0x00)  
        self.send_data(0x00)   
        self.send_data(0x00)  
        self.send_data(0x00)

        self.send_command(0x3C)
        self.send_data(0x80)

        self.send_command(0x22) 
        self.send_data(0xC0)   
        self.send_command(0x20) 
        self.ReadBusy()

        self.SetWindow(0, 0, self.width - 1, self.height - 1)
        self.SetCursor(0, 0)

        self.send_command(0x24)
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(image[i])
        self.TurnOnDisplay_Partial()

    def Clear(self, color):
        self.send_command(0x24)
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(color)
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x10)
        self.send_data(0x01)
        self.config.delay_ms(2000)
        self.config.module_exit()


class ICNT_Development():
    def __init__(self):
        self.Touch = 0
        self.TouchGestureid = 0
        self.TouchCount = 0

        self.TouchEvenid = [0, 1, 2, 3, 4]
        self.X = [0, 1, 2, 3, 4]
        self.Y = [0, 1, 2, 3, 4]
        self.P = [0, 1, 2, 3, 4]


class ICNT86():
    def __init__(self):
        self.config = config(0x48)
        # Touch calibration parameters
        self.x_min = 0
        self.x_max = 4095
        self.y_min = 0
        self.y_max = 4095
        self.x_offset = 0
        self.y_offset = 0
        self.x_scale = 1.0
        self.y_scale = 1.0
        self.invert_x = False
        self.invert_y = False
        self.swap_xy = False

    def ICNT_Reset(self):
        self.config.digital_write(self.config.trst_pin, 1)
        self.config.delay_ms(100)
        self.config.digital_write(self.config.trst_pin, 0)
        self.config.delay_ms(100)
        self.config.digital_write(self.config.trst_pin, 1)
        self.config.delay_ms(100)

    def ICNT_Write(self, Reg, Data):
        self.config.i2c_writebyte(Reg, Data)

    def ICNT_Read(self, Reg, len):
        return self.config.i2c_readbyte(Reg, len)

    def ICNT_ReadVersion(self):
        buf = self.ICNT_Read(0x000a, 4)
        print(buf)

    def ICNT_Init(self):
        self.ICNT_Reset()
        self.ICNT_ReadVersion()

    def calibrate_touch(self, raw_x, raw_y):
        """Calibrate touch coordinates to match display"""
        # Apply offset
        calibrated_x = raw_x + self.x_offset
        calibrated_y = raw_y + self.y_offset
        
        # Clamp to range
        calibrated_x = max(self.x_min, min(calibrated_x, self.x_max))
        calibrated_y = max(self.y_min, min(calibrated_y, self.y_max))
        
        # Normalize to 0-1 range
        norm_x = (calibrated_x - self.x_min) / (self.x_max - self.x_min)
        norm_y = (calibrated_y - self.y_min) / (self.y_max - self.y_min)
        
        # Apply inversion if needed
        if self.invert_x:
            norm_x = 1.0 - norm_x
        if self.invert_y:
            norm_y = 1.0 - norm_y
            
        # Scale to display coordinates (128x296)
        display_x = int(norm_x * 127 * self.x_scale)
        display_y = int(norm_y * 295 * self.y_scale)
        
        # Swap X and Y if needed
        if self.swap_xy:
            display_x, display_y = display_y, display_x
            
        # Clamp to display bounds
        display_x = max(0, min(display_x, 127))
        display_y = max(0, min(display_y, 295))
        
        return display_x, display_y

    def ICNT_Scan(self, ICNT_Dev, ICNT_Old, debug=False):
        buf = []
        mask = 0x00

        if ICNT_Dev.Touch == 1:
            ICNT_Dev.Touch = 0
            buf = self.ICNT_Read(0x1001, 1)

            if buf[0] == 0x00:
                self.ICNT_Write(0x1001, mask)
                self.config.delay_ms(1)
                if debug:
                    print("No touch data")
                return
            else:
                ICNT_Dev.TouchCount = buf[0]

            if ICNT_Dev.TouchCount > 5 or ICNT_Dev.TouchCount < 1:
                self.ICNT_Write(0x1001, mask)
                ICNT_Dev.TouchCount = 0
                if debug:
                    print("Invalid touch count:", ICNT_Dev.TouchCount)
                return

            buf = self.ICNT_Read(0x1002, ICNT_Dev.TouchCount * 7)
            self.ICNT_Write(0x1001, mask)

            ICNT_Old.X[0] = ICNT_Dev.X[0]
            ICNT_Old.Y[0] = ICNT_Dev.Y[0]
            ICNT_Old.P[0] = ICNT_Dev.P[0]

            for i in range(0, ICNT_Dev.TouchCount):
                ICNT_Dev.TouchEvenid[i] = buf[6 + 7*i]
                
                # Read raw coordinates from touch controller
                raw_x = ((buf[4 + 7*i] << 8) + buf[3 + 7*i])
                raw_y = ((buf[2 + 7*i] << 8) + buf[1 + 7*i])
                ICNT_Dev.P[i] = buf[5 + 7*i]
                
                # Calibrate the coordinates
                display_x, display_y = self.calibrate_touch(raw_x, raw_y)
                ICNT_Dev.X[i] = display_x
                ICNT_Dev.Y[i] = display_y
                
                if debug:
                    print(f"Raw: X={raw_x}, Y={raw_y} | Display: X={display_x}, Y={display_y}")

            return
        return


def touch_callback(pin):
    """Callback for touch interrupt"""
    icnt_dev.Touch = 1


def get_key():
    """Check for key presses"""
    if tp.config.digital_read(tp.config.key0) == 0:
        return 1  # KEY0
    elif tp.config.digital_read(tp.config.key1) == 0:
        return 2  # KEY1
    elif tp.config.digital_read(tp.config.key2) == 0:
        return 3  # KEY2
    else:
        return 0  # No key pressed


def draw_test_screen(epd):
    """Draw a test screen with calibration points"""
    epd.fill(0xff)  # Clear with white
    
    # Draw title
    epd.text("Touch Test", 35, 10, 0x00)
    epd.hline(20, 30, 88, 0x00)
    
    # Draw calibration points
    # Top-left corner
    epd.fill_circle(10, 50, 3, 0x00)
    epd.text("TL", 15, 60, 0x00)
    
    # Top-right corner
    epd.fill_circle(118, 50, 3, 0x00)
    epd.text("TR", 110, 60, 0x00)
    
    # Bottom-left corner
    epd.fill_circle(10, 250, 3, 0x00)
    epd.text("BL", 15, 260, 0x00)
    
    # Bottom-right corner
    epd.fill_circle(118, 250, 3, 0x00)
    epd.text("BR", 110, 260, 0x00)
    
    # Center
    epd.fill_circle(64, 150, 3, 0x00)
    epd.text("CENTER", 45, 160, 0x00)
    
    # Instructions
    epd.text("Touch each point", 20, 280, 0x00)
    epd.text("to calibrate", 35, 290, 0x00)


def draw_sketch_screen(epd, last_point=None):
    """Draw the sketch screen"""
    epd.fill(0xff)  # Clear with white
    
    # Draw title bar
    epd.fill_rect(0, 0, 128, 20, 0x00)
    epd.text("Sketch Mode", 25, 6, 0xff)
    
    # Draw drawing area border
    epd.rect(2, 22, 124, 250, 0x00)
    
    # Draw instructions
    epd.text("Draw here", 40, 275, 0x00)
    
    # Draw crosshair at last point if provided
    if last_point:
        x, y = last_point
        epd.hline(x-5, y, 11, 0x00)
        epd.vline(x, y-5, 11, 0x00)


def simple_sketch_mode():
    """Simple sketch mode with debug output"""
    global icnt_dev, icnt_old, tp, epd
    
    print("\n=== Simple Sketch Mode ===")
    print("Touch the screen to draw")
    print("Press KEY1 to clear")
    print("Press KEY2 to exit\n")
    
    # Clear screen
    epd.fill(0xff)
    epd.text("Simple Sketch", 20, 10, 0x00)
    epd.text("Touch to draw", 25, 140, 0x00)
    epd.display_Base(epd.buffer)
    
    last_x = -1
    last_y = -1
    is_drawing = False
    
    while True:
        # Check for key presses
        key = get_key()
        if key == 2:  # KEY1 - Clear
            epd.fill(0xff)
            epd.text("Simple Sketch", 20, 10, 0x00)
            epd.text("Touch to draw", 25, 140, 0x00)
            epd.display_Base(epd.buffer)
            print("Screen cleared")
            utime.sleep_ms(300)
            
        elif key == 3:  # KEY2 - Exit
            print("Exiting sketch mode")
            return
        
        # Check for touch with debug enabled
        tp.ICNT_Scan(icnt_dev, icnt_old, debug=True)
        
        if icnt_dev.TouchCount > 0:
            x = icnt_dev.X[0]
            y = icnt_dev.Y[0]
            
            # Print raw coordinates for debugging
            print(f"Touch at: X={x}, Y={y}")
            
            # Draw a point at the touch location
            if 0 <= x < 128 and 0 <= y < 296:
                # Draw a small circle
                radius = 2
                for i in range(-radius, radius + 1):
                    for j in range(-radius, radius + 1):
                        if i*i + j*j <= radius*radius:
                            px = x + i
                            py = y + j
                            if 0 <= px < 128 and 0 <= py < 296:
                                epd.pixel(px, py, 0)
                
                # If we have a previous point, draw a line
                if last_x != -1 and last_y != -1 and is_drawing:
                    # Simple line drawing
                    dx = abs(x - last_x)
                    dy = abs(y - last_y)
                    sx = 1 if last_x < x else -1
                    sy = 1 if last_y < y else -1
                    err = dx - dy
                    
                    while True:
                        # Draw point
                        for i in range(-radius, radius + 1):
                            for j in range(-radius, radius + 1):
                                if i*i + j*j <= radius*radius:
                                    px = last_x + i
                                    py = last_y + j
                                    if 0 <= px < 128 and 0 <= py < 296:
                                        epd.pixel(px, py, 0)
                        
                        if last_x == x and last_y == y:
                            break
                        
                        e2 = 2 * err
                        if e2 > -dy:
                            err -= dy
                            last_x += sx
                        if e2 < dx:
                            err += dx
                            last_y += sy
                
                last_x = x
                last_y = y
                is_drawing = True
                
                # Update display
                epd.display_Partial(epd.buffer)
        else:
            # Touch released
            if is_drawing:
                last_x = -1
                last_y = -1
                is_drawing = False
        
        utime.sleep_ms(10)


def calibration_mode():
    """Calibration mode to fix touch coordinates"""
    global icnt_dev, icnt_old, tp, epd
    
    print("\n=== Calibration Mode ===")
    print("Touch each of the 5 points on screen")
    print("We'll adjust calibration based on your touches")
    
    # Draw calibration screen
    draw_test_screen(epd)
    epd.display_Base(epd.buffer)
    
    calibration_points = [
        (10, 50),   # Top-left
        (118, 50),  # Top-right
        (64, 150),  # Center
        (10, 250),  # Bottom-left
        (118, 250)  # Bottom-right
    ]
    
    raw_points = []
    
    for i, (target_x, target_y) in enumerate(calibration_points):
        print(f"\nTouch point {i+1}: ({target_x}, {target_y})")
        print("Waiting for touch...")
        
        # Wait for touch
        touched = False
        while not touched:
            tp.ICNT_Scan(icnt_dev, icnt_old)
            if icnt_dev.TouchCount > 0:
                # Get raw coordinates (before calibration)
                buf = tp.ICNT_Read(0x1002, 7)
                raw_x = ((buf[4] << 8) + buf[3])
                raw_y = ((buf[2] << 8) + buf[1])
                
                print(f"Raw touch: X={raw_x}, Y={raw_y}")
                raw_points.append((raw_x, raw_y, target_x, target_y))
                
                # Draw feedback
                epd.fill_circle(target_x, target_y, 5, 0x00)
                epd.display_Partial(epd.buffer)
                
                touched = True
                utime.sleep_ms(500)  # Wait a bit
        
        utime.sleep_ms(100)
    
    # Calculate calibration parameters
    if len(raw_points) >= 3:
        # Find min/max raw values
        raw_x_vals = [p[0] for p in raw_points]
        raw_y_vals = [p[1] for p in raw_points]
        
        tp.x_min = min(raw_x_vals)
        tp.x_max = max(raw_x_vals)
        tp.y_min = min(raw_y_vals)
        tp.y_max = max(raw_y_vals)
        
        print(f"\nCalibration results:")
        print(f"X range: {tp.x_min} to {tp.x_max}")
        print(f"Y range: {tp.y_min} to {tp.y_max}")
        
        # Try to detect if coordinates are swapped
        if abs(tp.x_max - tp.x_min) < abs(tp.y_max - tp.y_min):
            print("Detected: X and Y might be swapped")
            tp.swap_xy = True
        
        # Save calibration to file
        try:
            with open("calibration.txt", "w") as f:
                f.write(f"x_min={tp.x_min}\n")
                f.write(f"x_max={tp.x_max}\n")
                f.write(f"y_min={tp.y_min}\n")
                f.write(f"y_max={tp.y_max}\n")
                f.write(f"swap_xy={tp.swap_xy}\n")
            print("Calibration saved to calibration.txt")
        except:
            print("Could not save calibration")
    
    print("\nCalibration complete!")
    print("Testing calibration...")
    
    # Test calibration
    epd.fill(0xff)
    epd.text("Calibration Test", 20, 10, 0x00)
    epd.text("Touch screen", 30, 140, 0x00)
    epd.text("to see cursor", 30, 155, 0x00)
    epd.display_Base(epd.buffer)
    
    for _ in range(100):  # Test for 100 iterations
        tp.ICNT_Scan(icnt_dev, icnt_old, debug=True)
        if icnt_dev.TouchCount > 0:
            x = icnt_dev.X[0]
            y = icnt_dev.Y[0]
            
            # Draw cursor at touch point
            epd.fill(0xff)
            epd.text("Calibration Test", 20, 10, 0x00)
            epd.fill_circle(x, y, 3, 0x00)
            epd.text(f"X={x}", 10, 280, 0x00)
            epd.text(f"Y={y}", 70, 280, 0x00)
            epd.display_Partial(epd.buffer)
            
            print(f"Display: X={x}, Y={y}")
        
        utime.sleep_ms(50)


def load_calibration():
    """Load calibration from file"""
    try:
        with open("calibration.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("x_min="):
                    tp.x_min = int(line.split("=")[1])
                elif line.startswith("x_max="):
                    tp.x_max = int(line.split("=")[1])
                elif line.startswith("y_min="):
                    tp.y_min = int(line.split("=")[1])
                elif line.startswith("y_max="):
                    tp.y_max = int(line.split("=")[1])
                elif line.startswith("swap_xy="):
                    tp.swap_xy = line.split("=")[1].strip() == "True"
        print("Calibration loaded from file")
        return True
    except:
        print("No calibration file found")
        return False


def main():
    global icnt_dev, icnt_old, tp, epd
    
    # Initialize display and touch
    epd = EPD_2in9()
    tp = ICNT86()
    icnt_dev = ICNT_Development()
    icnt_old = ICNT_Development()
    
    print("Initializing e-Paper Sketchbook...")
    epd.init()
    
    print("Initializing touch controller...")
    tp.ICNT_Init()
    
    # Set up touch interrupt
    tp.config.int_pin.irq(trigger=Pin.IRQ_FALLING, handler=touch_callback)
    
    # Try to load calibration
    load_calibration()
    
    # Main menu
    while True:
        epd.fill(0xff)
        epd.text("SketchBook", 30, 30, 0x00)
        epd.hline(20, 50, 88, 0x00)
        
        epd.text("1. Simple Sketch", 10, 80, 0x00)
        epd.text("2. Calibration", 10, 100, 0x00)
        epd.text("3. Exit", 10, 120, 0x00)
        
        epd.text("Use KEY0/1/2", 10, 180, 0x00)
        epd.text("to select", 10, 195, 0x00)
        
        epd.display_Base(epd.buffer)
        
        print("\n=== Main Menu ===")
        print("1. Simple Sketch Mode")
        print("2. Calibration Mode")
        print("3. Exit")
        print("\nPress KEY0 for option 1")
        print("Press KEY1 for option 2")
        print("Press KEY2 for option 3")
        
        selection = 0
        while selection == 0:
            key = get_key()
            if key == 1:  # KEY0
                selection = 1
            elif key == 2:  # KEY1
                selection = 2
            elif key == 3:  # KEY2
                selection = 3
            utime.sleep_ms(100)
        
        if selection == 1:
            simple_sketch_mode()
        elif selection == 2:
            calibration_mode()
        elif selection == 3:
            print("Exiting...")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting SketchBook...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        try:
            epd = EPD_2in9()
            epd.sleep()
            print("e-Paper is in sleep mode")
        except:
            pass
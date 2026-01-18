import machine
import time
import framebuf  # YAZI İÇİN GEREKLİ KÜTÜPHANE EKLENDİ
from math import sqrt

# ST7735 constants
NOP = 0x00
SWRESET = 0x01
RDDID = 0x04
RDDST = 0x09
SLPIN = 0x10
SLPOUT = 0x11
PTLON = 0x12
NORON = 0x13
INVOFF = 0x20
INVON = 0x21
DISPOFF = 0x28
DISPON = 0x29
CASET = 0x2A
RASET = 0x2B
RAMWR = 0x2C
RAMRD = 0x2E
COLMOD = 0x3A
MADCTL = 0x36
FRMCTR1 = 0xB1
FRMCTR2 = 0xB2
FRMCTR3 = 0xB3
INVCTR = 0xB4
DISSET5 = 0xB6
PWCTR1 = 0xC0
PWCTR2 = 0xC1
PWCTR3 = 0xC2
PWCTR4 = 0xC3
PWCTR5 = 0xC4
VMCTR1 = 0xC5
PWCTR6 = 0xFC
GMCTRP1 = 0xE0
GMCTRN1 = 0xE1

class TFT(object):
    def __init__(self, spi, dc, reset, cs):
        self.spi = spi
        self.dc = machine.Pin(dc, machine.Pin.OUT, value=0)
        self.reset = machine.Pin(reset, machine.Pin.OUT, value=0)
        self.cs = machine.Pin(cs, machine.Pin.OUT, value=1)
        self._size = (128, 128)
        
        # KIRMIZI dogru ciktigi icin OFFSET (0, 0) OLARAK AYARLANDI
        self._offset = (0, 0) 
        
        self.buf = bytearray(2)

    def _write_cmd(self, cmd):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def _write_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def init(self):
        # Hard reset
        self.reset(1)
        time.sleep_ms(5)
        self.reset(0)
        time.sleep_ms(20)
        self.reset(1)
        time.sleep_ms(150)

        self._write_cmd(SWRESET)
        time.sleep_ms(150)
        self._write_cmd(SLPOUT)
        time.sleep_ms(255)

        # Frame Rate
        self._write_cmd(FRMCTR1)
        self._write_data(bytearray([0x01, 0x2C, 0x2D]))
        self._write_cmd(FRMCTR2)
        self._write_data(bytearray([0x01, 0x2C, 0x2D]))
        self._write_cmd(FRMCTR3)
        self._write_data(bytearray([0x01, 0x2C, 0x2D, 0x01, 0x2C, 0x2D]))

        self._write_cmd(INVCTR)
        self._write_data(bytearray([0x07]))

        # Power
        self._write_cmd(PWCTR1)
        self._write_data(bytearray([0xA2, 0x02, 0x84]))
        self._write_cmd(PWCTR2)
        self._write_data(bytearray([0xC5]))
        self._write_cmd(PWCTR3)
        self._write_data(bytearray([0x0A, 0x00]))
        self._write_cmd(PWCTR4)
        self._write_data(bytearray([0x8A, 0x2A]))
        self._write_cmd(PWCTR5)
        self._write_data(bytearray([0x8A, 0xEE]))

        self._write_cmd(VMCTR1)
        self._write_data(bytearray([0x0E]))

        self._write_cmd(INVOFF)
        self._write_cmd(MADCTL)
        self._write_data(bytearray([0xC0])) 

        self._write_cmd(COLMOD)
        self._write_data(bytearray([0x05])) # 16-bit mode

        # Gamma
        self._write_cmd(GMCTRP1)
        self._write_data(bytearray([0x02, 0x1c, 0x07, 0x12, 0x37, 0x32, 0x29, 0x2d, 0x29, 0x25, 0x2b, 0x39, 0x00, 0x01, 0x03, 0x10]))
        self._write_cmd(GMCTRN1)
        self._write_data(bytearray([0x03, 0x1d, 0x07, 0x06, 0x2e, 0x2c, 0x29, 0x2d, 0x2e, 0x2e, 0x37, 0x3f, 0x00, 0x00, 0x02, 0x10]))

        self._write_cmd(NORON)
        time.sleep_ms(10)
        self._write_cmd(DISPON)
        time.sleep_ms(100)
        
        self.set_window(0, 0, 127, 127)

    def set_window(self, x0, y0, x1, y1):
        x0 += self._offset[0]
        x1 += self._offset[0]
        y0 += self._offset[1]
        y1 += self._offset[1]
        
        self._write_cmd(CASET)
        self._write_data(bytearray([0, x0, 0, x1]))
        self._write_cmd(RASET)
        self._write_data(bytearray([0, y0, 0, y1]))
        self._write_cmd(RAMWR)

    def fill(self, color):
        self.fill_rect(0, 0, self._size[0], self._size[1], color)

    def fill_rect(self, x, y, w, h, color):
        if x >= self._size[0] or y >= self._size[1]: return
        w = min(w, self._size[0] - x)
        h = min(h, self._size[1] - y)
        
        self.set_window(x, y, x + w - 1, y + h - 1)
        
        high = color >> 8
        low = color & 0xFF
        
        chunk_size = 1024
        buffer = bytearray(chunk_size * 2)
        for i in range(chunk_size):
            buffer[2*i] = high
            buffer[2*i+1] = low
            
        pixels = w * h
        while pixels > 0:
            count = min(pixels, chunk_size)
            self._write_data(buffer[:count*2])
            pixels -= count

    def pixel(self, x, y, color):
        if 0 <= x < self._size[0] and 0 <= y < self._size[1]:
            self.set_window(x, y, x, y)
            self._write_data(bytearray([color >> 8, color & 0xFF]))

    # --- TEXT FONKSIYONU DUZELTILDI ---
    def text(self, x, y, string, color):
        w = len(string) * 8
        h = 8
        
        # Framebuffer icin tampon bellek olustur
        # RGB565 formatinda her piksel 2 byte'tir
        buffer = bytearray(w * h * 2)
        
        # Framebuf nesnesi yarat
        fb = framebuf.FrameBuffer(buffer, w, h, framebuf.RGB565)
        fb.fill(0) # Siyah arka plan
        
        # Framebuffer (Little Endian) ile ST7735 (Big Endian) arasinda renk farki olusabilir.
        # Bu yuzden renk byte'larini burada ters ceviriyoruz ki dogru renk ciksin.
        swapped_color = ((color & 0xFF) << 8) | (color >> 8)
        
        fb.text(string, 0, 0, swapped_color)
        
        # Ekrana bas
        self.set_window(x, y, x + w - 1, y + h - 1)
        self._write_data(buffer)
    
    @staticmethod
    def color565(r, g, b):
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
 

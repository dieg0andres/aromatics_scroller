import math
import picounicorn
import uasyncio as asyncio

from fonts import *
from time import sleep


picounicorn.init()

class Scroller():

    offset = 0
    gap = 1
    hue = 1.0
    saturation = 1.0
    brightness = 1.0

    def hsv2rgb(self, hue, sat, val):
        """ Returns the RGB of Hue Saturation and Brightnes values """
    
        i = math.floor(hue * 6)
        f = hue * 6 - i
        p = val * (1 - sat)
        q = val * (1 - f * sat)
        t = val * (1 - (1 - f) * sat)

        r, g, b = [
            (val, t, p),
            (q, val, p),
            (p, val, t),
            (p, q, val),
            (t, p, val),
            (val, p, q),
        ][int(i % 6)]
        r = int(r*255)
        g = int(g*255)
        b = int(b*255)
        
        return r, g, b
    
    def rgb2hsv(self, r:int, g:int, b:int):
        """ Returns the Hue Saturation and Value of RGB values """
        h = 0
        s = 0
        v = 0
        # constrain the values to the range 0 to 1
        r_normal, g_normal, b_normal,  = r / 255, g / 255, b / 255
        cmax = max(r_normal, g_normal, b_normal)
        cmin = min(r_normal, g_normal, b_normal)
        delta = cmax - cmin
        
        # Hue calculation
        if(delta ==0):
            h = 0
        elif (cmax == r_normal):
            h = (60 * (((g_normal - b_normal) / delta) % 6))
        elif (cmax == g_normal):
            h = (60 * (((b_normal - r_normal) / delta) + 2))
        elif (cmax == b_normal):
            h = (60 * (((r_normal - g_normal) / delta) + 4))
        
        # Saturation calculation
        if cmax== 0:
            s = 0
        else:
            s = delta / cmax
            
        # Value calculation
        v = cmax

        return h, s, v 
    
    def clear(self):
        for col in range(16):
            for row in range(7):
                picounicorn.set_pixel(col, row, 0, 0, 0)
        
    def display_character(self, character,pos):
        r,g,b = self.hsv2rgb(self.hue, self.saturation, self.brightness)
        for row in range(0,5):
            length = len(character[0])

            for col in range (0,length):
                x = col+self.offset+pos
                y = row+1
                
                # clear gap
                if x+1 < 16 and x+1 > -1:
                    picounicorn.set_pixel(x+1, y, 0, 0, 0)
                
                # write pixel
                if x < 16 and x > -1:
                    if character[row][col] == '1':
                        picounicorn.set_pixel(x, y, r, g, b)
                        
                    else:
                        picounicorn.set_pixel(x, y, 0, 0, 0)
        
        self.offset += len(character[0]) + self.gap
       
    
    def show_message(self, message, position, hue:None):
        """ Shows the message on the display, at the
            position provided, using the Hue value
            specified """
        if hue is None:
            hue = 1.0
        self.hue = hue    
        for character in message:
            if character == ' ':
                self.display_character(space, position)
            if character == '1':
                self.display_character(one, position)
            if character == '2':
                self.display_character(two, position)
            if character == '3':
                self.display_character(three, position)
            if character == '4':
                self.display_character(four, position)
            if character == '5':
                self.display_character(five, position)
            if character == '6':
                self.display_character(six, position)
            if character == '7':
                self.display_character(seven, position)
            if character == '8':
                self.display_character(eight, position)
            if character == '9':
                self.display_character(nine, position)
            if character == '0':
                self.display_character(zero, position)
            if character == '.':
                self.display_character(fullstop, position)
            if character == 'A':
                self.display_character(A, position)
            if character == 'B':
                self.display_character(B, position)
            if character == 'C':
                self.display_character(C, position)
            if character == 'D':
                self.display_character(D, position)
            if character == 'E':
                self.display_character(E, position)
            if character == 'F':
                self.display_character(F, position)
            if character == 'G':
                self.display_character(G, position)
            if character == 'H':
                self.display_character(H, position)
            if character == 'I':
                self.display_character(I, position)
            if character == 'J':
                self.display_character(J, position)
            if character == 'K':
                self.display_character(K, position)    
            if character == 'L':
                self.display_character(L, position)
            if character == 'M':
                self.display_character(M, position)
            if character == 'N':
                self.display_character(N, position)
            if character == 'O':
                self.display_character(O, position)
            if character == 'P':
                self.display_character(P, position)
            if character == 'Q':
                self.display_character(Q, position)
            if character == 'R':
                self.display_character(R, position)
            if character == 'S':
                self.display_character(S, position)
            if character == 'T':
                self.display_character(T, position)
            if character == 'U':
                self.display_character(U, position)
            if character == 'V':
                self.display_character(V, position)
            if character == 'W':
                self.display_character(W, position)
            if character == 'X':
                self.display_character(X, position)
            if character == 'Y':
                self.display_character(Y, position)
            if character == 'Z':
                self.display_character(Z, position)

                
        self.offset = 0
        

    async def continously_display_prices(self, messages):
    # messages is an array of tuples, in which [0] is the message and [1] the hue, for example
    #messages = [("BZ 290", 0), ("RBOB 210", 1.2)]
    
        while True:
            
            for msg in messages:
                hue = msg[1]
                message = msg[0]

                for position in range(16,-len(message*(5+1)),-1):
                    self.show_message(message, position, hue)
                    sleep(0.002)
            
            await asyncio.sleep(0.5)
    

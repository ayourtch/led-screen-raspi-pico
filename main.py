#x# from machine import Pin, Timer
#x# led = Pin(15, Pin.OUT)
#x# timer = Timer()
#x# 
#x# def blink(timer):
#x#     led.toggle()
#x# 
#x# timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)

# Example using PIO to drive a set of WS2812 LEDs.

import array, time
from machine import Pin
import rp2

# Configure the number of WS2812 LEDs.
NUM_LEDS = 16*16*3
PIN_NUM = 15
brightness = 0.2

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

##########################################################################
def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(2)

def pixels_set(i, color):
    if i>=0 and i<NUM_LEDS:
        ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)

def color_chase(color, wait):
    for i in range(NUM_LEDS):
        pixels_set(i, color)
        pixels_show()
    time.sleep(0.1)
 
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)
 
 
def rainbow_cycle(wait):
    for k in range(16):
        j = k * 16
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            pixels_set(i, wheel(rc_index & 255))
        pixels_show()
        time.sleep(wait)


BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

NUM_LETTERS = int(NUM_LEDS/8/6)

def display_text(text_color, text, offs):
    for c in range(NUM_LETTERS+1):
        index = c + int(offs/6)
        if index < len(text):
            char_data = char_data_dict[text[index]]
        else:
            char_data = char_data_dict[' ']
        for y in range(8):
            for x in range(6):
                if char_data[y*6 + x] == 1:
                    color = text_color
                else:
                    color = BLACK
                if x % 2 == offs%2:
                    pixels_set(c*48 + y + 8*x - (offs%6)*8, color)
                else:
                    pixels_set(c*48 + 7 - y + 8*x - (offs%6)*8, color)
    pixels_show()

# You can add other characters to the dictionary as needed
char_data_dict = {
    'A': [
        0, 1, 1, 1, 0, 0,  #  OOO  
        1, 0, 0, 0, 1, 0,  # O   O
        1, 0, 0, 0, 1, 0,  # O   O
        1, 1, 1, 1, 1, 0,  # OOOOO
        1, 0, 0, 0, 1, 0,  # O   O
        1, 0, 0, 0, 1, 0,  # O   O
        1, 0, 0, 0, 1, 0,  # O   O
        0, 0, 0, 0, 0, 0,  #      
    ],
    'B': [
        1, 1, 1, 1, 0, 0,  # OOOO  
        1, 0, 0, 0, 1, 0,  # O   O
        1, 0, 0, 0, 1, 0,  # O   O
        1, 1, 1, 1, 0, 0,  # OOOO 
        1, 0, 0, 0, 1, 0,  # O   O
        1, 0, 0, 0, 1, 0,  # O   O
        1, 1, 1, 1, 0, 0,  # OOOO 
        0, 0, 0, 0, 0, 0,  #      
    ],
    'C': [
        0, 1, 1, 1, 0, 0,  #  OOO  
        1, 0, 0, 0, 1, 0,  # O   O
        1, 0, 0, 0, 0, 0,  # O    
        1, 0, 0, 0, 0, 0,  # O    
        1, 0, 0, 0, 0, 0,  # O    
        1, 0, 0, 0, 1, 0,  # O   O
        0, 1, 1, 1, 0, 0,  #  OOO  
        0, 0, 0, 0, 0, 0,  #      
    ],
    'D': [
        1, 1, 1, 0, 0, 0,  # OOO   
        1, 0, 0, 1, 0, 0,  # O  O  
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 1, 0, 0,  # O  O  
        1, 1, 1, 0, 0, 0,  # OOO   
        0, 0, 0, 0, 0, 0,  #       
    ],
    'E': [
        1, 1, 1, 1, 1, 0,  # OOOOO 
        1, 0, 0, 0, 0, 0,  # O     
        1, 0, 0, 0, 0, 0,  # O     
        1, 1, 1, 1, 0, 0,  # OOOO  
        1, 0, 0, 0, 0, 0,  # O     
        1, 0, 0, 0, 0, 0,  # O     
        1, 1, 1, 1, 1, 0,  # OOOOO 
        0, 0, 0, 0, 0, 0,  #       
    ],
    'F': [
        1, 1, 1, 1, 1, 0,  # OOOOO 
        1, 0, 0, 0, 0, 0,  # O     
        1, 0, 0, 0, 0, 0,  # O     
        1, 1, 1, 1, 0, 0,  # OOOO  
        1, 0, 0, 0, 0, 0,  # O     
        1, 0, 0, 0, 0, 0,  # O     
        1, 0, 0, 0, 0, 0,  # O     
        0, 0, 0, 0, 0, 0,  #       
    ],
    'G': [
        0, 1, 1, 1, 0, 0,  #  OOO  
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 0, 0,  # O     
        1, 0, 1, 1, 1, 0,  # O OOO 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        0, 1, 1, 1, 0, 0,  #  OOO  
        0, 0, 0, 0, 0, 0,  #       
    ],
    'H': [
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 1, 1, 1, 1, 0,  # OOOOO 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        0, 0, 0, 0, 0, 0,  #       
    ],
    'I': [
        1, 1, 1, 1, 1, 0,  # OOOOO 
        0, 0, 1, 0, 0, 0,  #   O   
        0, 0, 1, 0, 0, 0,  #   O   
        0, 0, 1, 0, 0, 0,  #   O   
        0, 0, 1, 0, 0, 0,  #   O   
        0, 0, 1, 0, 0, 0,  #   O   
        1, 1, 1, 1, 1, 0,  # OOOOO 
        0, 0, 0, 0, 0, 0,  #       
    ],
    'J': [
        0, 1, 1, 1, 1, 0,  #  OOOO 
        0, 0, 0, 0, 1, 0,  #     O 
        0, 0, 0, 0, 1, 0,  #     O 
        0, 0, 0, 0, 1, 0,  #     O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        0, 1, 1, 1, 0, 0,  #  OOO  
        0, 0, 0, 0, 0, 0,  #       
    ],
    'K': [
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 1, 0, 0,  # O  O  
        1, 0, 1, 0, 0, 0,  # OOO   
        1, 1, 0, 0, 0, 0,  # OOO   
        1, 0, 1, 0, 0, 0,  # O  O  
        1, 0, 0, 1, 0, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  #       
        0, 0, 0, 0, 0, 0,  #       
    ],
    'L': [
        1, 0, 0, 0, 0, 0,  # O     
        1, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0,  # O     
        1, 0, 0, 0, 0, 0,  # O     
        1, 0, 0, 0, 0, 0,  # O     
        1, 0, 0, 0, 0, 0,  # O     
        1, 1, 1, 1, 1, 0,  # OOOOO 
        0, 0, 0, 0, 0, 0,  #       
    ],
    'M': [
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 1, 0, 1, 1, 0,  # OO OO 
        1, 0, 1, 0, 1, 0,  # O O O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        0, 0, 0, 0, 0, 0,  #       
    ],
    'N': [
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # OO  O 
        1, 1, 0, 0, 1, 0,  # O O O 
        1, 0, 1, 0, 1, 0,  # O  OO 
        1, 0, 0, 1, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  #       
        0, 0, 0, 0, 0, 0,  #       
    ],
    'O': [
        0, 1, 1, 1, 0, 0,  #  OOO  
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        0, 1, 1, 1, 0, 0,  #  OOO  
        0, 0, 0, 0, 0, 0,  #       
    ],
    'P': [
        1, 1, 1, 1, 0, 0, # OOOO
        1, 0, 0, 0, 1, 0, # O O
        1, 0, 0, 0, 1, 0, # O O
        1, 1, 1, 1, 0, 0, # OOOO
        1, 0, 0, 0, 0, 0, # O
        1, 0, 0, 0, 0, 0, # O
        1, 0, 0, 0, 0, 0, # O
        0, 0, 0, 0, 0, 0, #
    ],
    'Q': [
        0, 1, 1, 1, 0, 0, # OOO
        1, 0, 0, 0, 1, 0, # O O
        1, 0, 0, 0, 1, 0, # O O
        1, 0, 0, 0, 1, 0, # O O
        1, 0, 1, 0, 1, 0, # O O O
        1, 0, 0, 1, 0, 0, # O O
        0, 1, 1, 0, 0, 0, # OOO
        0, 0, 0, 0, 0, 0, #
    ],
    'R': [
        1, 1, 1, 1, 0, 0, # OOOO
        1, 0, 0, 0, 1, 0, # O O
        1, 0, 0, 0, 1, 0, # O O
        1, 1, 1, 1, 0, 0, # OOOO
        1, 0, 1, 0, 0, 0, # O O
        1, 0, 0, 1, 0, 0, # O O
        1, 0, 0, 0, 1, 0, # O   O
        0, 0, 0, 0, 0, 0, #
    ],
    'S': [
        0, 1, 1, 1, 1, 0, # OOOO
        1, 0, 0, 0, 0, 0, # O
        1, 0, 0, 0, 0, 0, # O
        0, 1, 1, 1, 0, 0, # OOO
        0, 0, 0, 0, 1, 0, # O
        0, 0, 0, 0, 1, 0, # O
        1, 1, 1, 1, 0, 0, # OOOO
        0, 0, 0, 0, 0, 0, #
    ],
    'T': [
        1, 1, 1, 1, 1, 0,  # OOOOO 
        0, 0, 1, 0, 0, 0,  #     O 
        0, 0, 1, 0, 0, 0,  #     O 
        0, 0, 1, 0, 0, 0,  #     O 
        0, 0, 1, 0, 0, 0,  #     O 
        0, 0, 1, 0, 0, 0,  #     O 
        0, 0, 1, 0, 0, 0,  #       
        0, 0, 0, 0, 0, 0,  #       
    ],
    'U': [
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        0, 1, 1, 1, 0, 0,  #  OOO  
        0, 0, 0, 0, 0, 0,  #       
    ],
    'V': [
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        0, 1, 0, 1, 0, 0,  #  O O  
        0, 1, 0, 1, 0, 0,  #  O O  
        0, 0, 1, 0, 0, 0,  #   O   
        0, 0, 0, 0, 0, 0,  #       
    ],
    'W': [
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 0, 0, 1, 0,  # O   O 
        1, 0, 1, 0, 1, 0,  # O O O 
        1, 0, 1, 0, 1, 0,  # O O O 
        1, 1, 0, 1, 1, 0,  # OO OO 
        1, 0, 0, 0, 1, 0,  # O   O 
        0, 0, 0, 0, 0, 0, #
    ],
    'X': [
        1, 0, 0, 0, 1, 0, # O O
        1, 0, 0, 0, 1, 0, # O O
        0, 1, 0, 1, 0, 0, # O O
        0, 0, 1, 0, 0, 0, # O
        0, 1, 0, 1, 0, 0, # O O
        1, 0, 0, 0, 1, 0, # O O
        1, 0, 0, 0, 1, 0, # O O
        0, 0, 0, 0, 0, 0, #
    ],
    'Y': [
        1, 0, 0, 0, 1, 0, # O O
        1, 0, 0, 0, 1, 0, # O O
        1, 0, 0, 0, 1, 0, # O O
        0, 1, 0, 1, 0, 0, # O O
        0, 0, 1, 0, 0, 0, # O
        0, 0, 1, 0, 0, 0, # O
        0, 0, 1, 0, 0, 0, # O
        0, 0, 0, 0, 0, 0, #
    ],
    'Z': [
        1, 1, 1, 1, 1, 0, # OOOOO
        0, 0, 0, 0, 1, 0,
        0, 0, 0, 1, 0, 0, # O
        0, 0, 1, 0, 0, 0, # O
        0, 1, 0, 0, 0, 0, # O
        1, 0, 0, 0, 0, 0, # O
        1, 1, 1, 1, 1, 0, # OOOOO
        0, 0, 0, 0, 0, 0, #
    ],
    ' ': [
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
    ],
    '-': [
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 1, 1, 1, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
    ],
    '#': [
        0, 1, 0, 1, 0, 0,  # O   O 
        1, 1, 1, 1, 1, 0,  # O   O 
        0, 1, 0, 1, 0, 0,  # O   O 
        0, 1, 0, 1, 0, 0,  # O   O 
        0, 1, 0, 1, 0, 0,  # O   O 
        1, 1, 1, 1, 1, 0,  # O   O 
        0, 1, 0, 1, 0, 0,  # O   O 
        0, 0, 0, 0, 0, 0,  #       
    ],
  '~': []
}


while True:
    text = "    CRITICAL MASS - #LETSRIDETOGETHER    "
    for color in COLORS:       
      for off in range(6*len(text)):
        display_text(color, text, off)

    print("fills")
    for color in COLORS:       
        pixels_fill(color)
        pixels_show()

    print("chases")
    # for color in COLORS:       
    #     color_chase(color, 0.001)

    print("rainbow")
    rainbow_cycle(0)


import array, time
import network
import socket
from machine import Pin
import rp2
import _thread

# Configure the number of WS2812 LEDs.
NUM_LEDS = 16*16
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
    global PIN_NUM
    global NUM_LETTERS
    global char_data_dict

    for c in range(NUM_LETTERS+1):
        index = c + int(offs/6)
        if index < len(text):
            if text[index] in char_data_dict.keys():
                char_data = char_data_dict[text[index]]
            else:
                char_data = char_data_dict['X']
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
    ':': [
        0, 0, 0, 0, 0, 0, #
        0, 0, 1, 1, 0, 0, #
        0, 0, 1, 1, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
        0, 0, 1, 1, 0, 0, #
        0, 0, 1, 1, 0, 0, #
        0, 0, 0, 0, 0, 0, #
    ],
    ')': [
        0, 0, 1, 0, 0, 0, #
        0, 0, 0, 1, 0, 0, #
        0, 0, 0, 0, 1, 0, #
        0, 0, 0, 0, 1, 0, #
        0, 0, 0, 0, 1, 0, #
        0, 0, 0, 1, 0, 0, #
        0, 0, 1, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
    ],
    '(': [
        0, 0, 0, 0, 1, 0, #
        0, 0, 0, 1, 0, 0, #
        0, 0, 1, 0, 0, 0, #
        0, 0, 1, 0, 0, 0, #
        0, 0, 1, 0, 0, 0, #
        0, 0, 0, 1, 0, 0, #
        0, 0, 0, 0, 1, 0, #
        0, 0, 0, 0, 0, 0, #
    ],
    '>': [
        0, 0, 1, 0, 0, 0, #
        0, 0, 0, 1, 0, 0, #
        0, 0, 0, 0, 1, 0, #
        1, 1, 1, 1, 1, 1, #
        0, 0, 0, 0, 1, 0, #
        0, 0, 0, 1, 0, 0, #
        0, 0, 1, 0, 0, 0, #
        0, 0, 0, 0, 0, 0, #
    ],
    '<': [
        0, 0, 0, 1, 0, 0, #
        0, 0, 1, 0, 0, 0, #
        0, 1, 0, 0, 0, 0, #
        1, 1, 1, 1, 1, 1, #
        0, 1, 0, 0, 0, 0, #
        0, 0, 1, 0, 0, 0, #
        0, 0, 0, 1, 0, 0, #
        0, 0, 0, 0, 0, 0, #
    ],
  '~': []
}

thread_text1 = ""
thread_text2 = ""
thread_color = YELLOW
thread_run_text = False
thread_reset_offset = False

def led_func():
    global thread_text1
    global thread_text1
    global thread_color
    global thread_run_text
    global thread_reset_offset
    i = 0;
    while True:
        if thread_run_text:
            for ofs in range(6*len(thread_text1)):
                if not thread_run_text:
                    break
                if thread_reset_offset:
                    thread_reset_offset = False
                    break
                display_text(thread_color, thread_text1, ofs)
        else:
            display_text(thread_color, thread_text1, 0)
            time.sleep_ms(200)
            display_text(thread_color, thread_text2, 0)
            time.sleep_ms(200)



# change these please :-)
ssid = 'PHI'
password = 'chimera1'
wlan = network.WLAN(network.AP_IF)
wlan.config(essid=ssid, password=password)
wlan.active(True)
while wlan.active() == False:
    print("waiting for ap activation...")
    time.sleep(1)
    pass

print(wlan.ifconfig())

html = """<!DOCTYPE html>
<html lang="en">
    <head>
  <style>
      input[type="submit"] {
        font-size: 80px;
        padding: 35px 30px;
      }
      b {
        font-size: 140px;
      }
  </style>

    </head>
    <body>
        <form method="GET">
        <center>
        <p><b>%s</b></p>
        <hr>
        <input type="submit" name="LEFT" value="<<">
        <input type="submit" name="STOP" value="STOP">
        <input type="submit" name="RIGHT" value=">>">
        <hr/>
        <input type="submit" name="OFF" value=" * * * OFF * * * ">
        <hr/>
        <input type="submit" name="THANKS" value=" * * THANKS * *">
        <input type="submit" name="IRIGHT" value="I HAD RIGHT">
        <input type="submit" name="OVERTAKE" value="NO OVERTAKE HERE">
        <input type="submit" name="DISTANCE" value="KEEP DISTANCE">
        </center>
        </form>
    </body>
</html>
"""

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

_thread.start_new_thread(led_func, ())

print('listening on', addr)
status = "- - -"

# Listen for connections
while True:
    try:
        print('waiting for conn...')
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        led_left = request.find('/?LEFT')
        led_right = request.find('/?RIGHT')
        led_off = request.find('/?OFF')
        led_stop = request.find('/?STOP')
        led_thanks = request.find('/?THANKS')
        led_iright = request.find('/?IRIGHT')
        led_overtake = request.find('/?OVERTAKE')
        led_distance = request.find('/?DISTANCE')
        some_req = False

        if led_left == 6:
            # display_text(YELLOW, "<      ", 0)
            thread_text1 = "<      "
            thread_text2 = " <      "
            thread_run_text = False
            thread_color = YELLOW
            some_req = True
            status = " < < < < "

        if led_right == 6:
            # display_text(YELLOW, "    >  ", 0)
            thread_text1 = "    >  "
            thread_text2 = "   >   "
            thread_run_text = False
            thread_color = YELLOW
            some_req = True
            status = " > > > > "

        if led_stop == 6:
            # display_text(RED, " STOP", 0)
            thread_text1 = " STOP"
            thread_text2 = " STOP"
            thread_run_text = False
            thread_color = RED
            some_req = True
            status = " STOP "

        if led_off == 6:
            pixels_fill(BLACK)
            pixels_show()
            thread_text1 = ""
            thread_text2 = ""
            thread_run_text = False
            thread_color = RED
            some_req = True
            status = " - - - "

        if led_thanks == 6:
            thread_text1 = "     THANK YOU :) "
            thread_run_text = True
            thread_color = GREEN
            thread_reset_offset = True
            some_req = True
            status = "THANKS"

        if led_iright == 6:
            thread_text1 = "     I HAD RIGHT OF WAY "
            thread_run_text = True
            thread_color = BLUE
            thread_reset_offset = True
            some_req = True
            status = "I HAD RIGHT"

        if led_overtake == 6:
            thread_text1 = "     YOU CAN NOT OVERTAKE HERE "
            thread_run_text = True
            thread_color = YELLOW
            thread_reset_offset = True
            some_req = True
            status = "NO OVRTAKE"

        if led_distance == 6:
            thread_text1 = "     DISTANCE PLEASE RESPECT SAFETY DISTANCE "
            thread_run_text = True
            thread_color = YELLOW
            thread_reset_offset = True
            some_req = True
            status = "DISTNCE PLS"

        response = html % status
        if some_req:
            cl.send('HTTP/1.0 302 Moved\r\nLocation: /\r\n\r\n')
            print("send redirect")
        else:
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')



# Simple CircuitPython example for M5Core ESP32 board with button support

import board
import digitalio
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import time


# Set up the display
display = board.DISPLAY
splash = displayio.Group()
display.show(splash)

# Load a font
font = bitmap_font.load_font("/fonts/LeaugeSpartan.bdf")
palette = displayio.Palette(1)
palette[0] = 0xFFFFFF  # White

# Create a label
text = "Hello, World!"
text_area = label.Label(font, text=text, color=0xFFFFFF, x=10, y=10)
splash.append(text_area)

# Set up buttons
button_a = digitalio.DigitalInOut(board.BTN_A)
button_a.switch_to_input(pull=digitalio.Pull.UP)

button_b = digitalio.DigitalInOut(board.BTN_B)
button_b.switch_to_input(pull=digitalio.Pull.UP)

button_c = digitalio.DigitalInOut(board.BTN_C)
button_c.switch_to_input(pull=digitalio.Pull.UP)

while True:
    if not button_a.value:
        text_area.text = "Button A pressed"
    elif not button_b.value:
        text_area.text = "Button B pressed"
    elif not button_c.value:
        text_area.text = "Button C pressed"
    else:
        text_area.text = "Hello, World!"

    display.refresh()

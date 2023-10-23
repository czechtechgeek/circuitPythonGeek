# display  imports
import time
import board
import busio
import digitalio
import adafruit_sharpmemorydisplay

# wifi imports
import ipaddress
import ssl
import wifi
import socketpool


# import adafruit_requests

def pixel_test():
    print("Pixel test")

    # Clear the display.  Always call show after changing pixels to make the display
    # update visible!
    display.fill(1)
    display.show()

    # Set a pixel in the origin 0,0 position.
    display.pixel(0, 0, 0)
    # Set a pixel in the middle position.
    display.pixel(display.width // 2, display.width // 2, 0)
    # Set a pixel in the opposite corner position.
    display.pixel(display.width - 1, display.height - 1, 0)
    display.show()
    time.sleep(2)


def lines_test():
    print("Lines test")
    # we'll draw from corner to corner, lets define all the pair coordinates here
    corners = (
        (0, 0),
        (0, display.height - 1),
        (display.width - 1, 0),
        (display.width - 1, display.height - 1),
    )

    display.fill(1)
    for corner_from in corners:
        for corner_to in corners:
            display.line(corner_from[0], corner_from[1], corner_to[0], corner_to[1], 0)
    display.show()
    time.sleep(2)


def rectangle_test():
    print("Rectangle test")
    display.fill(1)
    w_delta = display.width / 10
    h_delta = display.height / 10
    for i in range(11):
        display.rect(0, 0, int(w_delta * i), int(h_delta * i), 0)
    display.show()
    time.sleep(2)


def text_test():
    print("Text test")
    while (True):
        display.fill(1)
        display.text(" hello world!", 0, 0, 0, size=4)
        display.hline(0, 9, 400, 0)
        # display.text(" This is the", 0, 8, 0)
        # display.text(" CircuitPython", 0, 16, 0)
        # display.text("adafruit library", 0, 24, 0)
        # display.text(" for the SHARP", 0, 32, 0)
        # display.text(" Memory Display :) ", 0, 40, 0)
        display.show()


def get_mac_addr() -> str:
    text = [hex(i) for i in wifi.radio.mac_address]
    text = ' '.join(text)
    print(text)
    return text


def get_wifi_networks():
    print("Available WiFi networks:")
    for network in wifi.radio.start_scanning_networks():
        print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
                                                 network.rssi, network.channel))
    wifi.radio.stop_scanning_networks()


def print_wifi_to_display(display):
    cursor = 60
    display.text("Available WiFi:", 0, cursor, 0, size=3)
    cursor += 30

    for network in wifi.radio.start_scanning_networks():
        print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"), network.rssi, network.channel))
        display.text(str(network.ssid), 0, cursor, 0, size=1)
        cursor += 10
    wifi.radio.stop_scanning_networks()


# Display ports
SCK = board.IO36
MOSI = board.IO35

# URLs to fetch from
TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_QUOTES_URL = "https://www.adafruit.com/api/quotes.php"
JSON_STARS_URL = "https://api.github.com/repos/adafruit/circuitpython"

# Initialize SPI bus and control pins
spi = busio.SPI(SCK, MOSI=MOSI)
scs = digitalio.DigitalInOut(board.IO34)  # inverted chip select

# pass in the display size, width and height, as well
display = adafruit_sharpmemorydisplay.SharpMemoryDisplay(spi, scs, 400, 240)

text = get_mac_addr()

get_wifi_networks()

while True:
    display.fill(1)
    display.text("ESP32-S2 WiFi Test", 0, 0, 0, size=3)
    display.text("MAC addr:" + text, 0, 40, 0, size=1)
    #
    print_wifi_to_display(display)

    display.show()

# for network in wifi.radio.start_scanning_networks():
#     print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
#             network.rssi, network.channel))
# wifi.radio.stop_scanning_networks()








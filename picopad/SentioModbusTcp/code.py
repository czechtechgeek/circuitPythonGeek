# Import intrnet and modbus TCP/IP
import os
import ipaddress
import wifi
import socketpool
import time
from modbus.client import *

# Import display
import board
import terminalio
import displayio
from adafruit_display_text import label 


# Internet connection beggins
print("Connecting to WiFi")

# connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi %s" % (os.getenv('CIRCUITPY_WIFI_SSID')))

pool = socketpool.SocketPool(wifi.radio)
sock = pool.socket()
# prints MAC address to REPL
print("MAC addr:", ":".join([hex(i).replace("0x","").upper() for i in wifi.radio.mac_address]))

# prints IP address to REPL
print("IP addr: ", wifi.radio.ipv4_address)

# set Google IPv4 address
google_ipv4 = ipaddress.ip_address("8.8.4.4")

mb = client(host="192.168.11.2", unit=1, sock=sock)

# LCD setup
display = board.DISPLAY
font = terminalio.FONT
group = displayio.Group()

# ping Google every 15 seconds
while True:
    outdoor_temp = mb.read(FC=0x4, ADR=3301, LEN=1)
    room1_temp = mb.read(FC=0x4, ADR=104, LEN=1)
    room1_hum = mb.read(FC=0x4, ADR=106, LEN=1)
    room2_temp = mb.read(FC=0x4, ADR=204, LEN=1)
    room2_hum = mb.read(FC=0x4, ADR=206, LEN=1)
    room3_temp = mb.read(FC=0x4, ADR=304, LEN=1)
    room3_hum = mb.read(FC=0x4, ADR=306, LEN=1)
    
    display.refresh()
    text = "Sentio"
    text_label = label.Label(font, text=text, color=0xFFFFFF, scale=3)
    text_label.x = 30
    text_label.y = 30
    group.append(text_label)

    text_outdoor = f"Outdoor temp: {int(outdoor_temp[0])/100} °C"
    text_label_1 = label.Label(font, text=text_outdoor, color=0xFFFFFF, scale=2)
    text_label_1.x = text_label.x 
    text_label_1.y = text_label.y + 30
    group.append(text_label_1)
    
    text_room1_temp = f"Livingroom tepm: {int(room1_temp[0])/100} °C"
    text_label_2 = label.Label(font, text=text_room1_temp, color=0xFFFFFF, scale=2)
    text_label_2.x = text_label.x 
    text_label_2.y = text_label.y + 30 * 2
    group.append(text_label_2)
    
    text_room2_temp = f"Kitchen temp: {int(room2_temp[0])/100} °C"
    text_label_3 = label.Label(font, text=text_room2_temp, color=0xFFFFFF, scale=2)
    text_label_3.x = text_label.x 
    text_label_3.y = text_label.y + 30 * 3
    group.append(text_label_3)
    
    text_room3_temp = f"Bathroom temp: {int(room3_temp[0])/100} °C"
    text_label_4 = label.Label(font, text=text_room3_temp, color=0xFFFFFF, scale=2)
    text_label_4.x = text_label.x 
    text_label_4.y = text_label.y + 30 * 4
    group.append(text_label_4)
    
    
    display.show(group)
    
    
    print("=============================================")
    print(f"Outdoor temp: {int(outdoor_temp[0])/100} °C")
    print(f"Livingroom temp: {int(room1_temp[0])/100} °C,   hum: {int(room1_hum[0])/100}%")
    print(f"Kitchen temp: {int(room2_temp[0])/100} °C,     hum:{int(room2_hum[0])/100}%")
    print(f"Bathroom temp: {int(room3_temp[0])/100} °C,    hum:{int(room3_hum[0])/100}%")
    print("=============================================")
    
    #print("Ping google.com: %.1f ms" % (wifi.radio.ping(google_ipv4)*1000))
    time.sleep(15)

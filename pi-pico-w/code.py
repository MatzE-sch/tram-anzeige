import wifi
import socketpool
import ssl
import adafruit_requests
# import board
import neopixel
import time
import os
import microcontroller
import sys
import traceback

from color import Color
from settings import *

# WLAN-Zugangsdaten in settings.toml speichern
WIFI_SSID = os.getenv('CIRCUITPY_WIFI_SSID')
WIFI_PW = os.getenv('CIRCUITPY_WIFI_PASSWORD')

# Datenquelle, nur ändern falls du selber einen Server betreibst
DATA_SRC = 'https://tramanzeige.schu.gg/abfahrten.php?stop_id=' + STOP_ID
REFRESH_AFTER = 20 # seconds

# NeoPixel initialisieren
# pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS)
# print(NUM_PIXELS, ' pixels on pin ', PIXEL_PIN)


class LedStrip():
    def __init__(self, io_pin, num_leds, station_led):
        self.pixels = neopixel.NeoPixel(io_pin, num_leds, brightness=BRIGHTNESS, auto_write=False)
        self.station_led = station_led
        # self.pixel_values = [[] for _ in range(num_leds)]
        self.reset_pixel_values()
        self.show_number = 0

    def __repr__(self):
        return ''.join(Color.dominant_channel(color) for color in self.pixels)

    def __getitem__(self, key):
        key = key - self.station_led
        if key < 0:
            raise IndexError('index on hardware leds < 0')
        return self.pixel_values[key]
    
    def __setitem__(self, pixel_id, color):
        pixel_id = pixel_id + self.station_led
        self.pixel_values[pixel_id] = [color]
        self.show()

    def show(self):
        # print('pixel_values', self.pixel_values)
        print('strip: ', led_strip_tmp)

        self.pixels[:] = [color_list[self.show_number % len(color_list)] if len(color_list) > 0 else Color.black for color_list in self.pixel_values]
        self.pixels.show()
        print('show_number', self.show_number)
        self.show_number += 1

    def reset_pixel_values(self):
        # reset the pixel values for animation and preparation of new data
        self.pixel_values = [[] for _ in range(len(self.pixels))]

    def reset_pixels(self):
        # resets pyhsical pixels
        self.pixels.fill(Color.black)


    def push_center(self, color):
        half_pixels = list(self.pixels[self.station_led:])
        # print('half_pixels', half_pixels)
        centered = half_pixels[::-1] + [color] + half_pixels
        # print('centered', centered)
        self.pixels[:] = centered[1:-1] # push in from left
        self.pixels.show()


    def pixel_add(self, pixel, color):
        pixel = pixel + PIXEL_FOR_STATION
        try:
            if pixel < 0:
                raise IndexError('pixel < 0')
            self.pixel_values[pixel].append(color)
        except IndexError as e:
            # print(f'pixel {pixel} out of range')
            # print(e)
            pass
        # self.show()

led_strip_tmp = LedStrip(PIXEL_PIN, NUM_PIXELS, PIXEL_FOR_STATION)

# pixels = led_strip_tmp.pixels
    

# pixels init
led_strip_tmp.push_center((255, 170, 0))

def reset_microcontroller(wait_seconds = 10, led_strip=led_strip_tmp):
    print(f"Resetting microcontroller in {wait_seconds} seconds")
    for _ in range(wait_seconds):
        led_strip[PIXEL_FOR_STATION] = Color.red
        led_strip.show()
        time.sleep(0.5)
        led_strip[PIXEL_FOR_STATION] = Color.black
        led_strip.show()
        time.sleep(0.5)
    led_strip.reset_pixels()
    microcontroller.reset()

try:
    #  connect to SSID
    wifi.radio.connect(WIFI_SSID, WIFI_PW)

    led_strip_tmp.push_center(Color.blue)

    print('Verbunden:', wifi.radio.ipv4_address)
    if wifi.radio.ipv4_address == None:
        raise Exception('No ipv4 address')
    led_strip_tmp.push_center((0, 255, 255))

except:
    print('Keine Verbindung zum WLAN aufgebaut')
    led_strip_tmp.push_center(Color.red)
    reset_microcontroller(30)

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())


led_strip_tmp.push_center((0, 255, 0))



# JSON-Daten von URL abrufen
def fetch_json(url):
    try:
        # print('get')
        # print('url', url)
        response = requests.get(url)
        try:
            data = response.json()
        except ValueError as json_error:
            print("JSON Decode Error:\n", str(json_error))
            print("Response content:\n", response.text)
            raise
        # print('data')
        # print(data)
        # example:
        # [
        #   {"destination":"Augsburg, Josefinum","lineNumber":"2","estimated":9},
        #   {"destination":"Oberhausen, Nord P+R","lineNumber":"4","estimated":297},
        #   ...
        # ]
        response.close()

    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        for _ in range(5):
            #  TODO: fix!!!
            led_strip_tmp[PIXEL_FOR_STATION] = Color.red
            # led_strip_tmp.show()
            time.sleep(0.5)
            led_strip_tmp[PIXEL_FOR_STATION] = Color.black
            # led_strip_tmp.show()
            time.sleep(0.5)
        # time.sleep(5)
        reset_microcontroller()    
    return data
 

# JSON-Daten verarbeiten
def process_json(data):

    led_strip_tmp.reset_pixel_values()

    did_warning_occur = False
    for stop in data:
        # defaults:
        pixel = 0
        color = None
        direction = None # invalid

        # Sanitize
        #print(item)
        # example:  
        # [
        #   {"destination":"Augsburg, Josefinum","lineNumber":"2","estimated":9},
        #   {"destination":"Oberhausen, Nord P+R","lineNumber":"4","estimated":297},
        #   ...
        # ]
        # destinations:
        # Augsburg Hbf
        # Oberhausen, Nord P+R
        # Augsburg, Josefinum
        # Haunstetten, Nord
        # print('stop', stop)

        # work with data
        # Line -> Color
        try:
            color = LINE_COLORS[stop['lineNumber']]
        except KeyError:
            print('unknown line:', stop['lineNumber'])
            did_warning_occur = True
            continue

        # Direction 
        try:
            direction = DIRECTIONS[stop['platform']]
        except KeyError:
            print('unknown platform: ', stop['platform'])
            did_warning_occur = True

            continue
        
        # Time
        seconds_to_stop = stop['estimated'] - (time.monotonic() - time_of_data)
        minutes = round(seconds_to_stop / SECONDS_PER_LED) # rounds to nearest minute

        # Put Time, Pixe, Direction together
        pixel = minutes
        if direction == 'against_data_arrow':
            pixel *= -1

        # print('pixel', pixel, 'color', color, 'direction', direction)
        led_strip_tmp.pixel_add(pixel, color)


    station_color = Color.station_color1 if not did_warning_occur else Color.warning
    led_strip_tmp.pixel_add(0, station_color)
    
    led_strip_tmp.show()

    return did_warning_occur


def fetch_data():
    # print('fetch')
    data = fetch_json(DATA_SRC)
    time_of_data = time.monotonic()
    return time_of_data, data




while True:
    print("neue Runde...")

    try:
        time_of_data, data = fetch_data()
        warning = process_json(data)
        

        # update visual every second
        start_time = time.monotonic()
        while time.monotonic() - start_time < REFRESH_AFTER-0.5:
            time.sleep(0.5)
            led_strip_tmp[0] = Color.station_color2
            time.sleep(0.5)
            # led_strip_tmp.show()

            led_strip_tmp[0] = Color.station_color1
            
        time.sleep(0.5)

        led_strip_tmp[0] = Color.white

    except Exception as e:

        traceback.print_exc(file=sys.stdout)
        traceback.print_exc()
        print('caught')
        print(e)

        reset_microcontroller(10)
        continue
    
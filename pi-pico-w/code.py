import wifi
import socketpool
import ssl
import adafruit_requests
# import board
import neopixel
import time
import os
import microcontroller

from color import Color
from settings import *

# WLAN-Zugangsdaten in settings.toml speichern
WIFI_SSID = os.getenv('CIRCUITPY_WIFI_SSID')
WIFI_PW = os.getenv('CIRCUITPY_WIFI_PASSWORD')

# Datenquelle, nur ändern falls du selber einen Server betreibst
DATA_SRC = 'https://tramanzeige.schu.gg/abfahrten.php?stop_id=' + STOP_ID
REFRESH_AFTER = 20 # seconds

# NeoPixel initialisieren
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS)
print(NUM_PIXELS, ' pixels on pin ', PIXEL_PIN)

LED_STRIP = None

def reset_strip_array():
    global LED_STRIP
    LED_STRIP = [Color.black() for _ in range(NUM_PIXELS)]

def push_strip(color):
    global LED_STRIP
    LED_STRIP = [color] + LED_STRIP[:-1] # push in from left
    write_strip()

def print_strip_to_serial():
    def get_dominant_color(color):
        if color.red == 0 and color.green == 0 and color.blue == 0:
            return '-'
        elif color.red >= color.green and color.red >= color.blue:
            return 'R'
        elif color.green >= color.red and color.green >= color.blue:
            return 'G'
        else:
            return 'B'

    strip_visual = ''.join(get_dominant_color(color) for color in LED_STRIP)
    print(strip_visual)

def write_strip():
    pixels[:] = [color.tupel() for color in LED_STRIP]
    pixels.show()
    print_strip_to_serial()
    
reset_strip_array()

# pixels init
push_strip(Color(255, 170, 0))

def reset_microcontroller(wait_seconds = 10):
    print(f"Resetting microcontroller in {wait_seconds} seconds")
    for _ in range(wait_seconds):
        pixels[PIXEL_FOR_STATION] = Color.red().tupel()
        time.sleep(0.5)
        pixels[PIXEL_FOR_STATION] = Color.black().tupel()
        time.sleep(0.5)
    microcontroller.reset()

try:
    #  connect to SSID
    wifi.radio.connect(WIFI_SSID, WIFI_PW)

    push_strip(Color.blue())

    print('Verbunden:', wifi.radio.ipv4_address)
    if wifi.radio.ipv4_address == None:
        raise Exception('No ipv4 address')
    push_strip(Color(0, 255, 255))

except:
    print('Keine Verbindung zum WLAN aufgebaut')
    print("Resetting microcontroller in 10 seconds")
    push_strip(Color.red())
    reset_microcontroller(30)

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())


push_strip(Color(0, 255, 0))


def pixel_add(pixel, color):
    pixel = pixel + PIXEL_FOR_STATION
    try:
        if pixel < 0:
            raise IndexError('pixel < 0')
        LED_STRIP[pixel] += color
    except IndexError as e:
        # print(f'pixel {pixel} out of range')
        # print(e)
        pass

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
            pixels[PIXEL_FOR_STATION] = Color.red().tupel()
            pixels.show()
            time.sleep(0.5)
            pixels[PIXEL_FOR_STATION] = Color.black().tupel()
            pixels.show()
            time.sleep(0.5)
        # time.sleep(5)
        reset_microcontroller()    
    return data
 

# JSON-Daten verarbeiten
def process_json(data):
    reset_strip_array()
    # print('process_json')
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
            direction = LINE_COLORS[stop['platform']]
        except KeyError:
            print('unknown platform:', stop['platform'])
            did_warning_occur = True

            continue
        
        # Time
        seconds_to_stop = stop['estimated'] - (time.monotonic() - time_of_data)
        minutes = round(seconds_to_stop / SECONDS_PER_LED) # rounds to nearest minute

        # Put Time, Pixe, Direction together
        pixel = minutes
        if direction == 'against_data_arrow':
            pixel *= -1
        pixel_add(pixel, color)

    station_color = Color.station_color1() if not did_warning_occur else Color.warning()
    LED_STRIP[PIXEL_FOR_STATION] = station_color
    write_strip()
    
    return did_warning_occur

def color_chase(color, wait):
    pixels[PIXEL_FOR_STATION] = Color.white().tupel()
    for i in range(NUM_PIXELS//2):
        pixels[i] = color
        pixels[NUM_PIXELS-1-i] = color
        time.sleep(wait)
    time.sleep(wait)

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
        while time.monotonic() - start_time < REFRESH_AFTER:
            time.sleep(0.5)
            pixels[PIXEL_FOR_STATION] = Color.station_color2().tupel()
            time.sleep(0.5)
            process_json(data)
            pixels[PIXEL_FOR_STATION] = Color.station_color1().tupel()

        pixels[PIXEL_FOR_STATION] = Color.white().tupel()

    except Exception as e:
        print('caught')
        print(e)
        reset_microcontroller(10)
        continue
    
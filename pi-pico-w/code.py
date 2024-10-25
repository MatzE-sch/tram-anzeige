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
import analogio

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
    def __init__(self, io_pin, num_leds, station_led, brightness):
        self.pixels = neopixel.NeoPixel(io_pin, num_leds, brightness=brightness, auto_write=False)
        self.station_led = station_led
        # self.pixel_values = [[] for _ in range(num_leds)]
        self.reset_pixel_values()
        self.show_number = 0

    def __repr__(self):
        return ''.join(Color.dominant_channel(color) for color in self.pixels)

    def __getitem__(self, key):
        key = key + self.station_led
        if key < 0:
            raise IndexError('index on hardware leds < 0')
        return self.pixel_values[key]
    
    def __setitem__(self, pixel_id, color):
        pixel_id = pixel_id + self.station_led
        # print(pixel_id, color)
        self.pixel_values[pixel_id] = [color]
        self.show()
        

    def brightness(self, brightness):
        self.pixels.brightness = brightness

    def show(self):
        # print('pixel_values', self.pixel_values)
        # print('strip: ', self)

        self.pixels[:] = [color_list[self.show_number % len(color_list)] if len(color_list) > 0 else Color.black for color_list in self.pixel_values]
        self.pixels.show()
        # print('show_number', self.show_number)
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


# JSON-Daten von URL abrufen
def fetch_json(requests, url, led_strip):
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
        
        # example: 
        # [
        #   {
        #     "destination": "Augsburg, Josefinum",
        #     "platform": "a",
        #     "lineNumber": "2",
        #     "estimated": 23
        #   },
        #   {
        #     "destination": "Haunstetten, Nord",
        #     "platform": "e",
        #     "lineNumber": "2",
        #     "estimated": 35
        #   },
        #   {
        #     "destination": "Oberhausen, Nord P+R",
        #     "platform": "a",
        #     "lineNumber": "4",
        #     "estimated": 323
        #   },
        #   {...}
        # ]
        response.close()

    except Exception as e:
        print("Error:\n", str(e))
        reset_microcontroller(led_strip, 5)  
    return data
 

# JSON-Daten verarbeiten
def process_json(led_strip, data, time_of_data):

    led_strip.reset_pixel_values()

    did_warning_occur = False
    for stop in data:
        # defaults:
        pixel = 0
        color = None
        direction = None # invalid

        # work with data
        # Line -> Color
        try:
            color = LINE_COLORS[stop['lineNumber']]
        except KeyError:
            print('unknown line:', stop['lineNumber'])
            did_warning_occur = True
            continue

        # Direction 
        # platform -> direction
        try:
            direction = DIRECTIONS[stop['platform']]
        except KeyError:
            print('unknown platform: ', stop['platform'])
            did_warning_occur = True

            continue
        
        # Time
        seconds_to_stop = stop['estimated'] - (time.monotonic() - time_of_data)
        pixel = round(seconds_to_stop / SECONDS_PER_LED) # rounds to nearest minute
        if pixel <= 0:
            continue

        if direction == 'against_data_arrow':
            pixel *= -1

        # Put Time, Pixe, Direction together
        # print('pixel', pixel, 'color', color, 'direction', direction)
        led_strip.pixel_add(pixel, color)


    station_color = Color.station_color1 if not did_warning_occur else Color.warning
    led_strip.pixel_add(0, station_color)

    led_strip.show()
    print('warning:', did_warning_occur)

    return did_warning_occur


def fetch_data(requests, led_strip):
    # print('fetch')
    data = fetch_json(requests, DATA_SRC, led_strip)
    time_of_data = time.monotonic()
    return time_of_data, data

def adjust_brightness(light_sensor, led_strip, average_over_secunds = 0.5):
    # Set the brightness of the LED strip based on the sensor reading
    average_sensor_value = light_sensor.value
    sensor_readings = 1
    start_time = time.monotonic()
    while time.monotonic() - start_time < average_over_secunds:
        average_sensor_value = (average_sensor_value * sensor_readings + light_sensor.value) / (sensor_readings + 1)
        sensor_readings += 1
        # print('average_sensor_value', average_sensor_value)
    # value ca between 1500 and 200
    sensor_max = 1500 # very dark
    sensor_min = 200 # very bright
    sensor_value_max_min = max(sensor_min, min(sensor_max, average_sensor_value)) # ensure range
    sensor_value_0_1 = (sensor_value_max_min - sensor_min) / (sensor_max - sensor_min) # normalize to 0-1
    try:
        brightness = MAX_BRIGHTNESS - sensor_value_0_1 * (MAX_BRIGHTNESS - MIN_BRIGHTNESS)
    except NameError:
        brightness = BRIGHTNESS

    print('sensor_value', average_sensor_value)
    # scale brightness to be between MIN_BRIGHTNESS and MAX_BRIGHTNESS
    
    print('brightness', brightness)

    led_strip.brightness(brightness)

def sleep_or_adjust_brightness(sleep_time, light_sensor=None, led_strip=None):
    if light_sensor == None or led_strip == None:
        time.sleep(sleep_time)
        return
    adjust_brightness(light_sensor, led_strip, 0.5)

def reset_microcontroller(led_strip, wait_seconds = 10):
    print(f"Resetting microcontroller in {wait_seconds} seconds")
    for _ in range(wait_seconds):
        led_strip[0] = Color.red
        time.sleep(0.5)
        led_strip[0] = Color.black
        time.sleep(0.5)
    led_strip.reset_pixels()
    microcontroller.reset()

def main():
    led_strip = LedStrip(PIXEL_PIN, NUM_PIXELS, PIXEL_FOR_STATION, BRIGHTNESS)
    # pixels init
    led_strip.push_center((255, 170, 0))

    # Initialize the analog input for the photosensitive resistor
    try:
        light_sensor = analogio.AnalogIn(SENSOR_PIN)
        print('Light sensor found')
    except NameError:
        light_sensor = None
        print('No light sensor found')

    try:
        #  connect to SSID
        wifi.radio.connect(WIFI_SSID, WIFI_PW)

        led_strip.push_center(Color.blue)

        print('Verbunden:', wifi.radio.ipv4_address)
        if wifi.radio.ipv4_address == None:
            raise Exception('No ipv4 address')
        led_strip.push_center((0, 255, 255))

    except:
        print('Keine Verbindung zum WLAN aufgebaut')
        led_strip.push_center(Color.red)
        reset_microcontroller(led_strip, 30)

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())


    led_strip.push_center((0, 255, 0))


    while True:
        print("neue Runde...")



        try:
            time_of_data, data = fetch_data(requests, led_strip)
            warning = process_json(led_strip, data, time_of_data)
            

            # update visual every second
            start_time = time.monotonic()
            while time.monotonic() - start_time < REFRESH_AFTER-0.5:

                # sleep_or_adjust_brightness(0.5, light_sensor, led_strip)
                time.sleep(0.5)
                led_strip[0] = Color.station_color2


                sleep_or_adjust_brightness(0.5, light_sensor, led_strip)
                led_strip[0] = Color.station_color1

                
                
            time.sleep(0.5)

            led_strip[0] = Color.white

        except Exception as e:

            print('caught')
            print(e)
            raise e
            reset_microcontroller(led_strip, 10)
            continue
        
if __name__ == '__main__':
    main()
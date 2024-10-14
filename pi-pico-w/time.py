import rtc
import adafruit_requests as requests
import wifi
import socketpool
import ssl
import time
import os
# from typing import Tuple
import re
import microcontroller
import neopixel
import board



from color import Color

# Init
PIXEL_PIN = board.GP19
NUM_PIXELS = 31
BRIGHTNESS = 0.4

REFRESH_AFTER = 10 # seconds


# Get Wi-Fi credentials from environment variables
WIFI_SSID = os.getenv('CIRCUITPY_WIFI_SSID')
WIFI_PW = os.getenv('CIRCUITPY_WIFI_PASSWORD')


# NeoPixel initialisieren
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS)#, auto_write=True) # TODO: no autowrite?

LED_STRIP = None

stop_data = None

def reset_strip_array():
    global LED_STRIP
    LED_STRIP = [Color.black() for _ in range(NUM_PIXELS)]

def push_strip(color):
    global LED_STRIP
    LED_STRIP = [color] + LED_STRIP[:-1] # push in from left
    write_strip()

def write_strip():
    pixel_clear()
    pixels[:] = [color.tupel() for color in LED_STRIP]
    pixels.show()

def pixel_clear():
    pixels.fill(Color.black().tupel())

def pixel_add(pixel, color):
    pixel = pixel + 15
    # print(LED_STRIP[pixel])
    # print(color)
    try:
        LED_STRIP[pixel] += color
    except IndexError as e:
        print(f'pixel {pixel} out of range')
        # print(e)
        pass
    except Exception as e:
        print('exception hier zur hölle')
        print(e)

reset_strip_array()
time_of_data = None


def reset_microcontroller():
    print("Resetting microcontroller in 10 seconds")
    pixels[15] = Color.black().tupel()
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
    time.sleep(10)
    reset_microcontroller()

# Create a socket pool and SSL context
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

# Initialize the requests session
session = requests.Session(pool, ssl_context)

# Function to parse the date string manually
def parse_date(date_str):
    # example date_str: 'Fri, 04 Oct 2024 12:14:22 GMT'
    # Use regular expressions to extract the date components
    match = re.match(r'(\w+), (\d+) (\w+) (\d+) (\d+):(\d+):(\d+) (\w+)', date_str)
    if not match:
        raise ValueError("Invalid date string format")
    # Extract the date components from the match object
    weekday, day, month, year, hour, minute, second, timezone = match.groups()
    # Convert month name to month number
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = month_names.index(month) + 1

    # Print the extracted values
    # print(f"Weekday: {weekday}, Day: {day}, Month: {month}, Year: {year}, Hour: {hour}, Minute: {minute}, Second: {second}, Timezone: {timezone}")
    # print(f'fucking date: {year=}, {month=}, {day=}, {hour=}, {minute=}, {second=}')
    return time.struct_time((int(year), int(month), int(day), int(hour), int(minute), int(second), -1, -1, -1))


def get_time_and_departures():# -> Tuple[time.struct_time, dict]:
    try:
        # Make the HTTP request to the EFA 
        print('reaching out to api')
        response = session.get("https://fahrtauskunft.avv-augsburg.de/efa/XML_DM_REQUEST?outputFormat=rapidJSON&name_dm=de%3A09761%3A407&itdDateTimeDepArr=dep&mode=direct&useRealtime=1&deleteAssignedStops_dm=1&depSequence=10&calcOneDirection=1&ptOptionsActive=1&language=de&type_dm=any&useAllStops=1&inclMOT_5=true&maxTimeLoop=1&limit=17")
        # Print all response headers
        # for header, value in response.headers.items():
        #     print(f"{header}: {value}")
        # Extract the 'Date' header
        date_str = response.headers['date']
        print(f"Server Date: {date_str}")
        date_time = parse_date(date_str)

        print('parse json')
        json_data = response.json()
        print('closing response')
        response.close()

    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        for _ in range(5):
            pixels[15] = Color.red().tupel()
            pixels.show()
            time.sleep(0.5)
            pixels[15] = Color.black().tupel()
            pixels.show()
            time.sleep(0.5)
        time.sleep(5)
        reset_microcontroller()  
   
    return date_time, json_data


# JSON-Daten verarbeiten
def process_json(data):
    print('processing json data')
    # print(f'{data=}')  # now memory alloc fails this syntax seems to be memory intensive
    print('data is', data)
    reset_strip_array()
    print('process_json') # now memory alloc fails
    for stop in data['stopEvents']: #TypeError: 'NoneType' object isn't subscriptable  
        print('stop')
        # defaults:
        pixel = 0
        color = None
        direction = None # invalid

        print(f'{stop}')

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
        if stop['lineNumber'] == '4':
            color = Color.red()
        if stop['lineNumber'] == '2':
            color = Color.blue()
        if (stop['destination'] == 'Augsburg, Josefinum' or 
            stop['destination'] == 'Oberhausen, Nord P+R'):
            direction = 'west'
        if (stop['destination'] == 'Augsburg Hbf' or
            stop['destination'] == 'Haunstetten, Nord' or
            stop['destination'] == 'Augsburg, Rotes Tor' or # TODO: verify that is the correct string
            stop['destination'] == 'Augsburg, Königsplatz'): # TODO: verify that is the correct string
            direction = 'east'

        seconds_to_stop = stop['estimated'] - (time.monotonic() - time_of_data)
        minutes = round(seconds_to_stop / 60) # rounds to nearest minute
        pixel = minutes
        if direction == 'east':
            pixel *= -1
        pixel_add(pixel, color)

        # seconds_to_stop = round(stop['estimated'] - (time.monotonic() - time_of_data))
        # minutes = seconds_to_stop // 60 # rounds down
        # seconds = seconds_to_stop % 60 # remainder
        # pixel1 = minutes
        # pixel2 = minutes + 1
        # if direction == 'east':
        #     pixel1 *= -1
        #     pixel2 *= -1
        #     # pixel_set(item['estimated'], LINE4)
        # # print('pixel', pixel)
        # pixel_add(pixel1, color * ((60-seconds)/60))
        # pixel_add(pixel2, color * (seconds/60))
        
    # pixel_add(0, Color.green()) # wertachbrücke
    LED_STRIP[15] = Color.green() # wertachbrücke
    write_strip()


# MAIN 

def main():

    global stop_data
    global time_of_data
    # Set the RTC to the parsed date and time
    date_time, json_data = get_time_and_departures()
    print('setting rtc')
    rtc.RTC().datetime = date_time
    print('done setting rtc')
    time_of_data = time.monotonic()
    process_json(json_data)
    print('done processing json')


# Continuously print the RTC time
while True:
    # time.sleep(1)


    print("neue Runde...")
    # main()
    try:
        main()
    except Exception as e:
        # print('caught')
        print(e)
        for _ in range(5):
            pixels.fill((255, 0, 0))  # Red color
            pixels.show()
            time.sleep(0.5)
            pixels.fill((0, 0, 0))  # Turn off
            pixels.show()
            time.sleep(0.5)
        # print('err end')
    print('done')
    pixels[15] = Color.green().tupel()

    # update visual every second
    start_time = time.monotonic()
    while time.monotonic() - start_time < REFRESH_AFTER:
        process_json(stop_data)

        current_time = rtc.RTC().datetime
        print(f"Current RTC Time: {current_time}")

        time.sleep(1)
    pixels[15] = Color.white().tupel()

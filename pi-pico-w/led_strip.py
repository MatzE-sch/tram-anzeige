import neopixel

from color import Color
from settings import *


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
        half_pixels = list(self.pixel_values[self.station_led:])
        # print('half_pixels', half_pixels)
        centered = half_pixels[::-1] + [[color]] + half_pixels
        # print('centered', centered)
        self.pixel_values[:] = centered[1:-1] # push in from left
        self.show()


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
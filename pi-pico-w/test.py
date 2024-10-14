
import board
import neopixel
import time


class Color: 
    @staticmethod
    def red():
        return Color(255, 0, 0)
    
    @staticmethod
    def green():
        return Color(0, 255, 0)
    
    @staticmethod
    def blue():
        return Color(0, 0, 255)
    
    @staticmethod
    def white():
        return Color(255, 255, 255)
    
    @staticmethod
    def black():
        return Color(0, 0, 0)
    
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return f"Color({self.red}, {self.green}, {self.blue})"

    def __add__(self, other):
        return Color(self.red + other.red, self.green + other.green, self.blue + other.blue)
    
    def __mul__(self, scalar):
        return Color(
            max(0, min(255, int(self.red * scalar))),
            max(0, min(255, int(self.green * scalar))),
            max(0, min(255, int(self.blue * scalar)))
        )

    def tupel(self):
        return (self.red, self.green, self.blue)

# Init
pixel_pin = board.GP19
num_pixels = 31
PIXEL_PIN = board.GP19
NUM_PIXELS = 31
BRIGHTNESS = 0.1

# NeoPixel an Pin GP1 initialisieren
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=True)

LED_STRIP = [Color.black() for _ in range(num_pixels)]


# LED_STRIP = None
def reset_strip():
    global LED_STRIP
    LED_STRIP = [Color.black() for _ in range(NUM_PIXELS)]

def write_strip():
    for i in range(num_pixels):
        pixels[i] = LED_STRIP[i].tupel()
    # pixels.show()



def pixel_clear():
    pixels.fill(Color.black().tupel())  
      

def pixel_add(pixel, color):
    pixel = pixel + 15
    # print(LED_STRIP[pixel])
    # print(color)
    try:
        LED_STRIP[pixel] += color
    except IndexError as e:
        # print(f'pixel {pixel} out of range')
        # print(e)
        pass
    except Exception as e:
        print(e)

def scale_brightness(input_value, gamma=3):
    """Scales the input brightness to appear linear to the human eye."""
    # Ensure input_value is within the expected range
    input_value = max(0, min(input_value, 1))
    input_value = 1 - input_value
    # Apply gamma correction
    corrected_output = input_value ** (1 / gamma)
    # return corrected_output
    return 1 - corrected_output


def test():
    
    color = Color.red()

    seconds_left = 600 # sekunden
    while seconds_left > 0:
        reset_strip()
        minutes = seconds_left // 60 # rounds down
        seconds = seconds_left % 60 # remainder

        print('minutes', minutes, 'seconds', seconds)
        pixel1 = minutes
        pixel2 = minutes + 1
        #     # pixel_set(item['estimated'], LINE4)
        # # print('pixel', pixel)

        # # partial brightness
        brightness1_in_percent = 1 - (seconds / 60)
        brightness2_in_percent = seconds / 60

        # # scale brightness
        # # 8 because 2**8 = 256 
        # # -1 so its max 255
        # expValue = (8/60)*seconds
        # print('exp', expValue)
        # brightness1 = min(255, 2 ** expValue - 1)
        # # brightness2 = 2 ** (brightness2_in_percent * 8) - 1


        # brightness1 = 2 ** ((8/60)*seconds) - 1
        # brightness1 /= 255

        brightness1 = scale_brightness(brightness1_in_percent)
        brightness2 = scale_brightness(brightness2_in_percent)

        

        # print(f'potVal: {potVal}, expVal: {expVal}, brightness1: {brightness1}')
        print(f'seconds_left: {seconds_left}')#, brightness2: {brightness2}')
        print(f'brightness1: {brightness1}')#, brightness2: {brightness2}')
        
        pixel_add(pixel1, color * (brightness1))
        pixel_add(pixel2, color * (brightness2))
        write_strip()
        seconds_left -= 2
        time.sleep(0.2)

    # sleep = 5 # sekunden
    
    # reset_strip()
    # LED_STRIP[10] = Color.red() * 0.5
    # LED_STRIP[11] = Color.red() * 0.5
    # write_strip()

    # time.sleep(sleep)

    # reset_strip()
    # LED_STRIP[10] = Color.red() * 0.25
    # LED_STRIP[11] = Color.red() * 0.75
    # write_strip()

    # time.sleep(sleep)

    # reset_strip()
    # LED_STRIP[10] = Color.red() * 0.25
    # LED_STRIP[11] = Color.red() * 0.75
    # write_strip()

    # time.sleep(sleep)

    # reset_strip()
    # LED_STRIP[11] = Color.red()
    # write_strip()

    # time.sleep(sleep)

    # reset_strip()
    # LED_STRIP[11] = Color.red() * 0.75
    # LED_STRIP[12] = Color.red() * 0.25
    # write_strip()

    # time.sleep(sleep)

    # reset_strip()
    # LED_STRIP[11] = Color.red() * 0.5
    # LED_STRIP[12] = Color.red() * 0.5
    # write_strip()

    # time.sleep(sleep)

    # reset_strip()
    # LED_STRIP[11] = Color.red() * 0.25
    # LED_STRIP[12] = Color.red() * 0.75
    # write_strip()

    # time.sleep(sleep)


    # LED_STRIP[11] *= 0.1
    # print(Color.red())
    # write_strip()

def run_test():

    for i in range(100):
        scaled = scale_brightness(i/100)
        print(f'{i}: {scaled}')

while True:
    for _ in range(5):
        print('hi')
        pixels.fill((255, 0, 0))  # Red color
        pixels.show()
        time.sleep(0.5)
        print('ho')
        pixels.fill((0, 0, 0))  # Turn off
        pixels.show()
        time.sleep(0.5)
    # color_chase(YELLOW, 0.01)
    # pixel_set(0, WHITE) # wertachbrücke
    test()
    # break
    # get_dep()
    print('done')
    # time.sleep(60)
    print("neue Runde...")


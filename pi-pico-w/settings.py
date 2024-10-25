from color import Color
import board # type: ignore

# Diese Werte für deine Haltestelle anpassen
STOP_ID = "de:09761:407"
LINE_COLORS = {
    # '6': Color(255, 0, 255), # magenta
    '2': Color.blue,
    'B2': Color.cyan,
    '4': Color.red,
}
DIRECTIONS = {
    # platform
    'a': 'with_data_arrow',  # richtung Oberhausen Nord P+R
    'e': 'against_data_arrow'
}


# Diese Werte für deinen LED Streifen anpassen
NUM_PIXELS = 61
PIXEL_FOR_STATION = 30 # Der Pixel der die Haltestelle repräsentiert
PIXEL_PIN = board.GP19
SECONDS_PER_LED = 30


# Diese Werte nach belieben anpassen
BRIGHTNESS = 0.1

# Wenn du einen Lichtsensor hast:
SENSOR_PIN = board.GP27_A1 # Analog input
MAX_BRIGHTNESS = 0.1
MIN_BRIGHTNESS = 0.012

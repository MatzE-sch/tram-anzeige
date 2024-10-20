from color import Color
import board

# Diese Werte für deine Haltestelle anpassen
STOP_ID = "de:09761:407"
LINE_COLORS = {
    # '6': Color(255, 0, 255), # magenta
    '2': Color.blue(),
    'B2': Color.blue(),
    '4': Color.red(),
}
DIRECTIONS = {
    'with_data_arrow': [
        'Augsburg, Josefinum',
        'Oberhausen, Nord P+R',
        'Oberh. Nord P+R'
    ],
    'against_data_arrow': [
        'Augsburg Hbf',
        'Haunstetten, Nord',
        'Augsburg, Rotes Tor',
        'Augsburg, Königsplatz'
    ]
}


# Diese Werte für deinen LED Streifen anpassen
NUM_PIXELS = 31
PIXEL_FOR_STATION = 15 # Der Pixel der die Haltestelle repräsentiert
PIXEL_PIN = board.GP19
SECONDS_PER_LED = 30


# Diese Werte nach belieben anpassen
BRIGHTNESS = 0.1

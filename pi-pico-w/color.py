class Color:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    white = (127, 127, 127)
    black = (0, 0, 0)
    dark_green = (0, 160, 0)
    yellow = (127, 127, 0)
    cyan = (0, 90, 127)
    purple = (200, 0, 70)
    
    warning = yellow
    station_color1 = green
    station_color2 = dark_green
    
    @staticmethod
    def dominant_channel(color):
        r,g,b = color
        if r == 0 and g == 0 and b == 0:
            return '-'
        elif r == g == b:
            return 'W'
        elif r >= g and r >= b:
            return 'R'
        elif g >= r and g >= b:
            return 'G'
        else:
            return 'B'
    
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return f"Color({self.red}, {self.green}, {self.blue})"
    
    def __iter__(self):
        return (self.red, self.green, self.blue)

    def __add__(self, other):
        # mix colors
        return Color(self.red + other.red, self.green + other.green, self.blue + other.blue)
    
    def __mul__(self, scalar):
        # scale color
        return Color(
            max(0, min(255, int(self.red * scalar))),
            max(0, min(255, int(self.green * scalar))),
            max(0, min(255, int(self.blue * scalar)))
        )

    def tuple(self):
        return (self.red, self.green, self.blue)

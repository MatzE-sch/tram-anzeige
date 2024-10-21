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
        return Color(127, 127, 127)
    
    @staticmethod
    def black():
        return Color(0, 0, 0)
    
    @staticmethod
    def dark_green():
        return Color(0, 100, 0)
    
    @staticmethod
    def yellow():
        return Color(127, 127, 0)
    
    @staticmethod
    def cyan():
        return Color(0, 90, 127)
    
    @staticmethod
    def warning():
        return Color.yellow()
    
    @staticmethod
    def station_color1():
        return Color.green()
    
    @staticmethod
    def station_color2():
        return Color.dark_green()
    

    
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return f"Color({self.red}, {self.green}, {self.blue})"

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

    def tupel(self):
        return (self.red, self.green, self.blue)
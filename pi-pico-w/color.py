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
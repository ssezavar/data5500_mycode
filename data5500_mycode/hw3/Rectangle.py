# Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
# HW3, Q1, Rectangle Class

# Rectangle.py
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calc_area(self):
        return self.length * self.width

    def get_length(self):
        return self.length

    def get_width(self):
        return self.width

    def set_length(self, length):
        self.length = length

    def set_width(self, width):
        self.width = width


rect1 = Rectangle(5, 3)
print("the rectnagle area is:", rect1.calc_area())   # 15

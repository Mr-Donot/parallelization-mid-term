


class Circle :

    def __init__(self, x, y, z, radius, color):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = color

    def __str__(self) -> str:
        return f"(x,y,z) : {self.x},{self.y},{self.z} | radius : {self.radius} | color : {self.color}"

    
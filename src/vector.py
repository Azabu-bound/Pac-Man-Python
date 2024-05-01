import math
from typing import _VT_co

class Vector2(object):
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y
        self.thresh = 0.000001

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __trudiv__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / scalar, self.y / scalar)
        return None

    # Equality check between vectors
    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    def magnitude_squared(self):
        return self.x ** 2 + self.y ** 2

    # Returns the length of the vector
    def magnitude(self):
        return math.sqrt(self.magnitude_squared())

    # Copy a vector to establish a new instance of it
    def copy(self):
        return Vector2(self.x, self.y)

    def as_tuple(self):
        return self.x, self.y

    def as_int(self):
        return int(self.x), int(self.y)

    # String method for debugging
    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"

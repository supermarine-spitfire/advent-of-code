class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point2D({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Point2D):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_touching(self, p):
        if p.y == self.y:
            if p.x == self.x + 1 or p.x == self.x - 1:  # Horizontal cases.
                return True
        elif p.x == self.x:
            if p.y == self.y + 1 or p.y == self.y - 1:  # Vertical cases.
                return True
        elif p.x == self.x + 1 or p.x == self.x - 1:
            if p.x == self.y + 1 or p.x == self.y - 1:  # Oblique cases.
                return True

        return False

    __repr__ = __str__

class LineSegment2D:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f"Line2D(start: {self.start}, end: {self.end}"

    def intersects(self, p):
        if p.x < self.start.x or p.x > self.end.y or p.y < self.start.y or p.y > self.end.y: # Outside of line segment.
            return False
        if p == self.start or p == self.end:    # Same as endpoints.
            return True
        elif p.x == self.start.x and p.y >= self.start.y and p.y <= self.end.y:   # Vertical case.
            return True
        elif p.y == self.start.y and p.x >= self.start.x and p.x <= self.end.x: # Horizontal case.
            return True
        else:                                                                   # Oblique case.
            if self.start.y == self.end.y:
                m = 0
            elif self.start.x == self.end.x:
                m = None
            else:
                m = (self.end.x - self.start.x) / (self.end.y - self.start.y)

            if m:
                return p.y - self.start.y == m * (p.x - self.start.x)
            else:
                return None # Should not happen.

    __repr__ = __str__
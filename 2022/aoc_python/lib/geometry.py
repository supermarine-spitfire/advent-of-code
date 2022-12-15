class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point2D({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

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

    def manhattan_distance(self, p):
        return abs(self.x - p.x) + abs(self.y - p.y)

    __repr__ = __str__

class LineSegment2D:
    def __init__(self, start, end):
        # Constructor enforces the condition that small is strictly less than end.
        self.start = Point2D(min(start.x, end.x), min(start.y, end.y))
        self.end = Point2D(max(start.x, end.x), max(start.y, end.y))

    def __str__(self):
        return f"Line2D(start: {self.start}, end: {self.end})"

    def intersects(self, p):
        # Assumes only horizontal and vertical line segments.
        if p.x == self.start.x and p.y >= self.start.y and p.y <= self.end.y:   # Vertical case.
            return True
        elif p.y == self.start.y and p.x >= self.start.x and p.x <= self.end.x: # Horizontal case.
            return True
        return False

    __repr__ = __str__
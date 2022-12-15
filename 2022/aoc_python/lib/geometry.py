from math import atan2, degrees, sqrt

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

    def euclidean_distance(self, p):
        return sqrt(pow(p.x - self.x, 2) + pow(p.y - self.y, 2))

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


class Circle:
    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius

    def __eq__(self, other):
        if isinstance(other, Circle):
            return self.centre == other.centre and self.radius == other.radius

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.centre, self.radius))

    def intersects(self, other_circle):
        distance_between_centres = self.centre.euclidean_distance(other_circle.centre)
        x_distance = other_circle.centre.x - self.centre.x
        y_distance = other_circle.centre.y - self.centre.y
        if distance_between_centres > self.radius + other_circle.radius:
            # The circles are separated from each other; no intersection.
            return False
        elif distance_between_centres < abs(self.radius - other_circle.radius):
            # One of the circles is inside the other; no intersection.
            return False
        elif distance_between_centres == 0 or distance_between_centres == self.radius - other_circle.radius:
            # The circles are copies of one another; infinite intersection points.
                return True, None
        else:
            # The circles have one or two intersection points.
            chord_distance = (self.radius ** 2 - other_circle.radius ** 2 + distance_between_centres ** 2) / (2 * distance_between_centres)

            # distance from 1st circle's centre to the chord between intersects
            half_chord_length = sqrt(self.radius ** 2 - chord_distance ** 2)
            chord_midpoint_x = self.centre.x + (chord_distance * x_distance) / distance_between_centres
            chord_midpoint_y = self.centre.y + (chord_distance * y_distance) / distance_between_centres
            intersection1 = (round(chord_midpoint_x + (half_chord_length * y_distance) / distance_between_centres),
                  round(chord_midpoint_y - (half_chord_length * x_distance) / distance_between_centres))
            theta1 = round(degrees(atan2(intersection1[1] - self.centre.y, intersection1[0] - self.centre.x)))
            intersection2 = (round(chord_midpoint_x - (half_chord_length * y_distance) / distance_between_centres),
                  round(chord_midpoint_y + (half_chord_length * x_distance) / distance_between_centres))
            theta2 = round(degrees(atan2(intersection2[1] - self.centre.y, intersection2[0] - self.centre.x)))

            if theta2 > theta1:
                intersection1, intersection2 = intersection2, intersection1

            if intersection1 == intersection2:
                return True, intersection1
            else:
                return True, (intersection1, intersection2)

    def __str__(self):
        return f"Circle(centre: {self.centre}, radius: {self.radius})"

    __repr__ = __str__

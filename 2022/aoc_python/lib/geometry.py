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

    def intersects_point(self, p):
        # Determines if a point lies on the line segment.
        min_x = min(self.start.x, self.end.x)
        max_x = max(self.start.x, self.end.x)
        min_y = min(self.start.y, self.end.y)
        max_y = max(self.start.y, self.end.y)

        return p.x >= min_x and p.x <= max_x and p.y >= min_y and p.y <= max_y

    def intersects_line_segment(self, ls):
        # Uses https://algotree.org/algorithms/computational_geometry/line_segment_intersection/
        def get_orientation(p, q, r):
            # Determine orientation of the line segments pq and qr.
            m_delta = ( q.y - p.y ) * ( r.x - q.x ) - \
            ( q.x - p.x ) * ( r.y - q.y )

            if m_delta > 0:
                # Clockwise: points are ordered clockwise; line segments are in the order pq, qr, rp.
                return 1
            elif m_delta < 0:
                # Anticlockwise: points are ordered anticlockwise; line segments are in the order pr, rq, qp.
                return -1
            else:
                # Parallel or collinear.
                return 0

        o1 = get_orientation(self.start, self.end, ls.start)
        o2 = get_orientation(self.start, self.end, ls.end)
        o3 = get_orientation(ls.start, ls.end, self.start)
        o4 = get_orientation(ls.start, ls.end, self.end)

        # Check if points are not collinear.
        # self ( p1, q1 ) and ls ( p2, q2 ) intersect
        # if points ( p1, q1, p2 ) and points ( p1, q1, q2 ) have different orientations;
        # and
        # if points ( p2, q2, p1 ) and points ( p2, q2, q1 ) have different orientations.
        if o1 != o2 and o3 != o4:
            return True

        # Check if points are collinear.
        if o1 == 0:     # ls.start is collinear with self. Check if it is in self.
            return self.intersects_point(ls.start)
        elif o2 == 0:   # ls.end is collinear with self. Check if it is in self.
            return self.intersects_point(ls.end)
        elif o3 == 0:   # self.start is collinear with ls. Check if it is in ls.
            return ls.intersects_point(self.start)
        elif o4 == 0:   # self.end is collinear with ls. Check if it is in ls.
            return ls.intersects_point(self.end)

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

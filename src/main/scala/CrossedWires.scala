import scala.collection.mutable.ListBuffer
import scala.io.Source

case class Point(x: Int, y: Int)

class CrossedWires {
  def manhattanDistance(startPoint: Point, endPoint: Point): Int = {
    val dx = math.abs(endPoint.x) - math.abs(startPoint.x)
    val dy = math.abs(endPoint.y) - math.abs(startPoint.y)
    dx + dy
  }

  def manhattanDistance(endPoint: Point): Int = {
    manhattanDistance(Point(0, 0), endPoint)
  }

  def getPoints(steps: Seq[String]): Seq[Point] = {
    var points = new ListBuffer[Point]()
    var startPoint = Point(0, 0)
    points += startPoint // Add the initial point.
    for (step <- steps) {
      val path = (step.substring(0, 1), step.substring(1).toInt)
      val endPoint = path._1 match {
        case "U" => Point(startPoint.x, startPoint.y + path._2)
        case "D" => Point(startPoint.x, startPoint.y - path._2)
        case "L" => Point(startPoint.x - path._2, startPoint.y)
        case "R" => Point(startPoint.x + path._2, startPoint.y)
      }
      points += endPoint
      startPoint = endPoint
    }
    points.toList
  }

  private def isValidIntersection(horizontalStart: Point, horizontalEnd: Point, verticalStart: Point, verticalEnd: Point, intersection: Point): Boolean = {
    if (intersection.x >= horizontalStart.x && intersection.x <= horizontalEnd.x) {
      if (intersection.y >= verticalStart.y && intersection.y <= verticalEnd.y) {
        return true
      }
      return false
    }
    false
  }

  private def findIntersection(wire1Start: Point, wire1End: Point, wire2Start: Point, wire2End: Point): Point = {
    // Determine if wires are vertical or horizontal.
    val wire1Horizontal = wire1Start.y == wire1End.y
    val wire2Horizontal = wire2Start.y == wire2End.y

    if (wire1Horizontal == wire2Horizontal) {
      // No intersection, return null.
      null
    } else {
      if (wire1Horizontal) {
        // Wire 1 is horizontal, Wire 2 is vertical.
        val intersection = Point(wire2Start.x, wire1Start.y)
        val intersectionExists = if (wire1End.x - wire1Start.x > 0) {
          if (wire2End.y - wire2Start.y > 0) {
            isValidIntersection(
              horizontalStart = wire1Start,
              horizontalEnd = wire1End,
              verticalStart = wire2Start,
              verticalEnd = wire2End,
              intersection = intersection
            )
          } else {
            isValidIntersection(
              horizontalStart = wire1Start,
              horizontalEnd = wire1End,
              verticalStart = wire2End,
              verticalEnd = wire2Start,
              intersection = intersection
            )
          }
        } else {
          if (wire2End.y - wire2Start.y > 0) {
            isValidIntersection(
              horizontalStart = wire1End,
              horizontalEnd = wire1Start,
              verticalStart = wire2Start,
              verticalEnd = wire2End,
              intersection = intersection
            )
          } else {
            isValidIntersection(
              horizontalStart = wire1End,
              horizontalEnd = wire1Start,
              verticalStart = wire2End,
              verticalEnd = wire2Start,
              intersection = intersection
            )
          }
        }
        if (intersectionExists) {
          intersection
        } else {
          // Point does not line on both wires, return null.
          null
        }
      } else {
        // Wire 1 is vertical, Wire 2 is horizontal.
        val intersection = Point(wire1Start.x, wire2Start.y)
        val intersectionExists = if (wire2End.x - wire2Start.x > 0) {
          if (wire1End.y - wire1Start.y > 0) {
            isValidIntersection(
              horizontalStart = wire2Start,
              horizontalEnd = wire2End,
              verticalStart = wire1Start,
              verticalEnd = wire1End,
              intersection = intersection
            )
          } else {
            isValidIntersection(
              horizontalStart = wire2Start,
              horizontalEnd = wire2End,
              verticalStart = wire1End,
              verticalEnd = wire1Start,
              intersection = intersection
            )
          }
        } else {
          if (wire1End.y - wire1Start.y > 0) {
            isValidIntersection(
              horizontalStart = wire2End,
              horizontalEnd = wire2Start,
              verticalStart = wire1Start,
              verticalEnd = wire1End,
              intersection = intersection
            )
          } else {
            isValidIntersection(
              horizontalStart = wire2End,
              horizontalEnd = wire2Start,
              verticalStart = wire1End,
              verticalEnd = wire1Start,
              intersection = intersection
            )
          }
        }
        if (intersectionExists) {
          intersection
        } else {
          // Point does not line on both wires, return null.
          null
        }
      }
    }
  }

  private def isCollinear(startPoint: Point, endPoint: Point, testPoint: Point): Boolean = {
    if (endPoint.x - startPoint.x > 0) {
      if (testPoint.x <= endPoint.x && testPoint.x >= startPoint.x) {
        if (testPoint.y != startPoint.y){
          false
        }
        else {
          true
        }
      } else {
        false
      }
    } else if (endPoint.x - startPoint.x < 0) {
      if (testPoint.x <= startPoint.x && testPoint.x >= endPoint.x) {
        if (testPoint.y != startPoint.y){
          false
        }
        else {
          true
        }
      } else {
        false
      }
    } else if (endPoint.y - startPoint.y > 0) {
      if (testPoint.y <= endPoint.y && testPoint.y >= startPoint.y) {
        if (testPoint.x != startPoint.x){
          false
        }
        else {
          true
        }
      } else {
        false
      }
    } else if (endPoint.y - startPoint.y < 0) {
      if (testPoint.y <= startPoint.y && testPoint.y >= endPoint.y) {
        if (testPoint.x != startPoint.x){
          false
        }
        else {
          true
        }
      } else {
        false
      }
    } else {
      false
    }
  }

  def getIntersections(wire1Points: Seq[Point], wire2Points: Seq[Point]): Seq[Point] = {
    val intersectionPoints = ListBuffer[Point]()
    var i = 0
    while (i < wire1Points.length - 1) {
      val wire1Start = wire1Points(i)
      val wire1End = wire1Points(i + 1)
      var j = 0
      while (j < wire2Points.length - 1) {
        val wire2Start = wire2Points(j)
        val wire2End = wire2Points(j + 1)
        val intersectionPoint = findIntersection(
          wire1Start,
          wire1End,
          wire2Start,
          wire2End
        )
        if (intersectionPoint != null && intersectionPoint != Point(0, 0)) {
          intersectionPoints += intersectionPoint
        }
        j += 1
      }
      i += 1
    }
    intersectionPoints.toList
  }

  def numSteps(wirePoints: Seq[Point], intersection: Point): Int = {
    var sum = 0
    var i = 0
    while (i < wirePoints.length - 1) {
      val startPoint = wirePoints(i)
      var endPoint = wirePoints(i + 1)
      if (isCollinear(startPoint, endPoint, intersection)) {
        endPoint = intersection
        sum += manhattanDistance(startPoint, endPoint)
        return sum
      } else {
        sum += manhattanDistance(startPoint, endPoint)
      }
      i += 1
    }
    sum
  }
}

object CrossedWires {
  def testCrossedWires(wire1Str: String, wire2Str: String) = {
    val cw = new CrossedWires()
    val wire1List = wire1Str.split(",")
    val wire2List = wire2Str.split(",")
    val wire1Points = cw.getPoints(wire1List)
    val wire2Points = cw.getPoints(wire2List)
    println(s"wire1Points: $wire1Points")
    println(s"wire2Points: $wire2Points")
    val intersections = cw.getIntersections(wire1Points, wire2Points)
    println(s"intersections: $intersections")
    var minDistance = Int.MaxValue
    var minNumSteps = Int.MaxValue
    for (intersection <- intersections) {
      val distance = cw.manhattanDistance(intersection)
      val numSteps = cw.numSteps(wire1Points, intersection) + cw.numSteps(wire2Points, intersection)
      if (distance < minDistance) {
        minDistance = distance
      }
      if (numSteps < minNumSteps) {
        minNumSteps = numSteps
      }
      println(s"Distance of $intersection from origin: $distance")
      println(s"Number of steps to $intersection: $numSteps")
    }
    println(s"Smallest distance: $minDistance")
    println(s"Smallest number of steps: $minDistance")
  }

  def main(args: Array[String]): Unit = {
    if (args.length > 0) {
      val wires = Source.fromFile(args(0)).getLines.toArray
      val wire1 = wires(0)
      val wire2 = wires(1)

      testCrossedWires(wire1, wire2)
    } else {
      Console.err.println("Please enter filename.")
    }
  }
}
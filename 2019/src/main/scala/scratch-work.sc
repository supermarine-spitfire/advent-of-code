// FOR DAY 1
def calcFuelForModule(moduleMass: Int): Int = {
  math.floor(moduleMass / 3).asInstanceOf[Int] - 2
}

def calcFuelForFuel(fuelMass: Int) = {
  def loop(acc: Int, mass: Int): Int = {
    Console.out.println(s"acc: ${acc}")
//    Console.out.println(s"mass: ${mass}")
    val reqFuel = calcFuelForModule(mass)
    if (reqFuel <= 0 ) {
      acc
    } else {
      Console.out.println(s"reqFuel: ${reqFuel}")
      loop(acc + reqFuel, reqFuel)
    }
  }

  loop(0, fuelMass)
}

def calcTotalFuel(mass: Int) = {
  val moduleFuel = calcFuelForModule(mass)
  val fuelFuel = calcFuelForFuel(moduleFuel)
  println(s"moduleFuel: ${moduleFuel}")
  println(s"fuelFuel: ${fuelFuel}")
  println(s"Total fuel: ${moduleFuel + fuelFuel}")
}

calcTotalFuel(14)
calcTotalFuel(1969)
calcTotalFuel(100756)
// FOR DAY 3
import scala.collection.mutable.ListBuffer
case class Point(x: Int, y: Int)
class CrossedWires {
  def manhattanDistance(startPoint: Point, endPoint: Point): Int = {
    val dx = math.abs(math.abs(endPoint.x) - math.abs(startPoint.x))
    val dy = math.abs(math.abs(endPoint.y) - math.abs(startPoint.y))
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
//      println("Point within horizontal x range.")
      if (intersection.y >= verticalStart.y && intersection.y <= verticalEnd.y) {
//        println("Point within vertical y range.")
        return true
      }
//      println("Point outside vertical y range.")
      return false
    }
//    println("Point outside horizontal x range.")
    false
  }

  private def findIntersection(wire1Start: Point, wire1End: Point, wire2Start: Point, wire2End: Point): Point = {
    // Determine if wires are vertical or horizontal.
    val wire1Horizontal = wire1Start.y == wire1End.y
    val wire2Horizontal = wire2Start.y == wire2End.y

    if (wire1Horizontal == wire2Horizontal) {
//      println("Parallel wires, no intersection.")
      // No intersection, return null.
      null
    } else {
      if (wire1Horizontal) {
        // Wire 1 is horizontal, Wire 2 is vertical.
        val intersection = Point(wire2Start.x, wire1Start.y)
        val intersectionExists = if (wire1End.x - wire1Start.x > 0) {
          if (wire2End.y - wire2Start.y > 0) {
            isValidIntersection(
              wire1Start,
              wire1End,
              wire2Start,
              wire2End,
              intersection
            )
          } else {
            isValidIntersection(
              wire1Start,
              wire1End,
              wire2End,
              wire2Start,
              intersection
            )
          }
        } else {
          if (wire2End.y - wire2Start.y > 0) {
            isValidIntersection(
              wire1End,
              wire1Start,
              wire2Start,
              wire2End,
              intersection
            )
          } else {
            isValidIntersection(
              wire1End,
              wire1Start,
              wire2End,
              wire2Start,
              intersection
            )
          }
        }
        if (intersectionExists) {
//          println(s"Intersection point: $intersection")
          intersection
        } else {
          // Point does not line on both wires, return null.
//          println(s"Point $intersection not on both wires")
          null
        }
      } else {
        // Wire 1 is vertical, Wire 2 is horizontal.
        val intersection = Point(wire1Start.x, wire2Start.y)
        val intersectionExists = if (wire2End.x - wire2Start.x > 0) {
          if (wire1End.y - wire1Start.y > 0) {
            isValidIntersection(
              wire2Start,
              wire2End,
              wire1Start,
              wire1End,
              intersection
            )
          } else {
            isValidIntersection(
              wire2Start,
              wire2End,
              wire1End,
              wire1Start,
              intersection
            )
          }
        } else {
          if (wire1End.y - wire1Start.y > 0) {
            isValidIntersection(
              wire2End,
              wire2Start,
              wire1Start,
              wire1End,
              intersection
            )
          } else {
            isValidIntersection(
              wire2End,
              wire2Start,
              wire1End,
              wire1Start,
              intersection
            )
          }
        }
        if (intersectionExists) {
//          println(s"Intersection point: $intersection")
          intersection
        } else {
          // Point does not line on both wires, return null.
//          println(s"Point $intersection not on both wires")
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
//      println("BEGIN WIRE CHECK")
//      println(s"Wire 1: (${wire1Start.x}, ${wire1Start.y}) -> (${wire1End.x}, ${wire1End.y})")
      var j = 0
      while (j < wire2Points.length - 1) {
        val wire2Start = wire2Points(j)
        val wire2End = wire2Points(j + 1)
//        println(s"Wire 2: (${wire2Start.x}, ${wire2Start.y}) -> (${wire2End.x}, ${wire2End.y})")
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
//      println("END WIRE CHECK")
    }
    intersectionPoints.toList
  }

  def numSteps(wirePoints: Seq[Point], intersection: Point): Int = {
    println(s"intersection: $intersection")
    var sum = 0
    var i = 0
    while (i < wirePoints.length - 1) {
      val startPoint = wirePoints(i)
      var endPoint = wirePoints(i + 1)
      if (isCollinear(startPoint, endPoint, intersection)) {
        println("Encountered intersection point.")
        endPoint = intersection
        val distance = manhattanDistance(startPoint, endPoint)
        println(s"distance: $distance")
        sum += distance
        println(s"sum: $sum")
        return sum
      } else {
        val distance = manhattanDistance(startPoint, endPoint)
        println(s"distance: $distance")
        sum += distance
      }
      i += 1
    }
    println(s"sum: $sum")
    sum
  }
}
def testCrossedWires(wire1Str: String, wire2Str: String) = {
  val cw = new CrossedWires()
  val wire1List = wire1Str.split(",")
  val wire2List = wire2Str.split(",")
  val wire1Points = cw.getPoints(wire1List)
  val wire2Points = cw.getPoints(wire2List)
//  println(s"wire1Points: $wire1Points")
//  println(s"wire2Points: $wire2Points")
  val intersections = cw.getIntersections(wire1Points, wire2Points)
//  println(s"intersections: $intersections")
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
  println(s"Smallest number of steps: $minNumSteps")
}

var wire1Str = "R8,U5,L5,D3"
var wire2Str = "U7,R6,D4,L4"
testCrossedWires(wire1Str, wire2Str)

wire1Str = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
wire2Str = "U62,R66,U55,R34,D71,R55,D58,R83"
testCrossedWires(wire1Str, wire2Str)

wire1Str = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
wire2Str = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
testCrossedWires(wire1Str, wire2Str)

wire1Str = "R991,U557,R554,U998,L861,D301,L891,U180,L280,D103,R828,D58,R373,D278,L352,D583,L465,D301,R384,D638,L648,D413,L511,U596,L701,U463,L664,U905,L374,D372,L269,U868,R494,U294,R661,U604,L629,U763,R771,U96,R222,U227,L97,D793,L924,U781,L295,D427,R205,D387,L455,D904,R254,D34,R341,U268,L344,D656,L715,U439,R158,U237,R199,U729,L428,D125,R487,D506,R486,D496,R932,D918,R603,U836,R258,U15,L120,U528,L102,D42,R385,U905,L472,D351,R506,U860,L331,D415,R963,D733,R108,D527,L634,U502,L553,D623,R973,U209,L632,D588,R264,U553,L768,D689,L708,D432,R247,U993,L146,U656,R710,U47,R783,U643,R954,U888,L84,U202,R495,U66,R414,U993,R100,D557,L326,D645,R975,U266,R143,U730,L491,D96,L161,U165,R97,D379,R930,D613,R178,D635,R192,U957,L450,U149,R911,U220,L914,U659,L67,D825,L904,U137,L392,U333,L317,U310,R298,D240,R646,U588,R746,U861,L958,D892,L200,U463,R246,D870,R687,U815,R969,U864,L972,U254,L120,D418,L567,D128,R934,D217,R764,U128,R146,U467,R690,U166,R996,D603,R144,D362,R885,D118,L882,U612,R270,U917,L599,D66,L749,D498,L346,D920,L222,U439,R822,U891,R458,U15,R831,U92,L164,D615,L439,U178,R409,D463,L452,U633,L683,U186,R402,D609,L38,D699,L679,D74,R125,D145,R424,U961,L353,U43,R794,D519,L359,D494,R812,D770,L657,U154,L137,U549,L193,D816,R333,U650,R49,D459,R414,U72,R313,U231,R370,U680,L27,D221,L355,U342,L597,U748,R821,D280,L307,U505,L160,U982,L527,D516,L245,U158,R565,D797,R99,D695,L712,U155,L23,U964,L266,U623,L317,U445,R689,U150,L41,U536,R638,D200,R763,D260,L234,U217,L881,D576,L223,U39,L808,D125,R950,U341,L405"
wire2Str = "L993,D508,R356,U210,R42,D68,R827,D513,L564,D407,L945,U757,L517,D253,R614,U824,R174,D536,R906,D291,R70,D295,R916,D754,L892,D736,L528,D399,R76,D588,R12,U617,R173,D625,L533,D355,R178,D706,R139,D419,R460,U976,L781,U973,L931,D254,R195,U42,R555,D151,R226,U713,L755,U398,L933,U264,R352,U461,L472,D810,L257,U901,R429,U848,L181,D362,R404,D234,L985,D392,R341,U608,L518,D59,L804,D219,L366,D28,L238,D491,R265,U131,L727,D504,R122,U461,R732,D411,L910,D884,R954,U341,L619,D949,L570,D823,R646,D226,R197,U892,L691,D294,L955,D303,R490,D469,L503,D482,R390,D741,L715,D187,R378,U853,L70,D903,L589,D481,L589,U911,R45,U348,R214,D10,R737,D305,R458,D291,R637,D721,R440,U573,R442,D407,L63,U569,L903,D936,R518,U859,L370,D888,R498,D759,R283,U469,R548,D185,R808,D81,L629,D761,R807,D878,R712,D183,R382,D484,L791,D371,L188,D397,R645,U679,R415,D446,L695,U174,R707,D36,R483,U877,L819,D538,L277,D2,R200,D838,R837,U347,L865,D945,R958,U575,L924,D351,L881,U961,R899,U845,R816,U866,R203,D380,R766,D97,R38,U148,L999,D332,R543,U10,R351,U281,L460,U309,L543,U795,L639,D556,L882,D513,R722,U314,R531,D604,L418,U840,R864,D694,L530,U862,R559,D639,R689,D201,L439,D697,R441,U175,R558,D585,R92,D191,L533,D788,R154,D528,R341,D908,R811,U750,R172,D742,R113,U56,L517,D826,L250,D269,L278,U74,R285,U904,L221,U270,R296,U671,L535,U340,L206,U603,L852,D60,R648,D313,L282,D685,R482,U10,R829,U14,L12,U365,R996,D10,R104,U654,R346,D458,R219,U247,L841,D731,R115,U400,L731,D904,L487,U430,R612,U437,L865,D618,R747,U522,R309,U302,R9,U609,L201"
testCrossedWires(wire1Str, wire2Str)
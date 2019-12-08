import scala.collection.mutable
import scala.io.Source

class OrbitMap {
  private val orbitGraph = new mutable.HashMap[String, String]()
  private val centreOfMass = "COM"

  def defineOrbits(orbits: Seq[String]): Unit = {
    for (orbit <- orbits) {
      val orbitBodies = orbit.split(raw"\)")
      val parent = orbitBodies(0)
      val child = orbitBodies(1)
      this.orbitGraph(child) = parent  // Given a body, find the body it orbits.
    }
  }

  def countOrbitalTransfers(
      startVertex: String, endVertex: String, commonAncestor: String
  ): Unit = {
    var numOrbitalTransfers = 0
    val keyQueue = mutable.Stack[String]()
    keyQueue.push(startVertex)
    keyQueue.push(endVertex)

    while (keyQueue.nonEmpty) {
      var key = keyQueue.pop()
      var value = this.orbitGraph(key)
      while (value != commonAncestor) {
        numOrbitalTransfers += 1
        key = value
        value = this.orbitGraph(key)
      }
      numOrbitalTransfers += 1
    }

    println(s"Total number of orbital transfers: $numOrbitalTransfers")
  }

  def countNumOrbits(): Unit = {
    var numOrbits = 0
    val keyQueue = mutable.Stack[String]()
    this.orbitGraph.keys.foreach(k => keyQueue.push(k))

    while (keyQueue.nonEmpty) {
      var key = keyQueue.pop()
      var value = this.orbitGraph(key)
      while (value != this.centreOfMass) {
        numOrbits += 1
        key = value
        value = this.orbitGraph(key)
      }
      numOrbits += 1
    }

    println(s"Total number of orbits: $numOrbits")
  }

  def findPathToCentre(start: String): mutable.Stack[String] = {
    val path = mutable.Stack[String]()

    var value = ""
    var key = start
    while (value != this.centreOfMass) {
      value = this.orbitGraph(key)
      path.push(value)
      key = value
    }

    path
  }

  def reset(): Unit = {
    this.orbitGraph.clear()
  }

  def getParentBody(child: String): String = {
    this.orbitGraph(child)
  }
}

object OrbitMap {
  def main(args: Array[String]): Unit = {
    val filename = "day-6-input.txt"
    var input = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L".split("\n")
    partOne(input)
    input = Source.fromFile(filename).getLines.toArray
    partOne(input)

    input = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN".split("\n")
    partTwo(input)
    input = Source.fromFile(filename).getLines.toArray
    partTwo(input)
  }

  def partOne(input: Seq[String]): Unit = {
    println("PART ONE")
    val orbitMap = new OrbitMap()
    orbitMap.defineOrbits(input)
    orbitMap.countNumOrbits()
    orbitMap.reset()
  }

  def partTwo(input: Seq[String]): Unit = {
    println("PART TWO")
    val orbitMap = new OrbitMap()
    orbitMap.defineOrbits(input)
    val santaPath = orbitMap.findPathToCentre("SAN")
    val youPath = orbitMap.findPathToCentre("YOU")
    println(s"santaPath: $santaPath")
    println(s"youPath: $youPath")

    var curSantaVertex = santaPath.pop()
    var curYouVertex = youPath.pop()
    var lastCommonAncestor = ""

    while (curSantaVertex == curYouVertex) {
      println(s"curSantaVertex: $curSantaVertex")
      println(s"curYouVertex: $curYouVertex")
      lastCommonAncestor = curSantaVertex
      curSantaVertex = santaPath.pop()
      curYouVertex = youPath.pop()
    }

    val startVertex = orbitMap.getParentBody("YOU")
    val endVertex = orbitMap.getParentBody("SAN")
    println(s"lastCommonAncestor: $lastCommonAncestor")
    println(s"startVertex: $startVertex")
    println(s"endVertex: $endVertex")

    orbitMap.countOrbitalTransfers(
      startVertex = startVertex,
      endVertex = endVertex,
      commonAncestor = lastCommonAncestor
    )
  }
}
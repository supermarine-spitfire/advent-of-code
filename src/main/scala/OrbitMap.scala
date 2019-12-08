import scala.collection.mutable
import scala.io.Source

class OrbitMap {
  private val orbitGraph = new mutable.HashMap[String, String]()
  private val start = "COM"

  def defineOrbits(orbits: Seq[String]): Unit = {
    for (orbit <- orbits) {
      val orbitBodies = orbit.split(raw"\)")
      val parent = orbitBodies(0)
      val child = orbitBodies(1)
      this.orbitGraph(child) = parent  // Given a body, find the body it orbits.
    }
  }

  def countNumOrbits(): Unit = {
    var numOrbits = 0
    val keyQueue = mutable.Stack[String]()
    this.orbitGraph.keys.foreach(k => keyQueue.push(k))

    while (keyQueue.nonEmpty) {
      var key = keyQueue.pop()
      var value = this.orbitGraph(key)
      while (value != this.start) {
        numOrbits += 1
        key = value
        value = this.orbitGraph(key)
      }
      numOrbits += 1
    }

    println(s"Total number of orbits: $numOrbits")
  }

  def reset(): Unit = {
    this.orbitGraph.clear()
  }
}

object OrbitMap {
  def main(args: Array[String]): Unit = {
    val filename = "day-6-input.txt"
    var input = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L".split("\n")
    partOne(input)
    input = Source.fromFile(filename).getLines.toArray
    partOne(input)
  }

  def partOne(input: Seq[String]) = {
    val orbitMap = new OrbitMap()
    orbitMap.defineOrbits(input)
    orbitMap.countNumOrbits()
    orbitMap.reset()
  }
}
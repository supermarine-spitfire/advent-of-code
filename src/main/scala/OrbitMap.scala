import scala.io.Source

import graph._

class OrbitMap {
  private val orbitGraph = new Graph[String]()
  private var centralBodyStr = ""
  private var centralBody:Vertex[String] = _

  def makeOrbit(parent: String, child: String) = {
    val parentVertex = orbitGraph.addVertex(parent)
    if (parent == centralBodyStr) {
      centralBody = parentVertex
    }
    val childVertex = orbitGraph.addVertex(child)
    orbitGraph.addEdge(parentVertex, childVertex)
  }

  def defineOrbits(orbits: Seq[String]): Unit = {
    for (orbit <- orbits) {
      val orbitBodies = orbit.split(raw"\)")
      val parent = orbitBodies(0)
      val child = orbitBodies(1)
      println(s"parent: $parent")
      println(s"child: $child")
      if (centralBodyStr.equals("")) {
        // Define the starting point.
        centralBodyStr = parent
      }
      makeOrbit(parent, child)
      println()
    }
//    println(s"this.orbitGraph: ${this.orbitGraph}")
  }

  def countNumOrbits() = {
    orbitGraph.bfs(centralBody)
    println(s"vertices (before filtering): ${orbitGraph.getVertices}")
    val vertices = orbitGraph.getVertices.filter(
      v => v.colour == Colour.Black || v.colour == Colour.Grey
    )
    println(s"vertices (after filtering): $vertices")

    var totalOrbits = 0
    for (v <- vertices) {
      println(s"v: (${v.label}, ${v.distance})")
      totalOrbits += v.distance
    }
    println(s"Total number of orbits: $totalOrbits")
  }

  def reset() = {
    orbitGraph.reset()
    centralBody = null
    centralBodyStr = ""
  }
}

object OrbitMap {
  def main(args: Array[String]): Unit = {
    val filename = "day-6-input.txt"
    var input = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L".split("\n")
    partOne(input)
//    input = Source.fromFile(filename).getLines.toList
//    partOne(input)
  }

  def partOne(input: Seq[String]) = {
    val orbitMap = new OrbitMap()
    orbitMap.defineOrbits(input)
    orbitMap.countNumOrbits()
  }
}
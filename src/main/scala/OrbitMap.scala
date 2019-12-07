import scala.collection.mutable.ListBuffer
import scala.io.Source

case class Vertex[T](label: String, wasVisited: Boolean)

class OrbitMap {
  private val orbitGraph = collection.mutable.HashMap[String, ListBuffer[String]]()
  private var centralBody = ""

  private def makeOrbit(parent: String, child: String) = {
    if (!orbitGraph.keySet.exists(k => k.equals(parent))) {
      // New parent body found.
      orbitGraph(parent) = ListBuffer[String]()
      orbitGraph(parent) += child
    } else {
      // Existing body found.
      orbitGraph(parent) += child
    }
  }

  def defineOrbits(orbits: Seq[String]): Unit = {
    for (orbit <- orbits) {
      val orbitBodies = orbit.split(raw"\)")
      val parent = orbitBodies(0)
      val child = orbitBodies(1)
      if (centralBody.equals("")) {
        // Define the starting point.
        centralBody = parent
      }
      this.makeOrbit(parent, child)
    }
    println(s"this.orbitGraph: ${this.orbitGraph}")
  }
}

object OrbitMap {
  def main(args: Array[String]): Unit = {
    val filename = "day-6-input.txt"
    val input = Source.fromFile(filename).getLines.toList
    val orbitMap = new OrbitMap()
    orbitMap.defineOrbits(input)
  }
}
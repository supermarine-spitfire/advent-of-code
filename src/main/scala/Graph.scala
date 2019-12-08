package graph

import scala.collection.mutable
import scala.collection.mutable.ListBuffer

class Graph[T] {
  private val adjacencyLists = collection.mutable.HashMap[T, mutable.ArrayBuffer[Vertex[T]]]()
  private val vertices = new ListBuffer[Vertex[T]]()

  def getVertices: Seq[Vertex[T]] = this.vertices.toList

  /** Adds a vertex to the graph.
   *  Returns the newly-created vertex, or the already-present vertex.
   */
  def addVertex(label: T): Vertex[T] = {
    // First check if a vertex with the provided label
    // already exists in vertices.
    for (vertex <- this.vertices) {
      if (vertex.label == label) {
        // Vertex exists; return it.
        println("Returning existing vertex.")
        return vertex
      }
    }

    // Vertex not present; make it.
    val vertex = new Vertex(label, Colour.White, Int.MaxValue, null)
    this.vertices += new Vertex(label, Colour.White, Int.MaxValue, null)
    println("Returning new vertex.")
    vertex
  }

  /** Adds an edge to the graph.
   *  Returns whether or not the edge already exists.
   *
   *  parent: The source of the edge.
   *  child: The destination of the edge.
   */
  def addEdge(parent: Vertex[T], child: Vertex[T]): Boolean = {
    if (!adjacencyLists.keySet.exists(k => k.equals(parent.label))) {
      // Defining new parent vertex.
      adjacencyLists(parent.label) = mutable.ArrayBuffer[Vertex[T]]()
    }

    if (!adjacencyLists(parent.label).contains(child)) {
      // An edge from the parent to the child does not exist yet.
      adjacencyLists(parent.label) += child
      true
    } else {
      false
    }
  }

  def bfs(source: Vertex[T]): Unit = {
    // Set source apart.
    source.colour = Colour.Grey
    source.distance = 0
    source.parent = null

    val queue = mutable.Queue[Vertex[T]]()
    queue.enqueue(source)
    while (queue.nonEmpty) {
      println(s"queue: $queue")
      val u = queue.dequeue()
      val uAdjacencyList = try {
        this.adjacencyLists(u.label)
      } catch {
        case _: Throwable => ListBuffer[Vertex[T]]()
      }
      for (i <- uAdjacencyList.indices) {
        val v = uAdjacencyList(i)
        println(s"u: (${u.label}, ${u.colour}, ${u.distance})")
        println(s"v: (${v.label}, ${v.colour}, ${v.distance})")
        if (v.colour == Colour.White) {
          v.colour = Colour.Grey
          v.distance = u.distance + 1
          v.parent = u
          queue.enqueue(v)
        }
      }
      u.colour = Colour.Black
    }
    println(s"vertices (after executing Graph.dfs()): ${this.getVertices}")
  }

  def printPath(s: Vertex[T], v: Vertex[T]): Unit = {
    if (v == s) {
      println(s"Current vertex: (${s.label}, ${s.distance})")
    } else if (v.parent == null) {
      println(s"No path from ${s.label} to ${v.label} exists.")
    } else {
      printPath(s, v.parent)
      println(s"Current vertex: (${v.label}, ${v.distance})")
    }
  }

  def reset(): Unit = {
    this.adjacencyLists.clear()
    this.vertices.clear()
  }

  override def toString: String = {
    var s = s"Vertices (${vertices.length} in total): "
    for (v <- vertices) {
      s += s"(${v.label}, ${v.distance})"
      s += ", "
    }
    s = s.stripSuffix(", ")
    s += s"\nEdges:\n"
    for (k <- adjacencyLists.keysIterator) {
      s += s"$k: "
      for (v <- adjacencyLists(k)) {
        s += s"${v.label}, "
      }
      s = s.stripSuffix(", ")
      s += "\n"
    }
    s
  }
}
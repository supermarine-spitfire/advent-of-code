package graph

/** Used to identify if a vertex has been visited.
 *  White denotes an unvisited vertex.
 *  Grey denotes a visited vertex that has unvisted neighbours.
 *  Black denotes a visited vertex with no unvisited neighbours.
 */
object Colour extends Enumeration {
  type Colour = Value
  val White, Grey, Black = Value
}
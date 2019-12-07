import Colour.Colour

/**
 * Defines a graph vertex.
 *
 * label: A name associated with the vertex.
 * colour: Identifies if the vertex has been visited or not.
 * distance: The number of edges between a source vertex and the vertex.
 * parent: The predecessor of the vertex.
 */
case class Vertex[T](label: String, colour: Colour, distance: Int, parent: Vertex[T])
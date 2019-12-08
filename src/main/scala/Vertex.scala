package graph

import graph.Colour.Colour

/**
 * Defines a graph vertex.
 *
 * label: A name associated with the vertex.
 * colour: Identifies if the vertex has been visited or not.
 * distance: The number of edges between a source vertex and the vertex.
 * parent: The predecessor of the vertex.
 */
case class Vertex[T](var label: T, var colour: Colour, var distance: Int, var parent: Vertex[T])

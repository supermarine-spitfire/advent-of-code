import java.util.List;

public interface Graph<V> {
    /** Return the number of vertices in the graph */
    int getSize();

    /** Return the vertices in the graph */
    List<V> getVertices();

    /** Return the object for the specified vertex index */
    V getVertex(int index);

    /** Return the index for the specified vertex object */
    int getIndex(V v);

    /** Return the neighbours of vertex with the specified index */
    List<Integer> getNeighbours(int index);

    /** Return the degree for a specified vertex */
    int getDegree(int v);

    /** Print the edges */
    void printEdges();

    /** Clear the graph */
    void clear();

    /** Add a vertex to the graph */
    boolean addVertex(V vertex);

    /** Add an edge to the graph */
    boolean addEdge(int u, int v);

    /** Obtain a depth-first search tree starting from v */
    AbstractGraph<V>.Tree dfs(int v);

    /** Obtain a breadth-first search tree starting from v */
    AbstractGraph<V>.Tree bfs(int v);
}

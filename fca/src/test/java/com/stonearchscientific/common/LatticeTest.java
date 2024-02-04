package com.stonearchscientific.common;

import com.tinkerpop.blueprints.Graph;
import com.tinkerpop.blueprints.Vertex;
import com.tinkerpop.blueprints.Edge;
import com.tinkerpop.blueprints.Direction;
import com.tinkerpop.blueprints.impls.tg.TinkerGraph;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertEquals;
import java.io.File;
import java.util.ArrayList;
import guru.nidi.graphviz.engine.Format;
import guru.nidi.graphviz.engine.Graphviz;
import guru.nidi.graphviz.model.MutableGraph;
import guru.nidi.graphviz.parse.Parser;
import com.stonearchscientific.service.Main;


import java.util.BitSet;
import java.util.Arrays;
import java.util.List;

public class LatticeTest {
    private Graph graph;
    List<String> objects, attributes;
    Lattice<BitSet, BitSet> lattice;

    private BitSet bitset(String bitstring) {
        return BitSet.valueOf(new long[]{Long.parseLong(bitstring, 2)});
    }

    private Vertex createVertex(Graph graph, Concept<BitSet, BitSet> concept) {
        Vertex vertex = graph.addVertex(null);
        vertex.setProperty("label", concept);
        vertex.setProperty("color", 0);
        return vertex;
    }

    private void createEdge(Graph graph, Vertex v1, Vertex v2) {
        graph.addEdge(null, v1, v2, "");
        graph.addEdge(null, v2, v1, "");
    }

    private int numberOfVertices(Graph graph) {
        int count = 0;
        for(Vertex vertex : graph.getVertices()) {
            count++;
        }
        return count;
    }

    private int numberOfEdges(Graph graph) {
        int count = 0;
        for(Edge edge : graph.getEdges()) {
            count++;
        }
        return count;
    }

    @Before
    public void setUp() {
        graph = new TinkerGraph();

        objects = Arrays.asList("1", "2", "3", "4", "5");
        attributes = Arrays.asList("a", "b", "c", "d", "e");

        Concept<BitSet, BitSet> c1 = new Concept<>(bitset("00001"), bitset("11111"));
        Concept<BitSet, BitSet> c2 = new Concept<>(bitset("00011"), bitset("10111"));
        Concept<BitSet, BitSet> c3 = new Concept<>(bitset("00101"), bitset("01100"));
        Concept<BitSet, BitSet> c4 = new Concept<>(bitset("01011"), bitset("10000"));
        Concept<BitSet, BitSet> c5 = new Concept<>(bitset("11111"), bitset("00000"));
        Concept<BitSet, BitSet> c6 = new Concept<>(bitset("00111"), bitset("00100"));

        lattice = new Lattice<>(graph, c1);

        Vertex v1 = lattice.bottom();
        Vertex v2 = createVertex(graph, c2);
        Vertex v3 = createVertex(graph, c3);
        Vertex v4 = createVertex(graph, c4);
        Vertex v5 = createVertex(graph, c5);
        Vertex v6 = createVertex(graph, c6);

        createEdge(graph, v2, v1);
        createEdge(graph, v3, v1);
        createEdge(graph, v4, v2);
        createEdge(graph, v6, v2);
        createEdge(graph, v6, v3);
        createEdge(graph, v5, v4);
        createEdge(graph, v5, v6);
    }

    @Test
    public void testSetup() {
        assertEquals(numberOfVertices(graph), 6);
        assertEquals(numberOfEdges(graph), 14);
    }
    @Test
    public void testAddIntent() {
        Concept<BitSet, BitSet> c7 = new Concept<>(bitset("10000"), bitset("01111"));
        lattice.insert(graph, c7);
        assertEquals(numberOfVertices(graph), 8);
        assertEquals(numberOfEdges(graph), 22);
    }
}
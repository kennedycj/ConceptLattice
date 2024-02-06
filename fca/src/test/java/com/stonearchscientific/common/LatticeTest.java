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

    int[][] expected = {
        {0, 1, 0, 1, 0, 0, 0, 0},
        {1, 0, 0, 0, 0, 1, 0, 1},
        {0, 0, 0, 0, 1, 1, 0, 0},
        {1, 0, 0, 0, 0, 0, 1, 1},
        {0, 0, 1, 0, 0, 0, 1, 1},
        {0, 1, 1, 0, 0, 0, 0, 0},
        {0, 0, 0, 1, 1, 0, 0, 0},
        {0, 1, 0, 1, 1, 0, 0, 0}
    };

    private BitSet bitset(String bitstring) {
        return BitSet.valueOf(new long[]{Long.parseLong(bitstring, 2)});
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
    }

    @Test
    public void testSetup() {
        assertEquals(numberOfVertices(graph), 0);
        assertEquals(numberOfEdges(graph), 0);
    }
    @Test
    public void testAddIntent() {
        lattice = new Lattice<>(graph, new Concept<>(bitset("00001"), bitset("11111")));
        lattice.insert(graph, new Concept<>(bitset("00010"), bitset("10111")));
        lattice.insert(graph, new Concept<>(bitset("00100"), bitset("01100")));
        lattice.insert(graph, new Concept<>(bitset("01000"), bitset("10000")));
        lattice.insert(graph, new Concept<>(bitset("10000"), bitset("01111")));

        String graphvizOutput = Main.graphviz(graph, objects, attributes);

        try {
            MutableGraph g = new Parser().read(graphvizOutput);
            Graphviz.fromGraph(g).width(700).render(Format.PNG).toFile(new File("LatticeTestAddIntent.png"));
        } catch (Exception e) {
            e.printStackTrace();
        }

        int[][] observed = Main.generateAdjacencyMatrix(graph);

        for(int i = 0; i < observed.length; i++) {
            for(int j = 0; j < observed[i].length; j++) {
                assertEquals(expected[i][j], observed[i][j]);
            }
            System.out.println();
        }
    }
}
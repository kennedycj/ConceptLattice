package com.stonearchscientific.service;

import com.stonearchscientific.common.Concept;
import com.stonearchscientific.common.Lattice;
import com.google.common.collect.Range;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.Collection;
import java.io.File;
import com.tinkerpop.blueprints.Graph;
import com.tinkerpop.blueprints.Edge;
import com.tinkerpop.blueprints.Vertex;
import com.tinkerpop.blueprints.Direction;
import com.tinkerpop.blueprints.impls.tg.TinkerGraph;
import java.util.BitSet;
import guru.nidi.graphviz.engine.Format;
import guru.nidi.graphviz.engine.Graphviz;
import guru.nidi.graphviz.model.MutableGraph;
import guru.nidi.graphviz.parse.Parser;

public class Main {
    private static BitSet bitset(String bitstring) {
        return BitSet.valueOf(new long[]{Long.parseLong(bitstring, 2)});
    }

    public static List<String> decode(List<String> objects, BitSet bits) {
        List<String> decodedObjects = new ArrayList<>();
        for (int i = bits.nextSetBit(0); i >= 0; i = bits.nextSetBit(i+1)) {
            decodedObjects.add(objects.get(i));
        }
        return decodedObjects;
    }

    private static int numberOfVertices(Graph graph) {
        int count = 0;
        for(Vertex vertex : graph.getVertices()) {
            count++;
        }
        return count;
    }

    private static int numberOfEdges(Graph graph) {
        int count = 0;
        for(Edge edge : graph.getEdges()) {
            count++;
        }
        return count;
    }

    public static int[][] generateAdjacencyMatrix(Graph graph) {
        List<Vertex> vertices = new ArrayList<>();
        for (Vertex vertex : graph.getVertices()) {
            vertices.add(vertex);
        }

        for (int i = 0; i < vertices.size(); i++) {
            System.out.println(i + " : " + vertices.get(i).getProperty("label"));
        }

        int n = vertices.size();
        int[][] adjacencyMatrix = new int[n][n];

        for (Edge edge : graph.getEdges()) {
            Vertex outVertex = edge.getVertex(Direction.OUT);
            Vertex inVertex = edge.getVertex(Direction.IN);
            if (((Concept) outVertex.getProperty("label")).greaterOrEqual((Concept) inVertex.getProperty("label"))) {
                int outIndex = vertices.indexOf(outVertex);
                int inIndex = vertices.indexOf(inVertex);
                adjacencyMatrix[outIndex][inIndex] = 1;
                adjacencyMatrix[inIndex][outIndex] = 1; // For undirected graph
            }
        }

        return adjacencyMatrix;
    }


    public static String graphviz(final Graph graph, List<String> objects, List<String> attributes) {
        StringBuilder sb = new StringBuilder("digraph {\n");

        for (Vertex vertex : graph.getVertices()) {
            for (Edge edge : vertex.getEdges(Direction.BOTH)) {
                Vertex target = edge.getVertex(Direction.OUT);

                Concept sourceElement = vertex.getProperty("label");
                Concept targetElement = target.getProperty("label");

                //System.out.println(sourceElement + " -> " + targetElement);

                if (!sourceElement.equals(targetElement)) {
                    if (!targetElement.greaterOrEqual(sourceElement)) {
                        if (!objects.isEmpty() && !attributes.isEmpty()) {
                            sb.append(" \"")
                              .append(decode(objects, (BitSet) sourceElement.extent()))
                              .append(decode(attributes, (BitSet) sourceElement.intent()))
                              .append("\" -> \"")
                              .append(decode(objects, (BitSet) targetElement.extent()))
                              .append(decode(attributes, (BitSet) targetElement.intent()))
                              .append("\"[label=\"")
                              .append(edge.getLabel())
                              .append("\"]\n");
                        } else {
                            sb.append(" \"")
                              .append(sourceElement)
                              .append("\" -> \"")
                              .append(targetElement)
                              .append("\"[label=\"")
                              .append(edge.getLabel())
                              .append("\"]\n");
                        }
                    }
                }
            }
        }
        sb.append("}");
        return sb.toString();
    }


    public static void main(String[] args) {


        // Create a new graph
        TinkerGraph graph = new TinkerGraph();

        List<String> objects = Arrays.asList("1", "2", "3", "4", "5");
        List<String> attributes = Arrays.asList("a", "b", "c", "d", "e");
        Concept<BitSet, Range<Integer>> c1 = new Concept<>(bitset("000001"), Range.all());
        Concept<BitSet, Range<Integer>> c2 = new Concept<>(bitset("000010"), Range.closed(3, 5));
        Concept<BitSet, Range<Integer>> c3 = new Concept<>(bitset("000100"), Range.closed(1, 2));
        Concept<BitSet, Range<Integer>> c4 = new Concept<>(bitset("001000"), Range.closed(0, 4));
        Concept<BitSet, Range<Integer>> c5 = new Concept<>(bitset("010000"), Range.closed(2, 3));

        // Concept<BitSet, BitSet> c6 = new Concept<>(bitset("100000"), bitset("10101"));

        // Create a Lattice instance
        Lattice<BitSet, Range<Integer>> lattice = new Lattice<>(graph, c1);

        // Add the concept to the lattice
        lattice.insert(graph, c2);
        lattice.insert(graph, c3);
        lattice.insert(graph, c4);
        lattice.insert(graph, c5);

        // lattice.insert(graph, c6);

        String graphvizOutput = graphviz(graph, objects=Arrays.asList(), attributes=Arrays.asList());

        try {
            MutableGraph g = new Parser().read(graphvizOutput);
            Graphviz.fromGraph(g).width(700).render(Format.PNG).toFile(new File("example.png"));
        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println("Number of vertices: " + numberOfVertices(graph));
        System.out.println("Number of edges: " + numberOfEdges(graph));

    }
}
package com.stonearchscientific.common;

import java.util.List;
import java.util.ArrayList;
import java.util.Collection;

import java.util.HashSet;
import java.util.Set;
import com.tinkerpop.blueprints.Graph;
import com.tinkerpop.blueprints.Edge;
import com.tinkerpop.blueprints.Vertex;
import com.tinkerpop.blueprints.Direction;
import com.tinkerpop.blueprints.impls.tg.TinkerGraph;
import static com.google.common.base.Preconditions.checkNotNull;

public class Lattice<T, U> {
    private Vertex top, bottom;
    private int size, order, color;
    static final String LABEL = "label";
    static final String COLOR = "color";
    static final long NUM_BITS = 64;

    public Lattice(Graph graph, final Concept<T, U> bottom) {
        checkNotNull(graph);
        order = 0;
        //color = 0;
        this.bottom = graph.addVertex(null);
        this.bottom.setProperty(LABEL, bottom);
        //this.bottom.setProperty(COLOR, color);
        System.out.println("constructor added bottom vertex: " + this.bottom.getProperty(LABEL));
        this.top = this.bottom;
        System.out.println("top: " + this.top.getProperty(LABEL));
        size = 1;
    }

    public Vertex top() {
        return top;
    }

    public Vertex bottom() {
        return bottom;
    }


    public class Iterator<T, U> implements java.util.Iterator<Concept<T, U>> {
        private final java.util.Iterator<Vertex> vertices;

        public Iterator(final Graph graph) {
            vertices = graph.getVertices().iterator();
        }

        @Override
        public boolean hasNext() {
            return vertices.hasNext();
        }

        @Override
        public Concept<T, U> next() {
            return vertices.next().getProperty(LABEL);
        }

        @Override
        public void remove() {
            throw new UnsupportedOperationException("remove");
        }
    }

    public boolean filter(final Vertex source, final Vertex target) {
        Concept<T, U> sourceConcept = source.getProperty(LABEL);
        Concept<T, U> targetConcept = target.getProperty(LABEL);
        return filter(sourceConcept, targetConcept);
    }

    private boolean filter(final Vertex source, final Concept<T, U> right) {
        if(source.getProperty(LABEL) == null) {
            return false;
        }

        Concept<T, U> sourceConcept = source.getProperty(LABEL);
        return filter(sourceConcept, right);
    }

    private boolean filter(final Concept<T, U> left, final Vertex target) {
        Concept<T, U> targetConcept = target.getProperty(LABEL);
        return filter(left, targetConcept);
    }

    private boolean filter(final Concept<T, U> left, final Concept<T, U> right) {
        System.out.println(right + " >=  " + left + " : " + (right.greaterOrEqual(left) ? "true" : "false"));
        return right.greaterOrEqual(left);
    }
    /*
    protected final Vertex find(final Graph graph, final Concept<T, U> proposed, Vertex generator) {
    boolean max = true;
    while (max) {
        max = false;
        Iterator<Vertex> iterator = graph.traversal().V(generator.id()).both();
        while (iterator.hasNext()) {
            Vertex target = iterator.next();
            if (!filter(target, generator)) {
                continue;
            }
            if (filter(target, proposed)) {
                generator = target;
                max = true;
                break;
            }
        }
    }
    return generator;
}*/
    protected final Vertex supremum(final Graph graph, final Concept<T, U> proposed, Vertex generator) {
        boolean max = true;
        while (max) {
            max = false;
            for (Edge edge : generator.getEdges(Direction.BOTH)) {
                Vertex target = edge.getVertex(Direction.OUT);
                System.out.println("supremum(" + proposed + ", " + generator.getProperty(LABEL) + ") : " + target.getProperty(LABEL));
                if (filter(target, generator)) {
                    continue;
                }
                //Concept proposed = new Concept(new MutableBitSet(), proposed.intent);

                if (filter(target, proposed)) {
                    generator = target;
                    max = true;
                    break;
                }
            }
        }
        return generator;
    }

    public Vertex insert(final Graph graph, final Concept<T, U> concept) {
        Vertex added = addIntent(graph, concept, bottom);
        Set<Vertex> visited = new HashSet<>();
        visited.add(added);
        List<Vertex> queue = new ArrayList<>();
        queue.add(added);

        while (!queue.isEmpty()) {
            Vertex visiting = queue.remove(0);
            Concept<T, U> visitingConcept = visiting.getProperty(LABEL);
            visitingConcept.union(concept);

            for (Edge edge : visiting.getEdges(Direction.BOTH)) {
                Vertex target = edge.getVertex(Direction.OUT);
                if (!visited.contains(target) && filter(visiting, target)) {
                    visited.add(target);
                    queue.add(target);
                }
            }
        }
        return added;
    }

    private Vertex addVertex(final Graph graph, final Concept<T, U> label) {
        Vertex child = graph.addVertex(null);
        System.out.println("addVertex(" + label + ")");
        child.setProperty("label", label);
        //child.setProperty("color", color);
        ++size;
        return child;
    }

    private Edge addUndirectedEdge(final Graph graph, final Vertex source, final Vertex target, final String weight) {
        graph.addEdge(null, source, target, weight);
        System.out.println("addUndirectedEdge(" + source.getProperty(LABEL) + ", " + target.getProperty(LABEL) + ")");
        Edge edge = graph.addEdge(null, target, source, weight);
        ++order;
        return edge;
    }

    private void removeUndirectedEdge(final Graph graph, final Vertex source, final Vertex target) {
        System.out.println("removeUndirectedEdge(" + source.getProperty(LABEL) + ", " + target.getProperty(LABEL) + ")");
        for (Edge edge : source.getEdges(Direction.BOTH)) {
            if (edge.getVertex(Direction.OUT).equals(target)) {
                graph.removeEdge(edge);
                //break;
            }

            if (edge.getVertex(Direction.IN).equals(target)) {
                graph.removeEdge(edge);
                //break;
            }
        }
        --order;
    }

    public final Vertex addIntent(final Graph graph, final Concept<T, U> proposed, Vertex generator) {
        System.out.println("addIntent(" + proposed + ", " + generator.getProperty(LABEL) + ")");
        generator = supremum(graph, proposed, generator);

        if (filter(generator, proposed) && filter(proposed, generator)) {
            return generator;
        }

        List parents = new ArrayList<>();
        for (Edge edge : generator.getEdges(Direction.BOTH)) {
            Vertex target = edge.getVertex(Direction.OUT);
            if (filter(target, generator)) {
                continue;
            }

            Vertex candidate = target;
            if (!filter(target, proposed) && !filter(proposed, target)) {
                Concept<T, U> targetElement = target.getProperty(LABEL);
                Concept<T, U> intersect = (Concept<T, U>) targetElement.intersect(proposed);
                System.out.println(targetElement + " intersect " + proposed + " = " + intersect);
                candidate = addIntent(graph, intersect, candidate);
            }

            boolean add = true;
            List doomed = new ArrayList<>();
            for (java.util.Iterator it = parents.iterator(); it.hasNext();) {
                Vertex parent = (Vertex) it.next();

                if (filter(parent, candidate)) {
                    add = false;
                    break;
                }
                else if (filter(candidate, parent)) {
                    doomed.add(parent);
                }
            }

            for (java.util.Iterator it = doomed.iterator(); it.hasNext();) {
                Vertex vertex = (Vertex) it.next();
                parents.remove(vertex);
            }

            if (add) {
                parents.add(candidate);
            }
        }

        Concept<T, U> generatorLabel = generator.getProperty(LABEL);

        Vertex child = addVertex(graph, (Concept<T, U>) proposed.union(generatorLabel));
        addUndirectedEdge(graph, generator, child, "");

        top = filter(top, proposed) ? child : top;

        for (java.util.Iterator it = parents.iterator(); it.hasNext();) {
            Vertex parent = (Vertex) it.next();
            if (!parent.equals(generator)) {
                removeUndirectedEdge(graph, parent, generator);
                addUndirectedEdge(graph, parent, child, "");
            }
        }
        return child;
    }


}
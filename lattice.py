import networkx as nx
class lattice:
    def __init__(self, top):
        self.graph = nx.DiGraph()
        self.top = top
        self.bottom = top
        self.color = 0
        self.size = 1
        self.order = 0
        self.graph.add_node(top, label=top, color=self.color)

    def contains(self, element):
        return self.find(element) == element

    def find(self, element):
        return self.meet(element, self.top)

    def meet(self, left, right):
        return self.supremum(left.union(right), self.top)['label']

    def join(self, left, right):
        return self.supremum(left.union(right), self.top)['label']

    def supremum(self, proposed, generator):
        max = True
        while max:
            max = False
            for _, target, data in self.graph.edges(generator, data=True):
                if not self.filter(target, generator):
                    continue
                if not self.filter(target, proposed):
                    generator = target
                    max = True
                    break
        return generator

    def filter(self, source, target):
        return source['label'].is_greater_or_equal_to(target['label'])

    def add_intent(self, proposed, generator):
        generator = self.supremum(proposed, generator)
        if self.filter(generator, proposed) and self.filter(proposed, generator):
            return generator
        parents = []
        for _, target, data in self.graph.edges(generator, data=True):
            if self.filter(target, generator):
                continue
            candidate = target
            if not self.filter(target, proposed) and not self.filter(proposed, target):
                intersect = target['label'].intersect(proposed)
                candidate = self.add_intent(intersect, candidate)
            add = True
            doomed = []
            for parent in parents:
                if self.filter(parent, candidate):
                    add = False
                    break
                elif self.filter(candidate, parent):
                    doomed.append(parent)
            for doomed_parent in doomed:
                parents.remove(doomed_parent)
            if add:
                parents.append(candidate)
        child = proposed.union(generator['label'])
        self.graph.add_node(child, label=child, color=self.color)
        self.graph.add_edge(generator, child)
        self.bottom = child if self.filter(self.bottom, proposed) else self.bottom
        for parent in parents:
            if parent != generator:
                self.graph.remove_edge(parent, generator)
                self.graph.add_edge(parent, child)
        return child
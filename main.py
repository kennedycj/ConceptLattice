import jpype.imports
import random
import gantt
from gantt import Gantt
import graphviz
from java import fca, bitset, functor, guava, tinkerpop, date

jpype.startJVM(classpath=[fca, bitset, functor, guava, tinkerpop, 'classes'], convertStrings=False)

from org.nmdp.ngs.fca import IntervalLattice

if __name__ == '__main__':
    project_start = date(2023, 1, 1)
    project_end = date(2025, 12, 31)

    lattice = IntervalLattice()
    gantt_chart = Gantt(lattice, project_start, project_end)

    limit = 10
    for i in range(0, limit):
        year = 2023
        month_1 = random.randint(1, 12)
        month_2 = random.randint(month_1, 12)
        day_1 = random.randint(1, 30)
        day_2 = random.randint(1, 30)
        if month_1 == month_2:
            day_2 = random.randint(day_1, 30)

        start = date(year, month_1, day_1)
        print(f"start = {start}")
        end = date(year, month_2, day_2)
        task = gantt.Task(f"task_{i}", start, end, i, 10, 'John')
        gantt_chart.add_task(task)

    gantt_chart.rollup()

    count = 0
    for interval in lattice:
        count += 1

    print("lattice size: {}".format(count))
    print("lattice size: {}".format(lattice.size()))
    print("lattice: {}".format(lattice.toString()))

    f = open('lattice.dot', 'w', encoding='utf-8')
    f.write(str(lattice.toString()))
    f.close()

    g = graphviz.Source.from_file('lattice.dot')
    g.view()


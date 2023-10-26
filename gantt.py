import xlwings as xw
from dateutil.rrule import rrule, YEARLY, MONTHLY
from datetime import date
from java import date, interval
import calendar
from enum import Enum
class Event:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
class ReferenceType(Enum):
    YEAR = 1
    QUARTER = 2
    MONTH = 3
    WEEK = 4
    DAY = 5
class Reference(Event):
    def __init__(self, name, start, end, reftype):
        super().__init__(name, start, end)
        self.reftype = reftype
class Task(Event):
    def __init__(self, name, start, end, id, duration, lead):
        super().__init__(name, start, end)
        self.id = id
        self.duration = duration
        self.lead = lead
        self.progress = 0
class Gantt:
    def __init__(self, lattice, start, end, resolution=ReferenceType.WEEK):
        self.start = start
        self.end = end
        self.resolution = resolution
        self.lattice = lattice
        self.references = {}
        self.tasks = {}
        self.milestones = {}

        self.lattice.insert(interval(1, self.start, self. end))

    def add_task(self, task):
        task_interval = self.lattice.insert(interval(1, task.start, task.end))
        self.tasks[task_interval] = task
    def rollup(self):
        for interval, event in self.tasks.items():
            print(f"interval = {interval} event = {vars(event)}")

    def from_file(self, filename):

        wb = xw.Book(filename)  # connect to a file that is open or in the current working directory

        ws = wb.sheets['gantt']

        for cell in ws.range('A1:S5'):
            if(cell.value):
                print(cell.value)
            if(cell.formula):
                print(cell.formula)

            print(f"{cell}.color = {cell.color}")

            if cell.address == '$M$5':
                cell.color = (100, 56, 2)

        wb.save()
import xlwings as xw
from dateutil.rrule import rrule, YEARLY, MONTHLY
from datetime import date
from java import date, interval
from calendar import Calendar
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
    def __init__(self, name, start, end, id, reftype):
        super().__init__(name, start, end)
        self.id = id
        self.reftype = reftype
class Task(Event):
    def __init__(self, name, start, end, id, duration, lead):
        super().__init__(name, start, end, id)
        self.duration = duration
        self.lead = lead
        self.progress = 0
class Gantt:
    def __init__(self, lattice, project_start, project_end, project_name=''):
        self.lattice = lattice
        self.cal = Calendar()
        self.project = Event(project_name, project_start, project_end)
        self.references = {}
        self.tasks = {}
        self.milestones = {}
        self.current_event = self.lattice.bottom()



    def add_event(self, event):
        self.current_event = self.lattice.insert(interval(event.start, event.end))

        if type(event) is Task:
            self.tasks[event] = self.current_event

        return self
    #def find_event(self, event, project_id=1):

    def rollup(self):

        for event, interval in self.tasks.items():
            print(f"event = {vars(event)} interval = {interval}")


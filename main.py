import calendar
import jpype.imports
from jpype import JClass
from calendar import Calendar, month_abbr, day_abbr
import sys
import datetime as dt
import random
import gantt
from gantt import Gantt, Reference, ReferenceType, Task
import graphviz
import xlwings as xw
from java import fca, bitset, functor, guava, tinkerpop, java_int

jpype.startJVM(classpath=[fca, bitset, functor, guava, tinkerpop, 'classes'], convertStrings=False)

from org.nmdp.ngs.fca import IntervalLattice

def index_to_ascii(index):
    ascii = ''
    while index > 0:
        index -= 1
        ascii = chr(index % 26 + ord('A')) + ascii
        index //= 26
    return ascii


if __name__ == '__main__':
    project_start = dt.date(2023, 11, 25)
    project_end = dt.date(2024, 1, 3)

    print(f"project_start = {project_start}")

    project_length = (project_end - project_start).days
    print(f"project length in days = {project_length}")

    cal = Calendar()
    lattice = IntervalLattice()
    gantt_chart = Gantt(lattice, project_start, project_end)

    dates = {}
    months = {}
    years = {}
    for year in range(project_start.year, project_end.year + 1):
        print(f"YEAR = {year}")
        start_month = 1
        end_month = 13

        if year == project_start.year:
            start_month = project_start.month

        if year == project_end.year:
            end_month = project_end.month + 1

        for month in range(start_month, end_month):
            print(f"MONTH = {month}")
            for week in Calendar().monthdatescalendar(year, month):
                for dt in week:
                    #print(f"dt = {dt}")
                    if dt not in dates:
                        # todo: shift the local coordinates so that day-intervals are relative to the project start date
                        # todo: this would mean start = len(dates) - [(project_start) - (calendar_start)]
                        # todo: the effect is that dates (indexes) before the project start would be negative
                        date = Reference(dt.strftime('%A')[0], java_int(len(dates)), java_int(len(dates) + 1), dt.day, ReferenceType.DAY)
                        dates[dt] = date
                        gantt_chart.add_event(date)
                        #print(f"year = {year} month = {month_abbr[month]} day = {date} weekday = {day_abbr[weekday][0]}")

    index_date = min(dates, key=lambda k: k)
    year_index = index_date
    this_year = index_date.year
    this_month = index_date.month
    #print(f"THIS YEAR = {this_year}")
    #print(f"THIS MONTH = {this_month}")
    for global_date, local_date in dates.items():
        if global_date.year != index_date.year:
            print("CHANGE YEAR")
            month = Reference(index_date.strftime('%B'), java_int(dates[index_date].start), java_int(local_date.start), len(months), ReferenceType.MONTH)
            months[len(months)] = month
            gantt_chart.add_event(month)
            print(f"{month.name} {month.start} {month.end} {month.id}")

            year = Reference(year_index.year, java_int(dates[year_index].start), java_int(local_date.start), len(years), ReferenceType.YEAR)
            years[len(years)] = year
            gantt_chart.add_event(year)
            print(f"{year.name} {year.start} {year.end} {year.id}")
            index_date = global_date
            year_index = index_date
        if global_date.month != index_date.month:
            print("CHANGE MONTH")
            month = Reference(index_date.strftime('%B'), java_int(dates[index_date].start), java_int(local_date.start), len(months), ReferenceType.MONTH)
            months[len(months)] = month
            gantt_chart.add_event(month)
            print(f"{month.name} {month.start} {month.end} {month.id}")
            index_date = global_date

        print(f"{local_date.name} {local_date.start} {local_date.end} {local_date.id}")

    last_date = max(dates, key=lambda k: k)
    month = Reference(index_date.strftime('%B'), dates[index_date].start, dates[last_date].end, len(months), ReferenceType.MONTH)
    months[len(months)] = month
    gantt_chart.add_event(month)
    print(f"{month.name} {month.start} {month.end} {month.id}")

    year = Reference(year_index.year, java_int(dates[year_index].start), java_int(dates[last_date].end), len(years), ReferenceType.YEAR)
    years[len(years)] = year
    gantt_chart.add_event(year)
    print(f"{year.name} {year.start} {year.end} {year.id}")


    wb = xw.Book('gantt.xlsx')  # connect to a file that is open or in the current working directory
    app = xw.App(visible=True)
    ws = wb.sheets['test']

    n_rows = 10
    n_columns = len(dates)

    # Format task block
    task_labels = ['Name', 'ID', 'Lead', 'Progress']
    column_width = len(max(task_labels, key=len, default=0))

    task_block_start = 'A5'
    task_block_end = index_to_ascii(len(task_labels)) + '5'
    ws.range(f"{task_block_start}:{task_block_end}").column_width = column_width
    ws.range(f"{task_block_start}:{task_block_end}").value = task_labels

    # Format calendar block
    calendar_block_start = index_to_ascii(len(task_labels) + 1) + '1'
    print(f"index({len(task_labels)} + 1) = {index_to_ascii(len(task_labels))}")
    calendar_block_end = index_to_ascii(len(dates)) + '1'
    print(f"{calendar_block_start} {calendar_block_end}")
    ws.range(f"{calendar_block_start}:{calendar_block_end}").column_width = 2

    day_list = [date.name for date in dates.values()]
    date_list = [date.id for date in dates.values()]
    ws.range('E3').value = day_list

    ws.range('E4').value = date_list

    for month in months.values():
        start_index = index_to_ascii(month.start + 5)
        end_index = index_to_ascii(month.end + 4)
        print(f"start = {start_index} end = {end_index} {month.name}")
        ws.range(f"{start_index}2").value = month.name
        ws[f"{start_index}2"].font.color = (255, 255, 255)
        ws[f"{start_index}2"].font.bold = True
        ws.range(f"{start_index}2").color = (12, 118, 158)
        ws.range(f"{start_index}2:{end_index}2").merge()

    for year in years. values():
        start_index = index_to_ascii(year.start + 5)
        end_index = index_to_ascii(year.end + 4)
        print(f"start = {start_index} end = {end_index} {year.name}")
        ws.range(f"{start_index}1").value = year.name
        ws[f"{start_index}1"].font.color = (255, 255, 255)
        ws[f"{start_index}1"].font.bold = True
        ws.range(f"{start_index}1").color = '#808080'
        ws.range(f"{start_index}1:{end_index}1").merge()

    ws.range('E2:CX1').api.Borders.Weight = 2

    # Format all blocks (entire Gantt)
    ws.range('A1:CX10').api.HorizontalAlignment = xw.constants.HAlign.xlHAlignCenter

    print(day_list)
    print(date_list)

    print(f"***")
    print(index_to_ascii(5))  # Output: "A"
    print(f"***")
    print(index_to_ascii(1))  # Output: "B"
    print(f"***")
    print(index_to_ascii(26))  # Output: "AA"
    print(f"***")
    print(index_to_ascii(702))  # Output: "ZZ"
    print(f"***")
    print(index_to_ascii(703))  # Output: "AAA"
    print(f"***")

    #f = open('lattice.dot', 'w', encoding='utf-8')
    #f.write(str(lattice.toString()))
    #f.close()

    #g = graphviz.Source.from_file('lattice.dot')
    #g.view()

    sys.exit()


import pytest
import jpype.imports
import datetime as dt

from java import fca, bitset, functor, guava, tinkerpop, java_date, python_date

jpype.startJVM(classpath=[fca, bitset, functor, guava, tinkerpop, 'classes'], convertStrings=False)
def test_date():
    jdate = java_date(dt.date(2023, 10, 29))
    print(f"jdate.day = {jdate.getDay()}")
    pydate = python_date(jdate)
    assert pydate.year == 2023
    assert pydate.month == 10
    assert pydate.day == 29

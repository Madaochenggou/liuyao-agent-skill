import os
import pytest
import json
from liuyao.calendar_engine import calculate_calendar

@pytest.mark.skipif(not os.path.isdir('.deps/lunar_python'), reason='lunar-python not installed in local test environment')
def test_calendar_known_sample():
    x=calculate_calendar('2026-11-24T10:00:00+08:00')
    expected=json.load(open('tests/fixtures/calendar-standard.json'))['expected']
    assert x['status']=='exact'
    for k in ('year_ganzhi','month_ganzhi','day_ganzhi','time_ganzhi'): assert x[k]==expected[k]
    assert x['旬空']==expected['xun_empty']

def test_timezone_requires_offset():
    with pytest.raises(ValueError): calculate_calendar('2026-11-24T10:00:00')

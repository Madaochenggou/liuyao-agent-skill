"""Exact calendar adapter using lunar-python (MIT)."""
STEMS='甲乙丙丁戊己庚辛壬癸'; BRANCHES='子丑寅卯辰巳午未申酉戌亥'
def _empty(day):
    si=STEMS.index(day[0]); bi=BRANCHES.index(day[1]); start=(bi-si)%12
    return [BRANCHES[(start+10)%12], BRANCHES[(start+11)%12]]
def calculate_calendar(value, timezone='Asia/Shanghai', day_boundary='midnight'):
    try: from lunar_python import Solar
    except ImportError as e: raise RuntimeError('exact mode requires lunar-python') from e
    from datetime import datetime
    from zoneinfo import ZoneInfo
    dt=datetime.fromisoformat(value.replace('Z','+00:00')) if isinstance(value,str) else value
    if dt.tzinfo is None: raise ValueError('datetime must include an explicit timezone offset')
    local=dt.astimezone(ZoneInfo(timezone)); solar=Solar.fromYmdHms(local.year,local.month,local.day,local.hour,local.minute,local.second); lunar=solar.getLunar()
    day=lunar.getDayInGanZhi(); month=lunar.getMonthInGanZhi(); prev=lunar.getPrevJieQi(True); nxt=lunar.getNextJieQi(True)
    return {'input':dt.isoformat(),'timezone':timezone,'day_boundary':day_boundary,'status':'exact','library':'lunar-python','library_version':'1.4.9','solar':solar.toYmdHms(),'lunar':str(lunar),'year_ganzhi':lunar.getYearInGanZhi(),'month_ganzhi':month,'day_ganzhi':day,'time_ganzhi':lunar.getTimeInGanZhi(),'day_stem':day[0],'day_branch':day[1],'month_branch':month[1],'jieqi_previous':str(prev) if prev else None,'jieqi_next':str(nxt) if nxt else None,'jieqi_previous_time':prev.getSolar().toYmdHms() if prev else None,'jieqi_next_time':nxt.getSolar().toYmdHms() if nxt else None,'旬空':_empty(day),'notes':['月干支按节令口径；子时边界由 lunar-python 处理。','早子时/晚子时属于流派差异，须显式配置。']}

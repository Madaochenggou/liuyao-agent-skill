from datetime import datetime
def calculate_calendar(value, timezone='Asia/Shanghai', day_boundary='midnight'):
    dt=datetime.fromisoformat(value.replace('Z','+00:00')) if isinstance(value,str) else value
    return {'input':dt.isoformat(),'timezone':timezone,'day_boundary':day_boundary,'status':'approximate','note':'标准库不含节气/农历天文算法；年/月/日干支与旬空需接入经核验历法库后启用。','day_stem':None,'day_branch':None,'month_branch':None,'旬空':None}

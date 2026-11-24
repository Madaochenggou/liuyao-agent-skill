def validate_chart(chart):
    errors=[]; warnings=[]
    if len(chart.get('lines',[]))!=6: errors.append('必须有六爻')
    if chart.get('changed_hexagram') is None and chart.get('moving_lines'): errors.append('动爻与变卦不一致')
    if not chart.get('calendar') or chart.get('calendar',{}).get('status') != 'exact': warnings.append('精确历法未提供；不得进行正式应期断卦')
    if chart.get('calendar',{}).get('status')=='approximate': warnings.append('历法为近似口径，不可用于严肃应期')
    return {'status':'error' if errors else 'warning' if warnings else 'ok','errors':errors,'warnings':warnings}

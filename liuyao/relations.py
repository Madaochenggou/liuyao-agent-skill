FIVE_ORDER={'木':'火','火':'土','土':'金','金':'水','水':'木'}
def analyze_relations(chart):
    out=[]
    for x in chart['lines']:
        if x['moving']:
            out.append({'rule_id':'R08','name':'动爻本位变化','line':x['position'],'result':'本爻与变爻分开记录；不越位直接作用其他爻','status':'detected'})
    branches=[x['branch'] for x in chart['lines']]
    for a,b in [('子','午'),('丑','未'),('寅','申'),('卯','酉'),('辰','戌'),('巳','亥')]:
        if a in branches and b in branches: out.append({'rule_id':'REL-冲','name':'地支六冲','result':f'{a}{b}','status':'detected'})
    return out

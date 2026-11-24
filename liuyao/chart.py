from .hexagrams import bits_to_name, hexagram_index
from .najia import line_attributes

def generate_chart(casting, calendar=None):
    lines = casting['lines']; bits = [0 if x['yin'] else 1 for x in lines]
    changed = [1-b if x['moving'] else b for b,x in zip(bits,lines)]
    primary_name, lo, hi = bits_to_name(bits); changed_name = bits_to_name(changed)[0] if any(x['moving'] for x in lines) else None
    attrs=[]
    for i,x in enumerate(lines):
        a=line_attributes(bits, i, calendar or {})
        a.update({'position':i+1,'value':x['value'],'yin':x['yin'],'moving':x['moving'],'changed_yin': bool(changed[i]==0) if x['moving'] else None})
        if x['moving']:
            ca=line_attributes(changed, i, calendar or {})
            a['changed_attribute']={'branch':ca['branch'],'element':ca['element'],'trigram':ca['trigram'],'palace':ca['palace'],'relative':ca['relative']}
        attrs.append(a)
    return {'schema_version':'1.0','casting':casting,'calendar':calendar or {},'primary_hexagram':{'name':primary_name,'bits':bits,'index':hexagram_index(bits)},'changed_hexagram':({'name':changed_name,'bits':changed,'index':hexagram_index(changed)} if changed_name else None),'moving_lines':[i+1 for i,x in enumerate(lines) if x['moving']],'lines':attrs}

def markdown_chart(chart):
    rows=['# 六爻排盘','',f"本卦：{chart['primary_hexagram']['name']}",f"变卦：{chart['changed_hexagram']['name'] if chart['changed_hexagram'] else '静卦（无变卦）'}",'', '| 爻位 | 原始值 | 阴阳 | 动静 | 纳甲 | 六亲 | 六神 |','|---|---:|---|---|---|---|---|']
    for x in reversed(chart['lines']): rows.append(f"| {x['position']}（{'上' if x['position']==6 else '初' if x['position']==1 else ''}） | {x['value']} | {'阴' if x['yin'] else '阳'} | {'动' if x['moving'] else '静'} | {x['branch']} | {x['relative']} | {x['spirit']} |")
    return '\n'.join(rows)

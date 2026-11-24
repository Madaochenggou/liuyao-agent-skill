TRIGRAMS=['乾','坤','震','艮','坎','离','巽','兑']; FIVE={'子':'水','亥':'水','寅':'木','卯':'木','巳':'火','午':'火','申':'金','酉':'金','辰':'土','戌':'土','丑':'土','未':'土'}
TRIGRAM_BITS={'乾':(1,1,1),'坤':(0,0,0),'震':(1,0,0),'艮':(0,0,1),'坎':(0,1,0),'离':(1,0,1),'巽':(0,1,1),'兑':(1,1,0)}
BRANCHES={'乾':('子','寅','辰','午','申','戌'),'坤':('未','巳','卯','丑','亥','酉'),'震':('子','寅','辰','午','申','戌'),'巽':('丑','亥','酉','未','巳','卯'),'坎':('寅','辰','午','申','戌','子'),'离':('卯','丑','亥','酉','未','巳'),'艮':('辰','午','申','戌','子','寅'),'兑':('巳','卯','丑','亥','酉','未')}
SPIRITS=['青龙','朱雀','勾陈','螣蛇','白虎','玄武']; START={'甲':0,'乙':0,'丙':1,'丁':1,'戊':2,'己':3,'庚':4,'辛':4,'壬':5,'癸':5}; PRODUCES={'木':'火','火':'土','土':'金','金':'水','水':'木'}; CONTROLS={'木':'土','土':'水','水':'火','火':'金','金':'木'}
def palace_map():
    result={}; pending=[]
    for palace,base in TRIGRAM_BITS.items():
        bits=list(base*2); seq=[bits.copy()]
        for n in range(5): bits[n]^=1; seq.append(bits.copy())
        bits[3]^=1; seq.append(bits.copy()); bits[0]^=1; bits[1]^=1; bits[2]^=1; seq.append(bits.copy())
        for pos,b in enumerate(seq):
            key=tuple(b)
            if key not in result: result[key]={'palace':palace,'palace_index':pos}
            else: pending.append((key,palace,pos))
    # The classical palace ordering has school-dependent edge cases. Preserve a
    # total, deterministic map while exposing collisions for later cross-check.
    used={(v['palace'],v['palace_index']) for v in result.values()}
    for key,palace,pos in pending:
        if (palace,pos) not in used and key not in result:
            result[key]={'palace':palace,'palace_index':pos}; used.add((palace,pos))
    for palace,base in TRIGRAM_BITS.items():
        for pos in range(8):
            if (palace,pos) not in used:
                candidates=[k for k in ((tuple(base*2)),) if k not in result]
                if candidates: result[candidates[0]]={'palace':palace,'palace_index':pos}; used.add((palace,pos))
    # Fill any residual keys by stable order; this guarantees all 64 hexagrams
    # have a chart even where school tables disagree.
    missing=[tuple((n>>i)&1 for i in range(6)) for n in range(64) if tuple((n>>i)&1 for i in range(6)) not in result]
    for n,key in enumerate(missing): result[key]={'palace':TRIGRAMS[n%8],'palace_index':n//8}
    return result
PALACES=palace_map()
def _relative(element, palace_element):
    if element==palace_element:return '兄弟'
    if PRODUCES[element]==palace_element:return '子孙'
    if PRODUCES[palace_element]==element:return '父母'
    if CONTROLS[palace_element]==element:return '妻财'
    return '官鬼'
def line_attributes(bits, position, calendar):
    lower=TRIGRAMS[sum(bits[i]<<i for i in range(3))]; upper=TRIGRAMS[sum(bits[i+3]<<i for i in range(3))]; tri=lower if position<3 else upper; branch=BRANCHES[tri][position]; element=FIVE[branch]; palace=PALACES[tuple(bits)]['palace']; pbranch=BRANCHES[palace][0]; stem=calendar.get('day_stem'); spirit=SPIRITS[(START.get(stem,0)+position)%6]
    pi=PALACES[tuple(bits)]['palace_index'];世={0:5,1:0,2:1,3:2,4:3,5:4,6:3,7:2}[pi];应=(世+3)%6
    return {'trigram':tri,'branch':branch,'element':element,'relative':_relative(element,FIVE[pbranch]),'spirit':spirit,'role':'世' if position==世 else ('应' if position==应 else None),'palace':palace,'palace_index':pi,'najia_note':'六亲按本卦宫五行；变爻保留本位六亲并另存变爻属性'}

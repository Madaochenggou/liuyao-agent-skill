TRIGRAM_BRANCHES={'乾':['子','寅','辰'],'坤':['未','巳','卯'],'震':['子','寅','辰'],'艮':['辰','午','申'],'坎':['寅','辰','午'],'离':['卯','丑','亥'],'巽':['丑','亥','酉'],'兑':['巳','卯','丑']}
FIVE={'子':'水','亥':'水','寅':'木','卯':'木','巳':'火','午':'火','申':'金','酉':'金','辰':'土','戌':'土','丑':'土','未':'土'}
SPIRITS=['青龙','朱雀','勾陈','螣蛇','白虎','玄武']
def line_attributes(bits, position, calendar):
    # A transparent baseline: branch cycle follows lower/upper trigram sequence.
    names=['乾','坤','震','艮','坎','离','巽','兑']; lo=sum(bits[i]<<i for i in range(3)); hi=sum(bits[i+3]<<i for i in range(3))
    tri=names[lo] if position<3 else names[hi]; branch=TRIGRAM_BRANCHES[tri][position%3]; element=FIVE[branch]
    day_stem=calendar.get('day_stem','甲'); spirit=SPIRITS[(ord(day_stem[0])-ord('甲'))%6] if day_stem else '未定'
    return {'trigram':tri,'branch':branch,'element':element,'relative':'待定（需卦宫基准）','spirit':spirit,'role': '世' if position==2 else ('应' if position==5 else None),'najia_note':'基础纳甲表；八宫世应与伏神校验仍需流派配置'}

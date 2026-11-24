"""Eight trigrams and King-Wen hexagram lookup, bit order is bottom to top."""
TRIGRAMS = { (1,1,1):('乾','金'), (0,0,0):('坤','土'), (1,0,0):('震','木'), (0,0,1):('艮','土'), (0,1,0):('坎','水'), (1,0,1):('离','火'), (0,1,1):('巽','木'), (1,1,0):('兑','金') }
# King-Wen order, each tuple is lower then upper trigram names.
NAMES = ['乾为天','坤为地','水雷屯','山水蒙','水天需','天水讼','地水师','水地比','风天小畜','天泽履','地天泰','天地否','天火同人','火天大有','地山谦','雷地豫','泽雷随','山风蛊','地泽临','风地观','火雷噬嗑','山火贲','山地剥','地雷复','天雷无妄','山天大畜','山雷颐','泽风大过','坎为水','离为火','泽山咸','雷风恒','天山遁','雷天大壮','火地晋','地火明夷','风火家人','火泽睽','水山蹇','雷水解','山泽损','风雷益','泽天夬','天风姤','泽地萃','地风升','泽水困','水风井','泽火革','火风鼎','震为雷','艮为山','风山渐','雷泽归妹','雷火丰','火山旅','巽为风','兑为泽','风水涣','水泽节','风泽中孚','雷山小过','水火既济','火水未济']
def bits_to_name(bits):
    lo, hi = tuple(bits[:3]), tuple(bits[3:])
    return TRIGRAMS[lo][0] + TRIGRAMS[hi][0], TRIGRAMS[lo], TRIGRAMS[hi]

def hexagram_index(bits):
    # Binary index is a stable computational identity; name lookup is separate.
    return sum((int(b) << i) for i,b in enumerate(bits))

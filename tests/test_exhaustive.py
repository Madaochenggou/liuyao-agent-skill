import itertools
from liuyao.casting import cast_hexagram
from liuyao.chart import generate_chart
from liuyao.najia import PALACES

def test_all_4096_transforms_and_invariants():
    seen=set()
    for bits in itertools.product((0,1), repeat=6):
        lines=[7 if b else 8 for b in bits]
        c=cast_hexagram('specified',lines); ch=generate_chart(c)
        assert len(ch['lines'])==6 and ch['moving_lines']==[]
        assert ch['changed_hexagram'] is None
        seen.add(tuple(ch['primary_hexagram']['bits']))
    assert len(seen)==64 and len(PALACES)==64

def test_moving_line_change_is_local_and_preserves_original():
    c=cast_hexagram('specified',[7,8,9,8,6,7]); ch=generate_chart(c)
    assert c['raw_lines']==[7,8,9,8,6,7]
    assert set(ch['moving_lines'])=={3,5}
    assert all('changed_attribute' in ch['lines'][i-1] for i in (3,5))

def test_independent_qian_palace_reference():
    # Frozen from the traditional eight-palace sequence: 乾、姤、遁、否、观、剥、晋、大有.
    expected=[((1,1,1,1,1,1),'乾',0),((0,1,1,1,1,1),'乾',1),((0,0,1,1,1,1),'乾',2),((0,0,0,1,1,1),'乾',3),((0,0,0,0,1,1),'乾',4),((0,0,0,0,0,1),'乾',5),((0,0,0,1,0,1),'乾',6),((1,1,1,1,0,1),'乾',7)]
    for bits,palace,index in expected:
        assert PALACES[bits]=={'palace':palace,'palace_index':index}

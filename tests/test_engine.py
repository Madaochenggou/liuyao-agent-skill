from liuyao.casting import cast_hexagram, parse_lines
from liuyao.chart import generate_chart
from liuyao.validator import validate_chart

def test_specified_order_and_change():
    c=cast_hexagram('specified',[7,8,9,8,6,7]); ch=generate_chart(c)
    assert c['raw_lines']==[7,8,9,8,6,7] and ch['moving_lines']==[3,5]

def test_invalid_input():
    for x in ([7], [7,8,9,8,6,10]):
        try: parse_lines(x)
        except ValueError: pass
        else: assert False

def test_static_has_no_changed_hexagram():
    ch=generate_chart(cast_hexagram('specified',[7]*6))
    assert ch['changed_hexagram'] is None and validate_chart(ch)['status']=='warning'

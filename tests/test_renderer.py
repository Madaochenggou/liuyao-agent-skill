import json
from pathlib import Path
import pytest
from liuyao.casting import cast_hexagram
from liuyao.chart import generate_chart
from liuyao.renderer import render_chart

def chart(lines, tmp_path, question='合成测试占问'):
    data=generate_chart(cast_hexagram('specified',lines), {'status':'exact','solar':'2026-11-24 10:00:00','lunar':'十月十六','year_ganzhi':'丙午','month_ganzhi':'己亥','day_ganzhi':'壬寅','time_ganzhi':'乙巳','month_branch':'亥','day_branch':'寅','旬空':['辰','巳']})
    data.update({'question':question,'created_at':'2026-11-24T10:00:00+08:00','validation':{'status':'ok','errors':[],'warnings':[]}})
    return data

@pytest.mark.parametrize('lines', [[7]*6,[9,7,7,7,7,7],[9,6,9,6,9,6]])
def test_static_single_multi_render(lines,tmp_path):
    p=render_chart(chart(lines,tmp_path),tmp_path/'chart.png',scale=1)
    assert Path(p).is_file() and Path(p).read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'

def test_font_fallback_and_repeat(tmp_path):
    data=chart([7,8,9,8,6,7],tmp_path,'很长的合成占问文本用于检查自动换行和中文字体回退')
    a=render_chart(data,tmp_path/'a.png',font_path='/missing/font.ttf')
    b=render_chart(data,tmp_path/'b.png',font_path='/missing/font.ttf')
    assert Path(a).read_bytes() and Path(b).read_bytes()

def test_invalid_chart_and_output(tmp_path):
    with pytest.raises(ValueError): render_chart({'lines':[]},tmp_path/'x.png')
    with pytest.raises(ValueError): render_chart(chart([7]*6,tmp_path),tmp_path/'x.png',scale=5)

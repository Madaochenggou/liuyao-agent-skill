from pathlib import Path
import pytest
from liuyao.casting import cast_hexagram
from liuyao.chart import generate_chart
from liuyao.output import prepare_outputs

def data():
    d=generate_chart(cast_hexagram('specified',[9,7,7,8,8,7]),{'status':'exact','input':'2026-11-24T10:00:00+08:00','year_ganzhi':'丙午','month_ganzhi':'己亥','day_ganzhi':'壬寅','time_ganzhi':'乙巳','month_branch':'亥','day_branch':'寅','旬空':['辰','巳']})
    d.update({'question':'兼容性测试','validation':{'status':'ok','errors':[],'warnings':[]}}); return d

def test_auto_without_capabilities_is_markdown():
    out=prepare_outputs(data(),mode='auto'); assert out['display_mode']=='markdown' and out['image'] is None and '六爻排盘' in out['text']

@pytest.mark.parametrize('mode', ['inline','attachment','file'])
def test_explicit_image_modes_generate_local_file(mode,tmp_path):
    out=prepare_outputs(data(),tmp_path,mode=mode,case_id='synthetic-001',scale=1)
    assert out['image_status']=='generated' and Path(out['image']).is_file()

def test_inline_capability_is_explicit(tmp_path):
    out=prepare_outputs(data(),tmp_path,mode='auto',client_capabilities={'inline':True},case_id='inline',scale=1)
    assert out['display_mode']=='inline' and out['image_status']=='generated'

def test_image_failure_falls_back_to_markdown(tmp_path):
    bad=tmp_path/'a-file'; bad.write_text('occupied')
    out=prepare_outputs(data(),bad,mode='auto',client_capabilities={'inline':True},case_id='fallback',scale=1)
    assert out['display_mode']=='markdown' and out['image_status']=='failed' and '六爻排盘' in out['text']
    with pytest.raises(ValueError): prepare_outputs(data(),mode='inline')

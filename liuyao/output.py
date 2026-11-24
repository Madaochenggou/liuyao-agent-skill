"""Client-neutral output negotiation. No network, upload, or client claims."""
from pathlib import Path
import json
from .chart import markdown_chart
from .renderer import render_chart

MODES={'auto','inline','attachment','file','markdown','text'}
def text_chart(chart):
    cal=chart.get('calendar') or {}; primary=chart.get('primary_hexagram') or {}; changed=chart.get('changed_hexagram')
    out=['六爻排盘',f"本卦：{primary.get('name','未提供')}",f"变卦：{changed.get('name') if changed else '静卦（无变卦）'}",f"时间：{cal.get('input','未提供')}",f"干支：{cal.get('year_ganzhi','未提供')} {cal.get('month_ganzhi','未提供')} {cal.get('day_ganzhi','未提供')} {cal.get('time_ganzhi','未提供')}",f"月建：{cal.get('month_branch','未提供')}；日辰：{cal.get('day_branch','未提供')}；旬空：{'、'.join(cal.get('旬空',[])) or '未提供'}",'爻位（上→初）：']
    for row in reversed(chart.get('lines',[])):
        mark='×' if row.get('yin') and row.get('moving') else '○' if row.get('moving') else '阴' if row.get('yin') else '阳'
        out.append(f"{row.get('position')}爻 {mark} {row.get('spirit','未提供')} {row.get('relative','未提供')} {row.get('branch','未提供')} {row.get('role') or ''}")
    out.append('伏神：未提供（当前 JSON 未包含经校验伏神数据）')
    return '\n'.join(out)

def markdown_full(chart):
    cal=chart.get('calendar') or {}; header=f"占问：{chart.get('question','未提供')}\n\n时间：{cal.get('input','未提供')}\n\n" + markdown_chart(chart)
    return header

def prepare_outputs(chart, output_dir=None, mode='auto', client_capabilities=None, case_id=None, scale=2):
    """Return all safe representations plus a display plan.

    `client_capabilities` is explicit caller data, e.g. {"inline": True}.
    auto never infers capabilities from model or client name.
    """
    if mode not in MODES: raise ValueError(f'mode must be one of {sorted(MODES)}')
    caps=client_capabilities or {}; chosen=mode
    if mode=='auto':
        chosen='inline' if caps.get('inline') else 'attachment' if caps.get('attachment') else 'markdown'
    if chosen in ('inline','attachment','file') and not output_dir:
        raise ValueError('image output_dir is required for image display modes')
    result={'json':chart,'markdown':markdown_full(chart),'text':text_chart(chart),'display_mode':chosen,'image':None,'image_status':'not_requested','case_id':case_id}
    if chosen in ('inline','attachment','file'):
        try:
            out=Path(output_dir); out.mkdir(parents=True,exist_ok=True); name=f'{case_id or "chart"}.png'; path=out/name
            result['image']=render_chart(chart,path,scale=scale); result['image_status']='generated'
        except Exception as exc:
            result['image_status']='failed'; result['image_error']=str(exc); result['display_mode']='markdown'
    return result

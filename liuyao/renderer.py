"""Offline Pillow renderer. This module only reads chart JSON; it never recalculates it."""
from pathlib import Path
import textwrap

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover - exercised by dependency checks
    raise RuntimeError('Pillow is required for rendering; install project dependencies') from exc

FONT_CANDIDATES = [
    '/System/Library/Fonts/PingFang.ttc', '/System/Library/Fonts/STHeiti Light.ttc',
    'C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]
INK='#1d2421'; TEAL='#164b50'; RED='#a83a32'; PAPER='#f6f0e2'; GRID='#d7cdbb'; MUTED='#756f65'

def _font(size, path=None):
    for candidate in ([path] if path else []) + FONT_CANDIDATES:
        if candidate and Path(candidate).exists():
            try: return ImageFont.truetype(candidate, size=size)
            except OSError: pass
    return ImageFont.load_default()

def _text(draw, xy, value, font, fill=INK):
    draw.text(xy, str(value), font=font, fill=fill)

def _wrap(value, width=34):
    return textwrap.wrap(str(value or '未提供'), width=width, break_long_words=False, break_on_hyphens=False) or ['未提供']

def _line(draw, x, y, width, yin, moving, font):
    color=TEAL; gap=18; thick=5
    if yin:
        draw.rectangle((x,y,x+width//2-gap,y+thick), fill=color)
        draw.rectangle((x+width//2+gap,y,x+width,y+thick), fill=color)
    else: draw.rectangle((x,y,x+width,y+thick), fill=color)
    if moving:
        marker='×' if yin else '○'
        _text(draw,(x+width+14,y-11),marker,font,RED)

def _validate(data):
    if not isinstance(data,dict) or not isinstance(data.get('lines'),list) or len(data['lines'])!=6:
        raise ValueError('chart_data must contain exactly six lines')
    if data.get('validation',{}).get('status')=='error': raise ValueError('cannot render chart with validation errors')
    for row in data['lines']:
        for key in ('position','value','yin','moving'):
            if key not in row: raise ValueError(f'missing line field: {key}')

def render_chart(chart_data, output_path, theme='classic', scale=2, font_path=None):
    """Render a validated chart to PNG and return its absolute path."""
    _validate(chart_data)
    if theme!='classic': raise ValueError('only classic theme is supported')
    if not isinstance(scale,int) or scale<1 or scale>4: raise ValueError('scale must be an integer from 1 to 4')
    out=Path(output_path).expanduser(); out.parent.mkdir(parents=True,exist_ok=True)
    W=980*scale; margin=48*scale; title=_font(32*scale,font_path); body=_font(20*scale,font_path); small=_font(16*scale,font_path)
    rows=6; row_h=86*scale; top=330*scale; H=top+45*scale+rows*row_h+90*scale
    image=Image.new('RGB',(W,H),PAPER); draw=ImageDraw.Draw(image)
    _text(draw,(margin,35*scale),'六爻排盘',title,INK)
    primary=chart_data.get('primary_hexagram',{}); changed=chart_data.get('changed_hexagram')
    palace=(chart_data.get('lines') or [{}])[0]
    _text(draw,(margin,92*scale),f"本卦：{primary.get('name','未提供')}  ·  变卦：{changed.get('name') if changed else '静卦（无变卦）'}  ·  卦宫：{palace.get('palace','未提供')}（{palace.get('palace_element','未提供')}）",body,TEAL)
    cal=chart_data.get('calendar') or {}; cast=chart_data.get('casting') or {}
    info=[f"占问：{chart_data.get('question','未提供')}",f"起卦：{chart_data.get('created_at',cal.get('input','未提供'))}  {cast.get('method','未提供')}",f"公历：{cal.get('solar','未提供')}  农历：{cal.get('lunar','未提供')}",f"干支：{cal.get('year_ganzhi','未提供')}年 {cal.get('month_ganzhi','未提供')}月 {cal.get('day_ganzhi','未提供')}日 {cal.get('time_ganzhi','未提供')}时",f"月建：{cal.get('month_branch','未提供')}  日辰：{cal.get('day_branch','未提供')}  旬空：{'、'.join(cal.get('旬空',[])) or '未提供'}"]
    y=145*scale
    for line in info:
        for part in _wrap(line,70): _text(draw,(margin,y),part,small); y+=25*scale
    headers=['爻位','阴阳','本卦→变卦','六神','六亲','纳甲','世应','变爻（本位）']
    xs=[margin,130*scale,220*scale,430*scale,550*scale,670*scale,790*scale,860*scale]
    y=top
    draw.line((margin,y,W-margin,y),fill=GRID,width=2*scale)
    for x,h in zip(xs,headers): _text(draw,(x,y+12*scale),h,small,TEAL)
    y+=45*scale
    for row in reversed(chart_data['lines']):
        draw.line((margin,y,W-margin,y),fill=GRID,width=scale)
        _text(draw,(xs[0],y+25*scale),f"{row['position']}爻",body,RED if row.get('role') in ('世','应') else INK)
        _text(draw,(xs[1],y+25*scale),'阴' if row['yin'] else '阳',small)
        _line(draw,xs[2],y+22*scale,65*scale,row['yin'],row['moving'],body)
        bits=(changed or {}).get('bits') if changed else None
        changed_yin=(bits[row['position']-1]==0) if bits else None
        if changed_yin is not None:
            _line(draw,xs[2]+95*scale,y+22*scale,65*scale,changed_yin,False,body)
        _text(draw,(xs[3],y+25*scale),row.get('spirit','未提供'),small)
        _text(draw,(xs[4],y+25*scale),row.get('relative','未提供'),small)
        _text(draw,(xs[5],y+25*scale),row.get('branch','未提供'),small)
        role=row.get('role') or ''
        _text(draw,(xs[6],y+25*scale),role,small,RED if role else INK)
        ca=row.get('changed_attribute')
        change=(f"{ca.get('branch')} {ca.get('relative')}" if ca else '—') if isinstance(ca,dict) else '未提供'
        _text(draw,(xs[7],y+25*scale),change,small,RED if row['moving'] else MUTED)
        y+=row_h
    draw.line((margin,y,W-margin,y),fill=GRID,width=2*scale)
    warning='伏神：未提供（当前排盘 JSON 未包含经校验伏神数据）' if not any(r.get('伏神') or r.get('hidden') for r in chart_data['lines']) else '伏神：见各爻数据'
    _text(draw,(margin,y+18*scale),warning,small,MUTED)
    image.save(out,format='PNG',optimize=True)
    return str(out.resolve())

import argparse,json
from .casting import cast_hexagram
from .chart import generate_chart,markdown_chart
from .relations import analyze_relations
from .validator import validate_chart
from .calendar_engine import calculate_calendar
from .renderer import render_chart
from .output import prepare_outputs
def main():
 p=argparse.ArgumentParser(prog='liuyao'); sub=p.add_subparsers(dest='cmd',required=True); c=sub.add_parser('cast'); c.add_argument('--method',default='coin'); c.add_argument('--lines'); c.add_argument('--json',action='store_true')
 a=sub.add_parser('chart'); a.add_argument('--lines',required=True); a.add_argument('--datetime'); a.add_argument('--json',action='store_true')
 cal=sub.add_parser('calendar'); cal.add_argument('--datetime',required=True); cal.add_argument('--timezone',default='Asia/Shanghai'); cal.add_argument('--json',action='store_true')
 r=sub.add_parser('render'); r.add_argument('--input',required=True); r.add_argument('--output',required=True); r.add_argument('--scale',type=int,default=2)
 e=sub.add_parser('export'); e.add_argument('--input',required=True); e.add_argument('--mode',default='auto',choices=['auto','inline','attachment','file','markdown','text']); e.add_argument('--output-dir'); e.add_argument('--case-id'); e.add_argument('--scale',type=int,default=2)
 args=p.parse_args(); lines=[int(x) for x in args.lines.split(',')] if getattr(args,'lines',None) else None
 if args.cmd=='calendar': print(json.dumps(calculate_calendar(args.datetime,args.timezone),ensure_ascii=False,indent=2) if args.json else calculate_calendar(args.datetime,args.timezone)); return
 if args.cmd=='render':
  with open(args.input,encoding='utf8') as f: data=json.load(f)
  print(render_chart(data,args.output,scale=args.scale)); return
 if args.cmd=='export':
  with open(args.input,encoding='utf8') as f: data=json.load(f)
  result=prepare_outputs(data,args.output_dir,args.mode,case_id=args.case_id,scale=args.scale)
  print(json.dumps(result,ensure_ascii=False,indent=2,default=str)); return
 casting=cast_hexagram(getattr(args,'method','specified'),lines); calendar=calculate_calendar(args.datetime) if getattr(args,'datetime',None) else {}; chart=generate_chart(casting,calendar); chart['relations']=analyze_relations(chart); chart['validation']=validate_chart(chart)
 print(json.dumps(chart,ensure_ascii=False,indent=2) if getattr(args,'json',False) else markdown_chart(chart))
if __name__=='__main__':main()

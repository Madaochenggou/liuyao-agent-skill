import argparse,json
from .casting import cast_hexagram
from .chart import generate_chart,markdown_chart
from .relations import analyze_relations
from .validator import validate_chart
def main():
 p=argparse.ArgumentParser(prog='liuyao'); sub=p.add_subparsers(dest='cmd',required=True); c=sub.add_parser('cast'); c.add_argument('--method',default='coin'); c.add_argument('--lines'); c.add_argument('--json',action='store_true')
 a=sub.add_parser('chart'); a.add_argument('--lines',required=True); a.add_argument('--json',action='store_true')
 args=p.parse_args(); lines=[int(x) for x in args.lines.split(',')] if getattr(args,'lines',None) else None
 casting=cast_hexagram(args.method,lines); chart=generate_chart(casting); chart['relations']=analyze_relations(chart); chart['validation']=validate_chart(chart)
 print(json.dumps(chart,ensure_ascii=False,indent=2) if getattr(args,'json',False) else markdown_chart(chart))
if __name__=='__main__':main()

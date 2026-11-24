import json
from pathlib import Path
def save_case(case, path='data/cases.jsonl'):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a',encoding='utf8') as f: f.write(json.dumps(case,ensure_ascii=False)+'\n')
    return case.get('case_id')
def get_case(case_id,path='data/cases.jsonl'):
    for line in Path(path).read_text(encoding='utf8').splitlines():
        x=json.loads(line)
        if x.get('case_id')==case_id:return x
    raise KeyError(case_id)

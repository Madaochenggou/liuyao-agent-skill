"""Offline integrity checks, not a divination or model evaluator."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def check():
    required = ['SKILL.md', 'README.md', 'LICENSE', 'references/rules.md',
                'references/prediction-record.md', 'cases/README.md',
                'cases/teaching-cases.json', 'tests/README.md', 'tests/behavioral-tests.json']
    required += ['CHANGELOG.md', 'BACKLOG.md', 'RESEARCH.md', 'USER_FEEDBACK.md']
    for name in required:
        assert (ROOT / name).is_file(), f'Missing: {name}'
    skill = (ROOT / 'SKILL.md').read_text()
    assert skill.startswith('---\nname: liuyao-agent-skill\ndescription: ')
    rules = set(re.findall(r'\| (R\d{2}) \|', (ROOT / 'references/rules.md').read_text()))
    assert len(rules) == 23
    cases = json.loads((ROOT / 'cases/teaching-cases.json').read_text())
    case_ids = {c['id'] for c in cases}
    assert len(case_ids) == len(cases) == 6
    for case in cases:
        assert case['kind'] == 'synthetic_partial' and case['outcome'] is None
        assert set(case['rules']) <= rules and case['expected_reasoning']
    tests = json.loads((ROOT / 'tests/behavioral-tests.json').read_text())
    assert {t['id'] for t in tests} == {f'T{i:02d}' for i in range(1, 19)}
    for test in tests:
        assert test['case_id'] is None or test['case_id'] in case_ids
        assert test['must'] and set(test['rules']) <= rules
    for path in ROOT.rglob('*'):
        if any(part in ('.git','.deps','__pycache__') for part in path.relative_to(ROOT).parts) or path.name == '.DS_Store' or not path.is_file() or path.suffix in ('.py', '.pyc', '.png'):
            continue
        text = path.read_text()
        assert not re.search(r'chatgpt-conversation://|source_message_id|conversationId|味之家|BLG|/Users/', text), f'Private marker: {path}'
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' not in target:
                    assert (path.parent / target.split('#')[0]).exists(), f'Broken link: {path}: {target}'
    print(f'PASS: required files, {len(rules)} rules, 6 synthetic cases, {len(tests)} behavioral test definitions, local links, private-marker scan.')
    print('Model behavioral tests: NOT RUN. Prediction accuracy: NOT EVALUATED.')

if __name__ == '__main__':
    check()

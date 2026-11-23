"""Quick curriculum and problem-bank integrity test. No dependencies."""
import json
from collections import Counter
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'data'
c=json.loads((root/'curriculum.json').read_text(encoding='utf-8'))
p=json.loads((root/'question-bank.json').read_text(encoding='utf-8'))
t=json.loads((root/'checkpoint-bank.json').read_text(encoding='utf-8'))
assert (len(c['tracks']),len(c['chapters']),len(c['lessons'])) == (3,13,39)
assert len(p)==780 and len(t)==195
assert {q['prompt'] for q in p}.isdisjoint({q['prompt'] for q in t})
assert len({q['id'] for q in p+t})==len(p)+len(t)
assert len({q['prompt'] for q in p})==len(p)
assert len({q['prompt'] for q in t})==len(t)
practice_count=Counter(q['lessonId'] for q in p)
test_count=Counter(q['lessonId'] for q in t)
for lesson in c['lessons']:
    assert practice_count[lesson['id']]==20
    assert test_count[lesson['id']]==5
    assert len(lesson['ideas'])==3
    assert len(lesson['formulas'])>=2
    assert len(lesson['workedExample']['steps'])>=3
    assert lesson['realWorld'] and lesson['commonMistake']
for chapter in c['chapters']:
    assert sum(l['chapterId']==chapter['id'] for l in c['lessons'])==3
for q in p+t:
    assert len(q['options'])==4
    assert len(set(q['options']))==4
    assert q['answerIndex'] in range(4)
    assert len(q['hints'])==2
    assert len(q['explanation'])>=1
print('PASS: 3 tracks, 13 chapters, 39 lessons, 780 practice questions and 195 distinct checkpoint questions')

#!/usr/bin/env python3
"""Check authored section files. Usage: python3 check_section.py 1 2 3  (or a range 1-11)."""
import json, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
places = {p['id'] for p in json.load(open(os.path.join(HERE, 'places-base.json')))}
people = {p['id'] for p in json.load(open(os.path.join(HERE, 'people-ids.json')))}
text = json.load(open(os.path.join(HERE, 'raw', 'doctrine-and-covenants.json')))
verses = {s['section']: {v['verse']: v['text'] for v in s['verses']} for s in text['sections']}
REQUIRED = ['section', 'title', 'dateLabel', 'month', 'receivedAt', 'setting', 'summary', 'contextNote', 'studyVerse', 'ldsText', 'placeIds', 'personIds', 'sources']
BANNED = re.compile(r'\b(delve|tapestry|testament to|underscores?|showcases?|pivotal|profound(?:ly)?|contextual anchor|navigat\w+|in conclusion|it is important to note)\b', re.I)

def sentences(t):
    # Split after . ! ? (optionally followed by a closing quote), but not after a middle initial such as "Newel K." or "Sen.".
    parts = re.split(r'(?<=[.!?][”"])\s+(?=[“"A-Z0-9])|(?<=[.!?])\s+(?=[“"A-Z0-9])', t.strip())
    out = []
    for p in parts:
        if out and re.search(r'(?:\b[A-Z]|\bSen|\bJun|\bSr|\bJr|\bSt|\bMr|\bMrs|\bDr|\bD&C \d+:\d+|\bv|\bvv)\.$', out[-1]):
            out[-1] += ' ' + p
        else: out.append(p)
    return [x for x in out if x]

def words(s):
    return len(re.findall(r"[A-Za-z0-9’'—–-]+", s))

def check(n):
    errs, warns = [], []
    path = os.path.join(HERE, 'sections', f'{n:03d}.json')
    if not os.path.exists(path):
        return [f'missing file {path}'], []
    try:
        d = json.load(open(path))
    except Exception as e:
        return [f'invalid JSON: {e}'], []
    for k in REQUIRED:
        if k not in d: errs.append(f'missing field {k}')
    if errs: return errs, warns
    if d['section'] != n: errs.append('section number mismatch')
    if not re.fullmatch(r'\d{4}-\d{2}', d['month'] or ''): errs.append('month must be YYYY-MM')
    if d['receivedAt'] not in places and d['receivedAt'] not in {p.get('id') for p in d.get('newPlaces', [])}:
        errs.append(f"receivedAt {d['receivedAt']} not in gazetteer (add it to newPlaces with an id)")
    for p in d['placeIds']:
        if p not in places and p not in {x.get('id') for x in d.get('newPlaces', [])}: errs.append(f'unknown place {p}')
    for p in d['personIds']:
        if p not in people and p not in {x.get('id') for x in d.get('newPeople', [])}: errs.append(f'unknown person {p}')
    if d['studyVerse'] not in verses[n]: errs.append(f"studyVerse {d['studyVerse']} not in section")
    for field, lo, hi in [('summary', 4, 9), ('setting', 2, 6)]:
        c = len(sentences(d[field]))
        if not lo <= c <= hi: warns.append(f'{field} has {c} sentences (want {lo}–{hi - 1 if hi == 9 else hi})')
    cn = d['contextNote']
    if not isinstance(cn, dict) or not cn.get('title') or not cn.get('text'): errs.append('contextNote needs title and text')
    else:
        c = len(sentences(cn['text']))
        if not 4 <= c <= 8: warns.append(f'contextNote has {c} sentences (want 4–7)')
        for m in re.finditer(r'\bverses? (\d+)(?:[–-](\d+))?', cn['text']):
            for v in [m.group(1), m.group(2)]:
                if v and int(v) not in verses[n]: errs.append(f'contextNote cites verse {v} which does not exist')
    for field in ['title', 'setting', 'summary', 'ldsText']:
        pass
    allprose = [('setting', d['setting']), ('summary', d['summary']), ('contextNote', cn.get('text', '')), ('ldsText', d['ldsText'])]
    for name, t in allprose:
        for s in sentences(t):
            w = words(s)
            if w > 25: errs.append(f'{name}: sentence over 25 words ({w}): {s[:90]}…')
        if BANNED.search(t): errs.append(f'{name}: banned phrase {BANNED.search(t).group(0)!r}')
        if '<' in t: errs.append(f'{name}: contains markup')
    if len(d['title'].split()) > 12: warns.append('title over 12 words')
    src = d['sources']
    if not src.get('officialUrl', '').startswith('https://www.churchofjesuschrist.org/study/scriptures/dc-testament/dc/'):
        errs.append('sources.officialUrl missing or wrong')
    jsp = src.get('jsp')
    if jsp and not (jsp.get('url', '').startswith('https://www.josephsmithpapers.org/') and jsp.get('title')):
        errs.append('sources.jsp needs title and josephsmithpapers.org url')
    return errs, warns

if __name__ == '__main__':
    nums = []
    for a in sys.argv[1:]:
        if '-' in a:
            x, y = map(int, a.split('-')); nums += range(x, y + 1)
        else: nums.append(int(a))
    bad = 0
    for n in nums:
        e, w = check(n)
        status = 'OK ' if not e else 'ERR'
        if e: bad += 1
        print(f'{status} section {n}' + ''.join(f'\n   error: {x}' for x in e) + ''.join(f'\n   warn: {x}' for x in w))
    sys.exit(1 if bad else 0)

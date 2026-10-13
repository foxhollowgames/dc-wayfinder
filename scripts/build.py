#!/usr/bin/env python3
"""Build the D&C Wayfinder reader data from the persistent files in content/.

Usage: python3 scripts/build.py

Reads   content/raw/doctrine-and-covenants.json   public-domain text (bcbooks/scriptures-json)
        content/sections/NNN.json, od1.json, od2.json   authored section studies
        content/places-base.json, places-extra.json     gazetteer
        content/people/*.json                           person profiles
        content/glossary.json, guides.json, routes.json, cfm-2025.json, state-outlines.json
Writes  dist/data/books/doctrine-and-covenants-{native-content,native-scripture,people,art}.json
        dist/data/books/directory.json, dist/data/sections.json, dist/doctrine-and-covenants.html
"""
import json, os, re, glob, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
C = lambda *p: os.path.join(ROOT, 'content', *p)
D = lambda *p: os.path.join(ROOT, 'dist', *p)
BOOK_ID = 'doctrine-and-covenants'
VERSION = '20261012.1'
REVIEW_DATE = '2026-10-12'
OFFICIAL = 'https://www.churchofjesuschrist.org/study/scriptures/dc-testament/dc/{n}?lang=eng'
warnings = []

def load(path): return json.load(open(path, encoding='utf-8'))
def month_index(ym):
    y, m = map(int, ym.split('-')); return y * 12 + m - 1
def tidy(text):
    # Writers moved periods outside closing quotes to satisfy the checker. Restore American punctuation.
    return re.sub(r'”([.,])', r'\1”', text or '')
def ranges(nums):
    nums = sorted(set(nums)); out = []; i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        out.append(f'{nums[i]}' if i == j else f'{nums[i]}–{nums[j]}'); i = j + 1
    return out

# ---------- text ----------
raw = load(C('raw', 'doctrine-and-covenants.json'))
chapters = {str(s['section']): [{'verse': v['verse'], 'text': v['text']} for v in s['verses']] for s in raw['sections']}
plain = {int(k): ' '.join(v['text'] for v in vs) for k, vs in chapters.items()}
COUNT = len(chapters)
assert COUNT == 138, COUNT

# ---------- places ----------
STATE = {'palmyra': 'New York', 'manchester': 'New York', 'hill-cumorah': 'New York', 'harmony': 'Pennsylvania', 'fayette': 'New York',
         'colesville': 'New York', 'perrysburg': 'New York', 'freedom': 'New York', 'new-york-city': 'New York', 'albany': 'New York',
         'boston': 'Massachusetts', 'salem': 'Massachusetts', 'kirtland': 'Ohio', 'hiram': 'Ohio', 'thompson': 'Ohio', 'amherst': 'Ohio',
         'cincinnati': 'Ohio', 'st-louis': 'Missouri', 'independence': 'Missouri', 'chariton': 'Missouri', 'mcilwaines-bend': 'Missouri',
         'fishing-river': 'Missouri', 'liberty': 'Missouri', 'far-west': 'Missouri', 'adam-ondi-ahman': 'Missouri', 'quincy': 'Illinois',
         'nauvoo': 'Illinois', 'montrose': 'Iowa Territory', 'ramus': 'Illinois', 'carthage': 'Illinois', 'warsaw': 'Illinois',
         'winter-quarters': 'unorganized territory, now Nebraska', 'salt-lake-city': 'Utah', 'lyons': 'New York', 'seneca-falls': 'New York',
         'canandaigua': 'New York', 'north-union': 'Ohio', 'detroit': 'Michigan Territory', 'wayne-county': 'New York',
         'mount-pleasant-upper-canada': 'Upper Canada', 'burlington': 'Iowa Territory', 'fort-madison': 'Iowa Territory',
         'zarahemla': 'Iowa Territory', 'nashville-iowa': 'Iowa Territory'}
HUBS = {'palmyra', 'harmony', 'fayette', 'kirtland', 'hiram', 'independence', 'liberty', 'far-west', 'nauvoo', 'carthage', 'winter-quarters'}
FOUNDED = {'far-west': '1836-08', 'adam-ondi-ahman': '1838-05', 'zarahemla': '1839-06', 'winter-quarters': '1846-09', 'salt-lake-city': '1847-07'}
places = {p['id']: p for p in load(C('places-base.json')) + load(C('places-extra.json'))}

# ---------- sections ----------
sections = {}
for n in range(1, COUNT + 1):
    d = load(C('sections', f'{n:03d}.json'))
    assert d['section'] == n
    for key in ['title', 'setting', 'summary', 'ldsText']: d[key] = tidy(d[key])
    d['contextNote']['text'] = tidy(d['contextNote']['text']); d['contextNote']['title'] = tidy(d['contextNote']['title'])
    known = [p for p in dict.fromkeys([d['receivedAt'], *d['placeIds']]) if p in places]
    for p in [d['receivedAt'], *d['placeIds']]:
        if p not in places: warnings.append(f'section {n}: place {p} is outside the map and was left off')
    d['places'] = known
    sections[n] = d
ods = [load(C('sections', f'od{i}.json')) for i in (1, 2)]

# ---------- sources ----------
cfm = load(C('cfm-2025.json'))
cfm_for = {s: c for c in cfm for s in c['sections']}
sources = [{
    'id': 'web', 'title': 'The Doctrine and Covenants · reading text', 'author': 'Joseph Smith and his successors; text prepared by the Scriptures in JSON project',
    'year': '2013 edition wording', 'type': 'Scripture', 'url': 'https://github.com/bcbooks/scriptures-json',
    'summary': 'All 138 sections appear in the reading text. The verses come from the public-domain “Scriptures in JSON” files, which follow the wording of the 2013 Church edition.',
    'limitations': 'The verses are the primary text for the study notes. They do not by themselves verify dates, places, or events. Section headings, footnotes, and the edition introduction are copyrighted and are not included.',
    'license': 'Public domain dedication by the Scriptures in JSON project', 'chapterCoverage': list(range(1, COUNT + 1)),
    'reviewed': {'date': REVIEW_DATE, 'scope': 'All 3,654 verses loaded and counted. Each section read in full by its writer.'}},
    {'id': 'chron', 'title': 'Chronological Order of Contents', 'author': 'The Church of Jesus Christ of Latter-day Saints', 'year': '2013 edition',
     'type': 'Scripture edition aid', 'group': 'official', 'url': 'https://www.churchofjesuschrist.org/study/scriptures/dc-testament/chron-order?lang=eng',
     'summary': 'The official table of when and where each section was received, by month and place.', 'limitations': 'Gives month and place only. Some places are marked as at or near the place named.',
     'license': '© Intellectual Reserve, Inc. Facts used; wording not copied.', 'reviewed': {'date': REVIEW_DATE, 'scope': 'Full table read.'}},
    {'id': 'earth', 'title': 'Natural Earth 1:10m physical data', 'author': 'Natural Earth', 'year': '2024', 'type': 'Map data',
     'url': 'https://www.naturalearthdata.com/', 'summary': 'Land, lakes, rivers, and state outlines used for the map.',
     'limitations': 'Modern geography. State outlines are modern lines, used only where the 1830s line was close to today’s.', 'license': 'Public domain'}]
src_ids = {s['id'] for s in sources}
def add_source(s):
    if s['id'] not in src_ids: sources.append(s); src_ids.add(s['id'])
for n, d in sections.items():
    add_source({'id': f'dc-{n}', 'title': f'Doctrine and Covenants {n} · official edition', 'author': 'The Church of Jesus Christ of Latter-day Saints',
                'year': '2013 edition', 'type': 'Scripture edition', 'group': 'official', 'url': OFFICIAL.format(n=n),
                'summary': f'The official page for section {n}, with its section heading, footnotes, and verse text. The setting note uses facts from the heading in our own words.',
                'limitations': 'The heading summarizes the Church’s historical understanding. It does not give every source or debate.',
                'license': '© Intellectual Reserve, Inc. Linked, not copied.', 'chapterCoverage': [n]})
    jsp = d['sources'].get('jsp')
    if jsp and jsp.get('url'):
        add_source({'id': f'jsp-{n}', 'title': jsp['title'], 'author': 'The Joseph Smith Papers', 'year': 'Church Historian’s Press', 'type': 'Documentary history',
                    'group': 'jsp', 'url': jsp['url'],
                    'summary': 'The Joseph Smith Papers edition of the earliest manuscript, with a historical introduction by its editors. The setting note draws on that introduction.',
                    'limitations': 'Editors’ conclusions about dates and circumstances can change as new sources appear.',
                    'license': '© Intellectual Reserve, Inc. Linked, not copied.', 'chapterCoverage': [n],
                    'reviewed': {'date': REVIEW_DATE, 'scope': 'Historical introduction read for the setting note.'}})
for c in cfm:
    add_source({'id': c['id'], 'title': f'Come, Follow Me 2025 · {c["title"]}', 'author': 'The Church of Jesus Christ of Latter-day Saints', 'year': '2025',
                'type': 'Church lesson', 'group': 'cfm', 'url': c['url'], 'chapterCoverage': c['sections'],
                'summary': f'The home and church study lesson for {c["week"]}. It covers {c["coverage"]}.',
                'limitations': 'Church teaching and study helps, not historical evidence.', 'license': '© Intellectual Reserve, Inc. Linked, not copied.'})

# ---------- people ----------
profiles = {}
for f in sorted(glob.glob(C('people', '*.json'))):
    p = load(f); profiles[p['id']] = p
DROP_LINKS = {'jesus-christ': {'Christ'}}
person_sections = {pid: set() for pid in profiles}
for n, d in sections.items():
    for pid in d['personIds']:
        if pid in profiles: person_sections[pid].add(n)
        else: warnings.append(f'section {n}: no profile for {pid}')
def occurs(name, n): return re.search(r'(?<![\w-])' + re.escape(name) + r'(?![\w])', plain[n]) is not None
people_out = {}
for pid, p in profiles.items():
    names = [x for x in p.get('linkNames', []) if x not in DROP_LINKS.get(pid, set())]
    secs = set(person_sections[pid])
    for n in range(1, COUNT + 1):
        if any(occurs(x, n) for x in names if ' ' in x): secs.add(n)
    # A bare first name links only where this person is in the section and no other person's full name starts with it.
    scope = {}
    for x in names:
        if ' ' in x: continue
        other_full = [y for q, qp in profiles.items() if q != pid for y in qp.get('linkNames', []) if y.startswith(x + ' ') or y.startswith(x + ',')]
        scope[x] = [n for n in sorted(secs) if not any(occurs(y, n) for y in other_full)]
    people_out[pid] = {
        'name': p['name'], 'role': tidy(p['role']).rstrip('.'), 'life': p.get('life') or 'Dates not known', 'dateNote': tidy(p.get('dateNote', '')),
        'locations': [places[x]['name'] for x in p.get('locations', []) if x in places],
        'passages': [f'D&C {r}' for r in ranges(secs)], 'importance': tidy(p['importance']), 'connections': tidy(p['connections']),
        'linkNames': names, 'chapterIds': sorted(secs), 'linkScope': scope, 'sources': p.get('sources', [])}

# ---------- glossary ----------
words = []
CASE = {'word-of-wisdom', 'seventy', 'twelve', 'the-twelve', 'first-presidency', 'comforter'}
person_names = {x.lower() for p in people_out.values() for x in [p['name'], *p['linkNames']]}
for g in load(C('glossary.json')):
    if g['label'].lower() in person_names: continue
    words.append({'id': f'glossary-{g["id"]}', 'label': g['label'], 'matches': g['matches'], 'chapter': None, 'verses': [],
                  'hebrew': '', 'transliteration': '', 'greek': '', 'greekNote': '', 'meaning': tidy(g['meaning']), 'grammar': '',
                  'discussion': tidy(g['discussion']), 'sourceIds': [f'dc-{g["firstSection"]}'] if g.get('firstSection') else [], 'related': g.get('related', []), 'scope': 'glossary',
                  'caseSensitive': True})  # Each match lists its own capitalized forms, e.g. “Twelve” but not “twelve men”.

# ---------- routes ----------
R = load(C('routes.json'))
def point(x):
    if x in places: return [places[x]['lat'], places[x]['lng']]
    w = R['waypoints'][x]; return [w[1], w[2]]
def pname(x): return places[x]['name'] if x in places else R['waypoints'][x][0]
campaigns = []; section_routes = {}
for r in R['routes']:
    pts = [point(x) for x in r['points']]
    campaigns.append({'id': r['id'], 'title': r['title'], 'kind': r['kind'], 'typeLabel': 'Journey',
                      'start': month_index(r['start']), 'end': month_index(r['end']), 'dateLabel': r['start'][:4] if r['start'][:4] == r['end'][:4] else f'{r["start"][:4]}–{r["end"][:4]}',
                      'points': pts, 'placeIds': [x for x in r['points'] if x in places], 'stops': [pname(x) for x in r['points']],
                      'summary': r['summary'], 'detail': 'Stops: ' + ' → '.join(pname(x) for x in r['points']) + '.', 'evidence': r['evidence'],
                      'uncertainty': r['evidence'], 'sourceIds': [f'dc-{s}' for s in r['sections']] , 'chapter': r['sections'][0], 'verse': 1,
                      'direction': True})
    for s in r['sections']: section_routes.setdefault(s, []).append(r)

# ---------- regions ----------
outlines = load(C('state-outlines.json'))
REG = [  # code, id, name, faction, start, end, pattern, summary, detail
    ('US-NY', 'new-york', 'New York', 'state', None, None, r'\bNew York\b', 'A U.S. state since 1788.', 'Joseph Smith’s family farmed near Palmyra, and the Church was organized at Fayette in 1830.'),
    ('US-PA', 'pennsylvania', 'Pennsylvania', 'state', None, None, r'\bPennsylvania\b', 'A U.S. state since 1787.', 'Joseph and Emma Smith lived at Harmony, on the Susquehanna River, while most of the Book of Mormon was translated.'),
    ('US-OH', 'ohio', 'Ohio', 'state', None, None, r'\bOhio\b', 'A U.S. state since 1803.', 'Kirtland was Church headquarters from 1831 to 1838. Revelations call the region “the Ohio.”'),
    ('US-MO', 'missouri', 'Missouri', 'state', None, None, r'\bMissouri\b', 'A U.S. state since 1821; the western edge of the nation in the 1830s.', 'Revelations named Jackson County as Zion in 1831. Saints were driven from the county in 1833 and from the state in 1838–39.'),
    ('US-IL', 'illinois', 'Illinois', 'state', None, None, r'\bIllinois\b', 'A U.S. state since 1818.', 'Quincy sheltered refugees from Missouri, and Nauvoo became headquarters from 1839 to 1846.'),
    ('US-MA', 'massachusetts', 'Massachusetts', 'state', None, None, r'\bMassachusetts\b|\bSalem\b|\bBoston\b', 'A U.S. state since 1788.', 'Section 111 was received at Salem in 1836.'),
    ('US-IA', 'iowa-territory', 'Iowa Territory', 'territory', '1838-07', '1846-12', r'\bIowa\b', 'Organized as a U.S. territory in July 1838; a state from December 1846.', 'Saints settled across the river from Nauvoo, and in 1846 they crossed it toward the Missouri River.'),
    ('US-MI', 'michigan', 'Michigan', 'territory', None, None, r'\bDetroit\b|\bMichigan\b', 'A U.S. territory until 1837, then a state.', 'Section 52 sends missionaries by way of Detroit.'),
    ('US-KS', 'lands-west-ks', 'Lands west of Missouri', 'unorganized', None, '1854-05', r'\bLamanites?\b', 'Unorganized land outside any state, set aside in the 1830s for Native nations moved from the East.', 'The 1830–31 mission to the Lamanites reached the Delaware nation just west of Independence.'),
    ('US-NE', 'lands-west-ne', 'Lands west of the Missouri River', 'unorganized', None, '1854-05', r'\bLamanites?\b', 'Unorganized land outside any state in the 1840s.', 'Winter Quarters stood here in 1846–48, on land of the Omaha nation.'),
    ('CA-ON', 'upper-canada', 'Upper Canada', 'british', None, '1841-01', r'\bCanada\b', 'A British colony; part of the Province of Canada from 1841.', 'Joseph Smith and Sidney Rigdon preached at Mount Pleasant in 1833 (section 100).'),
    ('US-UT', 'mexican-north', 'Mexico (northern frontier)', 'mexico', None, '1848-02', r'\bMexico\b', 'Part of Mexico until the Treaty of Guadalupe Hidalgo in February 1848.', 'The Salt Lake Valley lay inside Mexico when the pioneers arrived in July 1847.'),
]
def inside(lat, lng, ring):
    c = False; j = len(ring) - 1
    for i in range(len(ring)):
        yi, xi = ring[i]; yj, xj = ring[j]
        if ((yi > lat) != (yj > lat)) and (lng < (xj - xi) * (lat - yi) / (yj - yi) + xi): c = not c
        j = i
    return c
regions = []
for code, rid, name, faction, start, end, pattern, summary, detail in REG:
    ring = outlines[code][0]
    cover = [n for n, d in sections.items() if any(inside(places[p]['lat'], places[p]['lng'], ring) for p in d['places'])]
    regions.append({'id': rid, 'baseId': rid, 'name': name, 'faction': faction, 'points': ring, 'start': month_index(start) if start else None,
                    'end': month_index(end) if end else None, 'pattern': pattern, 'summary': summary, 'detail': detail,
                    'uncertainty': 'Outline follows modern lines.', 'sourceIds': ['earth'], 'chapterCoverage': cover,
                    'typeLabel': {'state': 'U.S. state', 'territory': 'U.S. territory', 'unorganized': 'Unorganized land', 'british': 'British colony', 'mexico': 'Mexico'}[faction]})
factions = {'state': {'name': 'U.S. state', 'color': '#6d7f4a', 'selectedBorder': '#3a4527'},
            'territory': {'name': 'U.S. territory', 'color': '#8a6a3a', 'selectedBorder': '#4b391f'},
            'unorganized': {'name': 'Unorganized land', 'color': '#7b5f8e', 'selectedBorder': '#45334f'},
            'british': {'name': 'British North America', 'color': '#a3423a', 'selectedBorder': '#5b221d'},
            'mexico': {'name': 'Mexico', 'color': '#4f8278', 'selectedBorder': '#285047'},
            'move-journey': {'name': 'Journey', 'color': '#128879', 'selectedBorder': '#0a4a42'},
            'move-mission': {'name': 'Mission journey', 'color': '#128879', 'selectedBorder': '#0a4a42'},
            'move-gathering': {'name': 'Move to gather', 'color': '#257fbd', 'selectedBorder': '#164a6e'},
            'move-expulsion': {'name': 'Forced departure', 'color': '#db8410', 'selectedBorder': '#7a4a09'},
            'move-custody': {'name': 'Taken as prisoners', 'color': '#904fac', 'selectedBorder': '#502b60'}}

# ---------- places out ----------
received = {}
for n, d in sections.items(): received.setdefault(d['receivedAt'], []).append(n)
named_in = {pid: [n for n, d in sections.items() if pid in d['places']] for pid in places}
places_out = []
for pid, p in places.items():
    if not named_in[pid] and not any(pid in r['points'] for r in R['routes']): continue
    full = f'{p["name"]}, {STATE[pid]}' if pid in STATE and STATE[pid] not in p['name'] else p['name']
    rec = received.get(pid, [])
    detail = (f'Sections received or recorded here: {", ".join(ranges(rec))}.' if rec else '') + \
             (f' Studied with sections {", ".join(ranges([n for n in named_in[pid] if n not in rec]))}.' if [n for n in named_in[pid] if n not in rec] else '')
    places_out.append({'id': pid, 'name': p['name'], 'fullName': full, 'lat': p['lat'], 'lng': p['lng'], 'summary': p['summary'], 'detail': detail.strip(),
                       'limits': 'Marker for the town or farm, not an exact building.', 'uncertainty': '', 'sourceIds': ['chron'] if rec else [],
                       'verseScope': {}, 'chapterLocation': pid not in HUBS,
                       **({'start': month_index(FOUNDED[pid])} if pid in FOUNDED else {})})
# Place names that are also people or common words link only where the place is in the section.
for pl in places_out:
    if pl['id'] == 'thompson': pl['verseScope'] = {str(n): [] for n in range(1, COUNT + 1) if 'thompson' not in sections[n]['places']}
    if pl['id'] == 'hiram': pl['verseScope'] = {str(n): [] for n in range(1, COUNT + 1) if 'hiram' not in sections[n]['places']}
    if pl['id'] == 'liberty': pl['verseScope'] = {str(n): [] for n in range(1, COUNT + 1) if 'liberty' not in sections[n]['places']}
    if pl['id'] == 'freedom': pl['verseScope'] = {str(n): [] for n in range(1, COUNT + 1) if 'freedom' not in sections[n]['places']}
    if pl['id'] == 'zarahemla': pl['verseScope'] = {str(n): [] for n in range(1, COUNT + 1) if 'zarahemla' not in sections[n]['places']}
pmap = {p['id']: p for p in places_out}

# ---------- passages, maps, studies ----------
passages, chapter_maps, studies, bands, events = [], [], [], [], []
TIMELINE = {'start': month_index('1823-09'), 'end': month_index('1847-12'), 'default': month_index('1831-02'), 'unit': 'month'}
for n, d in sections.items():
    verses = chapters[str(n)]
    m = month_index(d['month'])
    year = m if TIMELINE['start'] <= m <= TIMELINE['end'] else None
    src = [f'dc-{n}'] + ([f'jsp-{n}'] if f'jsp-{n}' in src_ids else [])
    rp = pmap[d['receivedAt']]
    place_label = rp['fullName']
    lds_ids = [cfm_for[n]['id']] if n in cfm_for else []
    passages.append({'id': f'dc-{n}', 'chapter': n, 'start': 1, 'end': verses[-1]['verse'], 'title': d['title'], 'setting': d['setting'],
                     'summary': d['summary'], 'year': year, 'dateLabel': f'{d["dateLabel"]} · {place_label}', 'uncertainty': '',
                     'placeIds': d['places'], 'sourceIds': src, 'lds': {'text': d['ldsText'], 'sourceIds': lds_ids},
                     'contextNote': {'title': d['contextNote']['title'], 'text': d['contextNote']['text'], 'sourceIds': [], 'evidenceSourceIds': []}})
    studies.append({'chapter': n, 'verse': d['studyVerse'], 'context': ''})
    bands.append({'from': n, 'to': n, 'label': f'{place_label} · {d["dateLabel"]}'})
    routes = section_routes.get(n, [])
    others = [p for p in d['places'] if p != d['receivedAt']]
    narrative = f'Received at {place_label}, {d["dateLabel"]}.' + (f' Other places tied to this section: {", ".join(pmap[p]["name"] for p in others)}.' if others else '')
    chapter_maps.append({'chapter': n, 'focusPlaceIds': [d['receivedAt']], 'placeIds': d['places'],
                         'routes': [{'id': r['id'], 'from': 0, 'to': len(r['points']) - 1} for r in routes],
                         'contextRoutes': [], 'contextPlaceIds': others, 'impacts': [], 'maxZoom': 7,
                         'note': narrative, 'narrative': narrative, 'limits': '', 'sourceIds': ['chron']})
    events.append({'id': f'dc-{n}', 'chapter': n, 'verse': 1, 'year': year if year is not None else TIMELINE['end'], 'title': f'D&C {n}: {d["title"]}',
                   'summary': d['summary'], 'dateLabel': d['dateLabel'], 'placeIds': [d['receivedAt']], 'sourceIds': src})

periods = [{'id': 'beginnings', 'label': 'New York and Pennsylvania', 'start': month_index('1828-07'), 'end': month_index('1830-12'), 'description': '1828–1830'},
           {'id': 'ohio-missouri', 'label': 'Ohio and Missouri', 'start': month_index('1831-01'), 'end': month_index('1838-12'), 'description': '1831–1838'},
           {'id': 'nauvoo', 'label': 'Nauvoo and the trek west', 'start': month_index('1839-01'), 'end': month_index('1847-07'), 'description': '1839–1847'}]

guides = []
for g in load(C('guides.json')):
    guides.append({'id': g['id'], 'title': g['title'], 'description': g['description'],
                   'steps': [{'title': tidy(s['title']), 'text': tidy(s['text']), 'chapter': s['chapter'], 'verse': s['verse'],
                              'year': passages[s['chapter'] - 1]['year'], 'sourceIds': [f'dc-{s["chapter"]}']} for s in g['steps']]})

book = {'id': BOOK_ID, 'name': 'D&C', 'fullName': 'Doctrine and Covenants', 'bibleCode': 'DC', 'chapterCount': COUNT, 'chapterDigits': 3,
        'unitLabel': 'section', 'verseLinks': 'entities', 'mapLimits': True, 'wordLanguages': False, 'relief': False,
        'scriptureUrl': 'https://www.churchofjesuschrist.org/study/scriptures/dc-testament/dc/{chapter}?lang=eng&id=p{verse}#p{verse}',
        'timeline': TIMELINE, 'portraitNote': 'People appear as initials. No portrait art is included yet.',
        'map': {'center': [40.6, -84.5], 'zoom': 5, 'bounds': [[22, -128], [55, -58]], 'minZoom': 4, 'maxZoom': 12},
        'geographyLabels': [['Lake Erie', 42.15, -81.3, 5, -18], ['Lake Ontario', 43.65, -77.9, 5, -5], ['Lake Michigan', 43.6, -87.05, 5, -82],
                            ['Lake Huron', 44.9, -82.5, 6, -55], ['Atlantic Ocean', 36.5, -70.5, 4, 0], ['Mississippi', 38.4, -90.25, 7, -75],
                            ['Missouri', 39.15, -92.9, 7, 15], ['Ohio River', 38.75, -84.9, 7, -10], ['Susquehanna', 41.2, -76.6, 8, -60],
                            ['Great Salt Lake', 41.15, -112.6, 6, 0]]}
content = {'book': book, 'sources': sources, 'passages': passages, 'events': events, 'places': places_out, 'campaigns': campaigns,
           'ancientRoads': [], 'regions': regions, 'factions': factions, 'words': words, 'guides': guides, 'periods': periods,
           'chapterMaps': chapter_maps, 'textRoutes': [], 'narrativeRegions': [], 'chapterStudies': studies, 'chapterDateBands': bands,
           'sourceGroups': [{'id': 'official', 'title': 'Official Doctrine and Covenants pages', 'description': 'Each section’s page on the Church’s site has its heading, footnotes, and text. Setting notes use the headings’ facts in our own words.'},
                            {'id': 'jsp', 'title': 'The Joseph Smith Papers', 'description': 'The earliest manuscripts of the revelations, with historical introductions by the project’s editors.'},
                            {'id': 'cfm', 'title': 'Come, Follow Me 2025', 'description': 'The Church’s 2025 home and church lessons on the Doctrine and Covenants. LDS mode only.'}]}

os.makedirs(D('data', 'books'), exist_ok=True)
def dump(obj, *p): json.dump(obj, open(D(*p), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
dump(content, 'data', 'books', f'{BOOK_ID}-native-content.json')
dump({'translation': 'Doctrine and Covenants', 'copyright': 'Public-domain text (Scriptures in JSON)', 'chapters': chapters}, 'data', 'books', f'{BOOK_ID}-native-scripture.json')
dump({'people': people_out, 'featurePeople': {}, 'aliases': {}, 'profileFacts': True}, 'data', 'books', f'{BOOK_ID}-people.json')
dump({}, 'data', 'books', f'{BOOK_ID}-art.json')
dump([{'id': BOOK_ID, 'name': 'Doctrine and Covenants', 'status': 'ready', 'url': f'{BOOK_ID}.html'}], 'data', 'books', 'directory.json')

# Home page directory: every section plus the two declarations.
home = []
for n, d in sections.items():
    home.append({'n': n, 'title': d['title'], 'date': d['dateLabel'], 'month': d['month'], 'place': pmap[d['receivedAt']]['fullName']})
for od in ods:
    home.append({'od': od['id'], 'title': tidy(od['title']), 'date': od['dateLabel'], 'month': od['month'], 'place': 'Salt Lake City, Utah',
                 'setting': tidy(od['setting']), 'summary': tidy(od['summary']), 'lds': tidy(od.get('ldsText', '')), 'url': od.get('officialUrl')})
dump(home, 'data', 'sections.json')

# Reader page for the book.
shell = open(D('book.html'), encoding='utf-8').read()
page = shell.replace('<html lang="en">', f'<html lang="en" data-book="{BOOK_ID}">', 1).replace('<title>D&amp;C Wayfinder</title>', '<title>Doctrine and Covenants · D&amp;C Wayfinder</title>', 1)
open(D(f'{BOOK_ID}.html'), 'w', encoding='utf-8').write(page)

print(f'Built {COUNT} sections, {len(places_out)} places, {len(people_out)} people, {len(words)} glossary terms, {len(campaigns)} journeys, {len(regions)} areas, {len(sources)} sources, {len(guides)} guides.')
for w in warnings: print('note:', w)

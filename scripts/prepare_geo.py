#!/usr/bin/env python3
"""Build regional map layers from Natural Earth 1:10m (public domain).
Usage: python3 scripts/prepare_geo.py <natural-earth-vector/geojson dir>
Writes dist/data/rivers.geojson and content/state-outlines.json."""
import json, sys, os
SRC = sys.argv[1]
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
W, S, E, N = -115, 28, -64, 50

def inside(p): return W <= p[0] <= E and S <= p[1] <= N

def dp(points, tol):
    if len(points) < 3: return points
    (x1, y1), (x2, y2) = points[0], points[-1]
    dx, dy = x2 - x1, y2 - y1; L = (dx*dx + dy*dy) ** .5 or 1e-12
    idx, dmax = 0, 0
    for i in range(1, len(points) - 1):
        x, y = points[i]
        d = abs(dy*x - dx*y + x2*y1 - y2*x1) / L if (dx or dy) else ((x-x1)**2+(y-y1)**2)**.5
        if d > dmax: idx, dmax = i, d
    if dmax <= tol: return [points[0], points[-1]]
    return dp(points[:idx+1], tol)[:-1] + dp(points[idx:], tol)

def lines(geom):
    if not geom: return []
    t = geom['type']
    return [geom['coordinates']] if t == 'LineString' else geom['coordinates'] if t == 'MultiLineString' else []

def clip_line(line):
    runs, cur = [], []
    for p in line:
        if inside(p): cur.append(p)
        elif cur: runs.append(cur); cur = []
    if cur: runs.append(cur)
    return [r for r in runs if len(r) > 1]

feats = []
def add(f, rank, tol):
    parts = []
    for l in lines(f['geometry']):
        for r in clip_line(l):
            r = [[round(x, 3), round(y, 3)] for x, y in dp(r, tol)]
            if len(r) > 1: parts.append(r)
    if parts:
        feats.append({'type': 'Feature', 'properties': {'name': f['properties'].get('name') or '', 'rank': rank},
                      'geometry': {'type': 'MultiLineString', 'coordinates': parts}})

for f in json.load(open(os.path.join(SRC, 'ne_10m_rivers_lake_centerlines.geojson')))['features']:
    if f['properties']['featurecla'] == 'River': add(f, int(f['properties']['scalerank']), .01)
for f in json.load(open(os.path.join(SRC, 'ne_10m_rivers_north_america.geojson')))['features']:
    pass  # The North America supplement (scalerank 10–12) is too dense at this map scale.
json.dump({'type': 'FeatureCollection', 'features': feats}, open(os.path.join(ROOT, 'dist/data/rivers.geojson'), 'w'), separators=(',', ':'))
print('rivers', len(feats))

# State and province outlines used for the historical areas layer.
wanted = {'US-NY', 'US-PA', 'US-OH', 'US-MO', 'US-IL', 'US-MA', 'US-IA', 'US-KS', 'US-NE', 'US-UT', 'CA-ON', 'US-MI', 'US-IN'}
out = {}
for f in json.load(open(os.path.join(SRC, 'ne_10m_admin_1_states_provinces.geojson')))['features']:
    code = f['properties'].get('iso_3166_2')
    if code not in wanted: continue
    g = f['geometry']
    polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
    rings = []
    for poly in polys:
        ring = poly[0]
        if code == 'CA-ON': ring = [p for p in ring if p[1] < 46.5]
        if len(ring) < 20: continue
        ring = dp(ring, .03)
        if len(ring) >= 4: rings.append([[round(y, 3), round(x, 3)] for x, y in ring])
    rings.sort(key=len, reverse=True)
    out[code] = rings[:1]
json.dump(out, open(os.path.join(ROOT, 'content/state-outlines.json'), 'w'))
print({k: len(v[0]) for k, v in out.items()})

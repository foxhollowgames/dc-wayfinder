// Check the built reader data for D&C Wayfinder. Run after `python3 scripts/build.py`.
import { readFileSync, existsSync } from 'node:fs';
const read = p => JSON.parse(readFileSync(new URL(`../dist/${p}`, import.meta.url), 'utf8'));
const id = 'doctrine-and-covenants';
const content = read(`data/books/${id}-native-content.json`);
const scripture = read(`data/books/${id}-native-scripture.json`);
const people = read(`data/books/${id}-people.json`).people;
const home = read('data/sections.json');
const errors = [];
const fail = m => errors.push(m);
const { book } = content;
const sources = new Set(content.sources.map(s => s.id));
const places = new Map(content.places.map(p => [p.id, p]));
const campaigns = new Set(content.campaigns.map(c => c.id));
const verseSet = n => new Set((scripture.chapters[n] || []).map(v => v.verse));
let verses = 0;
for (let n = 1; n <= book.chapterCount; n++) {
  const vs = scripture.chapters[n];
  if (!vs?.length) { fail(`section ${n}: no text`); continue; }
  verses += vs.length;
  vs.forEach((v, i) => { if (v.verse !== i + 1 || !v.text.trim()) fail(`section ${n}: verse ${i + 1} missing or empty`); });
  const ps = content.passages.filter(p => p.chapter === n);
  if (ps.length !== 1) fail(`section ${n}: expected one passage, found ${ps.length}`);
  const p = ps[0]; if (!p) continue;
  for (const key of ['title', 'setting', 'summary']) if (!p[key]) fail(`section ${n}: missing ${key}`);
  if (!p.contextNote?.text) fail(`section ${n}: missing context note`);
  if (!p.lds?.text || !p.lds.sourceIds.length) fail(`section ${n}: missing LDS lens or lesson`);
  if (p.end !== vs.length) fail(`section ${n}: passage end ${p.end} ≠ ${vs.length} verses`);
  for (const s of [...p.sourceIds, ...p.lds.sourceIds]) if (!sources.has(s)) fail(`section ${n}: unknown source ${s}`);
  for (const pl of p.placeIds) if (!places.has(pl)) fail(`section ${n}: unknown place ${pl}`);
  if (p.year != null && (p.year < book.timeline.start || p.year > book.timeline.end)) fail(`section ${n}: date outside timeline`);
  const study = content.chapterStudies.filter(s => s.chapter === n);
  if (study.length !== 1 || !verseSet(n).has(study[0].verse)) fail(`section ${n}: study verse invalid`);
  const map = content.chapterMaps.filter(m => m.chapter === n);
  if (map.length !== 1) fail(`section ${n}: expected one map entry`);
  for (const r of map[0]?.routes || []) if (!campaigns.has(r.id)) fail(`section ${n}: unknown route ${r.id}`);
  for (const pl of [...(map[0]?.focusPlaceIds || []), ...(map[0]?.contextPlaceIds || [])]) if (!places.has(pl)) fail(`section ${n}: map place ${pl} missing`);
  // Verse references in the close reading must exist.
  for (const m of p.contextNote.text.matchAll(/\bverses? (\d+)(?:[–-](\d+))?/g)) for (const v of [m[1], m[2]].filter(Boolean)) if (!verseSet(n).has(Number(v))) fail(`section ${n}: context note cites missing verse ${v}`);
  // Quoted phrases from the section must match its text.
  const text = vs.map(v => v.text).join(' ').replace(/[’']/g, "'").toLowerCase();
  for (const m of p.contextNote.text.matchAll(/“([^”]{6,})”/g)) {
    const q = m[1].replace(/[.,;:!?]+$/, '').replace(/[’']/g, "'").toLowerCase();
    if (!text.includes(q)) fail(`section ${n}: quotation not found in text: “${m[1]}”`);
  }
}
if (verses !== 3654) fail(`expected 3,654 verses, found ${verses}`);
for (const pl of content.places) if (!(pl.lat > 24 && pl.lat < 50 && pl.lng > -115 && pl.lng < -65)) fail(`place ${pl.id}: coordinates outside the map`);
for (const c of content.campaigns) { if (c.points.length < 2) fail(`route ${c.id}: needs two points`); for (const s of c.sourceIds) if (!sources.has(s)) fail(`route ${c.id}: unknown source ${s}`);
  // Each stop is a place on the map. The text does not list the stops.
  if (c.placeIds.length !== c.points.length) fail(`route ${c.id}: each point needs a stop`);
  for (const pl of c.placeIds) if (!places.has(pl)) fail(`route ${c.id}: stop ${pl} is not a place`);
  if (/Stops:|→/.test(`${c.summary} ${c.detail}`)) fail(`route ${c.id}: text lists stops`);
  if (!c.evidence) fail(`route ${c.id}: missing evidence`); }
for (const pl of content.places) if (pl.routeOnly && !content.campaigns.some(c => c.placeIds.includes(pl.id))) fail(`place ${pl.id}: on no route`);
for (const s of content.sources) if (s.group === 'jsp-maps' && !/^https:\/\/www\.josephsmithpapers\.org\/.+\.pdf$/.test(s.url)) fail(`source ${s.id}: bad map link`);
for (const g of content.guides) for (const s of g.steps) if (!verseSet(s.chapter).has(s.verse)) fail(`guide ${g.id}: ${s.chapter}:${s.verse} missing`);
for (const [pid, p] of Object.entries(people)) {
  for (const k of ['name', 'role', 'life', 'importance', 'connections']) if (!p[k]) fail(`person ${pid}: missing ${k}`);
  if (!p.chapterIds.length) fail(`person ${pid}: appears in no section`);
}
const art = read(`data/books/${id}-art.json`);
for (const [pid, a] of Object.entries(art)) {
  if (!people[pid]) fail(`art ${pid}: unknown person`);
  for (const k of ['src', 'sourceUrl', 'credit', 'license', 'licenseUrl']) if (!a[k]) fail(`art ${pid}: missing ${k}`);
  if (!existsSync(new URL(`../dist/${a.src}`, import.meta.url))) fail(`art ${pid}: image file missing`);
}
for (const w of content.words) for (const m of w.matches) if (!Object.values(scripture.chapters).some(vs => vs.some(v => new RegExp(`(?<![\\w-])${m.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?!\\w)`).test(v.text)))) fail(`glossary ${w.id}: “${m}” never occurs`);
if (home.filter(h => h.n).length !== 138 || home.filter(h => h.od).length !== 2) fail('home directory must list 138 sections and 2 declarations');
const long = [];
for (const p of content.passages) for (const t of [p.setting, p.summary, p.contextNote.text, p.lds.text]) for (const s of t.split(/(?<=[.!?][”"]?)\s+(?=[“"A-Z0-9])/)) if (s.split(/\s+/).length > 30) long.push(`${p.chapter}: ${s.slice(0, 60)}…`);
if (long.length) console.log(`note: ${long.length} sentences over 30 words (initials can join sentences):\n  ` + long.slice(0, 10).join('\n  '));
if (errors.length) { console.error(errors.join('\n')); console.error(`\n${errors.length} problems.`); process.exit(1); }
console.log(`Data check passed: 138 sections, ${verses.toLocaleString('en-US')} verses, ${content.places.length} places, ${Object.keys(people).length} people, ${content.words.length} glossary terms, ${content.campaigns.length} journeys, ${content.guides.length} guides.`);

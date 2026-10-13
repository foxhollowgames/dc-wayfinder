# D&C Wayfinder data contract

The reader is the Bible Wayfinder reader. See the Bible Wayfinder `DATA-CONTRACT.md` for the base format. Its four files per book are `<id>-native-content.json`, `-native-scripture.json`, `-people.json`, and `-art.json`. This file lists what D&C Wayfinder adds.

## New `book` settings (all optional; Bible books are unaffected)

- `unitLabel: "section"`: replaces “chapter” in reader labels.
- `map: {center, zoom, bounds, minZoom, maxZoom}`: the map area. The Levant is the default.
- `geographyLabels: [[name, lat, lng, minZoom, angle]]`: water labels. These replace the Levant labels.
- `relief: false`: no terrain image or terrain credit.
- `timeline.unit: "month"`: timeline values are `year*12 + month-1`, shown as “March 1831”. Passage `year` uses the same unit.
- `scriptureUrl`: a link template with `{chapter}` and `{verse}`.
- `wordLanguages: false`: hides the Hebrew/Greek panel in word studies.
- `portraitNote`: footer text about portraits.
- `fullName`: the long book name. `name` ("D&C") is used in references such as “D&C 76:22”.

## New data fields

- `passage.setting`: the historical setting, shown above the summary.
- `word.caseSensitive`: the term links only its exact `matches` forms (for example “Twelve”, not “twelve men”).
- `person.linkScope: {name: [units]}`: a short name links only in the listed units.
- `campaign.kind` without `faction`: the line uses the movement style color. Kinds include `mission`, `gathering`, `expulsion`, and `custody`, in `chapter-map.js`.
- `campaign.placeIds`: the ids of every stop on the path, in order. The map shows and labels these places while the path is on the map. The path text does not list the stops.
- Place `routeOnly: true`: the place shows only as a stop of a path that is on the map. The build sets it for each `waypoints` entry in `routes.json`.
- Place `start` (month index): the place appears in Map mode from that month. Used for Far West, Adam-ondi-Ahman, Zarahemla, Winter Quarters, and Salt Lake City.
- `dist/data/sections.json`: the home page list (`n` or `od`, title, date, month, place). Declarations also carry `setting`, `summary`, `lds`, and `url`.

## Content files (`content/`)

- `sections/NNN.json` has: `section`, `title`, `dateLabel`, `month` (YYYY-MM), `receivedAt` (place id), `setting`, `summary`, `contextNote {title, text}`, `studyVerse`, `ldsText`, `placeIds`, `personIds`, `newPlaces`, `newPeople`, `sources {officialUrl, jsp {title, url}}`, and `reviewNote`.
- `people/<id>.json` has: `name`, `role`, `life`, `dateNote`, `locations` (place ids), `importance`, `connections`, `linkNames`, `sources`, and `reviewNote`.
- `routes.json` has `waypoints` (stops that are not gazetteer places) and `routes`. Each route has `{id, title, kind, start, end, points, sections, summary, evidence}`.
- `jsp-maps.json` lists the Joseph Smith Papers reference maps. Each map has `{id, group, title, file}` and optional `routes` (route ids), `places` (place ids), `sections`, and `start`/`end` (YYYY-MM). The build makes one linked source per map (`jspmap-<id>`, group `jsp-maps`). The source joins the named routes and places. It covers the named sections, the sections of the named routes, and the sections received at a named place between `start` and `end`. The maps are linked, not copied.
- `glossary.json` entries have: `{id, label, matches, meaning, discussion, firstSection, sections, related}`.
- `guides.json` holds guides of 5–7 steps. Each step has `{title, text, chapter, verse}`.
- `art.json` maps a person id to `{file, commonsFile, sourceUrl, credit, kind, license, licenseUrl,reviewNote}` and an optional `crop`. The image is `dist/assets/portraits/<file>`. The build skips an entry when its image is missing. `scripts/fetch_art.py` downloads the images from Wikimedia Commons.

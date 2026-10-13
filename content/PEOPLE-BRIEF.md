# D&C Wayfinder — people profile brief

Write short reference profiles for people in the Doctrine and Covenants study guide. Read `/home/claude/dc-wayfinder/content/WRITER-BRIEF.md` first for voice and sentence rules (plain English, sentences ≤ 25 words, aim 8–15; historical voice; no banned words).

Inputs:
- Your batch: `/home/claude/dc-wayfinder/content/people-batch-N.json` — each row has `id`, `name`, `sections` (where the person appears), `note`.
- Section study files: `/home/claude/dc-wayfinder/content/sections/NNN.json` (setting + summary written for each section — read the ones listed for the person).
- Verse text: `/home/claude/dc-wayfinder/content/text/NNN.txt`.
- Place ids: `/home/claude/dc-wayfinder/content/places-base.json`.

Output: `/home/claude/dc-wayfinder/content/people/<id>.json`, one file per person:

```json
{
  "id": "oliver-cowdery",
  "name": "Oliver Cowdery",
  "role": "Book of Mormon scribe and Second Elder of the Church",       // label, no full stop, ≤ 10 words
  "life": "1806–1850",                                                 // or "About 1790–1850", or "Dates not known"
  "dateNote": "One sentence on the key dates the reader meets in the D&C, e.g. when he was baptized or called.",
  "locations": ["harmony", "fayette", "kirtland"],                     // place ids only, 0–5
  "importance": "2–4 sentences: what this person does in the D&C, in order, and what changes because of it.",
  "connections": "1–2 sentences: family and the named people they deal with in these sections.",
  "linkNames": ["Oliver Cowdery", "Oliver"],                           // exact forms that occur in the D&C text naming THIS person; [] if none. Do not include ambiguous forms (e.g. bare "Joseph", "John", "Smith").
  "sources": [{"title": "…", "url": "https://…"}],                     // 1–3 pages you actually loaded: prefer the Joseph Smith Papers person page (josephsmithpapers.org/person/…) or Church History Topics; Wikipedia acceptable for background
  "reviewNote": "What you checked; anything uncertain."
}
```

Rules:
- Verify life dates and key facts with a page you load (WebSearch + WebFetch). The Joseph Smith Papers has biographical pages for most early figures (search `josephsmithpapers.org person <name>`). For biblical/heavenly figures (Moroni, Elijah, Moses, Adam, Abraham, Enoch, Eve, John the Baptist, Peter/James/John, Jesus Christ, Aaron, Nathanael, Elias, John the Revelator) use `"life": "Dates not known"` and describe them only as the D&C presents them ("The revelation says…"), citing the official D&C pages as sources.
- `linkNames`: search the actual text files for how the person is named. For example check `grep -l "Sidney Rigdon" /home/claude/dc-wayfinder/content/text/*.txt`. Only list forms that occur.
- Contested people (e.g. John C. Bennett, William Law, apostates, critics) — factual and even-handed.
- Don't pad. A short true profile is better than a long one.

Check each file is valid JSON (`python3 -m json.tool file`). Return a brief report: count written, any person whose dates you could not verify, and any uncertainty.

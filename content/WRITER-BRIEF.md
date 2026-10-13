# D&C Wayfinder — section writer brief

You are writing study content for **D&C Wayfinder**, a map-first study guide to the Doctrine and Covenants (Church of Jesus Christ of Latter-day Saints). It is adapted from "Bible Wayfinder". Each section of the D&C gets one JSON file. Your work is the core content of the app, so accuracy matters more than speed.

## Files

- Verse text (read this, it is the primary text): `/home/claude/dc-wayfinder/content/text/NNN.txt` (one verse per line, `verse text`).
- Place ids you may use: `/home/claude/dc-wayfinder/content/places-base.json`
- Person ids you may use: `/home/claude/dc-wayfinder/content/people-ids.json`
- Come, Follow Me 2025 lessons and the sections each covers: `/home/claude/dc-wayfinder/content/cfm-2025.json`
- A finished model: `/home/claude/dc-wayfinder/content/sections/004.json` — read it first and match its quality and voice.
- Write your output to `/home/claude/dc-wayfinder/content/sections/NNN.json` (three-digit section number).
- Check every file: `python3 /home/claude/dc-wayfinder/content/check_section.py <first>-<last>`. Fix every error. Treat warnings seriously.

## Workflow for each section

1. Read the WHOLE section text from the local file. Long sections (76, 84, 88, 107, 124, 132…) must still be read in full.
2. WebFetch the official page `https://www.churchofjesuschrist.org/study/scriptures/dc-testament/dc/N?lang=eng` and read the section heading for date, place, recipients, and circumstances. The heading is copyrighted: use its facts, never copy its wording.
3. Find the Joseph Smith Papers document for the section. Try WebSearch like `josephsmithpapers.org "[D&C N]"`; JSP titles look like "Revelation, February 1829 [D&C 4]" and URLs like `https://www.josephsmithpapers.org/paperSummary/revelation-february-1829-dc-4`. WebFetch it and read the Historical Introduction. If you cannot find or load it after two tries, set `"jsp": null` and say so in `reviewNote`. Never invent a URL. (Some sections, e.g. 135 and 138, have no JSP revelation document — that is fine.)
4. Write the JSON. Run the checker. Fix.

## JSON schema

```json
{
  "section": 4,
  "title": "4–10 words stating the section's main move as a claim, not a label",
  "dateLabel": "February 1829",          // as precise as the official heading/JSP supports, e.g. "16 February 1832" or "February 1829" or "Summer 1829"
  "month": "1829-02",                    // YYYY-MM for the timeline; for a season use its best month and note it in reviewNote
  "receivedAt": "harmony",               // place id where it was received/recorded (from places-base.json)
  "setting": "2–5 sentences: who, when, where, and WHY this revelation came (the question, request, or event behind it). From the heading + JSP, paraphrased.",
  "summary": "4–8 short sentences: what the revelation says, in its own order. Include the turns. Name the people it names.",
  "contextNote": { "title": "short heading", "text": "4–7 connected sentences anchored on studyVerse — see below" },
  "studyVerse": 3,                       // the one verse the close reading is anchored on
  "ldsText": "1–2 sentences. First name the matching Come, Follow Me 2025 lesson (from cfm-2025.json) and the teaching it draws out; then ask one specific study question that points to verse numbers.",
  "placeIds": ["harmony"],               // receivedAt + real places the text names or that the setting requires. Not figurative places (Babylon, Zion as a concept, Mount Zion).
  "personIds": ["joseph-smith"],         // recipients + people the text names or addresses, from people-ids.json
  "newPlaces": [ {"id": "kebab-id", "name": "Name", "why": "verse or setting reason"} ],   // only if a needed real place is missing
  "newPeople": [ {"id": "kebab-id", "name": "Full Name", "why": "named in v. 12; who they were"} ],   // only if missing and named in the text
  "sources": {
    "officialUrl": "https://www.churchofjesuschrist.org/study/scriptures/dc-testament/dc/4?lang=eng",
    "jsp": { "title": "exact JSP title", "url": "exact URL you loaded", "checked": true }
  },
  "reviewNote": "What you read (verse count), what the heading/JSP established, and anything uncertain."
}
```

## How to write (from the project writing guide — follow strictly)

- Plain English for a general adult reader. Short sentences: aim for 8–15 words; **never over 25**. One main idea per sentence. Active voice. Concrete words.
- Keep needed facts and reasoning. Do not drop a fact just to simplify. Do not raise certainty when simplifying.
- **summary = what the text says.** Name the speaker or form first when helpful (a revelation, a vision, a prayer, a letter, instructions, a declaration). Follow the section's order. Name the people it names. State conditions and results ("If they repent, …"). Do not explain meaning here.
- **contextNote = why.** Start with the problem or question the study verse answers. Give the reason from the section itself, citing verse numbers ("Verse 5 …", "verses 12–14 …") so the reader can check. Connect the study verse with one other verse (a cause, contrast, or result). End with what the key word or action means *in this passage*. Do not end with a general moral. Do not repeat summary sentences.
- **setting** is history. Use the heading and JSP. Names, place, month/year, and the occasion. Mention when the date or place is uncertain.
- **Historical voice.** In setting/summary/contextNote, attribute religious claims to the text: "The revelation says…", "The voice in verse 1 speaks as…", "Joseph Smith reported…". Do not state supernatural claims as verified fact, and do not argue against them. Faithful interpretation belongs only in `ldsText`.
- **ldsText** may speak from Latter-day Saint belief, but must name its Church source (the CFM lesson) and stay modest. The question must be specific to this section — never generic ("How can this help you?").
- Never use: delve, tapestry, testament to, underscore, showcase, pivotal, profound, navigate, "it is important to note". No markup, no emojis, no curly-brace placeholders.
- Quoting the D&C text: short phrases only, in curly quotes “ ”, exact wording.
- Titles: a claim about the section, e.g. "Desire to serve is the first qualification for the work", not "Section 4" or "A Revelation to Joseph Smith Sr.".
- Contested topics (e.g. 132 plural marriage, 134 government, 87 war, OD-related race questions, 101 persecution, 121 Missouri conflict) — be accurate, even-handed, and factual; note what the text says and what the historical record shows; no editorializing either way.

## Final message

Return a short report: sections written, any sections with `jsp: null`, any `newPlaces`/`newPeople` you added (with ids), and any facts you were unsure of. Do not paste the JSON.

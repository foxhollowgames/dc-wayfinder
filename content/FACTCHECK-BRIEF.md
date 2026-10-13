# Fact-check brief

You are an independent fact-checker for "D&C Wayfinder", a Doctrine and Covenants study guide. Writers produced one JSON file per section in /home/claude/dc-wayfinder/content/sections/NNN.json (fields: setting, summary, contextNote, studyVerse, ldsText, dateLabel, month, receivedAt, placeIds, personIds, sources). Verse text: /home/claude/dc-wayfinder/content/text/NNN.txt. Writer rules: /home/claude/dc-wayfinder/content/WRITER-BRIEF.md (read it). An earlier sample found errors in about 1 of 3 sections, so read closely.

For each assigned section:
1. Read the full verse text. Compare summary and contextNote with it: wrong verse numbers, wrong speaker or addressee, claims the text does not make, misquotes (quoted words in “ ” must match the text exactly), and missing major turns.
2. Verify setting facts (date, place, people, occasion) against the official heading (WebFetch https://www.churchofjesuschrist.org/study/scriptures/dc-testament/dc/N?lang=eng) and the JSP page in sources.jsp.url when present. Flag facts that neither supports and that are not common, well-established history; soften or remove them.
3. Historical voice: supernatural claims attributed to the text or to Joseph Smith in setting/summary/contextNote; faithful interpretation only in ldsText.
4. ldsText names the correct Come, Follow Me 2025 lesson (/home/claude/dc-wayfinder/content/cfm-2025.json) and asks a section-specific question.

Fix real errors directly in the JSON (same schema and writing rules). Append to reviewNote: "Fact-check 2026-10-12: <what changed>" (or "Fact-check 2026-10-12: no changes"). Run `python3 /home/claude/dc-wayfinder/content/check_section.py <n>` on every file and fix errors. Do not rewrite for style alone. Keep scratch files in a private folder under /tmp. Write a log to the review file named in your assignment, one line per section: OK, or the error and fix. Return a short summary: error count and the most serious problems.

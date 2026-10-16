# Project instructions

The product name is D&C Wayfinder. It reuses the Bible Wayfinder reader.

- Read `content/WRITER-BRIEF.md` before changing study text. Use short, plain sentences. Write in historical voice outside the LDS lens.
- Read `DATA-CONTRACT.md` before changing generated data or the reader.
- The shared reader files come from the Wayfinder repository: `app.js`, `styles.css`, `native-book.js`, `portraits.js`, `chapter-map.js`, `breadcrumbs.js`, `breadcrumbs.css`, `chapter-picker.js`, `modal-drag.js`, and `settings-menu.js`. Each copy starts with a stamp line. Edit `Wayfinder/viewer/<file>`, then run `npm run sync-viewer` in the Wayfinder folder. Do not edit the copies in `dist/`.
- Do not test for a book's id in reader code. Put differences in the book's data settings.
- Edit `content/`, then run `python3 scripts/build.py` and `npm run check`. Never hand-edit `dist/data/books/*`.
- Do not copy section headings, footnotes, or other copyrighted Church text. Link to them.
- Supernatural claims are claims of the text or of Joseph Smith in Historical mode. Faithful reading goes in the LDS lens with its Church source.
- Treat contested topics factually and even-handedly. These include plural marriage (132), the priesthood and temple restriction (OD 2), and the Missouri conflict.
- Record what you checked in each file's `reviewNote`. Do not claim review you did not do.

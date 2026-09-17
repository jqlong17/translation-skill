---
name: academic-epub-translator
description: Translates EPUB books from English or other source languages into polished Chinese while preserving EPUB structure, examples, citations, figures, notes, and terminology. Supports quality-first and speed-first translation modes. Use when the user asks to translate an EPUB, 翻译电子书, 翻译学术书, 分章翻译, or rebuild a translated EPUB, especially for academic, technical, linguistics, cognitive science, psychology, or language-processing books.
---

# Academic EPUB Translator

## Core rule

Translate from the actual complete EPUB, not from metadata, a summary, or isolated paragraphs. Preserve distinctions that carry evidence. Never translate an example when translating it would destroy the phenomenon under discussion.

## Translation mode switch

Choose one mode at the start of the task and record it in `TRANSLATION_STATE.md` as `translation_mode`:

- `quality` (default): smallest safe unit, usually one section; reread and back-check each batch; parse XML after each batch; run full EPUB validation at every chapter and after risky structural edits.
- `speed`: translate in larger coherent batches, usually 3-8 short sections or about 10-20 source pages; freeze the glossary after the first representative section; do one consolidated bilingual review per batch; parse XML after each batch; run full EPUB validation every 2-3 batches and at each chapter boundary.

Speed mode changes batching and review cadence, not evidence-preservation rules. It must still preserve examples, notation, IDs, links, images, tables, footnotes, and pagebreak markers. It must never become an uncontrolled whole-book translation pass.

Users can select a mode with wording such as `translation_mode=speed`, `用速度优先模式`, or `质量优先模式`. If no mode is specified, use `quality`.

## Locate the skill

Set `SKILL_DIR` to the directory containing this `SKILL.md`. Run bundled scripts by absolute path so the workflow does not depend on the current directory:

```bash
python3 "$SKILL_DIR/scripts/inspect_epub.py" ...
```

## Start or resume

1. Never edit the source EPUB.
2. If a translation work directory and `TRANSLATION_STATE.md` already exist, inspect them and resume there. Do not unpack the source again or overwrite approved work.
3. Otherwise inspect the source:

```bash
python3 "$SKILL_DIR/scripts/inspect_epub.py" "/absolute/path/book.epub"
```

4. Read the table of contents, introduction, one technical middle section, conclusion, OPF, navigation document, and representative XHTML markup.
5. Create `TRANSLATION_STATE.md` in the work directory from [PROGRESS_TEMPLATE.md](PROGRESS_TEMPLATE.md). Record:
   - provisional Chinese title;
   - audience and register;
   - terminology table;
   - rules for examples, glosses, citations, figures, notes, and index;
   - completed sections and unresolved decisions.
6. For a new book, translate one representative section and obtain user approval before translating the whole book.
7. Unpack only after selecting a new, nonexisting work directory:

```bash
python3 "$SKILL_DIR/scripts/unpack_epub.py" source.epub work/
```

## Production loop

Work in reading order. Use a translate -> check -> continue loop until the requested scope is complete. In `quality` mode, the default unit is one complete section. In `speed` mode, combine 3-8 adjacent short sections or roughly 10-20 source pages when they share the same topic and risk profile.

1. Read the full section, its preceding and following paragraphs, and all footnotes it references.
2. Classify each block as prose, linguistic evidence, quotation, notation, caption, table, or navigation text.
3. Translate prose directly in XHTML. Prefer targeted patches over XML reserialization.
4. Translate the section's headings, captions, alt text, cross-references, and notes in the same pass.
5. Preserve object-language examples and all evidential notation.
6. In `quality` mode, reread the Chinese without the source and back-check each batch. In `speed` mode, do one consolidated bilingual review after the larger batch, prioritizing headings, claims, examples, citations, terminology, and paragraph alignment.
7. Parse the changed XHTML immediately after each batch.
8. Update the glossary and `TRANSLATION_STATE.md` after each verified batch.
9. In `speed` mode, run full EPUB validation every 2-3 batches and at each chapter boundary; in `quality` mode, run it at each chapter boundary or after risky structural edits.
10. Continue with the next section or batch.

Do not translate the entire book in one uncontrolled batch. Do not use global replacement for ambiguous terminology.

## Speed and output hygiene

Prefer one visible current output file and a quiet checkpoint directory:

- Keep the main build at a stable path such as `translated-current.epub` or `<Chinese title>（当前译稿）.epub`.
- Put dated or section-specific checkpoint EPUBs under a `checkpoints/` or `archive/` directory, not beside the main deliverable.
- Use XHTML/XML parsing after every translated batch.
- In `quality` mode, use full EPUB packaging and source/target validation after each chapter, after risky structural edits, or before handoff.
- In `speed` mode, use full EPUB packaging and source/target validation every 2-3 batches, at each chapter boundary, after risky structural edits, and before handoff.
- For long chapters, never let a speed-mode batch exceed roughly 20 source pages without an XML parse and structural review.
- When a packager refuses to overwrite, either move the old current build to the checkpoint directory or use the bundled `package_epub.py --replace` option intentionally for the stable current build.

Do not leave many similarly named EPUBs in the user's working or downloads folder unless the user explicitly asks for every checkpoint to be visible.

## Repackage and validate

```bash
python3 "$SKILL_DIR/scripts/package_epub.py" work/ translated.epub
python3 "$SKILL_DIR/scripts/validate_epub.py" translated.epub --source source.epub
```

Use a new output filename for checkpoints. For a stable current-build filename, use `--replace` only when the existing output is intentionally superseded. Open the result and inspect the cover, title page, contents, changed chapters, figures, notes, navigation, and end matter.

## Translation standard

- Write clear contemporary Chinese suitable for an academic textbook.
- Preserve the author's degree of certainty: distinguish claim, proposal, evidence, tendency, possibility, and speculation.
- Preserve logical scope, negation, comparison, causal direction, quantifiers, and antecedents.
- Prefer established Chinese disciplinary terms. Do not vary a term merely for style.
- Remove avoidable translationese, but do not simplify away technical content.
- Preserve paragraph boundaries unless Chinese readability clearly requires a split.
- Keep author-date citations, bibliography entries, DOI, equations, variable names, and dataset/model names unchanged.
- Translate headings, captions, table labels, cross-references, alt text, and navigation labels consistently.
- Translate meaning rather than English surface syntax. Keep the author's direct, explanatory rhythm and restrained humor where present.
- Never strengthen `may`, `likely`, `suggest`, `evidence`, or correlational claims into certainty or causation.

## Example-specific rules

- Keep object-language examples in the original language when their form, order, morphology, ambiguity, acceptability, rhythm, rhyme, typography, code, or notation is evidence.
- Preserve `*`, `?`, `??`, `#`, subscripts, indices, brackets, traces, gaps, arrows, italics, boldface, and small caps.
- Add a Chinese meaning gloss only when it helps comprehension and cannot be mistaken for experimental material.
- Do not “correct” intentionally unacceptable, ambiguous, fragmented, noisy, or ungrammatical examples.
- Distinguish `sentence acceptability` from grammaticality unless the author explicitly equates them.
- Preserve dependencies and tree labels. Do not localize labels inside image figures during the first pass.
- For quotations whose exact wording is analyzed, retain the English quotation and append a Chinese translation.
- Translate the footnotes cited by a translated section in the same pass.

For linguistics or cognitive-science books, read [LINGUISTICS_REFERENCE.md](LINGUISTICS_REFERENCE.md) before translating. For other domains, create a short domain glossary in `TRANSLATION_STATE.md` before translating beyond the first representative section.

## EPUB preservation rules

- Never edit the source EPUB in place.
- Keep `mimetype` first and uncompressed when packaging.
- Preserve manifest/spine order and all non-text assets.
- Do not regenerate IDs or filenames unless necessary.
- Do not translate CSS, URL fragments, metadata identifiers, code, MathML operators, or image filenames.
- Bibliography entries remain in their publication language. Translate only the section heading.
- Keep the original index by default and label it `索引（原文）`; do not pretend its terms or page references form a valid Chinese index.
- Keep the original cover image byte-identical unless the user explicitly requests a new cover.
- Give draft/sample builds a new package identifier so ebook readers do not show a cached older edition.

## Quality gates

Before translating beyond the sample:

- terminology brief exists;
- example-treatment rules are explicit;
- sample demonstrates technical accuracy and natural Chinese;
- source EPUB passes archive inspection.

Before delivery:

- no missing spine document or asset;
- internal links and fragments resolve;
- XHTML/XML parses;
- source and target preserve IDs, images, figures, tables, notes, and pagebreak markers;
- no source paragraphs are silently omitted;
- no accidental translation of citations or linguistic notation;
- navigation and metadata identify the translated edition clearly;
- image assets are byte-identical to the source when the user requested original images;
- the cover and title page are visually checked at a phone/tablet-sized viewport;
- `TRANSLATION_STATE.md` matches the actual EPUB and names all unfinished material.

## Domain-specific initialization

If the skill directory contains a book- or domain-specific reference file for the current project, read it before translating that book. Treat any source examples, judgments, formulas, tables, figures, or code-like passages as evidence until classified otherwise.

# Site design: consulting the dictionary

*Agreed with the editor, 25 Sep 2026, from the clickable mockup "Abhidhāna site mockup"
(https://claude.ai/artifact/Saz4t8VTXkBzn5Hz9pMfGT, vol. 1 data). The mockup is a design
reference, not code to copy. This spec is a first version: expect further changes.*

## Principles

1. Most readers are Western students of Pāḷi who read no Burmese. The default view must be
   usable without Burmese script.
2. People arrive with a word: **search and the alphabet** are the ways in. Volumes and pages stay,
   as the scholar's view.
3. Nothing drafted is presented as a reading. Every article and every translation carries its
   status (ocr / drafted / reviewed / corrected).

## Layout (desktop)

- **Header**: title (romanised; Burmese title only when Burmese script is on), search box, menu
  **Browse · Volumes · Introduction · Labels · About**, EN/ES, and a **dark/light button**
  (sun/moon icon). The theme follows the system setting until the reader presses the button,
  then the choice is remembered. All colours are CSS variables with a light and a dark set; the
  page image is dimmed slightly in dark mode, never inverted.
- **Mode bar** under the header: reading mode (two modes, below), a printed-page switch, and a
  Settings button.
- **Browse** has up to four columns:
  1. **Alphabet pane** (left): the 40 letters in the dictionary's order
     (a ā i ī u ū e o, k kh g gh ṅ, c ch j jh ñ, ṭ ṭh ḍ ḍh ṇ, t th d dh n, p ph b bh m, y r l v s h ḷ),
     in roman, with Burmese beside each when Burmese script is on; each letter shows the volumes
     it covers. Under the chosen letter, two levels of thumb index: the next consonant
     (*ak-, ag-, ac- …*) then the syllable (*aka-, akā-, akko- …*) with entry counts. Order
     follows the book: niggahīta (ṁ) first, simple consonants before conjuncts.
  2. **Headword list**: the entries of the chosen syllable, windowed (earlier/later) for long runs.
  3. **Article** (below).
  4. **Printed page**: the scan of the article's page from the image server, with page
     back/forward and close. Off by default in the Pāḷi-reader mode; when off, the article takes
     the width and each article has a "See the printed page" button.
- **Phone**: one column; search pinned; alphabet as a drawer; printed page as an overlay.
  (Not in the mockup yet.)

## Reading modes and settings

| setting | Pāḷi reader (default) | As printed |
|---|---|---|
| Script for Pāḷi | roman | Burmese |
| Burmese definition | folded away (one tap to show) | shown |
| Grammatical labels | abbreviated in EN/ES (*v.*, *m.*) | as printed, (ကြိ) |
| Printed page | off | on |

Settings panel: script (roman / Burmese / both), Burmese definition (show / fold away / hide),
labels (as printed / abbreviated / spelled out), printed page (on / off). Changing one marks the
mode "custom". Remember the choices per browser (localStorage, wrapped in try/catch).

## The article

In this order:

1. Volume, PDF page, status label; "located approximately" for fuzzy matches.
2. Headword (roman and/or Burmese per setting), homonym number as a superscript.
3. Label, shown per setting; **tap** (never hover) opens its meaning, Pāḷi term and printed form,
   from `docs/labels.md` §0. Missing Spanish abbreviations fall back to the full Spanish word.
4. Analysis `[ … ]`, roman and/or Burmese.
5. **See / See also**: a Pāḷi span followed by ကြည့် (or လည်း ကြည့်) becomes a link to that headword.
6. **Meaning**: the EN or ES translation with its status; until one exists, an honest
   "not yet translated" note. Then the Burmese definition per setting, with the Pāḷi spans in
   the chosen script, and the OCR caveat.
7. **Pāḷi passages quoted** (when the Burmese definition is folded or hidden): the Pāḷi spans in
   roman as a list. Later: each paired with its citation.
8. **Citations** in roman (or Burmese); tap expands the abbreviation to the work's title via
   `docs/introduction/citation-abbreviations.tsv` (match on the abbreviation with spaces removed).
9. Previous / next headword, "Report an error".

## Search

Roman with or without diacritics (NFD, strip combining marks: *nana* finds *ñāṇa*), Burmese
script, prefix first then substring; results show headword, Burmese when that script is on, and
volume/page. Across all volumes: the existing `search.json` split per first letter so a lookup
loads one small file.

## Web addresses

- `/w/<romanised headword>` for an entry (homonyms `-2`, `-3`), linkable and citable.
- `/v/<book>/<pdf page>` stays for the page view.
- `/browse/<letter>/<syllable>` optional, for sharing a place in the index.

## Other pages

- **Volumes**: the 29 books as cards with range, headword count and pages.
- **Introduction** (`/introduction/`): built from `docs/introduction/*.md`; table of contents
  with status labels; EN/ES translation with the Burmese original one tap away; `[p. N]` markers
  link to the printed page; `citation-abbreviations.tsv` as a searchable table.
- **Labels** and **About** as now; About gains a History section from `docs/history.md`
  (correcting "compiled by the Masoeyein board" to the five teams of vol. 17 pp. 6–7).

## Open, for the editor

- Show drafted machine translations in the Meaning box (marked "drafted"), or only reviewed ones.
- Spanish label abbreviations (`docs/labels.md` §0).
- Whether the empty Meaning box stays visible before translations exist.

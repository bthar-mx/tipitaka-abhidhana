# Full-text search: finding words inside the articles (plan, 25 Nov 2026)

**Status: built 25 Nov 2026, v0.31.0 (brief §98).** `tools/abhidhana_fulltext.py`, called by `abhidhana_browse.py`; the list *In the
articles / En los artículos* in `assets/browse.js`; editor test step 10. Measured on the real build: 505,994 forms, 1,959,912 postings in
194,314 articles; 601 shards, 17.4 MB (largest 287 KB); 444 article blocks (`data/ft/d/`, 19 MB). Departures from the plan below: no
snippet in the result line (it would roughly double the index; the article opens with the Burmese definition shown and the word marked
instead); shards keyed by up to five letters, not three.

*Asked by the editor (25 Nov 2026): make every word in the PDFs findable, e.g. *sesa*. Planned, not built. Figures measured on the
committed data at v0.30.0 (`tmp/gap97/ftsize.py`, `ftshard.py`).*

## Why the headword search cannot do it

The site's search looks only at headwords (221,752 rows). Many Pāḷi words are not headwords: the printed dictionary has no *se-*
section at all (vol. 24 ends at *sūsū*, vol. 25 begins at *so*; brief §97), and inflected forms, compounds and quoted words occur
only inside other articles. *sesa* occurs in **50** articles, *avasesa* in 26, *pabbata* in 87.

## What would be searched

The romanised Pāḷi that `abhidhana_romanise.py` already finds inside the Burmese bodies (`pali.jsonl` → `pali[].iast`): **657,692**
passages in 221,752 articles, **508,418** distinct word forms, **2,083,668** (word, article) pairs; 339,876 forms occur in one article
only, 127 in more than 1,000. Not searched, at least at first: the Burmese text itself, the Spanish and English drafts, the citations.

Limits to state on the page: the passages are those the span finder recognised (Pāḷi attested in OSBCT, brief §31–37); a quotation the
OCR damaged may be missed or misspelt; nothing is proofread.

## Design: a static index beside the headword shards

- **Build** (`tools/abhidhana_fulltext.py`, called by `abhidhana_site.py`): one inverted index `{form: [article ordinals]}`, ordinals
  delta-coded in base 36, sharded by the first two letters of the folded form (the fold of `common.js`, diacritics off, as in the
  headword search). Measured: **331 shards, 18.9 MB (7.0 MB gzipped)**, median 2 KB, 95th percentile 274 KB, largest 1.96 MB: shards
  over ~300 KB split by a third letter. Static files on Cloudflare Pages: no Function, no database, cached like `data/s/`.
- **Pointers**: postings hold the record's ordinal in Browse order, so a hit resolves through the chunk files the site already serves
  (`data/c/`), with no extra id map; a small `data/ft/meta.json` gives the shard splits and the build's version.
- **Matching**: whole word form and word prefix (typing *sesa* finds *sesa, sesaṁ, sesato …*), folded like the headword search; Burmese
  typed into the box converted with the site's roman converter. Inflection-aware matching (one lemma → all its forms) is a later step
  (DPD's inflection tables, as in Padakosa), not in the first version.
- **Page**: the search keeps its headword list first; below it a second list, *En los artículos / In articles (N)*, each hit as headword,
  vol. · p., and a short snippet (±40 characters) with the word marked; a click opens `/w/<address>` with the passage highlighted.
  Results in dictionary order; forms in more than ~2,000 articles show the count and the first 200 hits.
- **Tests**: a step in `site/test/editor/ui-test.js` (*sesa* finds ≥ 50 articles, the snippet marks the word, the link highlights it);
  a build check that every posting resolves to a record.

## Steps

1. The builder and the shard measurement on the real build (cloud session; it needs only committed data).
2. The page: the second list, snippets, highlighting, ES / EN strings (cloud session).
3. The editor tests on the Mac; the live check; brief section, VERSION (MINOR: a new site feature), CHANGELOG.

## Decided (the editor, 25 Nov 2026)

1. **Pāḷi only**: the Spanish and English drafts are not searched.
2. **Hits in dictionary order.**
3. **The commentary abbreviations** (the editor took the recommendation, 25 Nov): leave out the Pāḷi passages that lie inside a parsed
   citation, and nothing by frequency. Measured (a passage's Burmese found in the article's citation text, a rough test): of 55,181
   occurrences of *ṭṭha*, 32,486 are inside a citation; of *ca* 2 in 25,294, *na* 19 in 23,081, *ti* 3 in 25,878, *vā* 3 in 19,266,
   *sesa* 0 in 51, *pabbata* 0 in 96. A frequency cut-off would drop real words (*ca*, *na*, *vā*); the citation test drops almost only
   abbreviations. For the rest (citations the parser missed), a short stop-list of abbreviation fragments that are not Pāḷi words
   (*ṭṭha* …), taken from `docs/citation-abbreviations.tsv` and listed in the builder for review.

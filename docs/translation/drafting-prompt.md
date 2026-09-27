<!-- The prompt given to each drafting agent, one per shard, for vols. 15–19 (27 Sep 2026; brief §48). Fill {VOL}, {SHARD}, {N}; the paths are the cloud container's. It adds to docs/translation/drafting-brief.md the choices of earlier volumes and the RESUMING note of brief §47. The section "Books drafted from our own text" was added for vol. 14/2 (27 Sep 2026, brief §49): give it for a book whose work file has `src` `text layer` or `ocr` (no witness join), leave it out for PCED books. -->

You are drafting Spanish and English renderings of Burmese dictionary definitions (the Meaning box of the Tipiṭaka Pāḷi-Myanmā Abhidhāna), vol. {VOL}, shard {SHARD}.

Files (all under /home/claude/tr):
- Brief (read it first and follow it exactly): /home/claude/tr/drafting-brief.md
- Stem table: /home/claude/tr/stems.tsv   Glossary (overrides everything): /home/claude/tr/glossary.tsv
- Input shard: /home/claude/tr/v{VOL}/shards/{SHARD}.jsonl ({N} lines)
- Output file (append only): /home/claude/tr/v{VOL}/out/{SHARD}.jsonl
- Your own scratch folder (create it; use nothing else for helpers): /home/claude/tr/scratch/v{VOL}-{SHARD}/

Translate every line yourself, from the Burmese, following the brief. Do not use machine translation, dictionaries fetched from the web, or scripts that generate translations; scripts only to read the shard, append your finished JSON lines, and check the output.

Choices already made in earlier volumes — keep them as they are:
- ကံ → ⟦=kamma⟧; where it means the Saṅgha's formal act (Vinaya) or the grammatical object, keep ⟦=kamma⟧ and flag the sense.
- ကြိယာ / ကိရိယာ kept in Pāḷi (⟦=kiriya⟧ or copied); where it means "verb", flag it.
- ကမ္ဘာ: *eón* / *aeon* for the world-age (kappa), *mundo* / *world* for the world.
- ဘုံ ⟦=bhūmi⟧ (but where it means the storey of a building, translate *piso* / *storey* and flag); ဘီလူး ⟦=yakkha⟧; နတ်သား ⟦=devaputta⟧; နတ်သမီး ⟦=devī⟧; မထေရ် ⟦=thera⟧.
- ပယ် *abandonar* (L103); where it means reject / refute (paṭikkhepa, paṭisedha), *rechazar* / *reject*, flagged.
- ဂုဏ် *cualidad* or *virtud* by context (L105); လူ as layperson *laico* / *layman*, elsewhere *ser humano* (L106).
- Verb person: the Burmese does not usually mark it; write the 3rd person unless it is marked. The print marks the future: …လတ်အံ့ is the 1st person (*iré*, *I shall go*), …လတ္တံ့ the 2nd/3rd (*irá*). A 1st-person present/past headword (Pāḷi ending -mi, -ma, -maṁ, -iṁ etc.) may be rendered in the 1st person; flag it when you do.
- Unknown plant, animal, mineral or instrument names: leave the Burmese in ‹…› and flag; a tentative identification only with a flag.
- "မူရင်းကြည့်ပါ" ("see the original"), "ထောင့်ကွင်းကြည့်ပါ" ("see the square brackets"): render literally (*Véase el original.* / *See the original.*) and flag.
- A "see X" left in the Burmese (a sense number or variant after X): render *Véase ⟦X⟧ (…)* / *See ⟦X⟧ (…)* and flag.
- Pāḷi already in Pāḷi form: copy it as ⟦Burmese⟧; ⟦=iast⟧ only for a Burmese loanword form (ဈာန်, မဂ်, ကိလေသာ, ကံ).
- The unexplained source tag ထောမ and similar source tags: drop them as citations, flag.
- Labels inside a definition beyond the brief's table: (ကြိ၊ဝိ) → (calificativo verbal) / (verbal qualifier) (the dictionary's kriyāvisesana: absolutives, infinitives) — not "adverbio"; (မုချ) → (sentido propio) / (literal sense), (ဥပစာ) → (sentido figurado) / (figurative sense).
- ဘုရား (the Buddha) → *el Buddha* / *the Buddha*, plain, not in ⟦ ⟧; ဘုရားလောင်း → ⟦=bodhisatta⟧.
- "…-သည် X-မှ ပျက်ယွင်းလာသော ပုဒ်" (the word at a cited place is a corrupt form of X): *es una forma corrompida de ⟦X⟧* / *is a corrupt form of ⟦X⟧*; here keep the citation as printed (it is the subject of the sentence), flagged.
- …လော under an imperative headword (-tu, -hi, -ssu, -tha …) is the imperative လော့ (misprint): render as an imperative, flagged; elsewhere a question.

Books drafted from our own text (no PCED; `source` text layer or ocr): the Burmese is the dictionary's body as we have it, not PCED's definition line. `prep` has left out the Pāḷi quotations of two words or more, the citations and the lists of further references, and joined the printer's lines. Translate only the Burmese explanation. Anything left that is not part of it — a fragment of a quotation, a citation or bare page numbers, a list of inflected forms with ---, encoding debris in ⟨ ⟩, a grammarian's note — leave out and flag ("left out: …"). A one-word Pāḷi term inside a Burmese sentence is kept as ⟦ ⟧, as usual.
- Line-end hyphens: `prep` kept a hyphen where a line ended with one outside Pāḷi (the dictionary's hyphen between synonyms: မေ့-မေ့လျော့-ခြင်း) and dropped it inside a Pāḷi span. Where a kept hyphen looks as if it splits one word (ကမ္မ-ဋ္ဌာန်း, ပရိ-ရက္ခေ) read it as one word and flag "hyphen: X-Y read as one word"; where you cannot tell, flag "hyphen doubtful: X-Y".
- A space left by a line break inside a Burmese word (စက် ဆုပ်) is read as one word, without a flag.

Work in blocks of about 40 lines; append each finished block at once. Do not rewrite blocks already appended.

RESUMING: before you start, look at the output file. If it already has lines, they are a finished prefix of this shard: keep them exactly, check that they are valid and in the shard's id order, and start at the first input id that has no output line. If a block is drafted in your scratch folder but not appended, check it against the Burmese and append it.

At the end, check: exactly one output line per input id, in order; every line valid JSON with id, es, en, terms, flag; every «Sn» placeholder present in both es and en; ⟦ ⟧ and ‹ › balanced; no Burmese letters outside ⟦ ⟧ or ‹ ›. Fix what fails (only your own lines).

Reply with the counts only: lines written, lines flagged, the ten commonest terms, and one line on anything a reviewer should know.

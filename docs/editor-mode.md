# Editor mode

*Built 27 Sep 2026 (brief §52, v0.17.0). For one user, the editor. Not yet switched on: the steps in §2
are done by the editor in the Cloudflare dashboard.*

The editor corrects the site in place: in Browse, each article gets an **Editar** button with a form for the
Meaning (Spanish, English, the status of the Spanish, whole or by sense) and the article's fields (headword,
label, analysis, body, in Burmese). A save goes to a small database (Cloudflare D1); every visitor's page lays
the saved edits over the published data, marked *corregido* / *revisado*. The edits reach the repository only
when `tools/abhidhana_edits_export.py` writes them into `docs/translation/meanings/NN.jsonl` and
`docs/corrections.tsv` (§5).

| path | who | what |
|---|---|---|
| `/edit/` | the editor (Cloudflare Access) | switches editor mode on in this browser; the history of edits |
| `/api/admin/whoami`, `/api/admin/edits` | the editor (Access, and the function checks the Access token itself) | who is signed in; save, withdraw, history |
| `/api/edits?book=NN` | everyone | the latest saved edit per id + field + sense of a book; `book=all` for the export |
| everything else | everyone | unchanged; a visitor never loads the editor's script |

Code: `functions/` (Pages Functions: `api/edits.js`, `api/admin/_middleware.js`, `api/admin/edits.js`,
`api/admin/whoami.js`, `_lib/access.js`, `_lib/edits.js`), `site/d1/schema.sql`, `site/src/edit/`,
`site/src/assets/editor.js`, `editor.css`, `edit.js`, `roman.js`, the overlay in `browse.js` (`ov()`),
`tools/abhidhana_edits_export.py`, the tests in `site/test/editor/`.

## 1. What each part does

- **Access** (Cloudflare Zero Trust) asks for the editor's sign-in (a one-time PIN by e-mail by default) at
  `/edit/` and `/api/admin/`, and passes a signed token (`Cf-Access-Jwt-Assertion`) to the site.
- **The write API verifies that token itself** (`functions/_lib/access.js`: RS256 against the team's keys at
  `<team>/cdn-cgi/access/certs`; audience = `ACCESS_AUD`; issuer = `ACCESS_TEAM_DOMAIN`; not expired; the
  e-mail in `EDITOR_EMAILS` if that is set). Without a valid token it answers 401/403; without the settings,
  503. So a missing or wrong Access rule, or the project's `*.pages.dev` address (which Access does not cover),
  does not leave the API open. A write must also come from the site's own pages (same `Origin` and an
  `X-Abhidhana-Editor: 1` header, which a cross-site form cannot send).
- **The database** keeps every save. The site shows the latest row per id + field + sense; a row with status
  `reverted` withdraws the edit, and the published text shows again.
- **Browse** asks `/api/edits?book=NN` once per book, when an article of that book is first shown (cached 60 s
  at Cloudflare's edge; a save clears its book's entry). If the request fails, the page shows the published
  data as before.

## 2. Switching it on (the editor, in the Cloudflare dashboard)

Between the push of v0.17.0 and these steps, `/edit/` is an ordinary page that says the editor API is not set up,
`/api/admin/` refuses everything (503) and `/api/edits` answers 503, which Browse ignores.

Cloudflare renames its menus often; the names below are those of September 2026. In this order:

**A. The database**
1. *Storage & Databases → D1 SQL Database → Create*: name `abhidhana-edits`.
2. Open it, tab *Console*, paste the two statements of `site/d1/schema.sql` (the `CREATE TABLE` and the
   `CREATE INDEX`) and run them. (Or in Terminal: `npx wrangler d1 execute abhidhana-edits --remote --file site/d1/schema.sql`.)

**B. The Access application**
3. *Zero Trust → Access → Applications → Add an application → Self-hosted*. Name: *Abhidhāna editor*.
   Session duration: 24 hours (or as preferred).
4. Destinations (public hostnames): `abhidhana.buddha-dhamma.net` with path `edit`, and a second one,
   `abhidhana.buddha-dhamma.net` with path `api/admin`. (A path covers what lies below it; the check in step
   12 shows whether it does.)
5. Policy: *Allow*, include *Emails* = the editor's address. Login method: One-time PIN (the default) or
   any other already set up.
6. Save. On the application's page, copy the **Application Audience (AUD) Tag**. In *Zero Trust → Settings*,
   note the **team domain** (`<team>.cloudflareaccess.com`).

**C. The Pages project** (*Workers & Pages → the abhidhana project → Settings*)
7. *Build*: check that the **root directory** is the repository's root (empty or `/`): Pages looks for the
   `functions/` folder there. Build command and output stay as they are (`python3 tools/abhidhana_site.py`,
   `site/dist`).
8. *Bindings → Add → D1 database*: variable name **`DB`**, database `abhidhana-edits`. Production only.
9. *Variables and Secrets → Add* (Production), as plain text or secrets:
   - `ACCESS_TEAM_DOMAIN` = `https://<team>.cloudflareaccess.com` (with `https://`, no trailing slash)
   - `ACCESS_AUD` = the AUD tag of step 6
   - `EDITOR_EMAILS` = the editor's address (optional, recommended: a second check beside the Access policy)
10. Redeploy (*Deployments → the latest → Retry deployment*, or push): bindings and variables apply from the
    next deployment.

**D. Checks** (a private window first)
11. `https://abhidhana.buddha-dhamma.net/api/edits?book=18` → `{"book":"18","n":0,"edits":[]}`.
12. `https://abhidhana.buddha-dhamma.net/edit/` → Cloudflare's sign-in page, not the site. Also
    `…/api/admin/whoami` → the sign-in page.
13. `https://<project>.pages.dev/api/admin/whoami` → `{"error":"no Access token"}` (401): the function's own check.
14. Sign in at `/edit/`: it says *Sesión iniciada como …* and the history (empty). That page calls
    `/api/admin/whoami`, so this also shows that the sign-in covers `/api/admin/`.
15. *Consultar, con los botones Editar* → an article → *Editar*; change nothing and *Guardar* (→ *No ha
    cambiado nada*); then correct something small, see it marked on the page, open the page in another browser
    (it shows there too), and *retirar la edición*.

If step 14 says the API is not set up: 503 means a variable of step 9 is missing; "no database bound", step 8;
"wrong audience" or "wrong issuer", step 9's values.

## 3. Using it

- `/edit/` switches editor mode on **in that browser** (it remembers it) and lists the history, newest first;
  *Salir del modo editor* switches it off; *Cerrar sesión* signs out of Access. When the Access session has
  expired, Browse shows *Modo editor: no ha iniciado sesión* with a link back to `/edit/`.
- **Meaning.** *Español* and *Inglés* hold the source markup of `docs/translation/drafting-brief.md`
  (`*pāḷi*`, `[[iast]]` for "véase", `‹…›` for kept Burmese). A new Spanish text counts as *corregido*.
  *Estado del español*: *borrador*, *revisado* or *corregido*; with *sentidos* blank it applies to the whole
  Meaning; `1` or `1,3` makes it apply to those senses only (shown as *corregido en parte* / *revisado en
  parte*, with the senses named). A status saved at the same time as, or after, the text replaces the text's
  *corregido*. English has no status of its own: an English edit is *corrected*.
- **The article** (Burmese, as printed; the label without brackets, the analysis without `[ ]`). Type with
  a Myanmar **Unicode** keyboard; the form refuses these fields without Burmese letters. The headword, label
  and analysis show a **live roman preview** (`site/src/assets/roman.js`, a port of the Aksharamukha
  transliteration `tools/abhidhana_romanise.py` uses; the body has none, being Burmese prose with Pāḷi in it).
- **Roman input** (brief §53). The headword, label and analysis each have a switch *Birmano / Latín*. In
  *Latín* the field is typed in IAST (`omaka + patta`, `ti`, `pu,thī`, `na + kataludda. akata + ludda`) and the
  form converts it to Burmese script (`ROMAN.burmese` in `roman.js`, a port of Aksharamukha's IAST → Burmese).
  `+`, spaces, brackets and `-` stay; `.` becomes ။, `,` ၊, digits Burmese digits; `ṃ` is read as `ṁ`, `ḷ` as
  `l̤`. Under each field, in both modes: **se guarda** (the Burmese that will be stored) and **relectura** (its
  roman read-back through `roman.js`). In *Latín*, *Guardar* is disabled, and a save refused, while the read-back
  differs from what was typed (a capital, a letter it does not know such as `ṛ`, a letter left Latin): fix the
  roman or switch the field to *Birmano*. What is stored is always the Burmese. A field switched to *Latín* and
  not changed is not an edit, even when its Burmese would not come back identical (malformed OCR). The mode is
  kept per field in this browser (`localStorage` `abh-ed-mode-headword`, `-label`, `-analysis`).
  **Not visible in the read-back** (two Burmese spellings read the same in roman): the tall or round ā (ါ / ာ;
  the converter writes Aksharamukha's choice, e.g. သမ္ပာ where most volumes print သမ္ပါ), ဿ / သ္သ, ည / ဉ္ဉ,
  kinzi (င်္) / င္. And roman input is for Pāḷi: a Burmese word typed in roman is written as Pāḷi (stacked
  consonants, no ်), which the read-back does not show. Check the *se guarda* line, or use *Birmano*, for those.
- *retirar la edición* beside a field withdraws its edit (a new row, status `reverted`): the published text
  shows again. Nothing is ever deleted from the database.
- Until the export and the article step (§5), an edited analysis is romanised in the browser, an edited body
  shows without its Pāḷi spans in roman, and a `[[x]]` in an edited Meaning shows in italics, not as a link.

## 4. The database

`site/d1/schema.sql`: `edits(id, book, field, sense, value, old, status, date)`.

| column | |
|---|---|
| `id`, `book` | the article (index row id) and its book (`01`…`25`, `4a`–`4c`, `14b`, `14c`) |
| `field` | `es`, `en`, `status`, `analysis`, `label`, `body`, `headword` |
| `sense` | `status` only: `''` for the whole Meaning, or `1`, `1,3` |
| `value` | the new text; for `status`: `reviewed`, `corrected` or `drafted`; `''` when withdrawn |
| `old` | what the page showed before the save (so the export can tell if the repository has moved since) |
| `status` | the row's own state: `saved`, or `reverted` (withdraws the edit) |
| `date` | UTC, ISO 8601 with milliseconds, set by the server |

The latest row per id + field + sense counts (by insertion order, SQLite's `rowid`). No personal data is
stored: not the e-mail, not a name.

Free-plan limits (September 2026): 100,000 Function requests a day, 5 million D1 rows read a day. A visitor's
Browse makes one `/api/edits` request per book opened, kept 60 s at the edge; far inside both.

## 5. From the database to the repository

On the Mac, in `~/Documents/abhidhana`:

```sh
npx wrangler d1 export abhidhana-edits --remote --output ~/Downloads/edits.sql
python3 tools/abhidhana_edits_export.py --d1 ~/Downloads/edits.sql            # what would change
python3 tools/abhidhana_edits_export.py --d1 ~/Downloads/edits.sql --write
```

(`--summary FILE` also writes what changed as JSON: books, fields, the books to re-run. `--api` reads the live site's `/api/edits?book=all` instead; the export file is better, as it holds the
whole history, and the tool then checks each field against what the page showed before its *first* save.)

The tool writes `es` / `en` / status into `docs/translation/meanings/NN.jsonl` (the draft kept in
`es_drafted` / `en_drafted`; `corrected_es` / `reviewed_es` = {by IEBH, date, senses}), each Spanish
correction also into `docs/translation/corrections-es.tsv`, and the article fields into
`docs/corrections.tsv` (`ocr` = the OCR reading, `by` IEBH). It prints the books whose article step must be
re-run, in this order: `python3 tools/abhidhana_articles.py NN && python3 tools/abhidhana_romanise.py NN`.
Then VERSION, CHANGELOG, commit, push, tag, as for any change. A second run writes nothing. The rows stay in
D1 afterwards (the history); laid over the rebuilt data they change nothing. A withdrawn edit that had been
exported before is reported, not removed: take its line out by hand.

## 6. Testing locally

`sh site/test/editor/run.sh` builds the site into a temporary folder, serves it with `wrangler pages dev` and
an empty local D1, stands in for Access (`access-mock.js`: its own signing key, a token minted per request),
and runs `api-test.js` (the token checks, validation, history, latest per key, withdrawal) and `ui-test.js`
(a visitor, the API down, the editor's form, `/edit/`, a phone width, the roman input). Needs node, `npx` and
Playwright (in a cloud session: `PLAYWRIGHT=/opt/node22/lib/node_modules/playwright CHROME=/opt/pw-browsers/chromium`).
`node site/test/roman/roundtrip.js` checks the roman input's round trip on every headword and every PCED analysis
without a derivation (`--tsv FILE` writes the failures, `--list KIND` prints one kind).

## 7. Not covered

- The page view (`/v/<book>/<page>`) and the Reader artifact show the published data only.
- The search list and the alphabet use the published headword; an edited headword shows in the article and
  the headword list.
- One editor. More would need a `by` column; the Access policy and `EDITOR_EMAILS` already take a list.

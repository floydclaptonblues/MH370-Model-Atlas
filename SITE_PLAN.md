# Atlas restructure plan (branch `claude/atlas-rebuild`, for review — nothing published)

Five sections, replacing the current flat chapter list:

1. **Home** — headline: *"The flight histories and terminal envelope recovered within our MH370 world model."*
   The two incoming clusters and their terminal lobes, from the published catalogue; standing qualifications;
   plain statement of scope (the envelope covers exactly the stated model, histories, response families and
   tests — not every mathematically possible BTO/BFO-compatible flight). Population labels used consistently:
   6 incoming histories / 98 baseline response identities / 128 displayed Mach-0.89 records / 424 registered
   candidates / 68 floor-ending branches, with the dossier's definitions.
2. **The Flight Histories** (primary) — follow one aircraft through the recorded sequence: clock conventions,
   turns, Mach schedule, fuel and decreasing mass, atmosphere, arc-by-arc SATCOM comparisons, terminal branch;
   then inspect the data. "Export a saved flight" block: the reader, exact branch identifiers, expected counts,
   archive checksum — stated as reproducing the retained records, **not** rerunning the physics. Floor-ending
   paths reported at the **terminal reporting endpoint** convention, original event labels and heights in the
   detail.
3. **Canonical Data** (secondary focus, own front door) — original observations and supplied datasets
   distinguished from normalized tables, conventions and calculated outputs; each with source, version/date,
   hash where available, role. Consistency item: names the same ocean-forcing product and version as the drift
   pages. The 249 MB dossier stays outside the repository; the site carries its identity, checksum, audit
   record, and a download link once a public location exists.
4. **Archive of Attempts** — from `ARCHIVE_INVENTORY.md`/`.csv` after review; four outcomes explained in
   ordinary language; original committed records preserved and linked; withdrawn conclusions removed from the
   current-results presentation.
5. **Methods / how the work is checked** — condensed; includes the retained BFO convention and the "run it
   yourself" distinction (reproduce retained records vs rerun a calculation from pinned code and inputs, each
   offered where it genuinely applies).

**Held fixed:** `drift.html`–`drift4.html` and `currents.html` unchanged until the investigator reviews them;
Drift and Drift Runs keep their own pages in the navigation. The 32.355°S 97.4°E point appears as a point
marker labelled *"Proposed location; originating run and evaluation status awaiting verification"* — no
footprint, not attributed to any history, no Atlas claims until the A/B experiment results are reviewed.

**Presentation:** Windows 98 visual language carried over from the existing `design/windows-98-atlas` branch
(`docs/windows98-theme.md` + its `common.css` layer) applied to the **current** page tree — that branch itself
is stale (missing the newer pages) and will not be merged. Readable scientific figures, comfortable contrast,
meaning never carried by red-vs-green alone. All pages generated through `gen.py` from `src/`.

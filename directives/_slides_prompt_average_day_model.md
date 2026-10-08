# Prompt — slides for the MH370 Average Day Model walkthrough

Paste everything below the line into the engine/fuel thread where the Average Day Model artifact is being compiled.

---

## TASK: build a slide deck that shows the Average Day Model running, step by step

I need a slide deck for a screen-recorded walkthrough (private YouTube video) demonstrating how this program works. The audience is technically literate but has not seen the code. They should finish the deck able to describe, in their own words, what the program takes in, what it does to it, and what it reports.

**This is a mechanics deck, not a conclusions deck.** The subject is the pipeline — how one candidate flight is constructed, flown, scored and fuel-checked. Findings appear only where they illustrate the mechanics (e.g. one worked example's score), never as the point of a slide.

### Build it from the repository, not from memory

Every number, variable name, file path and function name on a slide must be read out of the actual project files in this run folder. Where you cannot find a number, put `[UNVERIFIED — not found in repo]` on the slide rather than a plausible value. Where a figure already exists as a PNG in the project, reference it by path instead of describing a new one. List at the end, in a build log, which file each quoted number came from.

### Deck structure

Target **14–18 slides**. One idea per slide. Titles are statements, not labels ("The score has nine terms", not "Scoring").

**Part 1 — What the program is (2 slides)**

1. What it does in one sentence: given a starting position, time, heading, speed and altitude command, it flies a 777-200ER forward through real archived weather and reports how well the resulting track matches the Inmarsat satellite handshakes, and whether the fuel lasts.
2. What it is not: not a search, not a locator, not a statement about where the aircraft is. It evaluates a commanded flight hypothesis and returns a number.

**Part 2 — Inputs (3–4 slides)**

3. The satellite observations. The BTO and BFO values actually scored, with their times and their stated uncertainties (σ_BTO and σ_BFO — read these from the burst configuration file, do not assume). State explicitly which observations are scored and which are present but not scored.
4. The weather. Which reanalysis product, which variables, which pressure levels, which time steps, and the **exact domain bounds as the loader sees them**. This slide matters — the domain is a real limit on what the program can represent, and the deck should say so plainly here rather than hiding it.
5. The aircraft model. Fuel flow and performance tables: where they come from, what regime they are supported in, and where the model substitutes a proxy. Name the proxy and say it is flagged unsupported in the code.
6. The command vector. The handful of numbers that define one candidate: start position, start time, bearing, Mach (or Mach schedule), pressure altitude, starting fuel. Show a real one.

**Part 3 — One flight, end to end (4–5 slides). This is the core of the deck.**

7. Integration. The timestep actually used, the integration scheme, and what the aircraft is told to hold constant (and what therefore drifts). Show the first few steps of a real flight as a table: time, position, heading, ground speed, fuel remaining.
8. Where weather enters the step. Wind and temperature are sampled and resolved into ground speed and track; the slide should show that force/weather evaluation is the dominant cost per step — quote the measured per-flight timing split from the benchmark in the repo.
9. Geometry at each handshake time. How the model gets from an aircraft position to a predicted BTO and BFO: slant range to the satellite, the round-trip delay, and the Doppler terms. Name the compensation convention in use and cite it (Holland, arXiv 1702.02432v2, §IV-A/IV-B) rather than describing it as an assumption of this project.
10. The score. Sum of squared standardised residuals over the nine scored terms. Show the formula, then show a real residual table for one flight: observation, observed, predicted, residual, residual in σ, z².
11. Fuel. Burn integrated along the same track to exhaustion, and what the program does at the exhaustion time. State what the fuel model does and does not include (one tank feeding both engines; whether any single-engine phase exists).

**Part 4 — Searching over commands (2–3 slides)**

12. The optimiser: what it varies, what it holds fixed, what the bounds are, and how a bound shows up in the result as an active constraint.
13. The frozen reference flight. Use the project's own primary reference case as the worked example: its score, its residual table, how many constraints are active, and which parameters sit at a bound. Say plainly that a solution pinned at a bound is a constrained optimum, not a free one.
14. The grid sweep mode: how the program evaluates many starting points on a coarse grid instead of refining one, and the cost per flight that makes grid resolution a budget decision rather than a preference.

**Part 5 — What the program reports and what it refuses to (2–3 slides)**

15. Outputs: the files written per run, and what each contains.
16. Guard rails built into the pipeline: no parameter is ever tuned toward the 7th arc or any flight path; declared thresholds are fixed before a run and reported as failed rather than adjusted; the satellite and drift branches are kept separate and no model coordinate crosses between them. Give one concrete example from the record of a declared gate that failed and was reported.
17. Closing slide: what a good score means and what it does not. A low χ² means a commanded flight exists that is consistent with the handshakes under this model's assumptions. It does not mean the aircraft flew it.

### Honesty constraints — these are hard, and they apply to every slide

- **No slide may present any model position as a location of the aircraft.** Positions are conditional model states. If a coordinate appears, the slide says what it is conditional on.
- **Do not present contact or endpoint coordinates as debris locations or as search recommendations.**
- Where a model region is not covered by the forcing data, say "not modellable here" — never "excluded" or "ruled out".
- Where an input is assumed, inherited or unverified, label it on the slide. Do not smooth it into a citation it does not have.
- Do not round a figure to make it look cleaner than it is, and do not quote a precision the input does not support.
- No slide claims the investigation reached a conclusion about where the aircraft went.

### Format

- 16:9. Large type — this will be read on video, possibly on a phone. No slide carries more than about 40 words of body text plus one table or figure.
- Every number on a slide is also in the speaker notes with its source file, so I can say it out loud correctly.
- Speaker notes: 3–5 sentences per slide, written as spoken narration, not as a second copy of the slide.
- Tables: at most 6 rows and 5 columns on a slide. Split a longer table across slides rather than shrinking the type.
- Monospace for variable names, file paths and function names.
- No stock imagery, no decorative backgrounds, no logos.

### Deliverables

1. The deck.
2. `slide_sources.csv` — one row per quoted number: slide number, the number as shown, the file it was read from, and the line or key.
3. A short list of any slide you had to mark `[UNVERIFIED]`, so I can decide whether to cut the slide or go find the number.

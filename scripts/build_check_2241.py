#!/usr/bin/env python3
"""Compile the published tables of the 22:41 check for the Atlas pages.

Reads committed CSV/JSON files only. No model import, flight calculation,
fitting or satellite prediction is performed here. Every number shown about
the 22:41 check is produced from the copied source tables and inserted by
gen.py; none is typed into a page.

    python3 scripts/build_check_2241.py           write source_manifest.json, display.json, validation.json
    python3 scripts/build_check_2241.py --check   verify sources and committed outputs; write nothing
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import html
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "check-2241-266"
SRC = OUT / "sources"
TERMINAL = ROOT / "data" / "terminal-responses-266" / "sources"
REPO = "floydclaptonblues/MH370-Ocean-GLORYS-Data"
COMMIT = "18dcd823ab6a5e47004b9596325149618578c240"
SOURCE_PATH = "reports/diagnostic/CHECK_2241_CRUISE_266"
REVISION = "91266581e659"
CRUISE_REVISION = "2a016b1294fa"
IMPORTED_ON = "2026-11-18"
# name -> directory below SOURCE_PATH
FILES = {
    "STAGE_B_RESULTS.csv": "STAGE_B_OUTPUT_91266581e659/", "STAGE_B_BY_GROUP.csv": "STAGE_B_OUTPUT_91266581e659/",
    "STAGE_B_SUMMARY.json": "STAGE_B_OUTPUT_91266581e659/", "LOCAL_REPRODUCTION.json": "STAGE_B_OUTPUT_91266581e659/",
    "STAGE_B_FINDINGS.md": "stage_b_results_9a67641/", "RECEIVED.md": "stage_b_results_9a67641/",
    "TERMINAL_OVERLAP.json": "stage_b_results_9a67641/evidence/", "RECONCILIATION.json": "stage_b_results_9a67641/independent/",
    "PREDICTIONS_2241_266.csv": "run/91266581e659/", "STAGE_A_REPORT.json": "run/91266581e659/", "STAGE_A_SEAL.json": "run/91266581e659/",
    "PROTOCOL.md": "", "STAGE_A_FINDINGS.md": "", "GATE_FINDINGS_91266581e659.md": "",
}
# incoming group label -> (pressure altitude of the arrival at 19:41 in ft, Mach)
GROUPS = collections.OrderedDict([
    ("365.113 hPa, Mach 0.67", (25661, "0.67")), ("365.113 hPa, Mach 0.75", (25661, "0.75")),
    ("331.655 hPa, Mach 0.67", (27830, "0.67")), ("331.655 hPa, Mach 0.75", (27830, "0.75")),
    ("300.9 hPa, Mach 0.75", (29987, "0.75")), ("300.9 hPa, Mach 0.78", (29987, "0.78")),
])
MEETS, OUTSIDE = "MEETS_THE_2241_TIMING", "OUTSIDE_THE_2241_TIMING_BAND"
MINUS = "−"
M_PER_US = 299792458.0 * 1e-6 / 2.0          # metres of aircraft-to-satellite distance for one microsecond of round-trip timing
NEAR_US = (1.0, 5.0)          # round distances from the band edge used to describe how close the two labels lie; they set no label


def read(name, base=SRC):
    with open(base / name, newline="") as f:
        return list(csv.DictReader(f))


def n(i):
    return f"{int(i):,}"


def sgn(x, d=2):
    s = f"{abs(x):.{d}f}"
    return s if float(s) == 0 else (MINUS if x < 0 else "+") + s


def compile_display():
    checks = []

    def ok(name, cond, detail=""):
        assert cond, f"reconciliation failed: {name} {detail}"
        checks.append(name)

    rows = read("STAGE_B_RESULTS.csv"); groups = read("STAGE_B_BY_GROUP.csv"); pred = read("PREDICTIONS_2241_266.csv")
    summ = json.loads((SRC / "STAGE_B_SUMMARY.json").read_text()); seal = json.loads((SRC / "STAGE_A_SEAL.json").read_text())
    rep = json.loads((SRC / "STAGE_A_REPORT.json").read_text()); over = json.loads((SRC / "TERMINAL_OVERLAP.json").read_text())
    rec = json.loads((SRC / "RECONCILIATION.json").read_text()); loc = json.loads((SRC / "LOCAL_REPRODUCTION.json").read_text())
    parents = read("SUMMARY_BY_FLIGHT.csv", TERMINAL)

    # ---- identities and counts, recomputed from the 266 rows
    ok("266 rows in catalogue order, each identity once", len(rows) == 266 and [int(r["order"]) for r in rows] == list(range(1, 267)) and len({r["flight_id"] for r in rows}) == 266)
    ok("the result rows and the predictions name the same flights in the same order", [r["flight_id"] for r in rows] == [p["flight_id"] for p in pred])
    st = collections.Counter(r["timing_status"] for r in rows)
    ok("timing labels reproduce the published summary", dict(st) == summ["timing_status"] and set(st) <= {MEETS, OUTSIDE})
    half = float(summ["criteria"]["timing_half_width_us"]); res = {r["flight_id"]: (float(r["timing_residual_full_us"]), float(r["timing_residual_half_us"])) for r in rows}
    ok("each label follows from its two residuals and the 43 microsecond half-width", half == 43.0 and all((r["timing_status"] == MEETS) == (abs(res[r["flight_id"]][0]) <= half and abs(res[r["flight_id"]][1]) <= half) for r in rows))
    ok("each label is the same at both integration steps", all((abs(a) <= half) == (abs(b) <= half) for a, b in res.values()))
    obs_t = float(summ["observation"]["observed_timing_us"]); obs_f = float(summ["observation"]["observed_frequency_hz"])
    ok("each residual is the recorded timing minus the predicted timing", all(abs(obs_t - float(p["predicted_timing_full_us"]) - res[p["flight_id"]][0]) < 1e-9 for p in pred))
    fr = collections.Counter(r["frequency_diagnostic"] for r in rows)
    ok("frequency diagnostic counts reproduce the published summary", dict(fr) == summ["frequency_diagnostic"])
    add = {k: sum(1 for r in rows if r["within_%d_us" % k] == "within") for k in (29, 86, 129)}
    ok("additional threshold counts reproduce the published summary", all(summ["additional_thresholds"]["within_%d_us" % k].get("within", 0) == v for k, v in add.items()))
    ok("the summary is for this package revision and seal", summ["package_revision"] == REVISION == seal["package_revision"] and summ["seal_sha256"] == hashlib.sha256((SRC / "STAGE_A_SEAL.json").read_bytes()).hexdigest()
       and summ["predictions_sha256"] == hashlib.sha256((SRC / "PREDICTIONS_2241_266.csv").read_bytes()).hexdigest())

    # ---- groups
    by = collections.OrderedDict()
    for r in rows:
        by.setdefault((r["group"], r["level_pressure_altitude_ft"]), []).append(r)
    ok("eleven combinations of incoming group and cruise level", len(by) == 11 == len(groups) and all(g in GROUPS for g, _ in by))
    ok("group counts reproduce the published group table", all(
        (int(g["flights"]), int(g["meets_the_2241_timing"]), int(g["outside_the_band"])) == (len(by[(g["group"], g["level_pressure_altitude_ft"])]), sum(1 for r in by[(g["group"], g["level_pressure_altitude_ft"])] if r["timing_status"] == MEETS),
                                                                                             sum(1 for r in by[(g["group"], g["level_pressure_altitude_ft"])] if r["timing_status"] == OUTSIDE)) for g in groups))
    mixed = [k for k, v in by.items() if any(r["timing_status"] == OUTSIDE for r in v)]
    ok("every flight outside the band entered at Mach 0.67 and cruised at one level", len({k[1] for k in mixed}) == 1 and all(GROUPS[k[0]][1] == "0.67" for k in mixed))
    lvl = mixed[0][1]; cl = [r for k in mixed for r in by[k]]; other = [r for k, v in by.items() if k not in mixed for r in v]
    ok("the other combinations hold no flight outside the band", all(r["timing_status"] == MEETS for r in other) and len(cl) + len(other) == 266)

    # ---- the terminal-response parents, joined here from the Atlas's own copy of the terminal tables
    pid = {p["flight_id"] for p in parents}
    ok("the parents of the terminal-response catalogue are among the 266", len(pid) == len(parents) and pid <= set(res))
    pm = sum(1 for r in rows if r["flight_id"] in pid and r["timing_status"] == MEETS); po = len(pid) - pm
    um = sum(1 for r in rows if r["flight_id"] not in pid and r["timing_status"] == MEETS); uo = sum(1 for r in rows if r["flight_id"] not in pid and r["timing_status"] == OUTSIDE)
    c = over["counts"]
    ok("the join to the terminal parents reproduces the published join", (len(pid), pm, po, um, uo) == (c["explicit_propagated_terminal_parents"], c["propagated_parents_meeting_2241"], c["propagated_parents_outside_2241"], c["unpropagated_parents_meeting_2241"], c["unpropagated_parents_outside_2241"])
       and sorted(pid) == sorted(over["propagated_parent_ids"]))

    # ---- how far the labels lie from the edge (description only)
    out = [r for r in rows if r["timing_status"] == OUTSIDE]; inn = [r for r in rows if r["timing_status"] == MEETS]
    exc = sorted(max(abs(a), abs(b)) - half for a, b in (res[r["flight_id"]] for r in out))
    ok("every flight outside the band has a negative residual: its predicted timing is above the recorded one", all(res[r["flight_id"]][0] < 0 for r in out))
    mar = sorted(half + min(res[r["flight_id"]]) for r in inn)                      # distance inside the lower edge, where the outside flights lie
    full = [a for a, _ in res.values()]; stepd = max(abs(a - b) for a, b in res.values())
    fstep = max(abs(float(p["frequency_half_minus_full_hz"])) for p in pred); cfr = [float(r["frequency_residual_centred_full_hz"]) for r in rows]
    tp = [float(p["predicted_timing_full_us"]) for p in pred]; fp = [float(p["predicted_frequency_full_hz"]) for p in pred]
    ok("the predicted timing spread reproduces the Stage A report", abs((max(tp) - min(tp)) - rep["expected_discrimination"]["all_flights"]["spread_us"]) < 1e-9)
    ok("Stage A coverage is complete: 266 usable pairs, 532 target evaluations", seal["coverage"]["by_status"] == {"PREDICTED": 266} and seal["coverage"]["counts"]["target_evaluations_begun"] == 532 == seal["coverage"]["counts"]["predictions_stored"] and seal["partial_reason"] is None)
    ok("the two comparison programs agree on every label, threshold, diagnostic and group count", rec["passed"] is True and rec["rows"] == 266 and rec["all_primary_labels_equal"] is True and rec["all_additional_threshold_labels_equal"] is True
       and rec["all_frequency_diagnostics_equal"] is True and rec["all_group_fields_equal"] is True)
    ok("the arithmetic repeated in the Stage A container equals the published files", all(v["identical_to_packet"] for v in loc["frozen_program"]["outputs"].values()))

    base = f"https://github.com/{REPO}/blob/{COMMIT}/{SOURCE_PATH}/"
    V = collections.OrderedDict()
    V.update(q_all=n(len(rows)), q_meet=n(st[MEETS]), q_out=n(st[OUTSIDE]), q_boundary=n(sum(1 for a, b in res.values() if (abs(a) <= half) != (abs(b) <= half))), q_nolabel=n(len(rows) - st[MEETS] - st[OUTSIDE]),
             q_freq_within=n(fr.get("WITHIN_7_HZ", 0)), q_band=f"{half:.0f}", q_band_full=f"{2 * half:.0f}", q_freq_band=f"{float(summ['criteria']['frequency_half_width_hz']):.0f}",
             q_obs_timing=n(obs_t), q_obs_freq=f"{obs_f:.0f}", q_mu=f"{MINUS}{abs(float(summ['conventions']['MU_BFO_hz'])):.2f}",
             q_within29=n(add[29]), q_within86=n(add[86]), q_within129=n(add[129]),
             q_res_min=sgn(min(full)), q_res_max=sgn(max(full)), q_res_range=f"{sgn(min(full))} to {sgn(max(full))}",
             q_pred_min=f"{min(tp):,.1f}", q_pred_max=f"{max(tp):,.1f}", q_pred_spread=f"{max(tp) - min(tp):.1f}", q_pred_between=f"{rep['expected_discrimination']['between_group_means_spread_us']:.1f}",
             q_fpred_min=f"{min(fp):.2f}", q_fpred_max=f"{max(fp):.2f}", q_cfr_range=f"{sgn(min(cfr))} to {sgn(max(cfr))}",
             q_exc_min=f"{exc[0]:.2f}", q_exc_med=f"{statistics.median(exc):.2f}", q_exc_max=f"{exc[-1]:.2f}",
             q_out_near1=n(sum(1 for e in exc if e < NEAR_US[0])), q_out_near5=n(sum(1 for e in exc if e < NEAR_US[1])),
             q_in_near1=n(sum(1 for m in mar if m < NEAR_US[0])), q_in_near5=n(sum(1 for m in mar if m < NEAR_US[1])), q_near5_all=n(sum(1 for e in exc if e < NEAR_US[1]) + sum(1 for m in mar if m < NEAR_US[1])),
             q_in_margin_min=f"{mar[0]:.2f}", q_step_timing=f"{stepd:.5f}", q_step_freq=f"{fstep:.7f}",
             q_cluster=n(len(cl)), q_cluster_meet=n(sum(1 for r in cl if r["timing_status"] == MEETS)), q_cluster_out=n(sum(1 for r in cl if r["timing_status"] == OUTSIDE)), q_cluster_level=n(lvl),
             q_other=n(len(other)), q_other_groups=n(len(by) - len(mixed)),
             q_parents=n(len(pid)), q_parents_meet=n(pm), q_parents_out=n(po), q_unprop=n(um + uo), q_unprop_meet=n(um), q_unprop_out=n(uo),
             q_band_km=f"{half * M_PER_US / 1000.0:.1f}", q_exc_min_m=f"{exc[0] * M_PER_US:.0f}", q_exc_max_km=f"{exc[-1] * M_PER_US / 1000.0:.2f}", q_m_per_us=f"{M_PER_US:.0f}",
             q_lat_range="{:.1f} to {:.1f}°S".format(-max(float(p["latitude_full"]) for p in pred), -min(float(p["latitude_full"]) for p in pred)),
             q_lon_range="{:.1f} to {:.1f}°E".format(min(float(p["longitude_full"]) for p in pred), max(float(p["longitude_full"]) for p in pred)),
             q_evals=n(seal["coverage"]["counts"]["target_evaluations_begun"]), q_revision=REVISION, q_commit_short=COMMIT[:7],
             q_seal_short=summ["seal_sha256"][:12], q_source_base=base, q_local_base="data/check-2241-266/sources/", q_repo_commit=f"https://github.com/{REPO}/commit/{COMMIT}")

    # ---- group table rows
    tr = []
    for (g, level), v in by.items():
        a = [res[r["flight_id"]][0] for r in v]; m = sum(1 for r in v if r["timing_status"] == MEETS); o = len(v) - m
        tr.append("<tr><td>{:,} ft, Mach {}</td><td class=\"n\">{:,} ft</td><td class=\"n\">{}</td><td class=\"n\">{}</td><td class=\"n\">{}</td><td class=\"n\">{} to {}</td></tr>".format(
            GROUPS[g][0], GROUPS[g][1], int(level), len(v), m, ("<b>%d</b>" % o) if o else "0", sgn(min(a)), sgn(max(a))))
    V["q_group_rows"] = "\n".join(tr)

    # ---- figure: one row for each combination, one tick for each flight
    W, LEFT, RIGHT, TOP, ROW = 920, 236, 716, 34, 24
    X = lambda u: LEFT + (u + 50.0) * (RIGHT - LEFT) / 100.0
    H = TOP + ROW * len(by) + 44; s = []
    s.append(f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="q-fig-title q-fig-desc" style="display:block;width:100%;min-width:680px;height:auto;font-family:var(--font-body);font-size:12px">')
    s.append(f'<title id="q-fig-title">Timing residual at 22:41:22 for each of the {len(rows)} cruise histories, by incoming group and cruise level</title>')
    s.append(f'<desc id="q-fig-desc">{st[MEETS]} histories lie inside the band of plus or minus {half:.0f} microseconds and {st[OUTSIDE]} lie just below its lower edge. The table after the figure gives the same counts.</desc>')
    s.append(f'<rect x="{X(-half):.1f}" y="{TOP - 6}" width="{X(half) - X(-half):.1f}" height="{ROW * len(by) + 8}" fill="var(--grid)"/>')
    for u in (-half, half):
        s.append(f'<line x1="{X(u):.1f}" x2="{X(u):.1f}" y1="{TOP - 10}" y2="{TOP + ROW * len(by) + 4}" stroke="var(--fg)" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<line x1="{X(0):.1f}" x2="{X(0):.1f}" y1="{TOP - 6}" y2="{TOP + ROW * len(by) + 2}" stroke="var(--line)" stroke-width="1"/>')
    s.append(f'<text x="{X(0):.1f}" y="{TOP - 16}" text-anchor="middle" fill="var(--muted)">band of {MINUS}{half:.0f} to +{half:.0f} µs</text>')
    for i, ((g, level), v) in enumerate(by.items()):
        y = TOP + ROW * i + ROW / 2; m = sum(1 for r in v if r["timing_status"] == MEETS); o = len(v) - m
        s.append(f'<text x="{LEFT - 12}" y="{y + 4:.1f}" text-anchor="end" fill="var(--fg)">{GROUPS[g][0]:,} ft, Mach {GROUPS[g][1]} → {int(level):,} ft</text>')
        s.append(f'<line x1="{LEFT}" x2="{RIGHT}" y1="{y:.1f}" y2="{y:.1f}" stroke="var(--line)" stroke-width="1"/>')
        for r in sorted(v, key=lambda r: r["timing_status"] == OUTSIDE):
            a = res[r["flight_id"]][0]; outside = r["timing_status"] == OUTSIDE; hh = 9 if outside else 6
            s.append(f'<line x1="{X(a):.2f}" x2="{X(a):.2f}" y1="{y - hh:.1f}" y2="{y + hh:.1f}" stroke="var(--{"c2" if outside else "c1"})" stroke-width="{2 if outside else 1.5}" stroke-opacity="{0.9 if outside else 0.75}"><title>{html.escape(r["flight_id"])}: {sgn(a)} µs, {"outside the band" if outside else "meets the band"}</title></line>')
        s.append(f'<text x="{RIGHT + 14}" y="{y + 4:.1f}" fill="var(--fg)">{m} meet' + (f' · <tspan font-weight="700">{o} outside</tspan>' if o else '') + '</text>')
    ya = TOP + ROW * len(by) + 8
    for u in (-50, -half, -25, 0, 25, half, 50):
        s.append(f'<line x1="{X(u):.1f}" x2="{X(u):.1f}" y1="{ya}" y2="{ya + 4}" stroke="var(--muted)"/><text x="{X(u):.1f}" y="{ya + 17}" text-anchor="middle" fill="var(--muted)" font-family="var(--font-mono)" font-size="11">{sgn(u, 0)}</text>')
    s.append(f'<text x="{(LEFT + RIGHT) / 2:.1f}" y="{ya + 33}" text-anchor="middle" fill="var(--muted)">recorded minus predicted timing at 22:41:22, µs</text>')
    s.append("</svg>")
    V["q_figure"] = "".join(s)
    V["q_legend"] = ('<span style="display:inline-flex;align-items:center;gap:6px"><svg width="10" height="14" aria-hidden="true"><line x1="5" x2="5" y1="1" y2="13" stroke="var(--c1)" stroke-width="1.5"/></svg>meets the band (%s)</span> '
                     '<span style="display:inline-flex;align-items:center;gap:6px;margin-left:14px"><svg width="10" height="20" aria-hidden="true"><line x1="5" x2="5" y1="1" y2="19" stroke="var(--c2)" stroke-width="2"/></svg>outside the band (%s), drawn taller</span>') % (n(st[MEETS]), n(st[OUTSIDE]))
    assert all(isinstance(v, str) for v in V.values())
    return collections.OrderedDict(
        meta=dict(repository=REPO, commit=COMMIT, path=SOURCE_PATH, revision=REVISION, cruise_revision=CRUISE_REVISION,
                  note="Values are formatted strings inserted into the page bodies by gen.py. Compiled from the copied source tables; no flight calculation. The comparison itself was made by the source project, not here."),
        values=V), checks


def blob(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def manifest():
    files = []
    for name in sorted(FILES):
        data = (SRC / name).read_bytes()
        files.append(dict(name=name, source_path=f"{SOURCE_PATH}/{FILES[name]}{name}", bytes=len(data), git_blob_sha=blob(data), sha256=hashlib.sha256(data).hexdigest()))
    return collections.OrderedDict(repository=REPO, commit=COMMIT, path=SOURCE_PATH, package_revision=REVISION, cruise_runner_revision=CRUISE_REVISION, imported_on=IMPORTED_ON, files=files)


def dump(obj):
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    extra = sorted(p.name for p in SRC.iterdir() if p.name not in FILES)
    assert not extra, f"files not in the declared list: {extra}"
    man = manifest()
    display, checks = compile_display()
    validation = collections.OrderedDict(
        commit=COMMIT, package_revision=REVISION, source_files=len(man["files"]), displayed_values=len(display["values"]),
        reconciliations_passed=len(checks), reconciliations=checks,
        scope="Display import only. Counts and ranges are recomputed from the copied tables and reconciled with the published summary, group table and terminal-parent join. This is not a scientific revalidation; no flight was computed and no prediction was formed here.")
    outputs = {"source_manifest.json": dump(man), "display.json": dump(display), "validation.json": dump(validation)}
    if a.check:
        bad = [k for k, v in outputs.items() if not (OUT / k).exists() or (OUT / k).read_text() != v]
        if bad:
            print("MISMATCH:", ", ".join(bad))
            sys.exit(1)
        print(f"OK: {len(man['files'])} source files match the manifest; {len(display['values'])} displayed values and {len(checks)} reconciliations reproduce the committed outputs")
        return
    for k, v in outputs.items():
        (OUT / k).write_text(v)
    print(f"wrote {', '.join(outputs)}: {len(display['values'])} values, {len(checks)} reconciliations")


if __name__ == "__main__":
    main()

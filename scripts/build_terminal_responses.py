#!/usr/bin/env python3
"""Compile the published terminal-response tables for the Atlas page.

Reads committed CSV/JSON files only. No model import, flight calculation,
fitting, satellite prediction or interpolation is performed, and nothing is
evaluated at 22:41. Every number shown on terminal.html is produced here from
the copied source tables and inserted by gen.py; none is typed into the page.

    python3 scripts/build_terminal_responses.py           write display.json, validation.json
    python3 scripts/build_terminal_responses.py --check   verify sources and committed outputs; write nothing
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "terminal-responses-266"
SRC = OUT / "sources"
REPO = "floydclaptonblues/MH370-Ocean-GLORYS-Data"
COMMIT = "429c11c4d41d7f26de46aaa71e74cba0cc3b401e"
SOURCE_PATH = "reports/diagnostic/CATALOGUE_TERMINAL"
REVISION = "c370b2cf70b9"
CRUISE_REVISION = "2a016b1294fa"
IMPORTED_ON = "2026-11-18"
# name -> directory below SOURCE_PATH
FILES = {
    "FINDINGS.md": "", "METHOD.md": "", "FUEL_POWER_ACCOUNT.md": "", "HANDOFF.md": "",
    "BY_GROUP_BANK_ONSET.csv": "RESULTS/", "CONTINUATION_ENDINGS.csv": "RESULTS/",
    "FLIGHTS_NOT_PROPAGATED.csv": "RESULTS/", "NUMERICAL_CHECKS.csv": "RESULTS/",
    "PROVENANCE_EXCEPTIONS.csv": "RESULTS/", "RESPONSES.csv": "RESULTS/",
    "RESULTS_SUMMARY.json": "RESULTS/", "SUMMARY_BY_FLIGHT.csv": "RESULTS/",
    "SUMMARY_BY_GROUP.csv": "RESULTS/", "MAP_OVERVIEW.png": "RESULTS/",
    "MAP_POSITIONS_AT_0019_29.png": "RESULTS/", "MAP_LAST_PROPAGATED_POSITIONS.png": "RESULTS/",
    "OUTCOME_BY_ONSET_TIME.png": "RESULTS/",
}
# source group label -> (key, height of the arrival at 19:41 in ft, Mach)
GROUPS = collections.OrderedDict([
    ("300.9 hPa, Mach 0.78", ("g1", 29987, "0.78")),
    ("331.655 hPa, Mach 0.75", ("g2", 27830, "0.75")),
    ("365.113 hPa, Mach 0.67", ("g3", 25661, "0.67")),
    ("365.113 hPa, Mach 0.75", ("g4", 25661, "0.75")),
])
TREATMENTS = collections.OrderedDict([
    ("frozen_equations_no_warmup", "fn"), ("historical_offset_no_warmup", "hn"),
    ("frozen_equations_warmup", "fw"), ("historical_offset_warmup", "hw"),
])
T_0019_29 = 16706.0          # seconds after 19:41:03 UTC
FT = 0.3048
MINUS = "−"
BOX = dict(lat=(-33.0, -32.0), lon=(94.0, 96.0))


def read(name):
    with open(SRC / name, newline="") as f:
        return list(csv.DictReader(f))


def num(v):
    if v is None or v == "":
        return None
    x = float(v)
    assert math.isfinite(x), "non-finite published value"
    return x


def true(v):
    assert v in ("True", "False", ""), v
    return v == "True"


def n(i):
    return f"{int(i):,}"


def sgn(x, d=1):
    """Signed number with a true minus sign."""
    s = f"{abs(x):.{d}f}"
    if float(s) == 0:
        return s
    return (MINUS if x < 0 else "+") + s


def neg(x, d=1):
    """Number with a true minus sign and no plus sign."""
    s = f"{abs(x):.{d}f}"
    return (MINUS + s) if x < 0 and float(s) != 0 else s


def span(v, d=1, f=neg, unit=""):
    v = [x for x in v if x is not None]
    lo, hi = f(min(v), d), f(max(v), d)
    return lo + unit if lo == hi else f"{lo} to {hi}{unit}"


def south(v, d=2):
    """Latitude range written as degrees south, smaller magnitude first."""
    v = [x for x in v if x is not None]
    assert max(v) < 0
    a, b = f"{-max(v):.{d}f}", f"{-min(v):.{d}f}"
    return f"{a}°S" if a == b else f"{a} to {b}°S"


def east(v, d=2):
    v = [x for x in v if x is not None]
    a, b = f"{min(v):.{d}f}", f"{max(v):.{d}f}"
    return f"{a}°E" if a == b else f"{a} to {b}°E"


def feet(v):
    """Heights in metres as a range in feet, rounded to 100 ft."""
    v = [x for x in v if x is not None]
    a, b = (int(round(x / FT / 100.0)) * 100 for x in (min(v), max(v)))
    return f"{a:,} ft" if a == b else f"{a:,} to {b:,} ft"


def km(lat1, lon1, lat2, lon2):
    a, b, c, d = map(math.radians, (lat1, lon1, lat2, lon2))
    h = math.sin((c - a) / 2) ** 2 + math.cos(a) * math.cos(c) * math.sin((d - b) / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(h))


def seconds(utc):
    """Seconds after 19:41:03 UTC on 7 March for a 2014-03-08T... stamp."""
    m = re.fullmatch(r"2014-03-0([78])T(\d\d):(\d\d):(\d\d(?:\.\d+)?)Z?(?:\+00:00)?", utc)
    assert m, utc
    day = int(m.group(1)) - 7
    return day * 86400 + int(m.group(2)) * 3600 + int(m.group(3)) * 60 + float(m.group(4)) - (19 * 3600 + 41 * 60 + 3)


def inside(lat, lon):
    return BOX["lat"][0] <= lat <= BOX["lat"][1] and BOX["lon"][0] <= lon <= BOX["lon"][1]


def compile_display():
    V = collections.OrderedDict()
    checks = []

    def same(label, a, b):
        assert a == b, f"{label}: {a!r} != {b!r}"
        checks.append(label)

    resp = read("RESPONSES.csv")
    ends = read("CONTINUATION_ENDINGS.csv")
    onset = read("BY_GROUP_BANK_ONSET.csv")
    byflight = read("SUMMARY_BY_FLIGHT.csv")
    bygroup = read("SUMMARY_BY_GROUP.csv")
    notprop = read("FLIGHTS_NOT_PROPAGATED.csv")
    numchk = read("NUMERICAL_CHECKS.csv")
    prov = read("PROVENANCE_EXCEPTIONS.csv")
    summary = json.loads((SRC / "RESULTS_SUMMARY.json").read_text())

    # ---- population
    same("revision", summary["revision"], REVISION)
    flights = sorted({r["flight_id"] for r in resp})
    same("propagated flights", len(flights), 90)
    same("flight summaries", sorted(r["flight_id"] for r in byflight), flights)
    st = collections.Counter(r["status"] for r in notprop)
    same("flights not propagated", dict(st), summary["flights_not_propagated"])
    assert not set(flights) & {r["flight_id"] for r in notprop}
    V["flights_all"] = n(len(flights) + len(notprop))
    V["flights_propagated"] = n(len(flights))
    V["flights_fuel_after"] = n(st["FUEL_EVENT_AFTER_BOTH_FINAL_TRANSMISSIONS"])
    V["flights_powered"] = n(st["POWERED_AT_0040_NO_FUEL_EVENT"])
    V["flights_not_propagated"] = n(len(notprop))
    late = [num(r["fuel_event_minus_0019_29_s"]) for r in notprop if r["status"] == "FUEL_EVENT_AFTER_BOTH_FINAL_TRANSMISSIONS"]
    assert min(late) > 8.0
    V["fuel_after_s"] = f"{min(late):,.0f} to {max(late):,.0f}"
    rows = collections.Counter((r["incoming_group"], int(r["level_pressure_altitude_ft"]), r["status"]) for r in notprop)
    arrival_ft = {"300.9 hPa": 29987, "331.655 hPa": 27830, "365.113 hPa": 25661}
    V["rows_not_propagated"] = "".join(
        "<tr><td>Mach {m}, arriving at {a:,} ft</td><td>{lv:,} ft</td><td>{c}</td><td>{s}</td></tr>".format(
            m=g.split("Mach ")[1], a=arrival_ft[g.split(",")[0]], lv=lv, c=c,
            s="Engine fuel runs out after both final transmissions" if s.startswith("FUEL") else "Engines still running at 00:40")
        for (g, lv, s), c in sorted(rows.items(), key=lambda kv: (kv[0][2], -kv[1], kv[0][0], kv[0][1])))

    # ---- responses and outcomes
    per = collections.Counter(r["flight_id"] for r in resp)
    same("responses per flight", set(per.values()), {138})
    same("onset times", sorted({int(r["onset_minus_0019_29_s"]) for r in resp}), list(range(-60, 9)))
    same("bank angles", sorted({r["bank_deg"] for r in resp}), ["-60.0", "60.0"])
    keys = {(r["flight_id"], r["bank_deg"], r["onset_minus_0019_29_s"]) for r in resp}
    same("each response once", len(keys), len(resp))
    oc = collections.Counter(r["outcome"].split(":")[0] for r in resp)
    same("outcome counts", dict(oc), summary["outcomes"])
    same("failed calculations", sum(1 for r in resp if r["calculation_failed"]), 0)
    V["responses"] = n(len(resp))
    V["out_before"] = n(oc["MODEL_LIMIT_STOP_BEFORE_0019_29"])
    V["out_between"] = n(oc["MODEL_LIMIT_STOP_BEFORE_0019_37"])
    V["out_mismatch"] = n(oc["FREQUENCY_NOT_MET_UNDER_ANY_DECLARED_TREATMENT"])
    V["out_continued"] = n(oc["CONTINUED"])
    V["out_failed"] = n(oc.get("CALCULATION_FAILED", 0))
    V["out_limit"] = n(oc["MODEL_LIMIT_STOP_BEFORE_0019_29"] + oc["MODEL_LIMIT_STOP_BEFORE_0019_37"])
    same("stop kinds", {r["stop_kind"] for r in resp if r["stop_kind"]}, {"OPERATIONAL_MACH_OR_CAS_LIMIT"})
    same("stops are the model-limit outcomes", sum(1 for r in resp if r["stop_kind"]), oc["MODEL_LIMIT_STOP_BEFORE_0019_29"] + oc["MODEL_LIMIT_STOP_BEFORE_0019_37"])
    after = [seconds(r["stop_utc"]) - (T_0019_29 + int(r["onset_minus_0019_29_s"])) for r in resp if r["stop_kind"]]
    V["stop_after_onset_s"] = span(after, 1)
    cont = [r for r in resp if true(r["continued_beyond_0019_37"])]
    same("continued flag", len(cont), oc["CONTINUED"])
    s29 = [r for r in resp if true(r["supported_to_0019_29"])]
    s37 = [r for r in resp if true(r["supported_to_0019_37"])]
    V["supported_29"] = n(len(s29))
    V["supported_37"] = n(len(s37))
    same("supported to 00:19:37", len(s37), oc["CONTINUED"] + oc["FREQUENCY_NOT_MET_UNDER_ANY_DECLARED_TREATMENT"])
    perc = collections.Counter(r["flight_id"] for r in cont)
    same("every flight has a continued response", len(perc), 90)
    dist = collections.Counter(perc.values())
    V["continued_per_flight"] = ", ".join(str(k) for k in sorted(dist)[:-1]) + " or " + str(max(dist))
    V["continued_per_flight_flights"] = ", ".join(str(dist[k]) for k in sorted(dist)[:-1]) + " and " + str(dist[max(dist)])
    V["continued_left"] = n(sum(1 for r in cont if r["bank_deg"] == "-60.0"))
    V["continued_right"] = n(sum(1 for r in cont if r["bank_deg"] == "60.0"))
    co = [int(r["onset_minus_0019_29_s"]) for r in cont]
    V["continued_onset_first"], V["continued_onset_last"] = str(-min(co)), str(-max(co))
    assert min(co) > -60 and max(co) < 8

    # ---- by onset time, both directions and all flights together
    by = collections.defaultdict(collections.Counter)
    for r in resp:
        by[int(r["onset_minus_0019_29_s"])][r["outcome"].split(":")[0]] += 1
    tot = collections.defaultdict(collections.Counter)
    for r in onset:
        o = int(r["onset_minus_0019_29_s"])
        tot[o]["MODEL_LIMIT_STOP_BEFORE_0019_29"] += int(r["stopped_before_0019_29_model_limit"])
        tot[o]["MODEL_LIMIT_STOP_BEFORE_0019_37"] += int(r["stopped_between_transmissions_model_limit"])
        tot[o]["CONTINUED"] += int(r["continued"])
        tot[o]["n"] += int(r["flights"])
    for o in range(-60, 9):
        same(f"onset {o}: responses", tot[o]["n"], 180)
        for k in ("MODEL_LIMIT_STOP_BEFORE_0019_29", "MODEL_LIMIT_STOP_BEFORE_0019_37", "CONTINUED"):
            same(f"onset {o}: {k}", tot[o][k], by[o][k])

    def label(o):
        return (MINUS + str(-o)) if o < 0 else ("+" + str(o) if o > 0 else "0")

    def describe(c):
        parts = []
        lim = c["MODEL_LIMIT_STOP_BEFORE_0019_29"] + c["MODEL_LIMIT_STOP_BEFORE_0019_37"]
        if lim:
            parts.append(f"{lim} reach the operating-speed limit before 00:19:37")
        if c["CONTINUED"]:
            parts.append(f"{c['CONTINUED']} continued")
        if c["FREQUENCY_NOT_MET_UNDER_ANY_DECLARED_TREATMENT"]:
            parts.append(f"{c['FREQUENCY_NOT_MET_UNDER_ANY_DECLARED_TREATMENT']} meet no frequency treatment")
        if len(parts) == 1:
            return "All " + parts[0]
        return "; ".join(parts)

    runs = []
    for o in range(-60, 9):
        d = describe(by[o])
        kind = d if d.startswith("All ") else None
        if runs and kind is not None and runs[-1][2] == kind:
            runs[-1][1] = o
        else:
            runs.append([o, o, kind, d])
    V["rows_by_onset"] = "".join(
        "<tr><td>{}</td><td>{}</td></tr>".format(label(a) if a == b else f"{label(a)} to {label(b)}", d)
        for a, b, _, d in runs)
    V["all_limit_until"] = str(-max(o for o in range(-60, 9) if by[o]["MODEL_LIMIT_STOP_BEFORE_0019_29"] + by[o]["MODEL_LIMIT_STOP_BEFORE_0019_37"] == 180))
    lat = [o for o in range(-60, 9) if by[o]["FREQUENCY_NOT_MET_UNDER_ANY_DECLARED_TREATMENT"] == 180]
    same("late onsets are one run to +8", lat, list(range(min(lat), 9)))
    V["none_from"] = str(-min(lat))
    V["late_responses"] = n(180 * len(lat))

    # ---- timing at 00:19:29
    res = [num(r["timing_residual_0019_29_us"]) for r in s29]
    V["timing_all"] = f"{sgn(min(res))} and {sgn(max(res))}"
    V["timing_max_abs"] = f"{math.ceil(max(abs(x) for x in res)):d}"
    same("timing inside 62 µs for every response reaching 00:19:29", all(true(r["timing_0019_29_within_62_us"]) for r in s29), True)
    spread = collections.defaultdict(list)
    for r in cont:
        spread[r["flight_id"]].append(num(r["timing_residual_0019_29_us"]))
    V["timing_spread_within_flight"] = f"{max(max(v) - min(v) for v in spread.values()):.1f}"
    alt = [(r["incoming_group"], num(r["timing_residual_0019_29_if_18440_us"])) for r in cont]
    for g, x in alt:
        assert abs(x) <= 124.0
    out62 = collections.Counter(g for g, x in alt if abs(x) > 62.0)
    same("alternative timing: one group outside 62 µs", list(out62), ["365.113 hPa, Mach 0.75"])
    V["alt_outside_62"] = n(out62["365.113 hPa, Mach 0.75"])
    V["alt_outside_max"] = f"{max(x for g, x in alt if abs(x) > 62.0):.1f}"
    same("00:19:37 timing not evaluated", {r["timing_0019_37"] for r in resp}, {"not evaluated"})

    # ---- hypotheses not supported (appendix)
    lateset = [r for r in s37 if int(r["onset_minus_0019_29_s"]) >= min(lat)]
    same("late onsets all supported to 00:19:37", len(lateset), 180 * len(lat))
    V["late_freq37"] = span([num(r["predicted_frequency_0019_37_hz"]) for r in lateset], 0)
    early = [r for r in s37 if -18 <= int(r["onset_minus_0019_29_s"]) <= -15]
    assert early and not any(true(r["continued_beyond_0019_37"]) for r in early)
    V["early_freq29"] = span([num(r["predicted_frequency_0019_29_hz"]) for r in early], 0, sgn)
    unfinished = [r for r in resp if int(r["onset_minus_0019_29_s"]) >= -1]
    assert not any(true(r["continued_beyond_0019_37"]) for r in unfinished)
    V["unfinished_responses"] = n(len(unfinished))

    # ---- frequency
    late0 = [r for r in s29 if int(r["onset_minus_0019_29_s"]) >= 0]
    V["freq_no_response"] = span([num(r["predicted_frequency_0019_29_hz"]) for r in late0], 0)
    V["vs_no_response"] = span([-num(r["vertical_speed_mps_at_0019_29"]) for r in late0], 0)
    V["freq_change"] = span([num(r["predicted_frequency_change_hz"]) for r in cont], 0)
    anyc = 0
    for t, k in TREATMENTS.items():
        m = [r for r in resp if true(r["frequency_" + t])]
        assert all(true(r["continued_beyond_0019_37"]) for r in m)
        same(f"joint 62 µs equals frequency, {t}", sum(1 for r in resp if true(r["joint_timing_62_us_and_frequency_" + t])), len(m))
        V[f"{k}_n"] = n(len(m))
        V[f"{k}_flights"] = n(len({r["flight_id"] for r in m}))
        on = [int(r["onset_minus_0019_29_s"]) for r in m]
        V[f"{k}_onset"] = f"{-max(on)} to {-min(on)}"
        V[f"{k}_vs29"] = span([num(r["vertical_speed_mps_at_0019_29"]) for r in m], 1)
        V[f"{k}_vs37"] = span([num(r["vertical_speed_mps_at_0019_37"]) for r in m], 1)
        anyc += 1
    m = [r for r in resp if true(r["frequency_any_declared_treatment"])]
    same("any treatment equals continued", len(m), len(cont))
    same("joint 62 µs, any treatment", sum(1 for r in resp if true(r["joint_timing_62_us_and_frequency_any_declared_treatment"])), len(cont))
    V["any_vs29"] = span([num(r["vertical_speed_mps_at_0019_29"]) for r in m], 1)
    V["any_vs37"] = span([num(r["vertical_speed_mps_at_0019_37"]) for r in m], 1)
    fpm = lambda v: int(round(-v / FT * 60 / 100.0)) * 100
    V["any_fpm29"] = f"{fpm(max(num(r['vertical_speed_mps_at_0019_29']) for r in m)):,} to {fpm(min(num(r['vertical_speed_mps_at_0019_29']) for r in m)):,}"
    V["any_fpm37"] = f"{fpm(max(num(r['vertical_speed_mps_at_0019_37']) for r in m)):,} to {fpm(min(num(r['vertical_speed_mps_at_0019_37']) for r in m)):,}"

    # ---- by group
    grp = {r["incoming_group"]: r for r in bygroup}
    same("groups", sorted(g for g in grp if g != "all four groups"), sorted(GROUPS))
    centre = {}
    for g, (k, arr, mach) in GROUPS.items():
        rs = [r for r in resp if r["incoming_group"] == g]
        cs = [r for r in cont if r["incoming_group"] == g]
        es = [e for e in ends if e["incoming_group"] == g]
        s = grp[g]
        fl = {r["flight_id"] for r in rs}
        same(f"{g}: flights", len(fl), int(s["flights"]))
        same(f"{g}: responses", len(rs), int(s["responses"]))
        same(f"{g}: continued", len(cs), int(s["continued"]))
        same(f"{g}: endings", len(es), int(s["last_stage_endings"]))
        level = {int(r["level_pressure_altitude_ft"]) for r in rs}
        assert len(level) == 1
        level = level.pop()
        V[f"{k}_level"] = f"{level:,} ft"
        V[f"{k}_arrival"] = f"{arr:,} ft"
        V[f"{k}_mach"] = mach
        V[f"{k}_label"] = g
        V[f"{k}_flights"] = n(len(fl))
        V[f"{k}_responses"] = n(len(rs))
        V[f"{k}_continued"] = n(len(cs))
        fe = [num(r["fuel_event_to_0019_29_s"]) for r in rs]
        V[f"{k}_fuel_event_s"] = f"{min(fe):.0f} to {max(fe):.0f}"
        a29 = [num(r["model_apu_fuel_0019_29_kg"]) for r in cs]
        a37 = [num(r["model_apu_fuel_0019_37_kg"]) for r in cs]
        V[f"{k}_apu29"] = "0" if max(a29) == 0 else f"{min(a29):.2f} to {max(a29):.2f} kg"
        V[f"{k}_apu37"] = "0" if max(a37) == 0 else f"{min(a37):.2f} to {max(a37):.2f} kg"
        es_ = collections.Counter(r["electrical_sequence"] for r in cs)
        assert len(es_) == 1
        V[f"{k}_electrical"] = (f"{len(cs)} conditional" if "CONDITIONAL" in es_
                                else f"{len(cs)}: model APU fuel exhausted before a final transmission")
        V[f"{k}_timing_continued"] = span([num(r["timing_residual_0019_29_us"]) for r in cs], 1, sgn)
        on = [int(r["onset_minus_0019_29_s"]) for r in cs]
        V[f"{k}_onset"] = f"{-max(on)} to {-min(on)}"
        st_ = [seconds(r["stop_utc"]) - (T_0019_29 + int(r["onset_minus_0019_29_s"])) for r in rs if r["stop_kind"]]
        V[f"{k}_stop_after_onset_s"] = span(st_, 1)
        la = [num(r["latitude_at_0019_29"]) for r in cs]
        lo = [num(r["longitude_at_0019_29"]) for r in cs]
        V[f"{k}_lat29"], V[f"{k}_lon29"] = south(la), east(lo)
        V[f"{k}_centre29"] = f"{-sum(la) / len(la):.1f}\u00b0S, {sum(lo) / len(lo):.1f}\u00b0E"
        V[f"{k}_h29"] = feet([num(r["height_m_at_0019_29"]) for r in cs])
        V[f"{k}_h37"] = feet([num(r["height_m_at_0019_37"]) for r in cs])
        # separations and centres use every response of the group that reaches 00:19:29
        g29 = [r for r in s29 if r["incoming_group"] == g]
        pts = sorted({(num(r["latitude_at_0019_29"]), num(r["longitude_at_0019_29"])) for r in g29})
        V[f"{k}_sep_km"] = f"{max(km(a[0], a[1], b[0], b[1]) for i, a in enumerate(pts) for b in pts[i + 1:]):.0f}"
        centre[k] = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
        ec = collections.Counter(e["ending"] for e in es)
        V[f"{k}_end_lift"] = n(ec.get("CL_MODEL_SUPPORT", 0))
        V[f"{k}_end_floor"] = n(ec.get("WEATHER_VERTICAL_DOMAIN_EXIT", 0))
        V[f"{k}_last_lat"] = south([num(e["latitude"]) for e in es])
        V[f"{k}_last_lon"] = east([num(e["longitude"]) for e in es])
        # effect of the two choices after Mach 0.89 on one response's last position
        one = collections.defaultdict(dict)
        for e in es:
            one[(e["flight_id"], e["bank_deg"], e["onset_minus_0019_29_s"])][(e["bank_law_after_mach_089"], e["drag_rise_formulation"])] = (num(e["latitude"]), num(e["longitude"]))
        laws = sorted({a for d in one.values() for a, _ in d})
        forms = sorted({b for d in one.values() for _, b in d})
        assert len(laws) == 2 and len(forms) == 2 and all(len(d) == 4 for d in one.values())
        # for each response, the larger of its two differences
        bl = [max(km(*d[(laws[0], f)], *d[(laws[1], f)]) for f in forms) for d in one.values()]
        df = [max(km(*d[(a, forms[0])], *d[(a, forms[1])]) for a in laws) for d in one.values()]
        kmfmt = lambda v: (f"under {math.ceil(max(v) * 100) / 100:.2f} km" if max(v) < 0.05 else
                           " to ".join((f"{x:.2f}" if x < 1 else (f"{x:.1f}" if x < 10 else f"{x:.0f}")) for x in (min(v), max(v))) + " km")
        V[f"{k}_between_laws"], V[f"{k}_between_drag"] = kmfmt(bl), kmfmt(df)
    seps = [int(V[f"{k}_sep_km"]) for k in ("g1", "g2", "g3", "g4")]
    V["sep_min_km"], V["sep_max_km"] = str(min(seps)), str(max(seps))
    V["centres_g2_g4_km"] = f"{km(*centre['g2'], *centre['g4']):.0f}"
    mid = tuple((centre["g2"][i] + centre["g4"][i]) / 2 for i in (0, 1))
    V["g1_from_mid_km"] = f"{round(km(*centre['g1'], *mid) / 5.0) * 5:.0f}"
    V["g3_from_mid_km"] = f"{round(km(*centre['g3'], *mid) / 5.0) * 5:.0f}"
    # the model's APU account: 15 lb reserve, 2 lb per 55 s (FUEL_POWER_ACCOUNT.md)
    reserve_kg, rate = 15 * 0.45359237, 2 * 0.45359237 / 55.0
    same("reserve", round(reserve_kg, 8), 6.80388555)
    burn = {round((num(r["model_apu_fuel_0019_29_kg"]) - num(r["model_apu_fuel_0019_37_kg"])) / 8.0, 6) for r in cont if num(r["model_apu_fuel_0019_37_kg"]) > 0}
    same("burn rate in the table", burn, {round(rate, 6)})
    V["apu_exhausted_before_29_s"] = span([num(r["fuel_event_to_0019_29_s"]) - reserve_kg / rate for r in cont if r["incoming_group"] == "365.113 hPa, Mach 0.75"], 0)
    V["apu_after_37_s"] = span([num(r["model_apu_fuel_0019_37_kg"]) / rate for r in cont if r["incoming_group"] == "365.113 hPa, Mach 0.67"], 0)
    V["apu_reserve_lasts_s"] = f"{reserve_kg / rate:.1f}"
    same("every fuel-event interval exceeds 120 s", min(num(r["fuel_event_to_0019_29_s"]) for r in resp) > 120.0, True)

    # ---- endings
    ec = collections.Counter(e["ending"] for e in ends)
    same("ending counts", dict(ec), summary["continuation_endings"])
    same("four endings per continued response", len(ends), 4 * len(cont))
    same("no early ending", summary["ended_before_last_stage"], {"None": len(cont)})
    same("entries", summary["entries"], {"published chain": len(cont)})
    same("no surface contact, none airborne at the horizon", set(ec), {"CL_MODEL_SUPPORT", "WEATHER_VERTICAL_DOMAIN_EXIT"})
    V["endings"] = n(len(ends))
    V["end_lift"] = n(ec["CL_MODEL_SUPPORT"])
    V["end_floor"] = n(ec["WEATHER_VERTICAL_DOMAIN_EXIT"])
    lift = [e for e in ends if e["ending"] == "CL_MODEL_SUPPORT"]
    floor = [e for e in ends if e["ending"] == "WEATHER_VERTICAL_DOMAIN_EXIT"]
    hk = lambda v: " to ".join(f"{x / 1000:.1f}" for x in (min(v), max(v))) + " km"
    V["lift_height"] = hk([num(e["height_above_model_surface_m"]) for e in lift])
    V["lift_vs"] = span([-num(e["vertical_speed_mps"]) for e in lift], 0)
    V["lift_mach"] = span([num(e["Mach"]) for e in lift], 2)
    V["floor_height"] = span([num(e["height_above_model_surface_m"]) for e in floor], 0) + " m"
    V["floor_height_ellipsoid"] = span([num(e["height_m"]) for e in floor], 0) + " m"

    def ending_row(name, sel):
        assert sel, name
        return ("<tr><td>{}</td><td>{}</td><td>{}</td><td>{} s</td><td>{} km</td><td>{}</td><td>{} m/s</td></tr>").format(
            name, n(len(sel)),
            hk([num(e["height_above_model_surface_m"]) for e in sel]) if min(num(e["height_above_model_surface_m"]) for e in sel) > 500
            else span([num(e["height_above_model_surface_m"]) for e in sel], 0) + " m",
            span([num(e["seconds_after_0019_37"]) for e in sel], 0),
            span([num(e["km_from_position_at_0019_37"]) for e in sel], 1 if max(num(e["km_from_position_at_0019_37"]) for e in sel) < 10 else 0),
            span([num(e["Mach"]) for e in sel], 2),
            span([num(e["vertical_speed_mps"]) for e in sel], 0))

    G = list(GROUPS)
    held = lambda e: e["bank_law_after_mach_089"] == "CONST_BANK"
    laws_seen = {e["bank_law_after_mach_089"] for e in ends}
    assert "CONST_BANK" in laws_seen and len(laws_seen) == 2, laws_seen
    rowsE = [
        ("Lift-support limit, Mach 0.78 at 33,985 ft", [e for e in lift if e["incoming_group"] == G[0]]),
        ("Lift-support limit, Mach 0.75 arriving at 27,830 ft", [e for e in lift if e["incoming_group"] == G[1]]),
        ("Lift-support limit, Mach 0.75 arriving at 25,661 ft", [e for e in lift if e["incoming_group"] == G[3]]),
        ("Lowest weather level, Mach 0.67 at 25,661 ft", [e for e in floor if e["incoming_group"] == G[2]]),
        ("Lowest weather level, Mach 0.75 arriving at 25,661 ft, bank held", [e for e in floor if e["incoming_group"] == G[3] and held(e)]),
        ("Lowest weather level, Mach 0.75 arriving at 25,661 ft, roll to wings level", [e for e in floor if e["incoming_group"] == G[3] and not held(e)]),
        ("Lowest weather level, Mach 0.75 arriving at 27,830 ft, roll to wings level", [e for e in floor if e["incoming_group"] == G[1]]),
    ]
    same("ending rows cover every ending once", sum(len(s) for _, s in rowsE), len(ends))
    same("no lift-limit ending in the Mach 0.67 group", sum(1 for e in lift if e["incoming_group"] == G[2]), 0)
    same("no weather-floor ending in the Mach 0.78 group", sum(1 for e in floor if e["incoming_group"] == G[0]), 0)
    V["rows_endings"] = "".join(ending_row(a, b) for a, b in rowsE)
    few = rowsE[-1][1]
    assert all(not held(e) for e in few)
    V["g2_floor_endings"] = n(len(few))
    V["g2_floor_flights"] = n(len({e["flight_id"] for e in few}))
    V["g2_floor_km"] = span([num(e["km_from_position_at_0019_37"]) for e in few], 0)
    t = sorted(e["last_propagated_utc"] for e in ends)
    V["last_first"], V["last_last"] = t[0][11:19], t[-1][11:19]
    bank_held = [num(e["km_from_position_at_0019_37"]) for e in ends if held(e)]
    V["held_km"] = f"{min(bank_held):.0f} to {max(bank_held):.0f}"
    rolled = [e for e in ends if not held(e)]
    V["rolled_max_g4_km"] = f"{max(num(e['km_from_position_at_0019_37']) for e in rolled if e['incoming_group'] == G[3]):.0f}"

    # ---- query rectangle
    q = summary["query_rectangle"]
    same("query box", (q["latitude"], q["longitude"]), ([-33.0, -32.0], [94.0, 96.0]))
    in29 = [r for r in s29 if inside(num(r["latitude_at_0019_29"]), num(r["longitude_at_0019_29"]))]
    in37 = [r for r in cont if inside(num(r["latitude_at_0019_37"]), num(r["longitude_at_0019_37"]))]
    inl = [e for e in ends if inside(num(e["latitude"]), num(e["longitude"]))]
    same("query at 00:19:29", len(in29), q["of_which_inside_at_0019_29"])
    same("query at 00:19:37", len(in37), q["of_which_inside_at_0019_37"])
    same("query, last positions", len(inl), q["of_which_last_propagated_position_inside"])
    same("query: one group only", {r["incoming_group"] for r in in29} | {r["incoming_group"] for r in in37} | {e["incoming_group"] for e in inl}, {G[2]})
    V["q29"], V["q37"], V["qlast"] = n(len(in29)), n(len(in37)), n(len(inl))
    V["q_flights"] = n(len({r["flight_id"] for r in in37}))
    g3e = [e for e in ends if e["incoming_group"] == G[2]]
    outside = [e for e in g3e if not inside(num(e["latitude"]), num(e["longitude"]))]
    same("query: endings outside are east of 96°E", all(num(e["longitude"]) > 96.0 and -33.0 <= num(e["latitude"]) <= -32.0 for e in outside), True)
    V["q_g3_outside"] = n(len(outside))
    V["q_g3_east_max"] = f"{max(num(e['longitude']) for e in outside):.2f}"

    # ---- numerical checks and cost
    same("numerical checks all met", {r["result"] for r in numchk}, {"MET"})
    on_ = [r for r in numchk if r["check"].startswith("onset")]
    ch_ = [r for r in numchk if r["check"].startswith("continuation")]
    same("numerical checks", (len(on_), len(ch_)), (24, 8))
    V["chk_onset"], V["chk_cont"] = n(len(on_)), n(len(ch_))
    mx = lambda rows_, c: max(num(r[c]) for r in rows_ if r[c] != "")
    V["chk_onset_pos_mm"] = f"{mx(on_, 'position_m') * 1000:.1f}"
    V["chk_cont_pos_mm"] = f"{mx(ch_, 'position_m') * 1000:.1f}"
    V["chk_freq_hz"] = f"{mx(on_, 'predicted_frequency_hz'):.5f}"
    V["chk_timing_us"] = f"{mx(on_, 'predicted_timing_us'):.5f}"
    assert mx(on_, "position_m") < 1 and mx(ch_, "position_m") < 1 and mx(on_, "predicted_frequency_hz") < 0.01 and mx(on_, "predicted_timing_us") < 0.1
    V["rows_onset_table"], V["rows_group_table"], V["rows_check_table"], V["rows_prov_table"] = n(len(onset)), n(len(bygroup)), n(len(numchk)), n(len(prov))
    V["cost_h"] = f"{sum(summary['used_s'].values()) / 3600:.1f}"
    V["cost_limit_h"] = f"{sum(summary['allowances_s'].values()) / 3600:.1f}"

    # ---- provenance exception
    same("one provenance exception", len(prov), 1)
    p = prov[0]
    marked = [r for r in resp if r["provenance_exception"]]
    same("exception marked on one response", [(r["flight_id"], r["bank_deg"], r["onset_minus_0019_29_s"]) for r in marked], [(p["flight_id"], p["bank_deg"], p["onset_minus_0019_29_s"])])
    same("exception is not a continued response", (p["continued"], marked[0]["outcome"]), ("False", "FREQUENCY_NOT_MET_UNDER_ANY_DECLARED_TREATMENT"))
    V["prov_flight"] = p["flight_id"]
    V["prov_bank"] = "left" if float(p["bank_deg"]) < 0 else "right"
    V["prov_onset"] = p["onset_minus_0019_29_s"]
    V["prov_text"] = p["exception"]

    # ---- identity
    V["revision"], V["cruise_revision"], V["commit_short"] = REVISION, CRUISE_REVISION, COMMIT[:7]
    V["source_base"] = f"https://github.com/{REPO}/blob/{COMMIT}/{SOURCE_PATH}/"
    V["local_base"] = "data/terminal-responses-266/sources/"
    return collections.OrderedDict(
        meta=dict(repository=REPO, commit=COMMIT, path=SOURCE_PATH, revision=REVISION, cruise_revision=CRUISE_REVISION,
                  note="Values are formatted strings inserted into src/terminal_body.html by gen.py. Compiled from the copied source tables; no flight calculation and nothing evaluated at 22:41."),
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
        scope="Display import only. Counts and ranges are recomputed from the copied tables and reconciled with the published summary. This is not a scientific revalidation; no flight was computed and nothing was evaluated at 22:41.")
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

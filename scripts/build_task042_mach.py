#!/usr/bin/env python3
"""Compile the published TASK042 starting-Mach experiment from saved records.

Uses Python's standard library and committed publication files only. It does
not import a flight model, read model inputs, fit a route, or make predictions.

    python3 scripts/build_task042_mach.py          write display/validation JSON
    python3 scripts/build_task042_mach.py --check  verify; write nothing
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "task042-mach080-084"


def read_json(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def encoded(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + "\n"


def same_csv_value(text, value):
    if isinstance(value, bool):
        return text == str(value)
    if isinstance(value, float):
        return math.isfinite(float(text)) and float(text).hex() == value.hex()
    if isinstance(value, (list, dict)):
        return json.loads(text) == value
    if value is None:
        return text == ""
    return text == str(value)


def cells(values):
    return "<tr>" + "".join(
        f'<td class="n">{html.escape(str(v))}</td>' for v in values
    ) + "</tr>"


def compile_display():
    checks = []

    def ok(name, condition):
        if not condition:
            raise ValueError("Publication reconciliation failed: " + name)
        checks.append(name)

    manifest = read_json("source_manifest.json")
    for entry in manifest["files"]:
        path = OUT / entry["name"]
        ok("source identity: " + entry["name"],
           path.parent == OUT and path.is_file()
           and path.stat().st_size == entry["bytes"]
           and hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"])

    data = read_json("comparisons.json")
    design = read_json("design.json")
    audit = read_json("CLOSING_AUDIT.json")
    rows = data["result_rows"]
    retained = data["selected_comparisons"]
    with (OUT / "RESULTS.csv").open(newline="", encoding="utf-8") as f:
        source_rows = list(csv.DictReader(f))
    ok("experiment and source identities agree",
       data["experiment_id"] == design["experiment_id"] == manifest["experiment_id"]
       and data["revision"] == design["revision"] == manifest["experiment_revision"]
       and design["repository_source_commit"] == manifest["repository_source_commit"]
       and data["extraction"]["original"] == manifest["original_retained_comparisons"])
    expected = {(origin, mach) for origin in ("north", "south")
                for mach in design["first_Mach_targets"]}
    ok("one selected row for every requested origin and starting Mach",
       len(rows) == len(expected) == 10
       and {(r["origin"], r["first_Mach"]) for r in rows} == expected)
    ok("CSV and compact JSON agree in every field",
       len(source_rows) == len(rows)
       and all(set(c) == set(r) and all(same_csv_value(c[k], v)
               for k, v in r.items()) for c, r in zip(source_rows, rows)))
    ok("closed record has no active or failed flight",
       data["final_status"]["status"] == "BOUNDED_EXPERIMENT_COMPLETE"
       and data["final_status"]["worker_active"] is False
       and data["usage"]["in_flight"] is None
       and data["usage"]["software_failures"] == 0
       and data["usage"]["flights_started"] == data["usage"]["flights_completed"])
    ok("closing audit passed its declared integrity checks",
       audit["status"] == "PASS" and not audit["failures"]
       and all(c["passed"] is True for c in audit["checks"]))
    ok("all selections retain declared support and verification labels",
       all(r["search_status"] == "ELIGIBLE_SAMPLED_BEST"
           and r["verification_status"] == "VERIFIED"
           and r["physically_eligible"] is True
           and r["half_step_eligible"] is True
           and r["quarter_step_eligible"] is True
           and r["half_step_pass"] is True and r["quarter_step_pass"] is True
           and r["at0011_support"] == "POWERED_ACCEPTED_HISTORY" for r in rows))
    ok("starting-Mach and late-Mach conventions agree",
       all(r["final_plateau_Mach"] == r["first_Mach"] - 0.01
           and r["at0011_Mach"] == r["final_plateau_Mach"] for r in rows))

    by_key = {(x["origin"], x["first_Mach"]): x for x in retained}
    ok("one retained comparison group per selected row",
       len(retained) == len(rows) and set(by_key) == expected)
    comparisons = []
    early, late = design["loss_window_seconds_from194103"]
    for row in rows:
        item = by_key[(row["origin"], row["first_Mach"])]
        label = f"{row['origin']} {row['first_Mach']:.3f}"
        ok("retained identity and search status: " + label,
           item["production_id"] == row["retained_id"] == item["search"]["best_id"]
           and item["verification_status"] == row["verification_status"]
           and item["search"]["termination"] == row["search_reason"]
           and item["search"]["software_success"] == row["optimizer_software_success"])
        ok("supported 00:11 state matches CSV: " + label,
           item["production_state_0011"]["support"] == row["at0011_support"]
           and all(item["production_state_0011"][k] == row["at0011_" + k]
                   for k in item["production_state_0011"] if k != "support"))
        mesh_rows = item["physical_eligibility_by_mesh"]
        ok("eligibility and fuel edges at every mesh: " + label,
           [x["mesh_s"] for x in mesh_rows] == [15.0, 7.5, 3.75]
           and all(x["eligible"] is True and not x["reasons"]
                   and early <= x["loss_seconds_from_194103"] <= late
                   and x["early_margin_s"] == x["loss_seconds_from_194103"] - early
                   and x["late_margin_s"] == late - x["loss_seconds_from_194103"]
                   for x in mesh_rows))
        for prefix, mesh_row in zip(("production", "half_step", "quarter_step"), mesh_rows):
            ok("CSV fuel edges agree: " + label + " " + prefix,
               row[prefix + "_early_loss_margin_s"] == mesh_row["early_margin_s"]
               and row[prefix + "_late_loss_margin_s"] == mesh_row["late_margin_s"])
        comparisons.extend(item["comparisons"])

    limits = design["qualification"]["thresholds"]
    thresholds = {
        "delta_observation_chi2": limits["abs_observation_chi2_change"],
        "position_shift_m": limits["position_m"],
        "fuel_shift_kg": limits["fuel_kg"],
        "loss_shift_s": limits["loss_time_s"],
    }
    ok("twenty passing adjacent refinement comparisons",
       len(comparisons) == 20
       and all(c["passed"] is True and c["both_eligible"] is True
               and c["finite"] is True and c["resource_status_matches"] is True
               and (c["from_mesh_s"], c["to_mesh_s"]) in ((15.0, 7.5), (7.5, 3.75))
               and all(abs(c[k]) < limit for k, limit in thresholds.items())
               for c in comparisons))
    ok("no new 22:41 BTO prediction recorded",
       data["usage"]["BTO_prediction_counts"]["3"] == 0)
    ok("five distinct origin comparisons refer to selected flights",
       len(data["same_Mach_origin_comparisons"]) == 5
       and all(c["status"] == "DISTINCT_RETAINED_SAMPLES"
               and c["both_mesh_verified"] is True
               and c["north_id"] == by_key[("north", c["first_Mach"])]["production_id"]
               and c["south_id"] == by_key[("south", c["first_Mach"])]["production_id"]
               for c in data["same_Mach_origin_comparisons"]))
    ok("assumed starting fuel and mass agree with the recorded convention",
       data["start_assumptions"]["total_start_fuel_kg"] == design["fuel_kg"]
       and data["start_assumptions"]["APU_reserve_kg"] == design["APU_kg"]
       and data["start_assumptions"]["total_start_mass_kg"]
           == data["start_assumptions"]["nonfuel_mass_kg"] + design["fuel_kg"])

    result_html = []
    state_html = []
    for r in rows:
        term = "Cap reached" if r["search_reason"] == "PER_TARGET_OR_RESTORATION_CAP" else "Optimizer success"
        result_html.append(cells((r["origin"].title(), f"{r['first_Mach']:.3f}",
            f"{r['constant_pressure_hPa']:.3f}", f"{r['modified_J']:.6f}",
            f"{r['max_abs_kept_BTO_z']:.4f}", f"{r['max_abs_BFO_z']:.4f}", term)))
        # Display only: truncate UTC fractions at milliseconds; never use this
        # string for physical eligibility. Full recorded precision stays in CSV.
        loss_time = r["combustion_loss_UTC"].split("T")[1][:12]
        state_html.append(cells((r["origin"].title(), f"{r['first_Mach']:.3f}",
            f"{r['at0011_latitude_deg']:.6f}, {r['at0011_longitude_deg']:.6f}",
            f"{r['at0011_geometric_height_m']:,.2f}",
            f"{r['at0011_total_fuel_kg']:,.3f}", f"{r['at0011_fuel_above_APU_kg']:,.3f}", loss_time)))
    maxima = {k: max(abs(c[k]) for c in comparisons) for k in thresholds}
    mesh_html = [
        cells(("|Δ observation χ²|", f"{maxima['delta_observation_chi2']:.8f}", f"< {thresholds['delta_observation_chi2']:g}")),
        cells(("00:11 position shift", f"{maxima['position_shift_m']:.6f} m", f"< {thresholds['position_shift_m']:g} m")),
        cells(("|Δ fuel|", f"{maxima['fuel_shift_kg']:.9f} kg", f"< {thresholds['fuel_shift_kg']:g} kg")),
        cells(("|Δ engine-loss time|", f"{maxima['loss_shift_s']:.9f} s", f"< {thresholds['loss_shift_s']:g} s")),
    ]
    values = {
        "m84_results_rows": "\n".join(result_html),
        "m84_states_rows": "\n".join(state_html),
        "m84_mesh_rows": "\n".join(mesh_html),
        "m84_selected": str(len(rows)),
        "m84_comparisons": str(len(comparisons)),
        "m84_started": f"{data['usage']['flights_started']:,}",
        "m84_charged_s": f"{data['usage']['charged_execution_s']:,.3f}",
        "m84_capped": str(sum(r["search_reason"] == "PER_TARGET_OR_RESTORATION_CAP" for r in rows)),
        "m84_optimizer_success": str(sum(r["optimizer_software_success"] for r in rows)),
        "m84_revision": data["revision"],
        "m84_revision_short": data["revision"][:12],
        "m84_base": design["repository_source_commit"],
        "m84_base_short": design["repository_source_commit"][:12],
        "m84_archive_sha": manifest["record_archive"]["sha256"],
        "m84_status": data["final_status"]["status"],
        "m84_source_base": "data/task042-mach080-084/",
        "m84_flight_cap": f"{design['flight_cap']:,}",
        "m84_time_budget_s": f"{design['ceiling_s']:,}",
        "m84_search_trials": str(sum(data["unique_search_record_outcomes"].values())),
        "m84_initial_fuel_kg": f"{design['fuel_kg']:,.3f}",
        "m84_initial_mass_kg": f"{data['start_assumptions']['total_start_mass_kg']:,.3f}",
        "m84_m084_north_late_margin_ms": f"{by_key[('north', .84)]['physical_eligibility_by_mesh'][2]['late_margin_s'] * 1000:.6f}",
        "m84_m084_south_late_margin_ms": f"{by_key[('south', .84)]['physical_eligibility_by_mesh'][2]['late_margin_s'] * 1000:.6f}",
    }
    display = {"meta": {
        "experiment_id": data["experiment_id"], "revision": data["revision"],
        "note": "Formatted saved-record strings only. No model or prediction. Loss UTC is truncated to milliseconds for display; full precision and eligibility are preserved in sources.",
        "source_manifest_sha256": hashlib.sha256((OUT / "source_manifest.json").read_bytes()).hexdigest(),
    }, "values": values}
    validation = {"status": "PASS", "scope": "Publication-source hashes and saved-record reconciliation only; not a new scientific validation.",
        "checks": checks, "selected_rows": len(rows), "mesh_comparisons": len(comparisons),
        "observed_maximum_refinement_changes": maxima}
    return {"display.json": display, "validation.json": validation}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify saved outputs; write nothing")
    args = parser.parse_args()
    outputs = compile_display()
    for name, value in outputs.items():
        expected = encoded(value)
        if args.check:
            if not (OUT / name).is_file() or (OUT / name).read_text(encoding="utf-8") != expected:
                raise ValueError("Stale or missing publication output: " + name)
        else:
            (OUT / name).write_text(expected, encoding="utf-8")
    print("PASS: TASK042 Mach 0.80–0.84 publication sources; 10 rows, 20 mesh comparisons; "
          + ("outputs match, no files written" if args.check else "display and validation written"))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)

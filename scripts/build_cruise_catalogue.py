#!/usr/bin/env python3
"""Compile the completed cruise run's published tables for the Atlas.

Reads committed CSV/JSON files only. No model import, flight calculation, fitting,
ephemeris calculation, or interpolation is performed. Run with --check to verify
the source identities, every display record, and the committed generated files.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "cruise-production-108"
SRC = OUT / "sources"
RESERVE_KG = 6.80388555
COMMIT = "24655869cf3fe2452615157cf59c1ed3f28c3677"
REPO = "floydclaptonblues/MH370-Ocean-GLORYS-Data"
SOURCE_PATH = "reports/diagnostic/CRUISE_LEVEL_PRODUCTION_108"
SOURCE_BASE = f"https://github.com/{REPO}/blob/{COMMIT}/{SOURCE_PATH}/"
LOCAL_BASE = "data/cruise-production-108/sources/"


def number(value):
    if value == "" or value is None:
        return None
    result = float(value)
    assert math.isfinite(result), "Non-finite published numeric value"
    return result


def integer(value):
    result = number(value)
    if result is None:
        return None
    assert result.is_integer()
    return int(result)


def boolean(value):
    assert value in ("True", "False"), value
    return value == "True"


def table(name):
    with (SRC / name).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        assert not any("2241" in c or "22:41" in c for c in reader.fieldnames)
        rows = []
        for row in reader:
            row["_line"] = reader.line_num
            rows.append(row)
        return rows


def commands(row):
    return (row["configuration"], number(row["first_turn_deg"]),
            number(row["second_turn_start_s"]), number(row["second_turn_deg"]))


def position(row, epoch):
    return {"latitude": number(row[f"latitude_{epoch}"]),
            "longitude": number(row[f"longitude_{epoch}"]),
            "heightM": number(row[f"geometric_height_{epoch}_m"])}


def trial_counts(row, directional=False):
    prefix = "trial_flights_of_direction" if directional else "trial_flights"
    return {
        "total": integer(row[prefix + "_to_0011_in_ledger"]),
        "withEngineFuel": integer(row[prefix + "_with_engine_fuel_at_0011"]),
        "withEngineFuelAndEarlyTiming": integer(row[prefix + "_with_engine_fuel_meeting_2041_and_2141_bands"]),
        "withEngineFuelAndAllTiming": integer(row[prefix + "_with_engine_fuel_meeting_all_three_bands"]),
        "outOfFuel": integer(row[prefix + "_out_of_fuel_before_0011"]),
        "outOfFuelAndEarlyTiming": integer(row[prefix + "_out_of_fuel_meeting_2041_and_2141_bands"]),
        "closest0011ResidualAmongPoweredEarlyFitsUs": number(row[prefix + "_with_engine_fuel_meeting_2041_and_2141_closest_abs_0011_residual_us"]),
        "latestExhaustionBefore0011AllTrialsS": number(row[prefix + "_out_of_fuel_exhaustion_minus_0011_00_latest_s"]),
        "latestExhaustionBefore0011EarlyTimingTrialsS": number(row[prefix + "_out_of_fuel_meeting_2041_and_2141_exhaustion_minus_0011_00_latest_s"]),
    }


def check_row(row):
    return {
        "searchId": row["search_id"], "side": row["side"], "solutionIndex": integer(row["solution_index"]),
        "status": row["status"], "resolved": boolean(row["resolved"]), "halfStepS": number(row["half_step_s"]),
        "supportedTo0011": boolean(row["supported_to_0011_at_half_step"]),
        "positionDifference0011M": number(row["position_difference_0011_m"]),
        "timingDifference0011Us": number(row["timing_difference_0011_us"]),
        "fuelDifference0011Kg": number(row["fuel_difference_0011_kg"]),
        "eventDifferenceS": number(row["event_difference_s"]),
        "eventNominalS": number(row["event_nominal_s"]), "eventHalfStepS": number(row["event_half_step_s"]),
        "sameEnding": boolean(row["same_ending"]), "nominalEnding": row["ending_nominal"],
        "halfStepEnding": row["ending_half_step"],
        "sourceUrl": SOURCE_BASE + "PROD_NUMERICAL_CHECKS.csv#L" + str(row["_line"]),
    }


def compile_catalogue():
    manifest = json.loads((OUT / "source_manifest.json").read_text())
    assert manifest["commit"] == COMMIT
    assert manifest["runner_revision"] == "2a016b1294fa"
    for item in manifest["files"]:
        data = (SRC / item["name"]).read_bytes()
        assert len(data) == item["bytes"], item["name"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"], item["name"]
        assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == item["git_blob_sha"], item["name"]

    arrivals_raw = table("ARRIVALS_108.csv")
    configs_raw = table("PROD_CONFIGURATIONS.csv")
    directions_raw = table("PROD_DIRECTIONS.csv")
    solutions_raw = table("PROD_SOLUTIONS.csv")
    checks_raw = table("PROD_NUMERICAL_CHECKS.csv")
    levels_raw = table("PROD_SUMMARY_BY_GROUP_AND_LEVEL.csv")
    mixed_raw = table("PROD_GROUPS_WITH_MIXED_OUTCOMES.csv")
    official = json.loads((SRC / "PROD_SUMMARY.json").read_text())
    assert (len(arrivals_raw), len(configs_raw), len(directions_raw), len(solutions_raw), len(checks_raw), len(levels_raw), len(mixed_raw)) == (108, 424, 848, 1129, 218, 22, 30)

    arrivals = [{
        "id": r["arrival"], "sourceId": r["arrival_id"], "order": integer(r["order"]),
        "startingState": r["starting_state"], "group": r["group"], "mach": number(r["Mach_commanded"]),
        "incomingPressureHpa": number(r["incoming_pressure_hPa"]), "incomingAltitudeFt": integer(r["incoming_pressure_altitude_ft"]),
        "latitude1941": number(r["latitude_1941"]), "longitude1941": number(r["longitude_1941"]),
        "course1941": number(r["course_1941_deg"]), "fuel1941Kg": number(r["fuel_1941_kg"]), "mass1941Kg": number(r["mass_1941_kg"]),
        "pilot": boolean(r["in_pilot"]), "sourceUrl": SOURCE_BASE + "ARRIVALS_108.csv#L" + str(r["_line"]),
    } for r in arrivals_raw]
    arrival_by_id = {a["id"]: a for a in arrivals}
    config_source = {r["configuration"]: r for r in configs_raw}
    assert len(arrival_by_id) == 108 and len(config_source) == 424

    directions = [{
        "id": r["search_id"], "configId": r["configuration"], "arrival": r["arrival"], "side": r["side"],
        "ending": r["ending"], "coverage": r["coverage"], "stage": r["stage_of_ending"], "check": r["numerical_check"],
        "regression": r["regression"], "firstTurnRange": r["first_turn_range_deg"],
        "shortFlights": integer(r["short_flights"]), "fullFlights": integer(r["full_flights"]),
        "acceptedFlights": integer(r["distinct_accepted_flights"]), "trialCounts": trial_counts(r, directional=True),
        "sourceUrl": SOURCE_BASE + "PROD_DIRECTIONS.csv#L" + str(r["_line"]),
    } for r in directions_raw]
    direction_by_id = {d["id"]: d for d in directions}
    assert len(direction_by_id) == 848 and all(d["coverage"] == "FINISHED" for d in directions)

    # Follow the source's declared distinct representatives, then merge only exact
    # command identity across directions. The 862 source alias rows remain in the
    # unchanged CSV; they are not silently reclassified as separate flights here.
    distinct = [r for r in solutions_raw if boolean(r["distinct"])]
    assert len(distinct) == 267
    grouped = collections.defaultdict(list)
    for r in distinct:
        grouped[commands(r)].append(r)
    assert len(grouped) == 266
    checks_by_ref = {(r["configuration"], r["side"], r["solution_index"]): r for r in checks_raw}
    assert len(checks_by_ref) == 218
    canonical_refs = {(r["configuration"], r["side"], r["solution_index"]) for r in distinct}
    assert set(checks_by_ref) <= canonical_refs
    assert all(r["status"] == "PERFORMED" and boolean(r["resolved"]) and boolean(r["supported_to_0011_at_half_step"]) for r in checks_raw)

    flights = []
    sequence = collections.Counter()
    for key, rows in sorted(grouped.items()):
        cfg, first, second_start, second = key
        row = rows[0]
        sequence[cfg] += 1
        flight_id = f"{cfg}.F{sequence[cfg]}"
        # A command-identical return from the other direction must agree in all
        # exported scientific values, including the exhaustion continuation.
        scientific = list(row)[list(row).index("timing_residual_2041_us"):list(row).index("numerical_check")]
        for other in rows[1:]:
            assert all(row[k] == other[k] for k in scientific), flight_id
        linked_checks = []
        for s in rows:
            ref = (cfg, s["side"], s["solution_index"])
            if ref in checks_by_ref:
                cr = checks_by_ref[ref]
                assert commands(cr) == key, flight_id
                linked_checks.append(check_row(cr))
        checkpoints = []
        for epoch, utc in (("2041", "20:41:05"), ("2141", "21:41:27"), ("0011", "00:11:00")):
            checkpoints.append({"utc": utc, **position(row, epoch),
                "timingResidualUs": number(row[f"timing_residual_{epoch}_us"]),
                "frequencyResidualHz": number(row[f"frequency_residual_centred_{epoch}_Hz_reported_only"]),
                "fuelKg": number(row["fuel_0011_kg"]) if epoch == "0011" else None})
        assert all(abs(x["timingResidualUs"]) <= 43 for x in checkpoints)
        assert all(abs(x["frequencyResidualHz"]) <= 7 for x in checkpoints)
        engine_fuel, total_fuel = number(row["engine_fuel_above_reserve_0011_kg"]), number(row["fuel_0011_kg"])
        assert engine_fuel > 0 and abs(total_fuel - engine_fuel - RESERVE_KG) < 1e-9
        exhaustion = None
        if row["fuel_exhaustion_s_after_1941_03"]:
            exhaustion = {"utc": row["fuel_exhaustion_utc"], "secondsAfter1941": number(row["fuel_exhaustion_s_after_1941_03"]),
                "secondsAfter0011": number(row["exhaustion_minus_0011_00_s"]),
                "secondsRelativeToFinalLogon": number(row["exhaustion_minus_0019_29_s"]),
                "position": position(row, "at_exhaustion")}
        flags = sorted({r["on_end_of_searched_range"] for r in rows if r["on_end_of_searched_range"]})
        powered = row["continuation"] == "POWERED_TO_0040_CERTIFIED"
        assert powered == (exhaustion is None)
        flights.append({
            "id": flight_id, "configId": cfg, "arrival": row["arrival"], "group": row["group"],
            "mach": number(config_source[cfg]["Mach"]), "levelFt": integer(row["level_pressure_altitude_ft"]),
            "firstTurnDeg": first, "secondTurnStartS": second_start, "secondTurnDeg": second,
            "sides": sorted({r["side"] for r in rows}), "rangeEnd": bool(flags), "rangeEndFlags": flags,
            "position0011": position(row, "0011"), "fuel0011Kg": total_fuel,
            "engineFuel0011Kg": engine_fuel, "reserveKg": RESERVE_KG,
            "exhaustion": exhaustion, "poweredTo0040": powered, "continuation": row["continuation"],
            "check": {"performed": bool(linked_checks), "resolved": bool(linked_checks) and all(c["resolved"] for c in linked_checks), "rows": linked_checks},
            "checkpoints": checkpoints,
            "sourceRows": [{"side": r["side"], "index": integer(r["solution_index"]), "line": r["_line"],
                            "url": SOURCE_BASE + "PROD_SOLUTIONS.csv#L" + str(r["_line"])} for r in rows],
        })

    by_config = collections.defaultdict(list)
    for f in flights:
        by_config[f["configId"]].append(f["id"])
    configurations = []
    for r in configs_raw:
        cfg = r["configuration"]
        assert boolean(r["accepted_flight_exists"]) == bool(by_config[cfg])
        assert integer(r["distinct_accepted_flights"]) == len(by_config[cfg])
        assert boolean(r["both_directions_finished"])
        configurations.append({
            "id": cfg, "arrival": r["arrival"], "group": r["group"], "mach": number(r["Mach"]),
            "levelFt": integer(r["level_pressure_altitude_ft"]), "kind": r["configuration_kind"],
            "targetPressureHpa": number(r["target_pressure_hPa"]),
            "accepted": boolean(r["accepted_flight_exists"]), "summary": r["summary"],
            "left": direction_by_id[cfg + "#L"], "right": direction_by_id[cfg + "#R"],
            "flightIds": by_config[cfg], "trialCounts": trial_counts(r),
            "sourceUrl": SOURCE_BASE + "PROD_CONFIGURATIONS.csv#L" + str(r["_line"]),
        })
    groups = []
    for group in dict.fromkeys(r["group"] for r in arrivals_raw):
        members = [a for a in arrivals if a["group"] == group]
        first = members[0]
        levels = []
        for r in levels_raw:
            if r["group"] != group:
                continue
            count = integer(r["configurations"])
            accepted = integer(r["ACCEPTED_FLIGHT_FOUND"])
            level = integer(r["level_pressure_altitude_ft"])
            found = [c for c in configurations if c["group"] == group and c["levelFt"] == level]
            assert len(found) == count and sum(c["accepted"] for c in found) == accepted
            levels.append({"altitudeFt": level, "kind": r["configuration_kind"], "configurations": count,
                           "accepted": accepted, "notFound": integer(r["NO_ACCEPTED_FLIGHT_IN_THE_COMPLETED_SEARCH"])})
        groups.append({"id": group, "label": f"{first['incomingAltitudeFt']:,} ft · Mach {first['mach']:.2f}",
                       "mach": first["mach"], "incomingPressureHpa": first["incomingPressureHpa"],
                       "incomingAltitudeFt": first["incomingAltitudeFt"], "arrivals": len(members), "levels": levels})

    before = sum(f["exhaustion"] is not None and f["exhaustion"]["secondsRelativeToFinalLogon"] < 0 for f in flights)
    after = sum(f["exhaustion"] is not None and f["exhaustion"]["secondsRelativeToFinalLogon"] > 8 for f in flights)
    powered = sum(f["poweredTo0040"] for f in flights)
    assert (before, after, powered) == (90, 139, 37)
    assert sum(f["rangeEnd"] for f in flights) == 7
    assert sum(f["check"]["performed"] for f in flights) == 218
    assert len({c["arrival"] for c in configurations if c["accepted"]}) == 108
    summary = {
        "arrivals": len(arrivals), "configurations": len(configurations), "searches": len(directions),
        "acceptedConfigurations": sum(c["accepted"] for c in configurations),
        "noAcceptedConfigurations": sum(not c["accepted"] for c in configurations),
        "distinctFlights": len(flights), "directionalSolutions": len(distinct), "rawReturnedRows": len(solutions_raw),
        "numericalChecks": len(checks_raw), "resolvedChecks": sum(boolean(r["resolved"]) for r in checks_raw),
        "fuelEventsBeforeFinal": before, "fuelEventsAfterFinal": after, "poweredTo0040": powered,
        "rangeEndFlights": sum(f["rangeEnd"] for f in flights), "reserveKg": RESERVE_KG,
        "positionCheckMaxM": max(number(r["position_difference_0011_m"]) for r in checks_raw),
        "eventCheckMaxS": max(abs(number(r["event_difference_s"]) or 0) for r in checks_raw),
        "chargedSeconds": official["durable_account"]["settled_s"],
        "lostSeconds": official["durable_account"]["lost_s"],
        "allowanceSeconds": official["ceilings"]["total"],
        "position0011Extent": {"south": min(f["position0011"]["latitude"] for f in flights),
                               "north": max(f["position0011"]["latitude"] for f in flights),
                               "west": min(f["position0011"]["longitude"] for f in flights),
                               "east": max(f["position0011"]["longitude"] for f in flights)},
    }
    assert summary["acceptedConfigurations"] == official["summaries"]["ACCEPTED_FLIGHT_FOUND"] == 208
    assert summary["noAcceptedConfigurations"] == official["summaries"]["NO_ACCEPTED_FLIGHT_IN_THE_COMPLETED_SEARCH"] == 216
    assert summary["distinctFlights"] == official["distinct_accepted_flights_counted_once_per_configuration"]
    assert summary["numericalChecks"] == official["numerical_checks"]["owed"] == official["numerical_checks"]["resolved"]
    assert sum(c["trialCounts"]["total"] for c in configurations) == 16039

    dataset = {
        "schemaVersion": 1,
        "provenance": {"title": "Completed 108-arrival cruise-level catalogue", "publishedOn": "2026-11-16",
                       "repository": REPO, "commit": COMMIT, "runnerRevision": manifest["runner_revision"],
                       "sourceBaseUrl": SOURCE_BASE,
                       "files": [{**item, "url": SOURCE_BASE + item["name"], "localUrl": LOCAL_BASE + item["name"]} for item in manifest["files"]],
                       "compilation": "Published tables only; no flight integration or interpolation.",
                       "flightIdentity": "The published distinct representatives, merged across directions only for identical command triples within a configuration; .F numbers follow sorted commands, as in the terminal manifest.",
                       "observationRoles": {"timingFitted": ["20:41:05", "21:41:27", "00:11:00"],
                                            "timingBandUs": 43, "frequency": "Reported diagnostic under frozen calibration; not used for later acceptance.",
                                            "finalTransmissions": "Not evaluated in this cruise run.",
                                            "withheldMeasurement": "No prediction, residual or comparison at the withheld epoch; prior exposure is disclosed separately."}},
        "summary": summary, "groups": groups, "arrivals": arrivals, "configurations": configurations,
        "directions": directions, "flights": flights,
    }
    # JSON contains finite values only; a missing source value remains null.
    encoded = json.dumps(dataset, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n"
    validation = {
        "sourceCommit": COMMIT, "runnerRevision": manifest["runner_revision"],
        "sourceFilesVerified": len(manifest["files"]), "sourceChecks": "byte length, Git blob SHA-1, SHA-256",
        "arrivals": 108, "configurations": 424, "directions": 848, "sourceReturnedRows": 1129,
        "directionalDistinctRepresentatives": 267, "uniqueCommandRepresentatives": 266,
        "acceptedConfigurations": 208, "noAcceptedConfigurations": 216,
        "individualFlightsRepeated": 218, "numericalCheckRows": 218, "allChecksResolved": True,
        "groupLevelRowsReconciled": 22, "savedTransmissionCheckpoints": 798,
        "fuelEvents": 229, "poweredAt0040": 37, "fuelEventsBeforeFinal": 90, "fuelEventsAfterBothFinal": 139,
        "rangeEndFlights": 7, "distinctTrialsReconciled": 16039,
        "scientificValues": "Copied from source tables; fuel-reserve arithmetic checked; command-identical directional states checked for equality.",
        "flightCalculationsPerformed": 0, "interpolatedStates": 0,
        "catalogueSha256": hashlib.sha256(encoded.encode()).hexdigest(),
    }
    return encoded, json.dumps(validation, indent=2) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify existing generated assets without writing files")
    args = parser.parse_args()
    dataset, validation = compile_catalogue()
    generated = {"catalogue.json": dataset,
                 "catalogue.js": "// Compiled from the pinned published cruise tables; see source_manifest.json.\nwindow.CRUISE_PRODUCTION_108=" + dataset.rstrip() + ";\n",
                 "validation.json": validation}
    for name, content in generated.items():
        path = OUT / name
        if args.check:
            assert path.read_bytes() == content.encode(), "Generated file differs: " + name
        else:
            path.write_bytes(content.encode())
    print("PASS: 9 byte-verified sources; 108 arrivals, 424 configurations, 848 searches, 266 distinct flights, 218 checks; no flight computation.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build or verify the display values for the LRC cruise-climb pilot page.

Reads only the byte-identical saved files in data/lrc-cruise-climb-pilot/.
It imports no model and computes no flight. Every displayed count is recomputed
from the CSV tables; the time account is taken from the source manifest.

  python3 scripts/build_lrc_pilot.py          # write display.json
  python3 scripts/build_lrc_pilot.py --check  # verify sources and display.json
"""
import csv
import hashlib
import html
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'lrc-cruise-climb-pilot'
OWN = 'OWN_MACH_UNCHANGED_LEVEL'
POLICY = {'OWN': 'Own Mach, unchanged level (control)', 'STEP': 'LRC, step climb',
          'CC': 'LRC, continuous climb', 'LRC': 'LRC, unchanged level'}


def fail(msg):
    sys.exit('build_lrc_pilot: ' + msg)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name):
    with (DATA / name).open(newline='') as f:
        return list(csv.DictReader(f))


def fmt(x, d):
    return '{:,.{}f}'.format(x, d)


def utc(stamp, d):
    """Round an ISO time of day to d decimal places of a second (no truncation)."""
    hms = stamp[11:].split('+')[0]
    h, m, sec = hms.split(':')
    total = round(int(h) * 3600 + int(m) * 60 + float(sec), d)
    h, rem = divmod(total, 3600)
    m, sec = divmod(rem, 60)
    return '%02d:%02d:%0*.*f' % (h, m, 3 + d, d, sec)


def span(a, b, d):
    lo, hi = min(a, b), max(a, b)
    return ('{:.%df}' % d).format(lo) if round(lo, d) == round(hi, d) else ('{:.%df}–{:.%df}' % (d, d)).format(lo, hi)


def build():
    manifest = json.loads((DATA / 'source_manifest.json').read_text())
    for f in manifest['files']:
        if sha(DATA / f['name']) != f['sha256']:
            fail('source file differs from manifest: ' + f['name'])

    sides = rows('pilot_config_sides.csv')
    flights = rows('pilot_accepted_flights.csv')
    repeats = rows('pilot_numerical_repeats.csv')
    states = rows('pilot_states_0019.csv')
    if len(sides) != 48:
        fail('expected 48 configuration sides')

    retained = [r for r in flights if r['policy'] == OWN or r['final_round'] == 'True']
    lrc_retained = [r for r in retained if r['policy'] != OWN]
    endings = Counter(r['ending'] for r in sides)
    accepted = [r for r in sides if r['ending'].startswith('ACCEPTED')]
    by_side = defaultdict(list)
    for r in retained:
        by_side[(r['configuration'], r['side'])].append(r)
    root_sides = [k for k, v in by_side.items() if any(r['kind'] == 'CONVERGED_ROOT' for r in v)]

    unavailable = sum(1 for s in states if s['transmission_utc'] == '00:19:29' and s['status'] != 'POWERED_HISTORY_SAMPLE')
    powered = sum(1 for s in states if s['transmission_utc'] == '00:19:29' and s['status'] == 'POWERED_HISTORY_SAMPLE')
    if unavailable + powered != len(retained):
        fail('00:19:29 rows do not cover the retained set')
    climb_events = sorted(utc(r['event_utc'], 2) for r in lrc_retained)

    table = []
    order = {'OWN': 0, 'STEP': 1, 'CC': 2, 'LRC': 3}
    for (cfg, side) in sorted(by_side, key=lambda k: (k[0][:2], order[k[0].split('_')[1]], k[1])):
        v = by_side[(cfg, side)]
        roots = sum(r['kind'] == 'CONVERGED_ROOT' for r in v)
        worst = [max(abs(float(r[c])) for c in ('residual_2041_us', 'residual_2141_us', 'residual_0011_us')) for r in v]
        ev = sorted(utc(r['event_utc'], 1) for r in v)
        ending = next(s['ending'] for s in sides if s['config'] == cfg and s['side'] == side)
        note = 'range boundary (first turn 0°)' if 'END_OF' in ending else ('in band, no converged root' if roots == 0 else '')
        table.append('<tr><td>Arrival {}</td><td>{}</td><td>{}</td><td class="n">{}</td><td class="n">{}</td>'
                     '<td class="n">{}</td><td class="n">{}</td><td class="n">{}</td><td>{}</td></tr>'.format(
                         cfg[1], html.escape(POLICY[cfg.split('_')[1]]), 'Left' if side == 'L' else 'Right',
                         len(v), roots, span(min(worst), max(worst), 2), fmt(float(v[0]['fuel_at_0011_kg']), 0),
                         ev[0] if ev[0] == ev[-1] else ev[0] + '–' + ev[-1][3:], note))

    pos = [float(r['position_difference_0011_m']) for r in repeats]
    exh = [float(r['exhaustion_diff_s']) for r in repeats]
    acc = manifest['recorded_account_s']
    values = {
        'lrc_sides': str(len(sides)),
        'lrc_accepted_sides': str(len(accepted)),
        'lrc_root_sides': str(len(root_sides)),
        'lrc_fuel_sides': str(endings['FUEL_EXHAUSTED_BEFORE_THE_FIT_TIME_ON_EVERY_TRIAL_FLIGHT']),
        'lrc_nostart_sides': str(endings['NO_STARTING_POINT']),
        'lrc_returned': str(len(flights)),
        'lrc_retained': str(len(retained)),
        'lrc_retained_lrc': str(len(lrc_retained)),
        'lrc_controls': str(len(retained) - len(lrc_retained)),
        'lrc_unavailable_0019': str(unavailable),
        'lrc_powered_0019': str(powered),
        'lrc_climb_event_first': climb_events[0],
        'lrc_climb_event_last': climb_events[-1],
        'lrc_repeats': str(len(repeats)),
        'lrc_repeats_resolved': str(sum(r['resolved'] == 'True' for r in repeats)),
        'lrc_repeat_pos_max_m': '{:.3f}'.format(max(pos)),
        'lrc_repeat_exh_max_s': '{:.3f}'.format(max(exh)),
        'lrc_charged_total_s': fmt(acc['total'], 1),
        'lrc_ceiling_s': fmt(acc['ceiling'], 0),
        'lrc_revision': manifest['frozen_revision'],
        'lrc_report_commit_short': manifest['report_commit'][:7],
        'lrc_accepted_rows': '\n'.join(table),
    }
    meta = {'experiment': manifest['experiment'], 'revision': manifest['frozen_revision'],
            'source_manifest_sha256': sha(DATA / 'source_manifest.json'),
            'note': 'Formatted saved-record values only. No model or prediction.'}
    return {'meta': meta, 'values': values}


def main():
    out = json.dumps(build(), indent=2, ensure_ascii=False) + '\n'
    target = DATA / 'display.json'
    if '--check' in sys.argv:
        if not target.exists() or target.read_text() != out:
            fail('display.json is missing or out of date; run without --check')
        print('build_lrc_pilot: sources and display.json verified')
    else:
        target.write_text(out)
        print('build_lrc_pilot: wrote', target.relative_to(ROOT))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build or verify LRC fixed-recipe satellite-assessment display values.

Reads saved CSV/JSON and reviewed text only. No model import, flight, prediction,
offset fit, ranking or selection occurs. Original results remain unchanged.

  python3 scripts/build_lrc_assessment.py
  python3 scripts/build_lrc_assessment.py --check
"""
import csv
import hashlib
import html
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'lrc-cruise-climb-assessment'
OWN = 'OWN_MACH_UNCHANGED_LEVEL'
INSIDE = 'MEETS_THE_2241_TIMING'
OUTSIDE = 'OUTSIDE_THE_2241_TIMING_BAND'
POLICY = {OWN: 'Own Mach, unchanged level (control)',
          'LRC_STEP_CLIMB': 'LRC, step climb',
          'LRC_CONTINUOUS_CLIMB': 'LRC, continuous climb'}
ORDER = {OWN: 0, 'LRC_STEP_CLIMB': 1, 'LRC_CONTINUOUS_CLIMB': 2}


def require(condition, reason):
    if not condition:
        sys.exit('build_lrc_assessment: ' + reason)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def counts(rows, key):
    return dict(Counter(r[key] for r in rows))


def span(values, places=3):
    lo, hi = min(values), max(values)
    a, b = f'{lo:.{places}f}', f'{hi:.{places}f}'
    return a if a == b else f'{a} to {b}'


def build():
    manifest = json.loads((DATA / 'source_manifest.json').read_text())
    for f in manifest['files']:
        require(sha(DATA / f['name']) == f['sha256'], 'source identity changed: ' + f['name'])
    rows = json.loads((DATA / 'ASSESSMENT_42_ROWS.json').read_text())
    summary = json.loads((DATA / 'SUMMARY.json').read_text())
    with (DATA / 'ASSESSMENT_42_ROWS.csv').open(newline='') as f:
        csv_rows = list(csv.DictReader(f))
    require(len(rows) == len(csv_rows) == 42, 'expected the complete 42-record population')
    require([r['order'] for r in rows] == list(range(1, 43)), 'record order changed')
    require(len({r['record_id'] for r in rows}) == 42, 'record identifiers are not unique')
    for r, c in zip(rows, csv_rows):
        require(set(r) == set(c), 'CSV and JSON columns differ')
        require(all(c[k] == ('' if v is None else str(v)) for k, v in r.items()),
                'CSV and JSON values differ: ' + r['record_id'])
        numeric = [v for v in r.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
        require(all(math.isfinite(v) for v in numeric), 'nonfinite numeric field')
        require(r['stage_a_status'] == r['voice2314_numerical_status'] == 'PREDICTED', 'unusable prediction')
        require(r['policy'] in POLICY, 'unknown policy')
        require(r['voice2314_primary_utc'] == '23:14:03', 'voice time changed')
        require(r['voice2314_reference_half_width_hz'] == 7.0, 'voice reference band changed')
        require(r['voice2314_channel_offset_hz'] is None and not r['voice2314_channel_offset_estimated'],
                'voice channel offset has been introduced')
        require(r['voice2314_standard_uncertainty_hz'] is None and r['voice2314_diagnostic_only'] is True,
                'voice uncertainty/diagnostic convention changed')
        require(not r['voice2314_handshake_offset_applied'], 'handshake offset transferred to voice')
        timing = [abs(r['timing_residual_' + step + '_us']) <= 43.0 for step in ('full', 'half')]
        require(timing[0] == timing[1], 'timing band-edge straddle must be reported explicitly')
        require(r['timing_status'] == (INSIDE if timing[0] else OUTSIDE), 'timing status disagrees')
        freq = [abs(r['frequency_residual_centred_' + step + '_hz']) <= 7.0 for step in ('full', 'half')]
        require(all(freq) and r['frequency_diagnostic'] == 'WITHIN_7_HZ', '22:41 frequency status disagrees')
        voice = [abs(r['voice2314_residual_raw_' + step + '_hz']) <= 7.0 for step in ('full', 'half')]
        require(voice[0] == voice[1] and not r['voice2314_band_edge_straddled'], 'voice band-edge straddle')
        require(r['voice2314_band_status'] == ('WITHIN_REFERENCE_BAND' if voice[0] else 'OUTSIDE_REFERENCE_BAND'),
                'voice reference status disagrees')

    aliases = defaultdict(list)
    for r in rows:
        aliases[r['evaluation_id']].append(r)
    unique = [v[0] for v in aliases.values()]
    require(len(unique) == 41, 'expected 41 distinct recipes')
    require([[r['record_id'] for r in v] for v in aliases.values() if len(v) > 1] ==
            [['L3_CC:L:r1:i0', 'L3_CC:L:r1:i1']], 'duplicate-recipe mapping changed')
    for versions in aliases.values():
        for r in versions[1:]:
            require(all(r[k] == versions[0][k] for k in r if 'residual' in k or 'status' in k),
                    'duplicate recipe has inconsistent results')
    require(summary['retained_records'] == len(rows) and summary['distinct_evaluations'] == len(unique),
            'summary population differs')
    require(summary['source_seal_sha256'] == manifest['stage_a_seal_sha256'], 'summary seal differs')
    require(summary['stage_a_status'] == 'SEALED_COMPLETE' and summary['G6'] == 'ADVISORY_UNCHANGED',
            'completion/G6 convention differs')
    require(summary['fuel_window_screen_applied'] is False and summary['frequency_is_diagnostic_only'] is True,
            'selection/diagnostic convention differs')
    require(counts(rows, 'timing_status') == summary['record_counts'] and
            counts(unique, 'timing_status') == summary['distinct_evaluation_counts'], 'timing counts differ')
    require(counts(rows, 'voice2314_band_status') == summary['voice_reference_record_counts'] and
            counts(unique, 'voice2314_band_status') == summary['voice_reference_distinct_evaluation_counts'],
            'voice counts differ')

    by_group = defaultdict(list)
    for r in rows:
        by_group[(r['arrival'], r['policy'])].append(r)
    require(len(by_group) == 8, 'expected eight retained configuration groups')
    configuration_rows = []
    for (arrival, policy), records in sorted(by_group.items(), key=lambda p: (p[0][0], ORDER[p[0][1]])):
        inside = sum(r['timing_status'] == INSIDE for r in records)
        distinct = len({r['evaluation_id'] for r in records})
        configuration_rows.append(
            '<tr><td>Arrival {}</td><td>{}</td><td class="n">{} ({})</td>'
            '<td class="n">{}</td><td class="n">{}</td><td class="n">{}</td>'
            '<td class="n">{}</td></tr>'.format(arrival, html.escape(POLICY[policy]), len(records), distinct,
                inside, len(records) - inside,
                span([r['frequency_residual_centred_full_hz'] for r in records]),
                span([r['voice2314_residual_raw_full_hz'] for r in records])))
    outside_rows = []
    for versions in aliases.values():
        r = versions[0]
        if r['timing_status'] == OUTSIDE:
            outside_rows.append('<tr><td>{}</td><td class="n">{:+.6f}</td><td class="n">{:.6f}</td></tr>'.format(
                '<br>'.join('<code>' + html.escape(v['record_id']) + '</code>' for v in versions),
                r['timing_residual_full_us'], abs(r['timing_residual_full_us']) - 43.0))

    controls = [r for r in rows if r['policy'] == OWN]
    lrc = [r for r in rows if r['policy'] != OWN]
    require(all(r['voice2314_band_status'] == 'WITHIN_REFERENCE_BAND' for r in controls) and
            all(r['voice2314_band_status'] == 'OUTSIDE_REFERENCE_BAND' for r in lrc), 'voice group labels differ')
    repeat_t = max(abs(r['timing_residual_half_us'] - r['timing_residual_full_us']) for r in rows)
    repeat_f = max(abs(r['frequency_residual_centred_half_hz'] - r['frequency_residual_centred_full_hz']) for r in rows)
    repeat_v = max(abs(r['voice2314_residual_raw_half_hz'] - r['voice2314_residual_raw_full_hz']) for r in rows)
    require(repeat_t <= 0.1 and repeat_f <= 0.01 and repeat_v <= 0.01, 'numerical-repeat limit exceeded')
    require(repeat_v == max(abs(r['voice2314_half_minus_full_hz']) for r in rows), 'voice repeat receipt differs')
    values = {
        'lrca_record_count': str(len(rows)), 'lrca_distinct_count': str(len(unique)),
        'lrca_timing_within_records': str(summary['record_counts'][INSIDE]),
        'lrca_timing_within_distinct': str(summary['distinct_evaluation_counts'][INSIDE]),
        'lrca_timing_outside_records': str(summary['record_counts'][OUTSIDE]),
        'lrca_timing_outside_distinct': str(summary['distinct_evaluation_counts'][OUTSIDE]),
        'lrca_frequency_within_records': str(sum(r['frequency_diagnostic'] == 'WITHIN_7_HZ' for r in rows)),
        'lrca_voice_control_records': str(len(controls)),
        'lrca_voice_lrc_records': str(len(lrc)),
        'lrca_voice_lrc_distinct': str(len({r['evaluation_id'] for r in lrc})),
        'lrca_configuration_rows': '\n'.join(configuration_rows),
        'lrca_outside_rows': '\n'.join(outside_rows),
        'lrca_repeat_bto_us': f'{repeat_t:.9f}',
        'lrca_repeat_bfo_hz': f'{repeat_f:.9f}',
        'lrca_repeat_voice_hz': f'{repeat_v:.9f}',
        'lrca_control_voice_range_hz': span([r['voice2314_residual_raw_full_hz'] for r in controls]),
        'lrca_lrc_voice_range_hz': span([r['voice2314_residual_raw_full_hz'] for r in lrc]),
        'lrca_control_frequency_range_hz': span([r['frequency_residual_centred_full_hz'] for r in controls]),
        'lrca_lrc_frequency_range_hz': span([r['frequency_residual_centred_full_hz'] for r in lrc]),
        'lrca_revision': manifest['assessment_revision'][:12],
        'lrca_seal_sha256': manifest['stage_a_seal_sha256'],
        'lrca_assessment_csv_sha256': sha(DATA / 'ASSESSMENT_42_ROWS.csv'),
    }
    return {'meta': {'experiment': manifest['experiment'], 'revision': manifest['assessment_revision'],
                     'source_manifest_sha256': sha(DATA / 'source_manifest.json'),
                     'note': 'Formatted saved-record comparisons only. No model, new prediction, offset fit or route selection.'},
            'values': values}


def main():
    out = json.dumps(build(), indent=2, ensure_ascii=False) + '\n'
    target = DATA / 'display.json'
    if '--check' in sys.argv:
        require(target.exists() and target.read_text() == out, 'display.json missing or out of date')
        print('build_lrc_assessment: exact sources, 42 records / 41 recipes, labels and display.json verified')
    else:
        target.write_text(out)
        print('build_lrc_assessment: wrote', target.relative_to(ROOT))


if __name__ == '__main__':
    main()

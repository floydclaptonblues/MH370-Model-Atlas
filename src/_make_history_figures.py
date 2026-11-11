#!/usr/bin/env python3
"""Figures for the Flight histories page, drawn from the retained dossier tables only.

Inputs, read directly from the extracted dossier root
(MH370_Flight_Histories_Data.zip, SHA-256 3d3e5c3e...eb8fe0ed):
  <root>/upstream/extracted/ACCEPTED_BOUNDARIES.csv   (all 24,217 accepted powered-flight rows)
  <root>/events/SATCOM_COMPARISONS.csv
and, for the terminal endpoints, TERMINAL_PATH_TO_SURFACE_CATALOGUE/CONTINUATION_OUTCOMES.csv
(MH370-Ocean-GLORYS-Data, commit 95d1b5a). Only the plotted columns are used; no intermediate
dataset is needed.

No model is run here: every plotted value is a stored number.
Usage: python3 src/_make_history_figures.py <extracted_dossier_root> [<continuation_outcomes.csv>]
"""
import csv, math, os, sys
from datetime import datetime, timezone
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

SRC = sys.argv[1] if len(sys.argv) > 1 else '.'
CONT = sys.argv[2] if len(sys.argv) > 2 else None
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img')

# Okabe-Ito, distinguishable without colour and in greyscale
COL = {'C190_J1': '#0072B2', 'C190_J2': '#56B4E9', 'C191_J1': '#D55E00', 'C191_J2': '#E69F00',
       'C192_J1': '#009E73', 'C192_J2': '#66C2A5'}
DASH = {'C190_J1': '-', 'C190_J2': (0, (5, 2)), 'C191_J1': '-', 'C191_J2': (0, (5, 2)),
        'C192_J1': '-', 'C192_J2': (0, (5, 2))}
HIST = ['C190_J1', 'C190_J2', 'C191_J1', 'C191_J2', 'C192_J1', 'C192_J2']
plt.rcParams.update({'font.size': 9, 'axes.titlesize': 10, 'figure.facecolor': 'white'})

T0 = datetime(2014, 3, 7, 18, 22, 12, tzinfo=timezone.utc)
def hrs(u):
    s = u.replace('Z', '+00:00')
    return (datetime.fromisoformat(s) - T0).total_seconds() / 3600.0
def hm(h):
    t = T0.timestamp() + h * 3600
    return datetime.fromtimestamp(t, timezone.utc).strftime('%H:%M')

rows = list(csv.DictReader(open(os.path.join(SRC, 'upstream', 'extracted', 'ACCEPTED_BOUNDARIES.csv'), newline='')))
by = {h: [r for r in rows if r['history'] == h] for h in HIST}
sat = list(csv.DictReader(open(os.path.join(SRC, 'events', 'SATCOM_COMPARISONS.csv'), newline='')))
f = lambda r, k: float(r[k]) if r.get(k) not in (None, '', 'NA') else float('nan')

# ---------------------------------------------------------------- 1. routes
fig, (ax, axz) = plt.subplots(1, 2, figsize=(12.6, 7.4), dpi=170,
                              gridspec_kw={'width_ratios': [1, 1.25]})
for h in HIST:
    r = by[h]
    ax.plot([f(x, 'longitude_deg') for x in r], [f(x, 'latitude_deg') for x in r],
            color=COL[h], ls=DASH[h], lw=1.5, label=h.replace('_', ' '), zorder=3)
# satellite epochs: mark the position of each history at each comparison epoch
ep_utc = sorted({x['epoch_utc'] for x in sat if x['epoch'] not in ('B1825', 'B1828a', 'B1828b', 'B1839')})
for eu in ep_utc:
    th = hrs(eu)
    for h in HIST:
        r = by[h]
        k = min(range(len(r)), key=lambda i: abs(hrs(r[i]['utc']) - th))
        if abs(hrs(r[k]['utc']) - th) < 0.02:
            ax.plot(f(r[k], 'longitude_deg'), f(r[k], 'latitude_deg'), 'o', ms=4.5,
                    mfc='none', mec='k', mew=1.0, zorder=5)
    r = by['C191_J1']
    k = min(range(len(r)), key=lambda i: abs(hrs(r[i]['utc']) - th))
    ax.annotate(eu[11:16], (f(r[k], 'longitude_deg'), f(r[k], 'latitude_deg')),
                (7, 4), textcoords='offset points', fontsize=8, color='0.25')
for h in HIST:                                   # fuel event = end of powered flight
    r = by[h][-1]
    ax.plot(f(r, 'longitude_deg'), f(r, 'latitude_deg'), marker='*', ms=11,
            color=COL[h], mec='k', mew=.5, zorder=6)
ax.plot(f(by['C190_J1'][0], 'longitude_deg'), f(by['C190_J1'][0], 'latitude_deg'), 's', ms=7, color='k', zorder=7)
ax.annotate('18:22:12 radar handoff',
            (f(by['C190_J1'][0], 'longitude_deg'), f(by['C190_J1'][0], 'latitude_deg')),
            (10, -2), textcoords='offset points', fontsize=8.5)
ax.set_xlabel('Longitude (°E)'); ax.set_ylabel('Latitude (°N)')
ax.set_title('Six connected histories: 18:22:12 UTC to fuel exhaustion\n'
             'circles: satellite epochs · stars: fuel event', loc='left', fontsize=9.5)
ax.set_xlim(86.5, 105.0); ax.set_ylim(-35.5, 8.5)
ax.set_aspect(1 / math.cos(math.radians(-14))); ax.grid(lw=.3, alpha=.5)
ax.legend(fontsize=7.5, loc='lower right', framealpha=.95)

for h in HIST:                                   # terminal zoom
    r = [x for x in by[h] if f(x, 'latitude_deg') < -31.5]
    axz.plot([f(x, 'longitude_deg') for x in r], [f(x, 'latitude_deg') for x in r],
             color=COL[h], ls=DASH[h], lw=1.6, zorder=3)
    axz.plot(f(by[h][-1], 'longitude_deg'), f(by[h][-1], 'latitude_deg'), marker='*',
             ms=12, color=COL[h], mec='k', mew=.5, zorder=6)
if CONT and os.path.exists(CONT):
    co = [x for x in csv.DictReader(open(CONT)) if x['phase'] == 'PRODUCTION']
    axz.plot([f(x, 'end_longitude_deg') for x in co], [f(x, 'end_latitude_deg') for x in co],
             'x', ms=5, color='0.25', mew=1.0, zorder=7, label='terminal reporting endpoints (68)')
    axz.legend(fontsize=8, loc='upper right', framealpha=.95)
axz.set_xlabel('Longitude (°E)'); axz.set_ylabel('Latitude (°N)')
axz.set_title('Terminal area: the final powered segment, the fuel event (stars)\nand the 68 terminal reporting endpoints (×)', loc='left', fontsize=9.5)
axz.set_xlim(94.2, 96.5); axz.set_ylim(-33.75, -31.6)
axz.set_aspect(1 / math.cos(math.radians(-33))); axz.grid(lw=.3, alpha=.5)
fig.text(.005, .006, 'Stored values from the retained dossier records; no model was run to draw this figure. '
         'Conditional reconstruction — not a located aircraft.', fontsize=7, color='0.35')
fig.tight_layout(rect=(0, .022, 1, 1), w_pad=2.5); fig.savefig(os.path.join(OUT, 'HISTORIES_ROUTES.png'))

# ------------------------------------------------------- 2. fuel and mass
fig, (a1, a2) = plt.subplots(2, 1, figsize=(11.4, 6.6), dpi=170, sharex=True)
for h in HIST:
    r = by[h]
    t = [hrs(x['utc']) for x in r]
    a1.plot(t, [f(x, 'fuel_total_kg') / 1000 for x in r], color=COL[h], ls=DASH[h], lw=1.5,
            label=h.replace('_', ' '))
    a2.plot(t, [f(x, 'mass_kg') / 1000 for x in r], color=COL[h], ls=DASH[h], lw=1.5)
    a1.plot(t[-1], f(r[-1], 'fuel_total_kg') / 1000, '*', ms=11, color=COL[h], mec='k', mew=.5)
for ax_, lbl in ((a1, 'Fuel on board (tonnes)'), (a2, 'Total aircraft mass (tonnes)')):
    ax_.grid(lw=.3, alpha=.5); ax_.set_ylabel(lbl)
    for th, txt in ((hrs('2014-03-07T19:41:03Z'), '19:41'), (hrs('2014-03-07T20:41:05Z'), '20:41'),
                    (hrs('2014-03-07T21:41:27Z'), '21:41'), (hrs('2014-03-07T22:41:22Z'), '22:41'),
                    (hrs('2014-03-08T00:11:00Z'), '00:11')):
        ax_.axvline(th, color='0.7', lw=.7, ls=':')
    ax_.axvline(hrs('2014-03-08T00:17:30Z'), color='#CC79A7', lw=1.1)
a1.annotate('satellite comparison epochs', (hrs('2014-03-07T20:41:05Z'), 30), (6, 0),
            textcoords='offset points', fontsize=8, color='0.35')
a1.annotate('engine-usable fuel exhausted ≈00:17:29–00:17:34\n(6.804 kg APU reserve retained)',
            (hrs('2014-03-08T00:17:30Z'), 12), (-224, 6), textcoords='offset points', fontsize=8.5,
            color='#8c4f72', arrowprops=dict(arrowstyle='->', color='#CC79A7', lw=.9))
APU0, APU1 = hrs('2014-03-08T00:24:21Z'), hrs('2014-03-08T00:24:26Z')
for ax_ in (a1, a2):
    ax_.axvline((APU0 + APU1) / 2, color='0.3', lw=1.3, ls=(0, (4, 2)))   # 5 s wide: drawn as a line at this scale
    ax_.set_xlim(-0.12, hrs('2014-03-08T00:30:00Z'))
a2.annotate('APU fuel exhausted 00:24:21–00:24:26 in all 68 continued flights\n(dashed line; after the powered record ends at the fuel event)',
            ((APU0 + APU1) / 2, 181), (-330, 14), textcoords='offset points', fontsize=8.5,
            color='0.3', arrowprops=dict(arrowstyle='->', color='0.5', lw=.9))
a2.set_xlabel('UTC, 7–8 March 2014')
tk = [0, 1, 2, 3, 4, 5, 6]
a2.set_xticks(tk); a2.set_xticklabels([hm(v) for v in tk])
a1.set_title('Fuel and decreasing mass against the clock, from the 18:22:12 handoff', loc='left')
a1.legend(fontsize=8, ncol=3, loc='lower left', framealpha=.95)
fig.text(.005, .006, 'Retained per-step resource records (λ_ff = 1.005). The six histories differ by under 3 kg at 19:41 '
         'and by about 6 kg at 00:11; the curves overlie at this scale.', fontsize=7, color='0.35')
fig.tight_layout(rect=(0, .022, 1, 1)); fig.savefig(os.path.join(OUT, 'HISTORIES_FUEL_MASS.png'))

# ------------------------------------------------- 3. satellite comparisons
fig, (b1, b2) = plt.subplots(2, 1, figsize=(11.4, 6.8), dpi=170, sharex=True)
order = ['B1825', 'B1828a', 'B1828b', 'B1839', '19:41:03', '20:41:05', '21:41:27', '22:41:22', '00:11:00']
xs = {e: i for i, e in enumerate(order)}
for comp, ax_ in (('BTO', b1), ('BFO', b2)):
    rowsc = [x for x in sat if x['component'] == comp]
    for h in HIST:
        hr = [x for x in rowsc if x['history'] == h]
        pts = [(xs[x['epoch']] + (HIST.index(h) - 2.5) * 0.08, f(x, 'residual_observed_minus_predicted')) for x in hr if x['epoch'] in xs]
        ax_.plot([p[0] for p in pts], [p[1] for p in pts], 'o', ms=5, color=COL[h],
                 mec='k', mew=.4, label=h.replace('_', ' ') if comp == 'BTO' else None)
    # The recorded bound applies to the CENTRED residual (raw minus the recorded centre mu).
    # On this raw-residual axis the band is therefore [-b + mu, +b + mu]: for BFO, mu = -0.18 Hz
    # gives -7.18 .. +6.82 Hz. BTO rows carry no centre, so their band is symmetric.
    bnd = {}
    for x in rowsc:
        if x['epoch'] in xs and x['descriptive_bound'] not in ('', 'NA'):
            mu = f(x, 'bfo_center_mu_hz') if comp == 'BFO' and x.get('bfo_center_mu_hz') not in (None, '', 'NA') else 0.0
            bnd[xs[x['epoch']]] = (f(x, 'descriptive_bound'), mu)
    for i, (b, mu) in bnd.items():
        ax_.plot([i - .42, i + .42], [b + mu, b + mu], color='0.45', lw=1.0)
        ax_.plot([i - .42, i + .42], [-b + mu, -b + mu], color='0.45', lw=1.0)
    wh = {xs[x['epoch']] for x in rowsc if 'WITHHELD' in x['policy_role'] and x['epoch'] in xs}
    for i in wh:
        ax_.axvspan(i - .45, i + .45, color='#F0E442', alpha=.35, zorder=0)
    ax_.axhline(0, color='k', lw=.7); ax_.grid(lw=.3, alpha=.45, axis='y')
    ax_.set_ylabel('BTO residual (µs)' if comp == 'BTO' else 'Raw BFO residual (Hz)')
b2.set_xticks(range(len(order)))
b2.set_xticklabels(['18:25', '18:28a', '18:28b', '18:39', '19:41', '20:41', '21:41', '22:41', '00:11'])
b2.set_xlabel('Satellite comparison epoch, 7–8 March 2014 UTC')
b1.set_title('Observed minus predicted satellite measurements, by history\n'
             'grey bars: the recorded descriptive bound · shaded: the withheld 22:41 BTO check, not used in fitting', loc='left')
b1.legend(fontsize=8, ncol=3, loc='upper right', framealpha=.95)
fig.text(.005, .006, 'Stored comparison records. Bounds are recorded only for the inherited 18:25–18:39 epochs: ±43 µs BTO, and ±7 Hz on the centred BFO residual '
         '(raw + 0.18 Hz), drawn here on the raw axis at −7.18 and +6.82 Hz.\nOnly the 22:41 BTO comparison was withheld; the 22:41 BFO is a supplementary, previously exposed value. '
         'Two withheld BTO residuals, −43.546 and −43.164 µs, fall just outside the inherited ±43 µs band and are reported as they stand.',
         fontsize=6.6, color='0.35')
fig.tight_layout(rect=(0, .04, 1, 1)); fig.savefig(os.path.join(OUT, 'HISTORIES_SATCOM.png'))
print('wrote HISTORIES_ROUTES.png, HISTORIES_FUEL_MASS.png, HISTORIES_SATCOM.png')

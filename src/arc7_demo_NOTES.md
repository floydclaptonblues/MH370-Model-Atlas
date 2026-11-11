# Arc 7 demonstration: source and adaptation

Added at Ryan's request as a demonstration tool within the existing Model Atlas.

## Source

- Supplied file: `Arc 7 Hotspot Demonstration.html` (62,168 bytes).
- SHA-256: `10f6ebd96cf4d3f7de682e1777d1073c1beb8265f83d47189abdf43b75e0fdeb`.
- The uploaded original is unchanged. This page is an adaptation.
- The source contains a six-vertex schematic arc, five fixed markers, fixed campaign counts and a browser-only fuel calculation. It imports no production kernel, weather, satellite observations or retained flight records.
- Its campaign snapshot is labelled 1 November 2026, 10:00 UTC. The adaptation preserves those supplied numbers as a historical snapshot, without independently certifying them or changing the current catalogue populations.

## Presentation and copy

The tool uses `common.css` and the existing ten-entry console shell. All additional styling is scoped to `.arc7-tool` in `arc7-demo.css`. It is linked from the Overview's Scientific tools section and from Methods. No shared scientific figures or datasets are regenerated.

The map and calculator are immediately available. Expandable notes retain the explanatory material and historical snapshot. Map markers are numbered and described as supplied reference points; unsupported assertions about their present admissibility, sonar coverage or comparative ranking are removed. All coordinates are preserved.

The explanatory copy distinguishes a finite evaluated family from all possible flights, describes a holdout as an out-of-sample diagnostic, and corrects the round-trip range conversion, fixed-airspeed wind explanation, induced-drag relation and regular ERA5 product-grid wording. These edits do not constitute new investigation results.

## Demonstration calculation

The supplied constants are unchanged: non-fuel mass 174,369 kg; initial fuel 27,856.86569474842 kg; Mach 0.84; wing area 427.8 m²; density 0.3639 kg/m³; sound speed 296.6 m/s; `CD0=0.019`, `KI=0.045`, `TSFC=1.55e-5`, `CLMAX=0.70`; flow scales 1.000000 and 1.024738. Reference clock: 7 March 2014, 19:41:03 UTC.

The explicit 60-second stepping is retained, with the final step shortened to the remaining inventory divided by that step's fuel flow. Reported exhaustion times therefore differ from the supplied version, which rounded up to the next full minute and allowed negative internal fuel. At depletion, actual flow and further burn display zero; the other aerodynamic readouts are the last fixed-cruise requirements. Step and Finish run are disabled until Reset or Replay. No post-exhaustion flight is integrated.

Controls: Play/Pause, Step 1 min, Finish run, Reset, and Replay after exhaustion. Reset clears playback and pending equation highlights. The chart shows both precomputed illustrative flow-scale runs, powered fuel flow and the current step cursor. The browser example does not estimate a terminal position.

## Build

`python3 gen.py` assembles `arc7-demo.html` from `src/arc7_demo_body.html`; `src/arc7_demo.js` is loaded as a separate script. The other generated pages change only where the two new links are added.

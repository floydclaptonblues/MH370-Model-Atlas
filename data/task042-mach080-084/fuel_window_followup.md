# TASK042 fuel-window follow-up | 22 November 2026

The original starting-Mach campaign remains frozen. See [its source identities](source_manifest.json).

- **Saved-record audit:** 523 distinct 15-second search trials were checked; 238 met the original support and combustion-thrust-loss criteria. The screen in [fuel_window_screen.csv](fuel_window_screen.csv) applies minimum headroom to either edge of the unchanged time window (00:16:29–00:17:59 UTC), then selects the lowest recorded combined score among retained rows. No flight was run for the audit. This is neither a new fit nor a physical uncertainty allowance.
- **Numerical refinement:** The two saved starting-Mach 0.830 recipes were replayed first at 15 seconds, then at 7.5 and 3.75 seconds, without refitting or changing the model. The criteria for each adjacent comparison were changes under 5 s in thrust-loss time, 10 m in 00:11 position, 1 kg in 00:11 total fuel and 0.01 in observation χ², with both records eligible with nonnegative model-support margins. Both candidates passed both refinements. The [six-row comparison export](mach083_fixed_step_checks.csv) measures each delta from the prior step, or from the archived result for 15-second replays.
- **Observation scope:** The original modified objective uses three fitted timing observations (BTO), five frequency observations (BFO) and the MID prior. The 19:41 BTO closes starting longitude. No new 22:41 BTO prediction was calculated; the 22:41 BFO term was retained. Historical setup exposure remains disclosed.
- **Interpretation:** No wider search, terminal continuation, impact calculation or LRC/G6 action took place. 00:11 coordinates in the CSV are model airborne checkpoints, not thrust-loss or impact locations. Mesh agreement is not a physical uncertainty bound.

## Full record identities

These archives are hash-identified here; the Atlas hosts the compact exports above, not the full archives.

| Record | SHA-256 |
| --- | --- |
| `TASK042_Fuel_Headroom_Audit.zip` | `7d686d01049ff9876de22b5706f8e79b8fc808c3b90db86400d24f706c27afbd` |
| `TASK042_Mach083_Fixed_Recipe_Refinement.zip` | `a51e8cb93a1e5b7107e33e2af276330788539d90d747f53023eabf547870c6e2` |

Refinement ID: `TASK042_MACH083_FIXED_INPUT_REFINEMENT_001`. Six calls, 73.465 seconds charged.

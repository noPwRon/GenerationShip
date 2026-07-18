# Next Steps

Status snapshot from a CORTEX project review, 2026-07-18. Overall dev status ~10%, matching the README estimate. 17/17 tests passing at time of review.

## Fix first

- **`structural/hull_stress.py:356`** — `run_hull_stress_analysis()` calls `angular_velocity_rad_s()`, but the function actually defined earlier in the file is `ring_angular_velocity_rad_s()`. This raises `NameError` on any call. Everything else in the file is a correct skeleton (stub returns), so this is a wiring mistake, not a design gap — one-line fix.
- Most recent commit (`aacd28a code update`) doesn't follow the `[VOICE]` commit-prefix convention from CLAUDE.md. Not urgent, just noted for consistency.

## Module completion, by zone

| Zone | Files | State |
|---|---|---|
| Habitat/Env (LYRA) | `env/hvac/*`, `env/rooms/*` | Most complete. 5 room types registered (`ChildDorm8`, `DormCommunal8`, `HygieneBlock`, `IntimacyPod`, `Warehouse`), ventilation/exhaust math implemented and tested. |
| Power (IGNIS) | `power/bus.py` | Fully implemented (52 lines, no TODOs) — generation/consumption summation, `power_balance()`. |
| Life Support (LYRA) | `life_support/air_cycle_design.py`, `air_cycle_sim.py` | Substantial (444 + 254 lines) but both still carry TODO stubs — mid-implementation. |
| Structural (TRUSS) | `structural/hull_stress.py` | Skeleton, newest file, currently broken (see Fix first). |
| Thermal (TRUSS) | `thermal/heat_recovery.py`, `network.py`, `materials.py` | `heat_recovery.py` has real content (261 lines). `network.py` (52) and `materials.py` (27) are near-empty — the node/edge thermal model isn't really built yet. |
| Maintenance (TRUSS) | `maintenance/*` | Planner/assets/policies all present with TODOs — mid-skeleton. |
| Propulsion (THRUM) | — | No module exists. `configs/structure/targets.yaml` has a placeholder `propulsion:` block (500 kN thrust) with an explicit note that there's no model yet. |
| Governance / Command | — | Not started. |

## Suggested entry points

1. Fix the `angular_velocity_rad_s` NameError in `structural/hull_stress.py` — restores the skeleton to a runnable state.
2. `thermal/network.py` and `materials.py` are the thinnest active files — natural next step for TRUSS work after hull stress.
3. THRUM (propulsion) has no code home at all. Starting it means creating a new module, not extending an existing one — will need a `propulsion/` package and a registry entry.

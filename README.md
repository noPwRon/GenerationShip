# Generation Ship — Habitat Systems Framework

> *"A starship is not built once. It is grown — layer by layer, equation by equation."*  
> — CORTEX, Core Systems Aggregate

A first-principles engineering simulation of a self-sustaining multi-generational interstellar vessel — built subsystem by subsystem in Python, grounded in NASA and NIST reference standards.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Tests](https://img.shields.io/badge/tests-17%20passing-brightgreen)
![Status](https://img.shields.io/badge/status-active%20development-orange)

---

## What This Demonstrates

This project is a portfolio showcase for engineering-focused Python development. It is intentionally ambitious in scope — the goal is not a finished product but a codebase that reflects how I approach complex, multi-domain systems problems.

**Software architecture**
- Strict separation between data (YAML specs), logic (domain modules), and configuration (scenario overrides)
- Flat-package Python with a registry pattern for extensible room calculators
- Type-annotated throughout; dataclasses for structured outputs; `pint` for unit-safe quantities

**Physics and engineering modeling**
- Thermodynamic helpers sourced from NIST CODATA 2018, NASA Glenn coefficients, and IAPWS IF-97
- Moist air density, saturation vapor pressure (Tetens), latent heat of vaporization, and specific heat polynomial (200–6000 K)
- Ventilation and heat load calculations referenced to NASA-STD-3001 and ASHRAE standards
- Explicit safety margins — no hidden multipliers

**Data architecture**
- YAML-first design: canonical specs in `data/specs/`, scenario overrides in `configs/`, deep-merged at load time
- In-memory caching layer (`data/cache.py`) with force-reload support
- Schema validation stubs in `data/schemas/` for evolving enforcement

**Testing discipline**
- 17 pytest tests pinning ventilation, exhaust, HVAC design tables, power bus, and room calculators
- Physical constants pinned at known reference points (273.15 K, 293.15 K) to catch silent regressions

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Language | Python 3.11+ |
| Unit handling | [pint](https://pint.readthedocs.io/) |
| Data | PyYAML + custom YAML cache |
| Numerics | NumPy |
| Testing | pytest |
| Package management | [uv](https://docs.astral.sh/uv/) |
| Reference standards | NASA-STD-3001, NIST CODATA 2018, IAPWS IF-97, ASHRAE |

---

## Quick Start

```bash
# Install dependencies
uv sync --dev

# Run the snapshot demo
uv run python scripts/demo.py

# Run the test suite
uv run pytest tests/ -v
```

**Example output from `demo.py`:**
```
=== Power Bus ===
  + main_reactor: 10.0 kW
  Net available: 10.0 kW

=== Room Environment Profiles ===
  child_dorm_8         ventilation=27.2 L/s  sensible=0.64 kW
  dorm_communal_8      ventilation=28.4 L/s  sensible=0.64 kW
  hygiene_block        ventilation=101.4 L/s  sensible=— kW
```

---

## Working with the API

```python
# Compute a room's environment profile from the registry
from ship.registry import compute

report = compute("child_dorm_8")
print(report.hvac)
# {'ventilation_Lps': 27.2, 'sensible_load_kW': 0.64, 'latent_load_kW': 0.28}

# List all registered room types
from ship.registry import list_types
print(list(list_types()))
# ['child_dorm_8', 'dorm_communal_8', 'hygiene_block', 'intimacy_pod', 'warehouse']
```

```python
# Query HVAC design rates for any room type and activity
from env.hvac.calc_tables import get_rates, list_available_rooms

print(list_available_rooms().keys())
# dict_keys(['dorm', 'mess_hall', 'command_deck', 'intimacy_pod', 'warehouse', 'lab', 'hygiene_block'])

rates = get_rates("dorm", activity="sleep")
print(rates["ventilation"])
# {'Rp_Lps_per_person': 2.5, 'Ra_Lps_per_m2': 0.3}
```

```python
# Ship-wide power balance
from power.bus import get_power_design, power_balance, summarize_power

cfg = get_power_design()
sources, sinks = summarize_power(cfg)
print(f"Net available power: {power_balance(cfg):.1f} kW")
```

---

## Repository Structure

```
common/          # Physical constants (NIST/NASA), unit registry, conversions, safety margins
data/            # Canonical YAML specs, validation schemas, loader + cache layer
  specs/         #   hvac_design, power_design, materials, equipment, air_cycle
  schemas/       #   YAML schema definitions for spec validation
configs/         # Scenario profiles and runtime overrides (never edited by logic modules)
env/             # Environmental systems
  hvac/          #   Ventilation, exhaust, heat load calculators and design tables
  rooms/         #   Room archetypes: dorm, hygiene block, warehouse, intimacy pod, etc.
life_support/    # O2/CO2 cycle design: crew gas budgets, biological and mech/chem blocks
power/           # Power bus: sources, sinks, and balance helpers
thermal/         # Thermal network: node/edge model, materials library, heat recovery
maintenance/     # Equipment catalog, fleet state, maintenance planner
ship/            # Registry and orchestration layer
tests/           # pytest suite — 17 tests across HVAC, power, and room calculators
scripts/         # Runnable demos and validation utilities
Research/        # NASA-STD-3001 Vol 2 Rev B, ECLSS studies, life-support analyses
```

---

## Architecture: YAML-First Data Flow

A core design principle is that **logic modules never own their source data**. All constants, rates, and specs flow from YAML through a single loading layer:

```
data/specs/*.yaml          ← canonical truths (HVAC rates, material constants, power layout)
        ↓  deep-merged with
configs/**/*.yaml          ← scenario overrides (crew profiles, bus variants, test conditions)
        ↓  loaded by
data/loader.py             ← single entry point; backed by in-memory cache
        ↓  consumed by
env/  power/  thermal/     ← domain logic; never reads YAML directly
        ↓
ship/registry.py           ← orchestration and unified query interface
```

This means swapping a scenario (e.g., minimum crew vs. maximum population) requires only a config override — no code changes.

---

## Core Subsystems

### Environmental Systems (`env/`)
- Ventilation model: `Rp × occupants + Ra × area` with per-fixture exhaust drivers
- Precedence chain: **activity profile → room defaults → global defaults**
- Heat load helpers for metabolic sensible/latent loads, device loads, comfort envelopes
- Room archetypes: child dorm, communal dorm, hygiene block, intimacy pod, warehouse

### Life Support (`life_support/`)
- Design contracts for O₂/CO₂ budgets: crew metabolic demand, natural systems (canopy, PBR), mech/chem (electrolyzers, scrubbers, storage)
- YAML-driven allocation planner with structured output for sizing biological and mechanical blocks
- Research hooks to Wheeler, Detrell, ISS CDRA/OGA, NASA-STD-3001

### Power Distribution (`power/`)
- Source/sink bus model with generation totals, consumption totals, and net balance
- Canonical specs in `data/specs/power_design.yaml`; scenario layouts in `configs/power/`

### Thermal Network (`thermal/`)
- Node/edge dataclass model for lumped-parameter thermal analysis
- Materials library for structural, insulation, and shielding properties
- Hooks for radiator sizing and waste-heat recovery coupling

### Ship Registry (`ship/`)
- Central calculator registry: maps room type IDs to calculator classes
- `compute(type_id, **overrides)` as the uniform query interface

---

## Engineering Philosophy

- **Cited, not assumed** — physical constants link to NIST, NASA Glenn, IAPWS, and ASHRAE. Every formula has a source.
- **Explicit over implicit** — safety margins are named multipliers in `common/safety.py`, not buried in formulas.
- **Data and logic are independent** — changing a design spec requires editing a YAML file, not hunting through Python.
- **Determinism by design** — pint units, clear precedence rules, reproducible outputs from any entry point.
- **Honest stubs** — unimplemented functions are named contracts with TODO prompts and cited research, not silent placeholders.

---

## The Voices (Narrative Layer)

Each subsystem is modeled as a named AI personality — CORTEX, LYRA, IGNIS, THRUM, ARRY, TRUSS, ECHO — that speaks from within its domain. This is not decoration: it is a structured way to reason about system autonomy, interdependence, and fault ownership in a distributed system. Commit messages use voice prefixes for traceability:

```
[LYRA]  Implement ventilation_rate with area + occupant drivers
[IGNIS] Add power_balance and summarize_power to bus.py
[TRUSS] Stub thermal node/edge dataclasses with capacity fields
```

---

## Research Basis

| Document | Used For |
|----------|----------|
| NASA-STD-3001 Vol 2 Rev B | Crew metabolic rates, atmosphere limits, comfort envelopes |
| NIST CODATA 2018 | Physical constants (gravity, Planck, Avogadro, gas constants) |
| IAPWS IF-97 | Water and steam property formulations |
| NASA Glenn Coefficients | 7-term Cp polynomial for dry air (200–6000 K) |
| ASHRAE Handbook (Fundamentals) | Ventilation rates, occupant loads, psychrometrics |
| ISS CDRA / OGA documentation | CO₂ scrubber and electrolyzer design references |

---

## Roadmap

| Phase | Focus | Status |
|-------|--------|--------|
| **1 — Habitat Model** | HVAC design tables, room-level energy and airflow | ✅ Active |
| **2 — Power & Thermal** | Bus topology, materials, heat-exchange coupling | 🔧 In progress |
| **3 — Life Support Cycle** | O₂/CO₂ budgets, biological and mech/chem sizing | 🔧 In progress |
| **4 — Scenario Engine** | Profile-driven simulation of population and load dynamics | 📋 Planned |
| **5 — Integration & Reporting** | Cross-subsystem analytics, ship-wide dashboard | 📋 Planned |
| **6 — Narrative Diagnostics** | AI voice logs as human-readable system telemetry | 📋 Planned |

---

## License & Intent

Released for educational and research use. Fork, extend, or adapt freely for your own simulation studies.

> *"Numbers are the heartbeat of the void. Write them well."* — VESSEL

# Generation Ship — Habitat Systems Framework

> “A starship is not built once.  
> It is grown — layer by layer, equation by equation.”  
> — CORTEX, Core Systems Aggregate  

**Generation Ship** is an open technical framework for modeling the internal infrastructure of a self-sustaining interstellar vessel — a craft designed to carry generations of people through deep time.  
It combines rigorous **systems-engineering practices** with a **creative design language**, treating each subsystem as both a piece of machinery and a voice in the ship’s evolving intelligence.

The result is part simulation platform, part engineering study: a place to explore how power, heat, air, and life could coexist in a closed, centuries-long voyage.

---

## Overview

- **Engineering focus:** realistic life-support, power, and thermal subsystems, organized into clear, testable modules.  
- **Narrative method:** a distributed-AI metaphor (CORTEX, LYRA, IGNIS …) used to model autonomy, interdependence, and fault tolerance between systems.  
- **Goal:** demonstrate how disciplined software structure and physical reasoning can scale to model the complexity of a generation ship.

---

## Repository Structure

```
configs/         # Scenario and runtime profiles
data/            # Canonical design specs and validation schemas
docs/            # Engineering documentation and data contracts
env/             # Environmental systems and room archetypes
power/           # Electrical generation and distribution network
thermal/         # Materials library and thermal coupling
ship/            # Registry and orchestration layer
scripts/         # Utilities and quick-run demos
tests/           # Verification scaffolds
Research/        # Reference papers and NASA standards
```

Each layer has a single purpose:
- **`data/specs/`** defines canonical truths (e.g., HVAC rates, material constants).  
- **`env/`, `power/`, `thermal/`** implement domain logic.  
- **`configs/`** holds scenario-specific overrides.  
- **`ship/`** orchestrates components into a unified vessel model.

---

## Example Usage

```bash
# Run a quick demonstration
python scripts/demo.py
```

```python
# Query an HVAC profile directly
from env.hvac.calc_env import resolve_room_activity
from data.loader import load_yaml

cfg = load_yaml("data/specs/hvac_design.yaml")
profile = resolve_room_activity(cfg, room_type="dorm", activity="sleep")
print(profile)
```

The same pattern applies to power and thermal subsystems: load canonical data, apply scenario overrides, and analyze results at any level — from room to ship.

---

## Core Subsystems

### Environmental Systems (`env/`)
- Models airflows, heat loads, humidity control, and comfort envelopes.  
- Precedence logic (`calc_env.py`): **activity → room defaults → global defaults**.  
- Structured constants and tables defined in `data/specs/hvac_design.yaml`.

### Power Distribution (`power/`)
- Graph-based bus model (`bus.py`) defining sources, loads, and redundancy.  
- Designed for future electrical analysis and heat-recovery coupling.  
- Canonical specs in `data/specs/power_design.yaml`.

### Thermal Network (`thermal/`)
- Material properties and conduction paths for habitat structures.  
- Stubs for radiators, insulation, and waste-heat reuse.

### Ship Registry (`ship/`)
- Central lookup and integration layer tying all subsystems together.  
- Future extension point for mission-level orchestration or simulation loops.

---

## Data Integrity & Validation

- **Schemas** in `data/schemas/` define expected structure and units.  
- **`scripts/validate.py`** runs automated checks to ensure specs remain consistent.  
- Ensures that design decisions stay traceable and reproducible.

---

## Engineering Philosophy

- **Separation of concerns:** computation, data, and configuration are independent.  
- **Determinism by design:** explicit units, clear precedence, reproducible results.  
- **Scalability through abstraction:** every component — from a hygiene pod to the reactor — uses the same input/output interface.  
- **Narrative as architecture:** the ship’s “voices” reflect subsystems negotiating shared resources; they make complex interactions legible, not fictional.

---

## Roadmap & Vision

| Phase | Focus | Outcome |
|-------|--------|----------|
| **1 — Habitat Model** | Environmental logic, HVAC design tables | Room-level energy and airflow balance |
| **2 — Power & Thermal** | Bus topology, materials, heat-exchange | Ship-wide power/heat coupling |
| **3 — Scenario Engine** | Profile-driven runtime configurations | Simulate population and load dynamics |
| **4 — Integration & Reporting** | Cross-subsystem analytics and visualization | Full habitat-system dashboard |
| **5 — Narrative Diagnostics** | AI voice logs as system telemetry | Human-readable diagnostics layer |

The end goal is a **verifiable, extensible simulation of a generation ship’s internal ecosystem**, built from first-principles engineering and implemented in transparent, modular code.

---

## Research Basis

The `Research/` directory includes core reference materials such as:

- **NASA-STD-3001 Vol 2 Rev B** — Man-Systems Integration Standards  
- **Habitat and ECLSS** patents and studies  
- Related life-support and long-duration-mission analyses  

These inform design limits, unit conventions, and environmental tolerances throughout the model.

---

## Contributing / Using the Voices

Subsystems can annotate commits or logs with their “voice” for traceability:

```
[LYRA]  Adjusted CO₂ scrubber efficiency model  
[IGNIS] Updated bus load balancing  
[TRUSS] Revised hull conductivity factors
```

It’s a human-friendly way to reason about distributed systems.

---

## License & Intent

This framework is released for educational and research use — a showcase of applied programming, engineering analysis, and structured creativity.  
You’re encouraged to fork, extend, or adapt it for your own generation-ship studies or simulation work.

> “Numbers are the heartbeat of the void. Write them well.” — VESSEL  

---

### Contact

For collaboration or questions about system design methodologies, reach out via the repository’s issue tracker or profile link.

# Generation Ship – Systems Skeleton

Conceptual scaffolding for modelling the habitat, environment, and power systems of a long-haul generation ship. The repository separates canonical design data (data/specs/), runtime overrides (configs/), and domain logic modules (env/, power/, 	hermal/, ship/).

## Layout
`
ship/      # Registry facade for room calculators
env/       # Room archetypes plus HVAC helpers
power/     # Power distribution helpers
thermal/   # Materials library and thermal network stubs
data/      # Canonical specs + validation schemas
configs/   # Runtime-tunable configuration knobs
scripts/   # Utility scripts (e.g., data validation)
tests/     # Unit tests
`

## Quick Start
`ash
# Inspect HVAC rates for a dormitory
python - <<'PY'
from env.hvac.calc_tables import get_rates
print(get_rates("dorm"))
PY

# Demo running a room calculator
python scripts/demo.py
`

## Data Validation
- data/schemas/*.yaml capture JSON Schema contracts for specs.
- scripts/validate.py performs simple checks on equipment_specs.yaml.

## Next Steps
1. Flesh out HVAC/environmental formulas in env/hvac/.
2. Expand room calculators in env/rooms/ with real geometry and utility logic.
3. Replace placeholder values in configs/ with scenario-specific data.
4. Wire 	hermal/network.py into room calculators for heat-transfer studies.

Treat the repository as a sandbox for iterating on generation-ship systems modelling.
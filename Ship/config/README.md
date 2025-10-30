# Configuration Directory

This folder holds **shipwide configuration** for the Generation Ship project.  
It is **source-controlled**, human‑readable, and intended to be consumed by tools, simulators, and CI checks.

## Layout
```
/config/
  equipment/                     # Hardware catalogs and schemas
    Generation_Ship_Equipment_v0.4.yaml
  hvac/                          # Airflow, heat, setpoints (future)
  power/                         # Buses, loads, breakers (future)
  structure/                     # Mass budgets, frames (future)
  globals.yaml                   # Cross‑cutting constants (future)
```

## Conventions
- **YAML only** for config (`*.yaml`). Keep code elsewhere.
- **SI units** unless the key explicitly states otherwise.
- **Schema versioning:** each file has `meta.schema_version`. On breaking changes, bump the version and keep prior file(s) under versioned names.
- **Categories:** hierarchical using slash notation (e.g., `medical/incubator`).

## Equipment Catalog (v0.4)
Canonical file:
```
config/equipment/Generation_Ship_Equipment_v0.4.yaml
```
Includes: dimensions, weight, clearances, **electrical**, **heat_load_w**, communications, and categories.

## How to extend
1. Copy the `_templates.equipment_item` block in the YAML.
2. Fill in dimensions, electrical, heat load, and categories.
3. Run any linters/validators (to be added in CI).

## Change control
- Prefer **small PRs** with one logical change per commit.
- Reference design notes or tickets in commit messages (`design:`, `hvac:`, `medical:` prefixes).

## Roadmap
- Add JSON Schema for validation (and CI step).
- Add auto-doc generation for equipment lists.

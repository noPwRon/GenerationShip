# Data Contracts

The Generation Ship repository stores canonical design data under data/specs/ and runtime-tunable configuration under configs/.

## Specs (data/specs/)
- equipment_specs.yaml – master equipment catalog and metadata
- hvac_design.yaml – ventilation and metabolic load references
- materials.yaml – thermal and structural material properties
- power_design.yaml – generation, storage, and sink definitions

Schemas for these files live in data/schemas/.

## Configs (configs/)
- env/hvac/defaults.yaml – runtime HVAC defaults for calculators
- power/bus_layout_v0.yaml – draft electrical bus layout
- profile_min_crew.yaml – baseline crew sizing and shift structure

All YAML files should remain human-editable, version-controlled, and validated through scripts/validate.py or future CI hooks.
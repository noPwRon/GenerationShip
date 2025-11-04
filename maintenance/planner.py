"""
maintenance/assets.py
---------------------
Integration layer between the equipment specifications and maintenance tracking.

Source of truth
    • data/specs/equipment_specs.yaml  (key: equipment)

This module provides the API that planner.py expects:
    - load_catalog()
    - load_fleet()
    - load_spares()
    - AssetInstance (type)
…and keeps YAML-first structure with TODO prompts only.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional

# --- YAML Loader (replace these stubs via data/loader.py) --------------------

from data.loader import load_yaml, dump_yaml  # type: ignore


# ---------------------------------------------------------------------------
# Catalog types (from equipment_specs.yaml)
# ---------------------------------------------------------------------------

@dataclass
class EquipmentType:
    """
    Canonical equipment descriptor loaded from equipment_specs.yaml.

    TODO:
      [ ] Validate presence of fields used downstream (category, electrical, heat_load_w).
      [ ] Optionally project subsystem from category ("hvac/…", "utilities/…", etc.).
      [ ] Attach reliability/maintainability meta if you add it to specs later.
    """
    name: str
    meta: Dict[str, Any] = field(default_factory=dict)

# ---------------------------------------------------------------------------
# Fleet types (instances installed/stowed)
# ---------------------------------------------------------------------------

@dataclass
class EquipmentInstance:
    """
    A specific installed or stowed instance of an equipment item.

    YAML (configs/maintenance/fleet_state.yaml) expected keys:
      - serial: str
      - equipment_id: str  # must match a key in equipment_specs.yaml > equipment
      - location: str
      - install_date: str (YYYY-MM-DD)
      - hours_run: float | null
      - starts_count: int | null
      - condition_code: str  # A/B/C/D
      - fault_flags: list[str]
      - maintenance_log: list[ {date, action, notes, parts_used?} ]
      - provenance: { role: new|refurbished|repurposed, source_serial: str|null }

    TODO:
      [ ] Decide required vs optional fields; validate on load.
      [ ] Add calibration_due_at or next_pm_due_at if you want static checks here.
    """
    serial: str
    equipment_id: str
    location: str
    install_date: Optional[str] = None
    hours_run: Optional[float] = None
    starts_count: Optional[int] = None
    condition_code: Optional[str] = None
    fault_flags: List[str] = field(default_factory=list)
    maintenance_log: List[Dict[str, Any]] = field(default_factory=list)
    provenance: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)

# --- Alias expected by planner.py -------------------------------------------
# planner.py imports `AssetInstance` from maintenance.assets
AssetInstance = EquipmentInstance  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Spares/scrap state
# ---------------------------------------------------------------------------

@dataclass
class SparesAndScrap:
    """
    Inventories of spares, loose parts, and material recovery bins.

    YAML (configs/maintenance/spares.yaml):
      spares: { equipment_id: { qty: int, shelf: str } }
      parts:  { part_id: { qty: int, shelf: str } }
      scrap:  { material: kg }
      recyclables: { material: kg }

    TODO:
      [ ] Add cost fields or recycling yield if you plan economics later.
    """
    spares: Dict[str, Any] = field(default_factory=dict)
    parts: Dict[str, Any] = field(default_factory=dict)
    scrap: Dict[str, Any] = field(default_factory=dict)
    recyclables: Dict[str, Any] = field(default_factory=dict)

# ---------------------------------------------------------------------------
# Loaders / Adapters
# ---------------------------------------------------------------------------

def load_equipment_catalog(path: str = "data/specs/equipment_specs.yaml") -> Dict[str, EquipmentType]:
    """
    Load canonical equipment catalog from equipment_specs.yaml.

    TODO:
      [ ] Validate presence of 'equipment' section and structure.
      [ ] Optionally cross-check categories exist in top-level 'categories'.
    """
    raw = load_yaml(path)
    equip = raw.get("equipment", {})
    return {k: EquipmentType(name=k, meta=v) for k, v in equip.items()}

def load_catalog(path: str = "data/specs/equipment_specs.yaml") -> Dict[str, EquipmentType]:
    """
    Alias expected by planner.py — returns the same as load_equipment_catalog().
    """
    return load_equipment_catalog(path)

def load_fleet(path: str = "configs/maintenance/fleet_state.yaml") -> Dict[str, AssetInstance]:
    """
    Load the installed/stowed fleet.

    TODO:
      [ ] Validate each equipment_id against the catalog (see helper below).
      [ ] Normalize locations to a consistent "Deck / Bay / Slot" convention.
    """
    raw = load_yaml(path)
    return {f["serial"]: EquipmentInstance(**f) for f in raw.get("fleet", [])}

def load_spares(path: str = "configs/maintenance/spares.yaml") -> SparesAndScrap:
    """
    Load spares/parts and recycling streams.
    """
    raw = load_yaml(path)
    return SparesAndScrap(**raw)

def save_fleet(fleet: Dict[str, AssetInstance], path: str = "configs/maintenance/fleet_state.yaml") -> None:
    """
    Persist fleet to YAML (no transformations).

    TODO:
      [ ] Consider sorting by location or type to reduce diff noise.
      [ ] Stamp metadata (author/date/commit) if desired.
    """
    dump_yaml(path, {"fleet": [asdict(f) for f in fleet.values()]})

# ---------------------------------------------------------------------------
# Small helpers (pure structure; fill logic later)
# ---------------------------------------------------------------------------

def validate_fleet_against_catalog(
    catalog: Dict[str, EquipmentType],
    fleet: Dict[str, AssetInstance],
) -> List[str]:
    """
    Return a list of human-readable validation issues.

    TODO:
      [ ] Check: instance.equipment_id ∈ catalog
      [ ] Check: condition_code in allowed set (A/B/C/D)
      [ ] Check: required fields present (serial, location, equipment_id)
      [ ] Optionally: verify location format and uniqueness of serials
    """
    return []

def record_maintenance_event(
    fleet: Dict[str, AssetInstance],
    serial: str,
    event: Dict[str, Any],
) -> None:
    """
    Append a maintenance event to a specific instance.

    TODO:
      [ ] Validate event shape: {date, action, notes, parts_used?}
      [ ] Optionally mutate hours_run / condition_code based on action.
      [ ] Optionally emit a separate 'work_order' artifact.
    """
    # placeholder: implement in your style
    if serial in fleet:
        fleet[serial].maintenance_log.append(event)

# Optional: a convenience fetch
def get_equipment(catalog: Dict[str, EquipmentType], equipment_id: str) -> Optional[EquipmentType]:
    """
    Fetch a single EquipmentType by ID.

    TODO:
      [ ] Add fuzzy/alias lookup if you keep synonyms in specs.
    """
    return catalog.get(equipment_id)

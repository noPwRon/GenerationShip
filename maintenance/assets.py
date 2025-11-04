"""
maintenance/assets.py
---------------------
Integration layer between the equipment specifications and maintenance tracking.

Purpose
    • Reuse data/specs/equipment_specs.yaml as canonical catalog.
    • Track installed instances, condition, usage hours, and material flows.
    • NO PHYSICS or reliability math — structure + TODO prompts only.

Files
    • data/specs/equipment_specs.yaml      # canonical catalog (already exists)
    • configs/maintenance/fleet_state.yaml # installed instances
    • configs/maintenance/spares.yaml      # spares, scrap, recyclables
    • configs/maintenance/policies.yaml    # PM/CM templates & refurb routes

Research TODO Prompts
    • Reliability curves: MTBF/MTTF, degradation models (MIL-HDBK-217F, NASA reliability).
    • Material reuse: recycling efficiency, 3D print feedstock composition.
    • Lifecycle costs: repair vs replace models (ISS logistics papers).
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional

# --- YAML Loader (replace stub via data/loader.py) ---------------------------
try:
    from data.loader import load_yaml, dump_yaml  # type: ignore
except Exception:
    def load_yaml(path: str) -> Dict[str, Any]: return {}
    def dump_yaml(path: str, data: Dict[str, Any]) -> None: ...

# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class EquipmentType:
    """
    Canonical equipment descriptor loaded from equipment_specs.yaml.

    TODO:
      [ ] Validate required fields exist (category, description, electrical, etc.).
      [ ] Extract lifecycle-related metadata:
            - heat_load_w, weight_kg, electrical.max_power_w
            - category for routing to subsystem (hvac, power, etc.)
      [ ] Optionally extend with reliability or maintainability data (MTBF, spare parts list).
    """
    name: str
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EquipmentInstance:
    """
    A specific installed or stowed instance of an equipment item.

    TODO:
      [ ] Fields (in configs/maintenance/fleet_state.yaml):
          - serial, equipment_id (matches key in equipment_specs.yaml)
          - location, install_date, hours_run, starts_count
          - condition_code (A/B/C/D)
          - maintenance_log (list of {date, action, notes})
          - provenance (if reused or refurbished)
      [ ] Add fault_flags (overheat, sensor_fail, etc.)
      [ ] Add power/runtime accumulation hook (future telemetry link).
    """
    serial: str
    equipment_id: str
    location: str
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SparesAndScrap:
    """
    Aggregated inventory of spare parts, scrap, and recyclables.

    TODO:
      [ ] Fields (in configs/maintenance/spares.yaml):
          - spares: { equipment_id: qty }
          - parts: { part_id: qty }
          - scrap: { material: kg }
          - recyclables: { material: kg }
      [ ] Add lifecycle cost metadata (credits, recycling yield).
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
    Load canonical equipment catalog (single source of truth).

    TODO:
      [ ] Parse equipment_specs.yaml > equipment section.
      [ ] Validate 'categories' and 'equipment' keys exist.
      [ ] Link subcategories to subsystems (hvac, power, etc.) if desired.
    """
    raw = load_yaml(path)
    equip = raw.get("equipment", {})
    return {k: EquipmentType(name=k, meta=v) for k, v in equip.items()}


def load_fleet(path: str = "configs/maintenance/fleet_state.yaml") -> Dict[str, EquipmentInstance]:
    """
    Load the installed equipment fleet.

    TODO:
      [ ] Validate each equipment_id against the catalog.
      [ ] Add cross-links to subsystem or location map.
    """
    raw = load_yaml(path)
    return {f["serial"]: EquipmentInstance(**f) for f in raw.get("fleet", [])}


def load_spares(path: str = "configs/maintenance/spares.yaml") -> SparesAndScrap:
    """
    Load spares/scrap state.
    """
    raw = load_yaml(path)
    return SparesAndScrap(**raw)


def save_fleet(fleet: Dict[str, EquipmentInstance], path: str = "configs/maintenance/fleet_state.yaml") -> None:
    """
    Persist fleet to YAML.
    """
    dump_yaml(path, {"fleet": [asdict(f) for f in fleet.values()]})

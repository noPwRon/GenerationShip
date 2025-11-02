"""
air_cycle_design.py
-------------------
Design-time aggregation for O2/CO2 modules using the project's YAML-first method.

Methodology
    • Read canonical values from data/specs/*.yaml (literature-derived).
    • Allow runtime overrides in configs/life_support/*.yaml.
    • Provide (de)serialization helpers, but NO PHYSICS OR MATH.

Research TODO Prompts (put citations into YAML fields)
    • Higher-plant canopy O2/CO2 exchange (Wheeler et al.; CELSS/BLSS papers)
    • Microalgae PBR productivity (Detrell 2021; Fahrion 2021 review)
    • Crew metabolic baselines (NASA-STD-3001 Vol. 2; ASHRAE)
    • Scrubber capacity & regeneration (ISS CDRA; LiOH; amine swing)
    • Electrolyzer sizing (ISS OGA; PEM performance surveys)
    • Storage buffers (compressed/liquid O2 standards)

File Contracts (proposed)
    • data/specs/air_cycle_design.yaml          # canonical default design values
    • configs/life_support/air_cycle_overrides.yaml  # scenario-specific overrides
    • data/schemas/air_cycle.design.schema.yaml  # JSON Schema for validation (optional)

NOTE
    Implement the actual loader in data/loader.py; here we only call it.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List

# TODO: Add load_air_cycle_design/dump_air_cycle_design utilities in data.loader so
# TODO: this module uses the shared YAML resolution & caching stack instead of raw paths.
try:
    from data.loader import load_yaml, dump_yaml, merge_dicts  # type: ignore
except Exception:
    # Fallback stubs to keep this module importable without side effects.
    def load_yaml(path: str) -> Dict[str, Any]:  # TODO: replace with real loader
        return {}
    def dump_yaml(path: str, data: Dict[str, Any]) -> None:  # TODO
        pass
    def merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:  # TODO
        out = dict(base); out.update(override); return out


# ------------------------- Dataclasses (no math) -----------------------------

@dataclass
class CanopyDesign:
    O2_g_per_m2_h: Optional[float] = None
    CO2_g_per_m2_h: Optional[float] = None
    PAR_umol_m2_s: Optional[float] = None
    power_W_per_m2: Optional[float] = None
    citations: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

@dataclass
class PBRDesign:
    O2_mmol_per_L_h: Optional[float] = None
    biomass_g_per_L_d: Optional[float] = None
    optical_depth_m: Optional[float] = None
    illuminated_area_m2: Optional[float] = None
    mixing_W_per_m3: Optional[float] = None
    citations: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

@dataclass
class CrewDesign:
    O2_g_per_person_h: Optional[float] = None
    CO2_g_per_person_h: Optional[float] = None
    activity_profile: Dict[str, float] = field(default_factory=dict)
    citations: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

@dataclass
class ScrubberDesign:
    tech: str = "amine"
    capacity_CO2_kg: Optional[float] = None
    regen_power_W: Optional[float] = None
    citations: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

@dataclass
class ElectrolyzerDesign:
    O2_kg_per_h: Optional[float] = None
    power_kW: Optional[float] = None
    water_kg_per_h: Optional[float] = None
    citations: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

@dataclass
class BufferDesign:
    O2_storage_kg: Optional[float] = None
    CO2_storage_kg: Optional[float] = None
    citations: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

@dataclass
class AirCycleDesignSpec:
    canopy: Optional[CanopyDesign] = None
    pbr: Optional[PBRDesign] = None
    crew: Optional[CrewDesign] = None
    scrubber: Optional[ScrubberDesign] = None
    electrolyzer: Optional[ElectrolyzerDesign] = None
    buffers: Optional[BufferDesign] = None
    citations: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    # ---- Serialization helpers (YAML-friendly dicts) ----
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AirCycleDesignSpec":
        # TODO: add type checks & schema validation (data/schemas/air_cycle.design.schema.yaml)
        return AirCycleDesignSpec(
            canopy=CanopyDesign(**d["canopy"]) if d.get("canopy") else None,
            pbr=PBRDesign(**d["pbr"]) if d.get("pbr") else None,
            crew=CrewDesign(**d["crew"]) if d.get("crew") else None,
            scrubber=ScrubberDesign(**d["scrubber"]) if d.get("scrubber") else None,
            electrolyzer=ElectrolyzerDesign(**d["electrolyzer"]) if d.get("electrolyzer") else None,
            buffers=BufferDesign(**d["buffers"]) if d.get("buffers") else None,
            citations=d.get("citations", []),
            notes=d.get("notes", []),
        )


# ----------------------- YAML I/O (no physics) ------------------------------

def load_design(spec_path: str, overrides_path: Optional[str] = None) -> AirCycleDesignSpec:
    """
    Load canonical design spec, overlay with scenario overrides.

    TODO:
      [ ] Align the signature with loader helpers that accept repo-relative keys rather
          than direct filesystem paths.
    TODO:
      [ ] Enforce schema(s).
      [ ] Track provenance per field for audit.
    """
    base = load_yaml(spec_path)
    out = base
    if overrides_path:
        overrides = load_yaml(overrides_path)
        out = merge_dicts(base, overrides)  # TODO: deep-merge per your loader rules
    return AirCycleDesignSpec.from_dict(out)

def save_design(spec: AirCycleDesignSpec, out_path: str) -> None:
    """Write a merged design spec to YAML (for freezing scenario configs)."""
    dump_yaml(out_path, spec.to_dict())

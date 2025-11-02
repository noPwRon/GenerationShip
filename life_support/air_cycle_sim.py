"""
air_cycle_sim.py
----------------
Real-time O2/CO2 simulator scaffold aligned with the repo's YAML workflow.

Methodology
    • Load a scenario YAML: zones, modules, references to design values.
    • Step a discrete-time loop; apply module deltas to zone gas state.
    • NO PHYSICS here — only structure and TODO prompts.

Files (proposed)
    • configs/life_support/air_cycle_scenario.yaml   # which zones & modules to simulate
    • data/schemas/air_cycle.scenario.schema.yaml    # optional schema for validation

Research TODO Prompts (put refs into YAML)
    • Gas-state representation & mixing assumptions (ASHRAE, NASA ECLSS texts)
    • Canopy/PBR exchange rates (Wheeler; Detrell; Fahrion review)
    • CO2 scrubber kinetics/capacity (ISS CDRA; LiOH)
    • Electrolyzer throughput/power (ISS OGA; PEM stacks)

Integration
    • This module can import design values via air_cycle_design.load_design(...) if needed.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Protocol

# Optional: pull design spec to resolve named references
try:
    from life_support.air_cycle_design import AirCycleDesignSpec, load_design  # type: ignore
except Exception:
    AirCycleDesignSpec = object  # placeholder
    def load_design(*args, **kwargs):  # noqa: D401
        """stub"""
        return None

# Reuse the project loader (implement real logic in data/loader.py)
try:
    from data.loader import load_yaml  # type: ignore
except Exception:
    def load_yaml(path: str) -> Dict[str, Any]:  # TODO
        return {}

# ----------------------------- State types ----------------------------------

@dataclass
class GasState:
    """Well-mixed gas state (NO MATH)."""
    O2: float
    CO2: float
    N2: float
    Ar: float = 0.0
    pressure_Pa: Optional[float] = None
    temperature_K: Optional[float] = None
    humidity_frac: Optional[float] = None
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Zone:
    """Habitat compartment defined in scenario YAML."""
    name: str
    volume_m3: float
    gas: GasState
    meta: Dict[str, Any] = field(default_factory=dict)

# ----------------------------- Module APIs ----------------------------------

class NaturalProducer(Protocol):
    def step(self, dt_s: float, zone: Zone) -> Dict[str, Any]:
        return {"dO2": 0.0, "dCO2": 0.0, "notes": ["TODO"]}

class MechChemModule(Protocol):
    def step(self, dt_s: float, zone: Zone, setpoint: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"dO2": 0.0, "dCO2": 0.0, "power_W": 0.0, "notes": ["TODO"]}

# ----------------------------- Module stubs ---------------------------------

@dataclass
class PlantCanopy:
    """
    Scenario-driven canopy.

    YAML fields (example):
        type: plant_canopy
        footprint_m2: 40
        design_ref: canopy.default  # path/key into design YAML (optional)
        params: { lighting_profile: day_night_12_12 }
    """
    footprint_m2: float
    params: Dict[str, Any] = field(default_factory=dict)
    design_ref: Optional[str] = None

    def step(self, dt_s: float, zone: Zone) -> Dict[str, Any]:
        # TODO: read needed rates from design_ref via AirCycleDesignSpec (if wired)
        return {"dO2": 0.0, "dCO2": 0.0, "notes": ["TODO: canopy exchange"]}

@dataclass
class AlgaePBR:
    """
    Scenario-driven PBR.

    YAML fields:
        type: algae_pbr
        illuminated_area_m2: 12
        depth_m: 0.05
        design_ref: pbr.default
    """
    illuminated_area_m2: float
    depth_m: float
    params: Dict[str, Any] = field(default_factory=dict)
    design_ref: Optional[str] = None

    def step(self, dt_s: float, zone: Zone) -> Dict[str, Any]:
        return {"dO2": 0.0, "dCO2": 0.0, "notes": ["TODO: PBR exchange"]}

@dataclass
class CO2Scrubber:
    """
    Scenario-driven scrubber.

    YAML fields:
        type: co2_scrubber
        tech: amine
        capacity_CO2_kg: 5.0
        design_ref: scrubber.amine_v0
    """
    tech: str = "amine"
    params: Dict[str, Any] = field(default_factory=dict)
    design_ref: Optional[str] = None

    def step(self, dt_s: float, zone: Zone, setpoint: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"dO2": 0.0, "dCO2": 0.0, "power_W": 0.0, "notes": ["TODO: scrubber removal"]}

@dataclass
class Electrolyzer:
    """
    Scenario-driven electrolyzer.

    YAML fields:
        type: electrolyzer
        O2_kg_per_h_max: 0.5
        design_ref: electrolyzer.oga_like
    """
    params: Dict[str, Any] = field(default_factory=dict)
    design_ref: Optional[str] = None

    def step(self, dt_s: float, zone: Zone, setpoint: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"dO2": 0.0, "dCO2": 0.0, "power_W": 0.0, "notes": ["TODO: electrolyzer generation"]}

# ----------------------------- Controller -----------------------------------

@dataclass
class AirController:
    """
    Placeholder controller; define policies in YAML or code.

    YAML (optional):
        control:
          targets: { O2_frac: 0.21, CO2_frac_max: 0.005 }
          modules: { electrolyzer: {...}, scrubber: {...} }
    """
    policy: Dict[str, Any] = field(default_factory=dict)

    def compute_setpoints(self, zone: Zone) -> Dict[str, Dict[str, Any]]:
        # TODO: map policy → module setpoints
        return {}

# ----------------------------- Simulator ------------------------------------

@dataclass
class AirCycleSimulator:
    """
    Discrete-time simulation harness driven by a scenario YAML.

    Scenario YAML skeleton:
        zones:
          - name: "Hab A"
            volume_m3: 400
            gas: { O2: 0.21, CO2: 0.004, N2: 0.786, pressure_Pa: 101325, temperature_K: 295 }
        modules:
          - type: plant_canopy
            footprint_m2: 40
            design_ref: canopy.default
          - type: algae_pbr
            illuminated_area_m2: 12
            depth_m: 0.05
            design_ref: pbr.default
          - type: co2_scrubber
            tech: amine
            design_ref: scrubber.amine_v0
          - type: electrolyzer
            design_ref: electrolyzer.oga_like
        control:
          targets: { O2_frac: 0.21, CO2_frac_max: 0.005 }

    TODO:
      [ ] Add multi-zone transport later if needed.
      [ ] Decide state units (fractions vs partial pressures) and enforce invariants.
    """
    zone: Zone
    natural_modules: List[NaturalProducer] = field(default_factory=list)
    mechchem_modules: List[MechChemModule] = field(default_factory=list)
    controller: Optional[AirController] = None
    t_s: float = 0.0

    def step(self, dt_s: float) -> Dict[str, Any]:
        notes: List[str] = []
        setpoints = self.controller.compute_setpoints(self.zone) if self.controller else {}
        for m in self.natural_modules:
            result = m.step(dt_s, self.zone)
            # TODO: apply result["dO2"], result["dCO2"] to self.zone.gas
            notes.extend(result.get("notes", []))
        for m in self.mechchem_modules:
            result = m.step(dt_s, self.zone, setpoints.get(m.__class__.__name__.lower()))
            # TODO: apply deltas; accumulate power/heat if you choose
            notes.extend(result.get("notes", []))
        self.t_s += dt_s
        return {"t_s": self.t_s, "zone": self.zone, "notes": notes}

# ----------------------------- Builders -------------------------------------

TYPE_MAP = {
    "plant_canopy": PlantCanopy,
    "algae_pbr": AlgaePBR,
    "co2_scrubber": CO2Scrubber,
    "electrolyzer": Electrolyzer,
}

def build_from_scenario(path: str) -> "AirCycleSimulator":
    """
    Construct simulator from a scenario YAML.

    TODO:
      [ ] Schema-validate (data/schemas/air_cycle.scenario.schema.yaml).
      [ ] Resolve design_ref keys against a loaded AirCycleDesignSpec if you wire it in.
    """
    cfg = load_yaml(path)
    # Zone
    z0 = cfg["zones"][0]  # TODO: extend to multi-zone later
    gas = GasState(**z0["gas"])
    zone = Zone(name=z0["name"], volume_m3=z0["volume_m3"], gas=gas)
    # Modules
    naturals, mechchems = [], []
    for m in cfg.get("modules", []):
        cls = TYPE_MAP[m["type"]]
        params = dict(m); params.pop("type")
        inst = cls(**params)
        if isinstance(inst, (PlantCanopy, AlgaePBR)):
            naturals.append(inst)  # type: ignore
        else:
            mechchems.append(inst)  # type: ignore
    controller = AirController(policy=cfg.get("control", {})) if cfg.get("control") else None
    return AirCycleSimulator(zone=zone, natural_modules=naturals, mechchem_modules=mechchems, controller=controller)

"""
air_cycle_design.py
-------------------
Design-time planning helpers for O2/CO2 budgets and capacity allocation.

Intent
    • Given crew profile(s) + target atmosphere policy, estimate REQUIRED:
        - O2 generation budget (by time window, e.g., kg/day)
        - CO2 scrubbing budget (kg/day, ppm ceilings)
        - Allocation targets across natural (canopy/PBR) and mech/chem systems
    • Produce structured "design plan" dicts you can write to YAML.
    • NO PHYSICS OR MATH — only prompts/TODO checklists and function contracts.

Data Flow (YAML-first)
    • Inputs (proposed):
        - data/specs/air_cycle_design.yaml           # canonical device/capacity descriptors
        - configs/life_support/air_cycle_overrides.yaml  # scenario overrides
        - configs/life_support/crew_profile.yaml     # crew count, activity schedule, phases
        - configs/life_support/targets.yaml          # policy: O2%, CO2 ppm max, buffers
    • Outputs (proposed):
        - configs/life_support/air_cycle_plan.yaml   # synthesized design plan (targets/capacities)

Research TODO Prompts (place citations into YAML)
    • Crew metab: NASA-STD-3001 Vol. 2; ASHRAE occupant loads.
    • Canopy yields: Wheeler et al. (CELSS/BLSS, crop RUE, canopy gas exchange).
    • PBR productivity: Detrell (2021), Fahrion (2021 review), species-specific data.
    • Scrubbers (CO2): ISS CDRA, LiOH canisters, amine/zeolite swing.
    • Electrolyzers (O2): ISS OGA; PEM reviews (efficiency, power, water).
    • Buffers: compressed/liquid O2/CO2 storage, safety codes/limits.

NOTE
    Implement YAML IO in data/loader.py (load_yaml, dump_yaml, merge_dicts).
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List, Tuple

# --- Loader hooks (STUBS; replace via data/loader.py) ------------------------

from data.loader import load_yaml, dump_yaml, merge_dicts  # type: ignore


# --- Input containers (NO MATH) ----------------------------------------------

@dataclass
class CrewProfile:
    """
    Crew counts and activity distribution.

    TODO:
      [ ] Populate from configs/life_support/crew_profile.yaml:
          - crew_count_total
          - activity_profile: { sleep: frac, light_work: frac, exercise: frac, ... }
          - special_phases: { EVA_days_per_year, illness_days, quarantine, etc. }
      [ ] Map each activity to metab class keys used in your HVAC/activity tables.
      [ ] Cite NASA-STD-3001 Vol. 2 / ASHRAE for O2/CO2 per activity.
    """
    
    # TODO implement some locgic to calculate the crew count total based on crew specs and compositions 
    crew_count_total: int = 2000 # maximum potential crew members
    activity_profile: Dict[str, float] = field(default_factory=dict)
    special_phases: Dict[str, Any] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)


@dataclass
class AtmosphereTargets:
    """
    Policy targets for cabin atmosphere and buffers.

    TODO:
      [ ] Populate from configs/life_support/targets.yaml:
          - O2_fraction_target, O2_fraction_min, O2_fraction_max
          - CO2_ppm_max (or fraction), warning_thresholds
          - buffer_days_O2, buffer_days_CO2 (emergency autonomy)
          - design_time_horizon_days (e.g., peak day, average week, contingency)
      [ ] Provide rationale/citations in YAML.
    """
    O2_fraction_target: Optional[float] = None
    O2_fraction_min: Optional[float] = None
    O2_fraction_max: Optional[float] = None
    CO2_ppm_max: Optional[int] = None
    buffer_days_O2: Optional[float] = None
    buffer_days_CO2: Optional[float] = None
    design_time_horizon_days: Optional[int] = None
    notes: List[str] = field(default_factory=list)


@dataclass
class NaturalOptions:
    """
    Natural (biological) capacity descriptors.

    TODO:
      [ ] Populate from data/specs/air_cycle_design.yaml (+ overrides):
          canopy:
            O2_g_per_m2_h: null
            CO2_g_per_m2_h: null
            PAR_umol_m2_s: null
            power_W_per_m2: null
            reliability: { uptime_frac, failure_modes }
          pbr:
            O2_mmol_per_L_h: null
            biomass_g_per_L_d: null
            optical_depth_m: null
            illuminated_area_m2: null
            mixing_W_per_m3: null
            reliability: { uptime_frac, maintenance_interval }
      [ ] Add species/crop variants via keys (e.g., canopy.wheat_v1, pbr.chlorella_v1).
      [ ] Cite Wheeler/Detrell with yield ranges (min/typ/max) in YAML.
    """
    canopy: Dict[str, Any] = field(default_factory=dict)
    pbr: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MechChemOptions:
    """
    Mechanical/Chemical capacity descriptors.

    TODO:
      [ ] Populate from data/specs/air_cycle_design.yaml (+ overrides):
          scrubber:
            variants: { amine_v1: {...}, LiOH_v1: {...}, zeolite_v1: {...} }
            fields: { capacity_CO2_kg, regen_power_W, media_life_hours, mass_kg, volume_m3 }
          electrolyzer:
            variants: { oga_like: {...}, pem_small: {...} }
            fields: { O2_kg_per_h, power_kW, water_kg_per_h, mass_kg, volume_m3 }
          storage:
            O2: { compressed: {...}, liquid: {...} }
            CO2: { compressed: {...} }
      [ ] Include reliability/maintenance in YAML.
      [ ] Cite ISS CDRA / OGA / vendor datasheets.
    """
    scrubber: Dict[str, Any] = field(default_factory=dict)
    electrolyzer: Dict[str, Any] = field(default_factory=dict)
    storage: Dict[str, Any] = field(default_factory=dict)


# --- Output container (NO MATH; planning only) -------------------------------

@dataclass
class AirCyclePlan:
    """
    Synthesized design-time plan for O2/CO2.

    Fields (placeholders; fill via TODOs in functions below):
      demand:
        O2_kg_per_day: null
        CO2_kg_per_day: null
        peak_modifiers: { exercise_day, EVA_day, quarantine, etc. }
      allocation:
        natural_target_share: { canopy: 0.0, pbr: 0.0 }      # fractions or kg/day intent
        mechchem_target_share: { electrolyzer: 0.0, scrubber: 0.0 }
        rationale: [citations/notes]
      sizing:
        canopy_area_m2: null          # derive from yields
        pbr_area_m2: null             # or pbr_volume_L, illuminated_area_m2
        electrolyzer_units: null
        scrubber_units: null
        storage: { O2_kg: null, CO2_kg: null }
      ops:
        duty_cycles: { canopy: {}, pbr: {}, electrolyzer: {}, scrubber: {} }
        maintenance_windows_days: []
        failure_resilience_notes: []
      citations: []
      notes: []
    """
    demand: Dict[str, Any] = field(default_factory=dict)
    allocation: Dict[str, Any] = field(default_factory=dict)
    sizing: Dict[str, Any] = field(default_factory=dict)
    ops: Dict[str, Any] = field(default_factory=dict)
    citations: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# --- Loaders for YAML inputs (NO MATH) --------------------------------------

def load_inputs(
    design_path: str,
    overrides_path: Optional[str],
    crew_profile_path: str,
    targets_path: str,
) -> Tuple[NaturalOptions, MechChemOptions, CrewProfile, AtmosphereTargets, Dict[str, Any]]:
    """
    Load all YAML inputs and return typed containers + merged raw dict.

    TODO:
      [ ] Apply schema validation (data/schemas/*.schema.yaml).
      [ ] Track provenance: for each field, record source path and citation key.
      [ ] Deep-merge overrides into design.
    """
    base = load_yaml(design_path)
    merged = base
    if overrides_path:
        overrides = load_yaml(overrides_path)
        merged = merge_dicts(base, overrides)

    natural = NaturalOptions(
        canopy=merged.get("canopy", {}),
        pbr=merged.get("pbr", {}),
    )
    mechchem = MechChemOptions(
        scrubber=merged.get("scrubber", {}),
        electrolyzer=merged.get("electrolyzer", {}),
        storage=merged.get("buffers", {}),
    )
    cp_raw = load_yaml(crew_profile_path)
    tgt_raw = load_yaml(targets_path)

    crew = CrewProfile(
        crew_count_total=cp_raw.get("crew_count_total", 0),
        activity_profile=cp_raw.get("activity_profile", {}),
        special_phases=cp_raw.get("special_phases", {}),
        notes=cp_raw.get("notes", []),
    )
    targets = AtmosphereTargets(
        O2_fraction_target=tgt_raw.get("O2_fraction_target"),
        O2_fraction_min=tgt_raw.get("O2_fraction_min"),
        O2_fraction_max=tgt_raw.get("O2_fraction_max"),
        CO2_ppm_max=tgt_raw.get("CO2_ppm_max"),
        buffer_days_O2=tgt_raw.get("buffer_days_O2"),
        buffer_days_CO2=tgt_raw.get("buffer_days_CO2"),
        design_time_horizon_days=tgt_raw.get("design_time_horizon_days"),
        notes=tgt_raw.get("notes", []),
    )
    return natural, mechchem, crew, targets, {"design": merged, "crew": cp_raw, "targets": tgt_raw}


# --- Planning helpers (NO MATH; prompts only) --------------------------------

def estimate_crew_gas_budget(crew: CrewProfile, targets: AtmosphereTargets) -> Dict[str, Any]:
    """
    Return required daily O2 generation and CO2 scrubbing.

    TODO:
      [ ] For each activity in crew.activity_profile, pull O2/CO2 rates (per person) from literature/YAML.
      [ ] Aggregate to daily totals:
            demand.O2_kg_per_day
            demand.CO2_kg_per_day
      [ ] Derive peak modifiers (exercise days, EVA, illness).
      [ ] Cross-check with targets (e.g., CO2 ppm max → implied removal rate for cabin volume).
      [ ] Add citations used to compute the figures.
    Returns:
      {"O2_kg_per_day": None, "CO2_kg_per_day": None, "peak_modifiers": {}, "citations": [], "notes": []}
    """
    return {
        "O2_kg_per_day": None,
        "CO2_kg_per_day": None,
        "peak_modifiers": {},
        "citations": [],
        "notes": ["TODO: implement using NASA-STD-3001/ASHRAE activity rates."],
    }


def propose_allocation_strategy(
    natural: NaturalOptions,
    mechchem: MechChemOptions,
    demand: Dict[str, Any],
    policy: AtmosphereTargets,
) -> Dict[str, Any]:
    """
    Decide how much of the demand should be targeted by natural vs mech/chem systems.

    TODO:
      [ ] Consider constraints:
            - Available deck area, optical access, power, uptime/reliability
            - Maintenance & crew-time cost
            - Mass/volume budgets (from YAML)
      [ ] Propose target shares (fractions or kg/day) for:
            allocation.natural_target_share: { canopy: x, pbr: y }
            allocation.mechchem_target_share: { electrolyzer: a, scrubber: b }
      [ ] Note rationale and citations (design philosophy/benchmark systems).
    Returns:
      {"natural_target_share": {}, "mechchem_target_share": {}, "rationale": [], "citations": []}
    """
    return {
        "natural_target_share": {},
        "mechchem_target_share": {},
        "rationale": ["TODO: record trade-offs and constraints here."],
        "citations": [],
    }


def size_biological_blocks(
    natural: NaturalOptions,
    allocation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert biological target shares into space/capacity requirements.

    TODO:
      [ ] Canopy:
            - Use canopy O2_g_per_m2_h (min/typ/max) to estimate canopy_area_m2.
            - Account for photoperiod/duty-cycle if specified in YAML.
            - Record uncertainties/safety factors (explicit in YAML).
      [ ] PBR:
            - Use O2_mmol_per_L_h or biomass_g_per_L_d with optical_depth_m to
              estimate illuminated_area_m2 or reactor_volume_L.
            - Check mixing_W_per_m3 and thermal integration constraints (hooks only).
    Returns:
      {"canopy_area_m2": None, "pbr_area_m2": None, "pbr_volume_L": None, "notes": [], "citations": []}
    """
    return {
        "canopy_area_m2": None,
        "pbr_area_m2": None,
        "pbr_volume_L": None,
        "notes": ["TODO: convert target O2 shares into areas/volumes using literature yields."],
        "citations": [],
    }


def size_mechchem_blocks(
    mechchem: MechChemOptions,
    allocation: Dict[str, Any],
    policy: AtmosphereTargets,
) -> Dict[str, Any]:
    """
    Convert mech/chem target shares into device counts and storage buffers.

    TODO:
      [ ] Electrolyzer:
            - Use O2_kg_per_h and power_kW to size 'electrolyzer_units' for target O2 share.
            - Consider water_kg_per_h and available water budget.
      [ ] Scrubber:
            - Use capacity_CO2_kg and regen_power_W to size 'scrubber_units' and duty cycles.
            - Include media life / regeneration windows.
      [ ] Storage:
            - Determine O2/CO2 buffer masses from policy.buffer_days_* and demand.
            - Select storage technology entries (compressed/liquid) from YAML.
    Returns:
      {"electrolyzer_units": None, "scrubber_units": None, "storage": {"O2_kg": None, "CO2_kg": None}, "notes": [], "citations": []}
    """
    return {
        "electrolyzer_units": None,
        "scrubber_units": None,
        "storage": {"O2_kg": None, "CO2_kg": None},
        "notes": ["TODO: translate targets to unit counts and buffers using spec sheets."],
        "citations": [],
    }


def propose_ops_patterns(
    biological: Dict[str, Any],
    mechchem: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Draft duty cycles and maintenance windows.

    TODO:
      [ ] Define duty_cycles per block (e.g., canopy photoperiod, PBR uptime, electrolyzer shift schedule).
      [ ] Add maintenance_windows_days from vendor/ISS practices (filters, media, stack service).
      [ ] Note failure-resilience strategies (N+1, cold-standby).
    Returns:
      {"duty_cycles": {"canopy": {}, "pbr": {}, "electrolyzer": {}, "scrubber": {}},
       "maintenance_windows_days": [],
       "failure_resilience_notes": []}
    """
    return {
        "duty_cycles": {"canopy": {}, "pbr": {}, "electrolyzer": {}, "scrubber": {}},
        "maintenance_windows_days": [],
        "failure_resilience_notes": ["TODO: define redundancy and swap-over strategy."],
    }


# --- Orchestrator ------------------------------------------------------------

def build_air_cycle_plan(
    design_path: str = "data/specs/air_cycle_design.yaml",
    overrides_path: Optional[str] = "configs/life_support/air_cycle_overrides.yaml",
    crew_profile_path: str = "configs/life_support/crew_profile.yaml",
    targets_path: str = "configs/life_support/targets.yaml",
) -> AirCyclePlan:
    """
    High-level planner: load inputs, estimate demand, propose allocation, and size blocks.

    TODO:
      [ ] Insert schema checks; fail early with actionable messages.
      [ ] Maintain a 'citations' list gathered from YAML throughout the plan.
      [ ] Consider profiles for multiple horizons: baseline day, peak day, contingency week.
    """
    natural, mechchem, crew, policy, raw = load_inputs(
        design_path, overrides_path, crew_profile_path, targets_path
    )

    demand = estimate_crew_gas_budget(crew, policy)
    allocation = propose_allocation_strategy(natural, mechchem, demand, policy)

    bio = size_biological_blocks(natural, allocation)
    mc = size_mechchem_blocks(mechchem, allocation, policy)
    ops = propose_ops_patterns(bio, mc)

    plan = AirCyclePlan(
        demand=demand,
        allocation=allocation,
        sizing={**bio, **mc},
        ops=ops,
        citations=[],  # TODO: aggregate unique citations used across all steps
        notes=["SKELETON: fill numbers from literature and spec YAMLs."],
    )
    return plan


def save_air_cycle_plan(plan: AirCyclePlan, out_path: str = "configs/life_support/air_cycle_plan.yaml") -> None:
    """
    Write the design plan to YAML.

    TODO:
      [ ] Add metadata header (version, author, date, repo commit hash).
      [ ] Optionally split into multiple files (plan, allocations, operations).
    """
    dump_yaml(out_path, plan.to_dict())

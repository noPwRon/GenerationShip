"""
calc_env.py
------------
Environmental and HVAC calculation utilities.

Design Notes
------------
• Keep schema/defaults in env.hvac.constants (not hardcoded strings).
• Stage temperature/pressure-aware values via common.physics (TODO below).
• Preserve current function signatures and behavior; add TODO hooks only.
• Output key names (e.g., 'supply_Lps', 'exhaust_Lps') can be centralized later.

TODO (High-level)
-----------------
[ ] Move temperature/pressure-dependent numbers into common.physics
[ ] Thread scenario ambient conditions (T, P, RH) through call sites when needed
[ ] Add minimal validation (types, >=0) where appropriate
[ ] Replace placeholder device/latent models with data-driven implementations
"""

from __future__ import annotations
from typing import Tuple, Optional, Dict, Any
from common.physics import (
    cp_dry_air_J_per_kgK,
    latent_heat_vap_kJ_per_kg,
    air_density_kg_per_m3,
)




from env.hvac.constants import (
    ACTIVITY_KEYS,
    VENTILATION_KEYS,
    EXHAUST_KEYS,
    DEFAULT_ACTIVITY_LEVELS,
    DEFAULT_VENTILATION,
)

# ---------------------------------------------------------------------------
# Physics constants — CURRENTLY LOCAL to avoid breaking callers.
# TODO: Replace with functions from common.physics and remove literals here.
#   - cp_dry_air_J_per_kgK(T_K)
#   - latent_heat_vap_kJ_per_kg(T_C)
#   - air_density_kg_per_m3(T_K, P_kPa, RH_frac)
# from common.physics import cp_dry_air_J_per_kgK, latent_heat_vap_kJ_per_kg, air_density_kg_per_m3  # noqa: E401,F401
# ---------------------------------------------------------------------------
AIR_DENSITY_KG_PER_M3 = 1.2  # TODO: deprecate → common.physics.air_density_kg_per_m3
AIR_HEAT_CAP_KJ_PER_KG_K = (
    1.0  # TODO: deprecate → common.physics.cp_dry_air_J_per_kgK/1000
)
LATENT_HEAT_VAP_KJ_PER_KG = (
    2450.0  # TODO: deprecate → common.physics.latent_heat_vap_kJ_per_kg
)


def validate_exhaust_keys(exhaust_dict: Dict[str, Any]) -> None:
    """
    Ensure all exhaust keys are recognized by the schema.

    TODO:
      [ ] Validate values are numeric and >= 0
      [ ] Consider warning/logging for unknown-but-present keys
    """
    for key in exhaust_dict.keys():
        if key not in EXHAUST_KEYS:
            raise KeyError(
                f"Unknown exhaust key '{key}' — expected one of {EXHAUST_KEYS}"
            )


def ventilation_rate(
    occupants: int,
    Lps_per_person: float = DEFAULT_VENTILATION["Rp_Lps_per_person"],
    area_m2: float = 0.0,
    lps_per_m2: float = DEFAULT_VENTILATION["Ra_Lps_per_m2"],
) -> float:
    """
    Compute required ventilation [L/s].

    Formula
    -------
        ventilation = Rp * occupants + Ra * area_m2

    TODO:
      [ ] Optional unit/type guards (ints/floats, >=0)
      [ ] (Later) allow schedule/duty modifiers at call site
    """
    Ra = area_m2 * lps_per_m2
    Rp = occupants * Lps_per_person
    return Ra + Rp


def exhaust_rate(
    area_m2: float,
    exhaust_info: Optional[Dict[str, Any]] = None,
    fixtures: int = 0,
) -> float:
    """
    Compute required exhaust airflow [L/s].

    Behavior
    --------
    - Uses the greater of area-based or per-fixture drivers.
    - Keys validated against EXHAUST_KEYS.

    TODO:
      [ ] Confirm precedence policy (max vs sum) for your standards
      [ ] Add type/>=0 guards on inputs
    """
    if not exhaust_info:
        return 0.0

    total = 0.0
    if "Ra_Lps_per_m2" in exhaust_info:
        total = max(total, float(exhaust_info["Ra_Lps_per_m2"]) * area_m2)

    per_fixture_keys = set(EXHAUST_KEYS) - {"Ra_Lps_per_m2"}
    for key in per_fixture_keys:
        if key in exhaust_info:
            total = max(total, float(exhaust_info[key]) * fixtures)

    return total


def supply_rate(total_ventilation: float, required_exhaust: float) -> float:
    """
    Compute supply airflow [L/s] given total ventilation and exhaust rates.

    Policy
    ------
    - Default: ensure supply meets or exceeds exhaust to avoid depressurization.

    TODO:
      [ ] Expose bias/pressurization strategy if needed (e.g., supply = exhaust + offset)
    """
    return max(total_ventilation, required_exhaust)


def metabolic_heat_kW(occupants: int, sensible_W: float = 100.0) -> float:
    """
    Compute occupant metabolic sensible load [kW].

    Notes
    -----
    - Caller should supply sensible_W from activity tables.
    - Kept simple to avoid premature coupling to cp(T).

    TODO:
      [ ] Validate inputs; consider using activity profiles directly at call sites
    """
    return occupants * sensible_W / 1000.0


def latent_heat_kW(occupants: int, latent_W: float) -> float:
    """
    Compute occupant latent load [kW].

    Notes
    -----
    - Caller should supply latent_W from activity tables.
    - For mass-based inputs later, convert via latent_heat_vap_kJ_per_kg(T).

    TODO:
      [ ] Add path to mass-flow-based latent calculations (kg/s × L_v(T))
    """
    return occupants * latent_W / 1000.0


def device_load_kW(occupants: int) -> Tuple[float, float]:
    """
    Placeholder for device load estimation (base, peak).

    TODO:
      [ ] Replace with equipment-driven model (specs + inventory + duty/diversity)
      [ ] Provide an interface that sums per-device sensible/latent/electric loads
    """
    base = occupants * 0.1  # TODO: remove when equipment model lands
    peak = base * 1.5
    return base, peak


def latent_load_kgph(occupants: int) -> float:
    """
    Placeholder latent moisture generation [kg/h].

    TODO:
      [ ] Replace with empirical activity-based model
      [ ] Optionally include equipment/process contributions
    """
    return occupants * 0.12  # TODO: replace with real data


def temp_band(_phase: str) -> Tuple[float, float]:
    """
    Placeholder temperature comfort range [°C].

    TODO:
      [ ] Parameterize by activity/space type; cite ASHRAE/NASA sources
    """
    return 20.0, 24.0


def rh_band(_phase: str) -> Tuple[float, float]:
    """
    Placeholder humidity comfort range [%].

    TODO:
      [ ] Parameterize by space type and contamination control class
    """
    return 35.0, 60.0

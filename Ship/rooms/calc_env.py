"""
calc_env.py
------------
Environmental and HVAC calculation utilities.

Purpose:
    - Centralize equations for airflow, heat, and humidity.
    - Provide consistent physical assumptions for all rooms.
"""

from typing import Tuple, Optional, Dict, Any
from Ship.rooms.calc_tables import get_rates
from Ship.config.constants import EXHAUST_KEYS


# --- Constants ---------------------------------------------------------------
AIR_DENSITY = 1.2
AIR_HEAT_CAP = 1.0
LATENT_HEAT_VAP = 2450.0
DEFAULT_LPS_PER_PERSON = get_rates("default", "default")["ventilation"][
    "Rp_Lps_per_person"
]
DEFAULT_LPS_PER_AREA = get_rates("default", "default")["ventilation"]["Ra_Lps_per_m2"]


# --- Ventilation Calculations -----------------------------------------------
def ventilation_rate(
    occupants: int,
    Lps_per_person: float = DEFAULT_LPS_PER_PERSON,
    area_m2: float = 0.0,
    lps_per_m2: float = DEFAULT_LPS_PER_AREA,
) -> float:
    """Compute required ventilation [L/s]."""
    Ra = area_m2 * lps_per_m2
    Rp = occupants * Lps_per_person
    Rt = Ra + Rp

    return Rt


def exhaust_rate(
    area_m2: float, exhaust_info: Optional[Dict[str, Any]] = None, fixtures: int = 0
) -> float:
    """Compute required exhaust airflow [L/s].
    Args:
        area_m2 (float): _description_
        exhaust_info (Optional[Dict[str, Any]], optional): _description_. Defaults to None.
        fixtures (int, optional): _description_. Defaults to 0.

    Returns:
        float: _description_
    """

    if not exhaust_info:
        return 0.0

    keys = EXHAUST_KEYS
    Re = 0.0

    for k in keys:
        if k not in exhaust_info:
            continue
        val = exhaust_info[k]
        if k == "Re_Lps_per_m2":
            Re = max(Re, val * area_m2)
        else:
            Re = max(Re, val * fixtures)

    return Re


def supply_rate(Rt: float, Re: float) -> float:
    """Compute required supply airflow [L/s] given total ventilation and exhaust rates"""

    Rs = max(Rt, Re)
    return Rs


# --- Heat Loads --------------------------------------------------------------
def metabolic_heat_kW(occupants: int, sensible_W: float = 100.0) -> float:
    """Compute occupant metabolic sensible load [kW]."""
    human_heat_gen = occupants * sensible_W  # W
    return human_heat_gen / 1000.0  # Convert to kW


def device_load_kW(occupants: int) -> Tuple[float, float]:
    """Estimate base and peak electrical loads [kW]."""
    # TODO: write formula
    pass


# --- Latent Heat & Moisture --------------------------------------------------
def latent_load_kgph(occupants: int) -> float:
    """Estimate latent moisture generation [kg/h]."""
    # TODO: write formula
    pass


def latent_heat_kW(occupants: int, latent_W: float) -> float:
    # compute total latent load for occupants in kW
    latent_kW = (latent_W * occupants) / 1000
    return latent_kW


# --- Environmental Comfort Bands --------------------------------------------
def temp_band(phase: str) -> Tuple[float, float]:
    """Return temperature comfort range [°C] for life phase."""
    # TODO: lookup dictionary or logic
    pass


def rh_band(phase: str) -> Tuple[float, float]:
    """Return humidity comfort range [%] for life phase."""
    # TODO: lookup dictionary or logic
    pass


# --- Cooling Requirements -------------------------------------------------------
# Assuming each room is perfectly insulated for now; implement later if needed.
# ASHRAE standards can guide this.

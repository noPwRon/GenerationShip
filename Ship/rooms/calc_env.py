"""
calc_env.py
------------
Environmental and HVAC calculation utilities.

Purpose:
    - Centralize equations for airflow, heat, and humidity.
    - Provide consistent physical assumptions for all rooms.
"""

from typing import Tuple


# --- Constants ---------------------------------------------------------------
AIR_DENSITY = 1.2
AIR_HEAT_CAP = 1.0
LATENT_HEAT_VAP = 2450.0
DEFAULT_LPS_PER_PERSON = 12.0


# --- Ventilation Calculations -----------------------------------------------
def ventilation_rate(
    occupants: int, Lps_per_person: float = DEFAULT_LPS_PER_PERSON
) -> float:
    """Compute required ventilation [L/s]."""
    # TODO: write formula
    pass


# --- Heat Loads --------------------------------------------------------------
def metabolic_heat_kW(occupants: int, sensible_W: float = 100.0) -> float:
    """Compute occupant metabolic sensible load [kW]."""
    # TODO: write formula
    pass


def device_load_kW(occupants: int) -> Tuple[float, float]:
    """Estimate base and peak electrical loads [kW]."""
    # TODO: write formula
    pass


# --- Latent Heat & Moisture --------------------------------------------------
def latent_load_kgph(occupants: int) -> float:
    """Estimate latent moisture generation [kg/h]."""
    # TODO: write formula
    pass


def latent_to_kW(latent_kgph: float) -> float:
    """Convert latent moisture load [kg/h] to heat power [kW]."""
    # TODO: write formula
    pass


# --- Environmental Comfort Bands --------------------------------------------
def temp_band(phase: str) -> Tuple[float, float]:
    """Return temperature comfort range [°C] for life phase."""
    # TODO: lookup dictionary or logic
    pass


def rh_band(phase: str) -> Tuple[float, float]:
    """Return humidity comfort range [%] for life phase."""
    # TODO: lookup dictionary or logic
    pass

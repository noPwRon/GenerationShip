"""
calc_env.py
------------
Environmental and HVAC calculation utilities.
"""

from __future__ import annotations

from typing import Tuple, Optional, Dict, Any

from env.hvac.constants import EXHAUST_KEYS, DEFAULT_VENTILATION


AIR_DENSITY_KG_PER_M3 = 1.2
AIR_HEAT_CAP_KJ_PER_KG_K = 1.0
LATENT_HEAT_VAP_KJ_PER_KG = 2450.0


def ventilation_rate(
    occupants: int,
    Lps_per_person: float = DEFAULT_VENTILATION["Rp_Lps_per_person"],
    area_m2: float = 0.0,
    lps_per_m2: float = DEFAULT_VENTILATION["Ra_Lps_per_m2"],
) -> float:
    """Compute required ventilation [L/s]."""

    Ra = area_m2 * lps_per_m2
    Rp = occupants * Lps_per_person
    return Ra + Rp


def exhaust_rate(
    area_m2: float,
    exhaust_info: Optional[Dict[str, Any]] = None,
    fixtures: int = 0,
) -> float:
    """Compute required exhaust airflow [L/s]."""

    if not exhaust_info:
        return 0.0

    total = 0.0
    if "Ra_Lps_per_m2" in exhaust_info:
        total = max(total, exhaust_info["Ra_Lps_per_m2"] * area_m2)

    per_fixture_keys = set(EXHAUST_KEYS) - {"Ra_Lps_per_m2"}
    for key in per_fixture_keys:
        if key in exhaust_info:
            total = max(total, exhaust_info[key] * fixtures)

    return total


def supply_rate(total_ventilation: float, required_exhaust: float) -> float:
    """Compute supply airflow [L/s] given total ventilation and exhaust rates."""

    return max(total_ventilation, required_exhaust)


def metabolic_heat_kW(occupants: int, sensible_W: float = 100.0) -> float:
    """Compute occupant metabolic sensible load [kW]."""

    return occupants * sensible_W / 1000.0


def latent_heat_kW(occupants: int, latent_W: float) -> float:
    """Compute occupant latent load [kW]."""

    return occupants * latent_W / 1000.0


def device_load_kW(occupants: int) -> Tuple[float, float]:
    """Placeholder for device load estimation (base, peak)."""

    base = occupants * 0.1  # TODO: replace with data driven model
    peak = base * 1.5
    return base, peak


def latent_load_kgph(occupants: int) -> float:
    """Placeholder latent moisture generation [kg/h]."""

    return occupants * 0.12  # TODO: replace with empirical data


def temp_band(_phase: str) -> Tuple[float, float]:
    """Placeholder temperature comfort range [°C]."""

    return 20.0, 24.0


def rh_band(_phase: str) -> Tuple[float, float]:
    """Placeholder humidity comfort range [%]."""

    return 35.0, 60.0

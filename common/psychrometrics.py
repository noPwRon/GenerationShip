"""
psychrometrics.py
-----------------
Purpose
    • Centralize moist-air relationships for HVAC/environmental calcs.
    • Keep calc_env free of embedded formulas.

Status
    • SKELETON ONLY — all functions return placeholders.
    • Replace TODO sections with vetted relations and citations.

Conventions
    • SI units unless stated.
    • T_C = degrees Celsius, T_K = Kelvin, P_kPa = kilopascals, RH_frac = 0..1.

References (suggested to cite once implemented)
    • ASHRAE Fundamentals (latest edition)
    • W. H. Carrier or Tetens approximations (for Psat)
    • NIST/NOAA tables if higher accuracy is needed
"""

from __future__ import annotations
from typing import Optional
import math


# ---------------------------------------------------------------------------
# Saturation vapor pressure
# ---------------------------------------------------------------------------
def saturation_vapor_pressure_kPa(T_C: float) -> float:
    """
    Saturation vapor pressure of water at T_C [kPa].
    # Using Tetens Equation to determine saturation vapor pressure
    # Monteith and Unsworth, 2008 for temp above 0 °C and Murray, 1967 for temp below 0 °C

    TODO:
    [ ] Add tests at 0, 20, 30, 40 °C anchors.
    """

    if T_C > 0:
        # Tetens equation for T_C > 0 °C
        Psat_kPa = 0.61078 * math.exp((17.27 * T_C) / (T_C + 237.3))
    elif T_C <= 0:
        # Murray equation for T_C <= 0 °C
        Psat_kPa = 0.61078 * math.exp((21.875 * T_C) / (T_C + 265.5))
    elif T_C > 50:
        raise ValueError("Temperature exceeds valid range for Tetens equation.")

    return Psat_kPa


# ---------------------------------------------------------------------------
# Humidity ratio
# ---------------------------------------------------------------------------
def humidity_ratio_w(P_kPa: float, T_C: float, RH_frac: float) -> float:
    """
    Humidity ratio w = kg_water / kg_dry_air.

    Inputs
        P_kPa  : total pressure
        T_C    : dry-bulb temperature
        RH_frac: relative humidity (0..1)

    TODO:
    [ ] Use Psat(T) and standard psychrometric relation.
    [ ] Guard against Pv >= P; clamp/raise with clear error.
    """
    return 0.0  # SKELETON


# ---------------------------------------------------------------------------
# Moist air enthalpy
# ---------------------------------------------------------------------------
def moist_air_enthalpy_kJ_per_kg_dryair(T_C: float, w: float) -> float:
    """
    Specific enthalpy of moist air per kg of dry air [kJ/kg_dry_air].

    TODO:
    [ ] Implement standard h = 1.005*T + w*(2501 + 1.88*T) (or chosen variant).
    [ ] Document constants and units; add unit tests for typical states.
    """
    return 0.0  # SKELETON


# ---------------------------------------------------------------------------
# Dew point
# ---------------------------------------------------------------------------
def dew_point_C(T_C: float, RH_frac: float) -> float:
    """
    Dew-point temperature [°C] at given dry-bulb and RH.

    References
        • ASHRAE Handbook — Fundamentals (2021), Chapter 1, “Psychrometrics”
        • W. H. Carrier or Tetens approximations (for Psat)
        • NIST/NOAA tables if higher accuracy is needed
    """

    a, b = 17.27, 237.3
    gamma = (a * T_C / (b + T_C)) + math.log(RH_frac)
    return (b * gamma) / (a - gamma)


# ---------------------------------------------------------------------------
# Wet-bulb (optional for later)
# ---------------------------------------------------------------------------
def wet_bulb_C(T_C: float, RH_frac: float, P_kPa: float = 101.325) -> float:
    """
    Wet-bulb temperature [°C] at given dry-bulb, RH, and pressure.

    TODO:
    [ ] Implement iterative / closed-form approximation per chosen reference.
    [ ] Consider performance vs. accuracy; expose tolerance if iterative.
    """
    return 0.0  # SKELETON

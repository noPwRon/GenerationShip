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


MBAR_PER_KPA = 10.0
STANDARD_ATM_KPA = 101.325

# Hyland & Wexler coefficients (Table 2) for Eq. 4a/4b.
_SAT_PRESSURE_CURVES = {
    "water": {
        "a": 6.1121,
        "b": 18.564,
        "c": 255.57,
        "d": 254.4,
        "t_min": 0.0,
        "t_max": 100.0,
    },  # e_w6
    "ice": {
        "a": 6.1115,
        "b": 23.036,
        "c": 279.82,
        "d": 333.7,
        "t_min": -80.0,
        "t_max": 0.0,
    },  # e_i3
}

# Enhancement factor coefficients (Table 3) for Eq. 6.
_ENHANCEMENT_COEFFS = {
    "water": {
        "A": 4.1e-4,
        "B": 3.48e-6,
        "C": 7.4e-10,
        "D": 30.6,
        "E": -3.8e-2,
    },  # f_w5
    "ice": {
        "A": 4.8e-4,
        "B": 3.47e-6,
        "C": 5.9e-10,
        "D": 23.8,
        "E": -3.1e-2,
    },  # f_i5
}


def _phase_for_temperature(T_C: float) -> str:
    return "water" if T_C >= 0.0 else "ice"


def _magnus_type_4a_mb(T_C: float, phase: str) -> float:
    coeffs = _SAT_PRESSURE_CURVES[phase]
    if not (coeffs["t_min"] <= T_C <= coeffs["t_max"]):
        raise ValueError(
            f"T_C={T_C}°C outside valid range [{coeffs['t_min']}, {coeffs['t_max']}] for {phase} curve"
        )
    a = coeffs["a"]
    b = coeffs["b"]
    c = coeffs["c"]
    d = coeffs["d"]
    numerator = (b - T_C / d) * T_C
    denominator = T_C + c
    return a * math.exp(numerator / denominator)


def _magnus_type_4b_C(e_mb: float, phase: str) -> float:
    if e_mb <= 0:
        raise ValueError("Vapor pressure must be > 0 mb for Eq. (4b).")
    a = _SAT_PRESSURE_CURVES[phase]["a"]
    b = _SAT_PRESSURE_CURVES[phase]["b"]
    c = _SAT_PRESSURE_CURVES[phase]["c"]
    d = _SAT_PRESSURE_CURVES[phase]["d"]
    z = math.log(e_mb / a)
    b_minus_z = b - z
    discriminant = b_minus_z**2 - (4.0 * c * z) / d
    if discriminant < 0:
        raise ValueError(
            f"Negative discriminant encountered in Eq. (4b): {discriminant}"
        )
    return 0.5 * d * (b_minus_z - math.sqrt(discriminant))


def _enhancement_factor(T_C: float, P_kPa: float, phase: str) -> float:
    coeffs = _ENHANCEMENT_COEFFS[phase]
    P_mb = P_kPa * MBAR_PER_KPA
    A = coeffs["A"]
    B = coeffs["B"]
    C = coeffs["C"]
    D = coeffs["D"]
    E = coeffs["E"]
    return 1.0 + A + P_mb * (B + C * (T_C + D + E * P_mb) ** 2)


# ---------------------------------------------------------------------------
# Saturation vapor pressure
# ---------------------------------------------------------------------------
def saturation_vapor_pressure_kPa(T_C: float, P_kPa: float = STANDARD_ATM_KPA) -> float:
    """
    Saturation vapor pressure of water at T_C [kPa].
    Uses Hyland and Wexler Eq. 4a with ew6/ei3 coefficients plus fw5/fi5 enhancement factors.

    TODO:
    [ ] Add tests at 0, 20, 30, 40 ?C anchors.
    """

    phase = _phase_for_temperature(T_C)
    e_mb = _magnus_type_4a_mb(T_C, phase)
    f = _enhancement_factor(T_C, P_kPa, phase)
    return 0.1 * f * e_mb


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
def dew_point_C(T_C: float, RH_frac: float, P_kPa: float = STANDARD_ATM_KPA) -> float:
    """
    Dew-point temperature [?C] at given dry-bulb, RH, and pressure.

    Uses Hyland and Wexler Eq. 4b with ei3/ew6 coefficients and fw5/fi5 enhancement
    factors via iterative solve.

    References
        ? ASHRAE Handbook ? Fundamentals (2021), Chapter 1, ?Psychrometrics?
        ? W. H. Carrier or Tetens approximations (for Psat)
        ? NIST/NOAA tables if higher accuracy is needed
    """

    if RH_frac <= 0.0:
        return float("-inf")
    if RH_frac > 1.0:
        raise ValueError("Relative humidity must be between 0 and 1.")

    e_s_kPa = saturation_vapor_pressure_kPa(T_C, P_kPa)
    e_actual_mb = RH_frac * e_s_kPa * MBAR_PER_KPA
    T_guess = T_C

    for _ in range(20):
        phase = _phase_for_temperature(T_guess)
        f = _enhancement_factor(T_guess, P_kPa, phase)
        e_curve_mb = e_actual_mb / f
        T_new = _magnus_type_4b_C(e_curve_mb, phase)
        if abs(T_new - T_guess) < 1e-6:
            return T_new
        T_guess = T_new

    return T_guess

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

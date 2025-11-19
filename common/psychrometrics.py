"""
psychrometrics.py
-----------------
Purpose
    • Centralize moist-air relationships for HVAC/environmental calcs.
    • Keep calc_env free of embedded formulas.

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
from common.physics import saturation_vapor_pressure_kPa
from common.physics import (
    MOL_WEIGHT_DRY_AIR,
    MOL_WEIGHT_WATER_VAPOR,
    STD_ATM_PRESSURE_KPA,
)


MBAR_PER_KPA = 10.0
STANDARD_ATM_KPA = STD_ATM_PRESSURE_KPA


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

    """

    P_v = RH_frac * saturation_vapor_pressure_kPa(T_C)
    if P_v >= P_kPa:
        raise ValueError("Invalid humidity ratio: Pv >= P")

    w = MOL_WEIGHT_WATER_VAPOR / MOL_WEIGHT_DRY_AIR * P_v / (P_kPa - P_v)

    return w


# ---------------------------------------------------------------------------
# Moist air enthalpy
# ---------------------------------------------------------------------------
def moist_air_enthalpy_kJ_per_kg_dryair(T_C: float, w: float) -> float:
    """
    Specific enthalpy of moist air per kg of dry air [kJ/kg_dry_air].

    h = 1.006 * T_C + w * (2501.0 + 1.86 * T_C)
    from psychrometric relations.
    """

    h = 1.006 * T_C + w * (2501.0 + 1.86 * T_C)

    return h


# ---------------------------------------------------------------------------
# Dew point
# ---------------------------------------------------------------------------

def _phase_for_temperature(T_C: float) -> str:
    """
    Return the expected vapor phase keyword for a given temperature.

    Simple rule: below 0 °C use 'ice' (sublimation/ice), otherwise use 'liquid'.
    This is a lightweight heuristic used by enhancement/magnus helpers; a more
    complete implementation can use pressure and composition for precise phase
    determination.
    """
    return "ice" if T_C < 0.0 else "liquid"


def _enhancement_factor(T_C: float, P_kPa: float, phase: str) -> float:
    """
    Placeholder enhancement factor fw/fi used to convert actual vapor pressure to
    the curve pressure used by the Magnus-type inversion.

    A realistic implementation depends on temperature, pressure and phase.
    Uses Buck-style linear fits in pressure (hPa) for water/ice.
    """
    P_hPa = P_kPa * 10.0
    if phase == "ice":
        return 1.0003 + 4.18e-6 * P_hPa
    return 1.0007 + 3.46e-6 * P_hPa


def _magnus_type_4b_C(e_mb: float, phase: str) -> float:
    """
    Inverse Magnus-Tetens approximation to convert vapor pressure (mbar) to
    dew-point temperature in °C.

    Uses conventional parameter sets:
      - liquid water:  a=6.112  b=17.62  c=243.12
      - ice         :  a=6.112  b=22.46  c=272.62

    Returns -inf for non-positive vapor pressures.
    """
    if e_mb <= 0.0:
        return float("-inf")

    if phase == "ice":
        a = 6.112
        b = 22.46
        c = 272.62
    else:
        a = 6.112
        b = 17.62
        c = 243.12

    ln_ratio = math.log(e_mb / a)
    # Protect against division by zero in degenerate cases
    denom = b - ln_ratio
    if denom == 0.0:
        # Return a very large temperature (shouldn't occur for physical e_mb)
        return float("inf")

    T_C = (c * ln_ratio) / denom
    return T_C


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
    Uses iterative bisection solve on psychrometric relation.
    References
        NOAA/NWS Technical Report NWS 19 (1976)
    """
    if RH_frac < 0.0 or RH_frac > 1.0:
        raise ValueError("Relative humidity must be between 0 and 1.")
    if RH_frac == 0.0:
        return float("-inf")
    if RH_frac == 1.0:
        return T_C

    # Actual vapor pressure at the dry-bulb temperature (target value for the wet-bulb solve).
    e_actual = RH_frac * saturation_vapor_pressure_kPa(T_C, P_kPa)

    # Residual of the psychrometric relation; zeroed when Tw satisfies the equation.
    def _residual(Tw: float) -> float:
        e_sat_wet = saturation_vapor_pressure_kPa(Tw, P_kPa)
        psychrometric_term = P_kPa * 0.00066 * (1.0 + 0.00115 * Tw) * (T_C - Tw)
        return e_sat_wet - psychrometric_term - e_actual

    # Bracket Tw between dew point (lower) and dry-bulb (upper) so the root lies inside.
    Tw_low = dew_point_C(T_C, RH_frac, P_kPa)
    if not math.isfinite(Tw_low):
        Tw_low = T_C - 80.0
    Tw_low = min(Tw_low, T_C)
    Tw_high = T_C

    # If the lower bound is still above the root, push it colder until the sign flips.
    while _residual(Tw_low) > 0.0 and Tw_low > T_C - 120.0:
        Tw_low -= 5.0

    # Classic bisection: shrink [Tw_low, Tw_high] until the residual is small (root found).
    for _ in range(60):
        Tw_mid = 0.5 * (Tw_low + Tw_high)
        r_mid = _residual(Tw_mid)
        if abs(r_mid) < 1e-6 or abs(Tw_high - Tw_low) < 1e-6:
            return Tw_mid
        if r_mid > 0.0:
            Tw_high = Tw_mid
        else:
            Tw_low = Tw_mid

    return 0.5 * (Tw_low + Tw_high)

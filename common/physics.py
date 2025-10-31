"""
physics.py
-----------
Purpose
    • Provide temperature/pressure-aware helpers (shared across env/power/thermal).
    • Centralize physical constants so calc_env doesn't hardcode values.

Status
    • SKELETON ONLY — functions return placeholders.
    • Replace TODO sections with vetted formulas/refs when ready.

Units
    • SI unless noted.
"""

from __future__ import annotations
from typing import Optional

# --- Constants (define/confirm) ---------------------------------------------

# All constants below are sourced from physics.nist.gov
GRAV_CONSTANT = 6.67430e-11  # gravitational constant [m3 kg-1 s-2]
PLANCK_CONSTANT = 6.62607015e-34  # Planck constant [J s]
AVROGADRO_CONSTANT = 6.02214076e23  # Avogadro constant [mol-1]
STD_ATM_PRESSURE_KPA = 101.325  # standard atmospheric pressure [kPa]
MOLAR_GAS_CONSTANT = 8.314462618  # universal gas constant [J mol-1 K-1]
STD_GRAV_ACCEL = 9.80665  # standard gravity [m s-2]
STEFAN_BOLTZMANN = 5.67e-8  # W/m^2/K^4


# --- Temperature-dependent helpers (stub returns) ---------------------------
def cp_dry_air_J_per_kgK(T_K: float) -> float:
    """
    Specific heat of dry air at temperature T_K.

    TODO:
    [ ] Choose a polynomial or table-based model and cite source.
    [ ] Define valid T range (e.g., 250–330 K) and behavior outside it.
    [ ] Add tests that pin values at key points (273.15 K, 293.15 K, 303.15 K).
    """
    # NASA 7-term polynomial for dry air (200 – 1000 K)
    # Cp(T_K) = R * (a1 + a2*T_K + a3*T_K^2 + a4*T_K^3 + a5*T_K^4)

    if T_K <= 200:
        raise ValueError("Temperature out of range for cp_dry_air_J_per_kgK")
    elif T_K > 200 and T_K <= 1000:
        a1 = 3.56839620e00
        a2 = -6.39647050e-04
        a3 = 1.73945600e-06
        a4 = -1.22326600e-09
        a5 = 3.13194300e-13
    elif T_K > 1000 and T_K <= 6000:
        a1 = 2.61547000e00
        a2 = 2.96796200e-03
        a3 = -5.43060700e-07
        a4 = 5.11584700e-10
        a5 = -1.97318600e-15

    C_p = MOLAR_GAS_CONSTANT * (a1 + a2 * T_K + a3 * T_K**2 + a4 * T_K**3 + a5 * T_K**4)

    return C_p


def latent_heat_vap_kJ_per_kg(T_C: float) -> float:
    """
    Latent heat of vaporization of water at temperature T_C.

    TODO:
    [ ] Pick a model (e.g., linear approximation or better) and cite.
    [ ] Verify against 0°C and 100°C anchors.
    """
    return 2450.0  # SKELETON: replace with temperature function


def air_density_kg_per_m3(
    T_K: float, P_kPa: float = 101.325, RH_frac: Optional[float] = None
) -> float:
    """
    Density of (dry/moist) air at T_K, pressure P_kPa, and optional RH.

    TODO:
    [ ] Implement ideal gas (dry) and moist-air correction when RH is provided.
    [ ] Document assumptions (e.g., 1 + 1.6078*w correction).
    [ ] Add bounds/guards for unphysical inputs.
    """
    return 1.2  # SKELETON: replace with calculation


def water_density_kg_per_m3(T_K: float) -> float:
    """
    Density of water at T_K

    TODO:
    [ ] Implement standard correlation or table lookup.
    [ ] Define valid T range (e.g., 273.15–373.15 K) and behavior outside it.
    [ ] Add tests at key points (0°C, 25°C, 100°C).
    """
    return 0.8  # SKELETON: replace with calculation

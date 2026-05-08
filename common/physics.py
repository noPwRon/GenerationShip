"""
physics.py
-----------
Purpose
    • Provide temperature/pressure-aware helpers (shared across env/power/thermal).
    • Centralize physical constants so calc_env doesn't hardcode values.
Conventions / References
    • Use NIST and other authoritative sources for physical constants and formulas.
    • IAPWS Formulation for water properties (https://www.iapws.org/relguide/IF97-Rev.html)
    • NASA Glenn Coefficients for specific heat (https://www.grc.nasa.gov/www/wind/valid/air.html)
Units
    • SI unless noted.
"""

from __future__ import annotations
from typing import Optional
from common.conversions import C_to_K, K_to_C
from numpy import exp
from common.units import ureg, Q


# --- Constants (define/confirm) ---------------------------------------------

# All constants below are sourced from physics.nist.gov

# CODATA 2018 — https://physics.nist.gov/cgi-bin/cuu/Value?bg
# example on building units into physics
GRAV_CONSTANT = Q(6.67430e-11, "m**3 / kg / s**2") 

# NIST 2018 CODATA exact value — https://physics.nist.gov/cgi-bin/cuu/Value?h
PLANCK_CONSTANT = Q(6.62607015e-34, "J * s")  # Planck constant [J s]
# TODO: use .to("eV * s") for photon/radiation contexts

AVROGADRO_CONSTANT = Q(6.02214076e23, "1/mole")  # Avogadro constant [mol-1]


STD_ATM_PRESSURE_KPA = Q(101.325, "kPa")  # standard atmospheric pressure [kPa]
MOLAR_GAS_CONSTANT = 8.314462618  # universal gas constant [J mol-1 K-1]
AIR_GAS_CONSTANT = 287.058  # specific gas constant for dry air [J kg-1 K-1]
WATER_VAPOR_GAS_CONSTANT = 461.495  # specific gas constant for water vapor [J kg-1 K-1]
STD_GRAV_ACCEL = 9.80665  # standard gravity [m s-2]
STEFAN_BOLTZMANN = 5.67e-8  # W/m^2/K^4
MOL_WEIGHT_DRY_AIR = 28.9647e-3  # molar weight of dry air [kg/mol]
MOL_WEIGHT_WATER_VAPOR = 18.01528e-3  #


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
    https://www.sciencedirect.com/topics/earth-and-planetary-sciences/heat-of-vaporization

    Valid between melting point and T_K = 323 K
    """
    T_K = C_to_K(T_C)
    if T_K > 323:
        raise ValueError("Temperature out of range for latent_heat_vap_kJ_per_kg")

    Lat_heat = 1.91846e6 * (T_K / (T_K - 33.91)) ** 2  # SKELETON: replace with formula

    return Lat_heat / 1000.0  # convert J/kg to kJ/kg


def air_density_kg_per_m3(
    T_K: float, P_kPa: float = 101.325, RH_frac: Optional[float] = None
) -> float:
    """
    Density of (dry/moist) air at T_K, pressure P_kPa, and optional RH.

    For dry air:
    rho_a =  P_a / (R_a * T_K)
    for moist air:
    rho_a = (P_d / (R_a * T_K)) + (P_w / (R_w * T_K))
    where P_d = P_a - P_w and P_w = RH_frac * Psat(T_K)
    Source: https://www.engineeringtoolbox.com/density-air-d_680.html
    """

    P_a = P_kPa * 1000.0  # convert kPa to Pa
    R_a = AIR_GAS_CONSTANT  # J/(kg·K) for dry air
    R_w = WATER_VAPOR_GAS_CONSTANT  # J/(kg·K) for water vapor

    if RH_frac is None:
        rho_a = P_a / (R_a * T_K)
    else:
        p_sat = saturation_vapor_pressure_kPa(T_K) * 1000.0  # Pa
        P_w = RH_frac * p_sat  # partial pressure of water vapor
        P_d = P_a - P_w  # partial pressure of dry air
        rho_a = (P_d / (R_a * T_K)) + (P_w / (R_w * T_K))

    return rho_a


def water_density_kg_per_m3(T_K: float) -> float:
    """
    Density of water at T_K

    Using NIST's IAPWS Formulation Kell extended to 0 °C - 100 °C range.
    Source: https://www.iapws.org/relguide/IF97-Rev.html

    """
    T_C = K_to_C(T_K)

    if T_C < 0 or T_C > 100:
        raise ValueError("Temperature out of range for water_density_kg_per_m3")

    # IAPWS Formulation for water density
    A = 999.83952
    B = 16.945176
    C = -7.9870401e-03
    D = 1.2509471e-04
    E = -1.0572258e-06
    F = 6.1164410e-09

    T_C = T_K - 273.15
    rho_w = A + B * T_C + C * T_C**2 + D * T_C**3 + E * T_C**4 + F * T_C**5

    return rho_w


def saturation_vapor_pressure_kPa(T_K: float) -> float:
    """
    Saturation vapor pressure of water at T_K [kPa]. Using tetens formula.
    """
    T_C = T_K - 273.15

    return 6.112 * exp(17.67 * (T_C) / (T_C + 243.5))

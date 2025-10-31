"""
common package
--------------
Shared, cross-domain utilities for physics and moist-air psychrometrics.

Purpose
    • Provide a single import point for repo-wide constants/helpers.
    • Keep env/power/thermal modules free of hard-coded numbers.

Status
    • SKELETON — re-exports only; underlying functions may be placeholders.

Usage
    from common import air_density_kg_per_m3, cp_dry_air_J_per_kgK
"""

# Re-export selected helpers for convenience.
# TODO: Adjust this surface as you finalize the underlying APIs.
from .physics import (  # noqa: F401
    # --- physics (temperature/pressure aware) ---
    cp_dry_air_J_per_kgK,
    latent_heat_vap_kJ_per_kg,
    air_density_kg_per_m3,
    water_density_kg_per_m3,
)

from .psychrometrics import (  # noqa: F401
    # --- moist-air relations ---
    saturation_vapor_pressure_kPa,
    humidity_ratio_w,
    moist_air_enthalpy_kJ_per_kg_dryair,
    dew_point_C,
    wet_bulb_C,
)

from .conversions import (  # noqa: F401
    # --- unit conversions (SI-centric) ---
    Lps_to_m3h,
    m3h_to_Lps,
    W_to_kW,
    kW_to_W,
    C_to_K,
    K_to_C,
    C_to_F,
    F_to_C,
    hours_to_seconds,
    seconds_to_hours,
    minutes_to_seconds,
    seconds_to_minutes,
    hours_to_minutes,
    minutes_to_hours,
    deg_to_rad,
    rad_to_deg,
)

from .safety import (  # noqa: F401
    # --- safety margin helpers ---
    apply_margin,
)

__all__ = [
    # physics
    "cp_dry_air_J_per_kgK",
    "latent_heat_vap_kJ_per_kg",
    "air_density_kg_per_m3",
    "water_density_kg_per_m3",
    # psychrometrics
    "saturation_vapor_pressure_kPa",
    "humidity_ratio_w",
    "moist_air_enthalpy_kJ_per_kg_dryair",
    "dew_point_C",
    "wet_bulb_C",
    # conversions
    "Lps_to_m3h",
    "m3h_to_Lps",
    "W_to_kW",
    "kW_to_W",
    "C_to_K",
    "K_to_C",
    "C_to_F",
    "F_to_C",
    "hours_to_seconds",
    "seconds_to_hours",
    "minutes_to_seconds",
    "seconds_to_minutes",
    "hours_to_minutes",
    "minutes_to_hours",
    "deg_to_rad",
    "rad_to_deg",
    # safety
    "apply_margin",
]

"""
utils.py
---------
Shared constants and helper methods used across multiple modules.
Keep these general-purpose; avoid module-specific logic.
"""

GRAVITY = 9.80665  # m/s^2
AIR_DENSITY = 1.2  # kg/m^3
WATER_DENSITY = 1000.0  # kg/m^3
STEFAN_BOLTZMANN = 5.67e-8  # W/m^2/K^4


def convert_Lps_to_m3h(lps: float) -> float:
    """Convert litres per second to cubic metres per hour."""

    return lps * 3.6


def safety_margin(value: float, factor: float = 1.2, risk_type: str = "normal") -> float:
    """Apply a simple safety margin multiplier."""

    adjustment = factor
    if risk_type == "high":
        adjustment *= 1.5
    elif risk_type == "low":
        adjustment *= 1.1
    return value * adjustment
"""
utils.py
---------
Shared constants and helper methods used across multiple modules.
Keep these general-purpose; avoid module-specific logic.
"""

# --- Constants ---------------------------------------------------------------
from unittest import case


GRAVITY = 9.80665  # m/s²
AIR_DENSITY = 1.2  # kg/m³
WATER_DENSITY = 1000.0  # kg/m³
STEFAN_BOLTZMANN = 5.67e-8  # W/m²·K⁴


# --- Helper Function Placeholders --------------------------------------------
def convert_Lps_to_m3h(Lps: float) -> float:
    """
    Convert litres per second to cubic metres per hour.
    """
    m3h = Lps * 60.0 * 60.0 / 1000.0  # converting Lps to m3/h
    return m3h


def safety_margin(
    value: float, factor: float = 1.2, risk_type: str = "normal"
) -> float:
    """
    Apply a safety margin multiplier.
    """
    if risk_type == "high":
        factor *= 1.5
    elif risk_type == "low":
        factor *= 1.1
    return value * factor

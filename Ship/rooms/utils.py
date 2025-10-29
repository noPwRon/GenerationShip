"""
utils.py
---------
Shared constants and helper methods used across multiple modules.
Keep these general-purpose; avoid module-specific logic.
"""

# --- Constants ---------------------------------------------------------------
GRAVITY = 9.80665      # m/s²
AIR_DENSITY = 1.2      # kg/m³
WATER_DENSITY = 1000.0 # kg/m³
STEFAN_BOLTZMANN = 5.67e-8 # W/m²·K⁴


# --- Helper Function Placeholders --------------------------------------------
def convert_Lps_to_m3h(Lps: float) -> float:
    """
    Convert litres per second to cubic metres per hour.
    TODO: Implement numeric conversion.
    """
    pass


def safety_margin(value: float, factor: float = 1.2) -> float:
    """
    Apply a safety margin multiplier.
    TODO: Implement actual formula.
    """
    pass

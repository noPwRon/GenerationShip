"""
utils.py
---------
NOTE: This module is now a compatibility shim.

The real functionality lives under ``common/`` (see ``common.conversions`` and
``common.safety``).  Update any imports that still reference
``env.rooms.utils`` to use those modules directly, then delete this file.

TODO(common):
    [ ] Replace remaining imports of env.rooms.utils with common.conversions/common.safety.
    [ ] Remove this shim once all callers migrate.
"""

from __future__ import annotations

import warnings


# Legacy constants left in place to avoid breaking callers. Prefer the values
# defined in common.physics instead.
GRAVITY = 9.80665  # m/s^2         # TODO(common): use common.physics.STD_GRAV_ACCEL
AIR_DENSITY = 1.2  # kg/m^3        # TODO(common): use common.physics.air_density_kg_per_m3
WATER_DENSITY = 1000.0  # kg/m^3   # TODO(common): use common.physics.water_density_kg_per_m3
STEFAN_BOLTZMANN = 5.67e-8  # W/m^2/K^4  # TODO(common): use common.physics.STEFAN_BOLTZMANN


def convert_Lps_to_m3h(lps: float) -> float:
    """
    Convert litres per second to cubic metres per hour.

    TODO(common): call common.conversions.Lps_to_m3h instead of this shim.
    """

    warnings.warn(
        "env.rooms.utils.convert_Lps_to_m3h is deprecated; "
        "use common.conversions.Lps_to_m3h",
        DeprecationWarning,
        stacklevel=2,
    )
    return lps * 3.6


def safety_margin(value: float, factor: float = 1.2, risk_type: str = "normal") -> float:
    """
    Apply a simple safety margin multiplier.

    TODO(common): call common.safety.apply_margin instead of this shim.
    """

    warnings.warn(
        "env.rooms.utils.safety_margin is deprecated; use common.safety.apply_margin",
        DeprecationWarning,
        stacklevel=2,
    )

    adjustment = factor
    if risk_type == "high":
        adjustment *= 1.5
    elif risk_type == "low":
        adjustment *= 1.1
    return value * adjustment

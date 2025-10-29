"""
base.py
--------
Abstract definitions for all room types.
Defines data structures and the base interface every calculator must follow.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


# --- Data Structures ---------------------------------------------------------
@dataclass
class RoomSpec:
    """
    Input parameters describing a room before calculation.
    Extend this class as needed for new attributes.
    """

    name: str
    occupants: int
    phase: str
    floor_area_m2: float
    height_m: float = 2.6
    notes: Optional[str] = None


@dataclass
class RoomReport:
    """
    Output results of a room calculation.
    All units should remain SI unless otherwise stated.
    """

    type_id: str
    name: str
    geometry: Dict[str, float]
    mass_kg: Dict[str, float]
    electrical_kW: Dict[str, float]
    hvac: Dict[str, float]
    water_L_per_day: Dict[str, float]
    waste_L_per_day: Dict[str, float]
    safety: Dict[str, Any]
    schematics: Dict[str, str]
    metadata: Dict[str, Any]


# --- Abstract Interface ------------------------------------------------------
class RoomCalculator:
    """
    Base interface class for any room calculator.
    """

    TYPE_ID: str = "base"

    @staticmethod
    def defaults() -> RoomSpec:
        """Return default RoomSpec parameters."""
        # TODO: define in subclass
        name: str
        occupants: int
        phase: str
        floor_area_m2: float
        height_m: float = 2.6
        deck_level: int = 0
        notes: Optional[str] = None

    @staticmethod
    def compute(spec: RoomSpec) -> RoomReport:
        """Perform internal computations and return RoomReport."""
        # TODO: define in subclass
        geometry: Dict[str, float] = {
            "floor_area_m2": spec.floor_area_m2,
            "height_m": spec.height_m,
            "volume_m3": spec.floor_area_m2 * spec.height_m,
        }
        hvac: Dict[str, float] = {}

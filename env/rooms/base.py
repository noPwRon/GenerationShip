"""
base.py
--------
Abstract definitions for all room types.
Defines data structures and the base interface every calculator must follow.
"""

from dataclasses import dataclass, field
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
    geometry: Dict[str, float] = field(default_factory=dict)
    mass_kg: Dict[str, float] = field(default_factory=dict)
    electrical_kW: Dict[str, float] = field(default_factory=dict)
    hvac: Dict[str, Any] = field(default_factory=dict)
    water_L_per_day: Dict[str, float] = field(default_factory=dict)
    waste_L_per_day: Dict[str, float] = field(default_factory=dict)
    safety: Dict[str, Any] = field(default_factory=dict)
    schematics: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ReportBuilder:
    """
    Quality-of-life helper for building RoomReport objects fluently.

    Example:
        report = (
            ReportBuilder("child_dorm_8", "Child Dorm 8")
            .geom(floor_area_m2=24.0, height_m=2.6)
            .hvac(ventilation_Lps=42.0, sensible_load_kW=0.8)
            .meta(phase="children")
            .build()
        )
    """

    def __init__(self, type_id: str, name: str):
        self._r = RoomReport(type_id=type_id, name=name)

    def geom(self, **kwargs):
        """Add or update geometry entries."""
        self._r.geometry.update(kwargs)
        return self

    def hvac(self, **kwargs):
        """Add or update HVAC entries."""
        self._r.hvac.update(kwargs)
        return self

    def elec(self, **kwargs):
        """Add or update electrical entries."""
        self._r.electrical_kW.update(kwargs)
        return self

    def water(self, **kwargs):
        """Add or update water consumption entries."""
        self._r.water_L_per_day.update(kwargs)
        return self

    def waste(self, **kwargs):
        """Add or update waste entries."""
        self._r.waste_L_per_day.update(kwargs)
        return self

    def mass(self, **kwargs):
        """Add or update mass entries."""
        self._r.mass_kg.update(kwargs)
        return self

    def safety(self, **kwargs):
        """Add or update safety fields."""
        self._r.safety.update(kwargs)
        return self

    def schem(self, **kwargs):
        """Add or update schematics links."""
        self._r.schematics.update(kwargs)
        return self

    def meta(self, **kwargs):
        """Add or update metadata fields."""
        self._r.metadata.update(kwargs)
        return self

    def build(self, *, round_config: Optional[Dict[str, int]] = None) -> RoomReport:
        """
        Return the fully assembled RoomReport.

        Parameters
        ----------
        round_config : dict[str, int] | None
            Mapping of section name -> decimal places. Defaults to rounding all
            numeric sections (geometry, hvac, electrical_kW, mass_kg, water,
            waste, safety) to 2 decimals. Pass an empty dict to disable.
        """

        report = self._r
        config = (
            round_config
            if round_config is not None
            else {
                "geometry": 2,
                "hvac": 2,
                "electrical_kW": 2,
                "mass_kg": 2,
                "water_L_per_day": 2,
                "waste_L_per_day": 2,
                "safety": 2,
            }
        )

        for section_name, precision in config.items():
            if precision is None:
                continue
            section = getattr(report, section_name, None)
            if not isinstance(section, dict):
                continue
            for key, value in list(section.items()):
                if isinstance(value, float):
                    section[key] = round(value, precision)

        return report


# --- Abstract Interface ------------------------------------------------------
class RoomCalculator:
    """Base interface class for any room calculator."""

    TYPE_ID: str = "base"

    @staticmethod
    def defaults() -> RoomSpec:
        """Return default RoomSpec parameters (subclasses must override)."""

        raise NotImplementedError(
            "RoomCalculator.defaults must be implemented by subclasses"
        )

    @staticmethod
    def compute(spec: RoomSpec) -> RoomReport:
        """Perform internal computations and return RoomReport (subclasses must override)."""

        raise NotImplementedError(
            "RoomCalculator.compute must be implemented by subclasses"
        )

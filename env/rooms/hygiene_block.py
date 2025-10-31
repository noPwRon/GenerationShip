"""
hygiene_block.py
----------------
Communal hygiene module handling showers, toilets, and lockers.
"""

from __future__ import annotations

from typing import Any, Dict

from env.hvac import calc_env
from env.hvac.calc_tables import get_rates
from env.rooms.base import RoomCalculator, RoomReport, RoomSpec


class HygieneBlock(RoomCalculator):
    """Placeholder implementation for hygiene blocks."""

    TYPE_ID = "hygiene_block"

    @staticmethod
    def defaults() -> RoomSpec:
        return RoomSpec(
            name="Hygiene Block",
            occupants=12,
            phase="mixed",
            floor_area_m2=18.0,
            height_m=2.6,
        )

    @staticmethod
    def compute(spec: RoomSpec) -> RoomReport:
        rates = get_rates("hygiene_block", activity="moderate_work")

        ventilation_lps = calc_env.ventilation_rate(
            occupants=spec.occupants,
            Lps_per_person=rates["ventilation"]["Rp_Lps_per_person"],
            area_m2=spec.floor_area_m2,
            lps_per_m2=rates["ventilation"]["Ra_Lps_per_m2"],
        )
        exhaust_lps = calc_env.exhaust_rate(
            area_m2=spec.floor_area_m2, exhaust_info=rates.get("exhaust")
        )

        geometry: Dict[str, float] = {
            "floor_area_m2": spec.floor_area_m2,
            "height_m": spec.height_m,
            "volume_m3": spec.floor_area_m2 * spec.height_m,
        }
        hvac: Dict[str, Any] = {
            "ventilation_Lps": ventilation_lps,
            "exhaust_Lps": exhaust_lps,
        }
        placeholder: Dict[str, Any] = {}

        return RoomReport(
            type_id=HygieneBlock.TYPE_ID,
            name=spec.name,
            geometry=geometry,
            mass_kg=placeholder,
            electrical_kW=placeholder,
            hvac=hvac,
            water_L_per_day=placeholder,
            waste_L_per_day=placeholder,
            safety=placeholder,
            schematics={},
            metadata={"phase": spec.phase},
        )

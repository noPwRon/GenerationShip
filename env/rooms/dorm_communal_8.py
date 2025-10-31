"""
dorm_communal_8.py
-------------------
Adult communal dormitory housing eight occupants.
"""

from __future__ import annotations

from typing import Any, Dict

from env.hvac import calc_env
from env.hvac.calc_tables import get_rates
from env.rooms.base import RoomCalculator, RoomReport, RoomSpec


class DormCommunal8(RoomCalculator):
    """Skeleton dormitory calculator using shared HVAC helpers."""

    TYPE_ID = "dorm_communal_8"

    @staticmethod
    def defaults() -> RoomSpec:
        return RoomSpec(
            name="Communal Dorm 8",
            occupants=8,
            phase="adults",
            floor_area_m2=28.0,
            height_m=2.6,
        )

    @staticmethod
    def compute(spec: RoomSpec) -> RoomReport:
        rates = get_rates("dorm", activity="rest")

        ventilation_lps = calc_env.ventilation_rate(
            occupants=spec.occupants,
            Lps_per_person=rates["ventilation"]["Rp_Lps_per_person"],
            area_m2=spec.floor_area_m2,
            lps_per_m2=rates["ventilation"]["Ra_Lps_per_m2"],
        )

        sensible_kW = calc_env.metabolic_heat_kW(
            occupants=spec.occupants,
            sensible_W=rates["activity"]["sensible_W_per_person"],
        )
        latent_kW = calc_env.latent_heat_kW(
            occupants=spec.occupants,
            latent_W=rates["activity"]["latent_W_per_person"],
        )

        geometry: Dict[str, float] = {
            "floor_area_m2": spec.floor_area_m2,
            "height_m": spec.height_m,
            "volume_m3": spec.floor_area_m2 * spec.height_m,
        }
        hvac: Dict[str, Any] = {
            "ventilation_Lps": ventilation_lps,
            "sensible_load_kW": sensible_kW,
            "latent_load_kW": latent_kW,
        }

        placeholder: Dict[str, Any] = {}

        return RoomReport(
            type_id=DormCommunal8.TYPE_ID,
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


ExampleRoom = DormCommunal8

"""
intimacy_pod.py
---------------
Private intimacy pod emphasizing environmental comfort.
"""

from __future__ import annotations

from typing import Any, Dict

from env.hvac import calc_env
from env.hvac.calc_tables import get_rates
from env.rooms.base import RoomCalculator, RoomReport, RoomSpec, ReportBuilder


class IntimacyPod(RoomCalculator):
    """Placeholder calculator for the intimacy pod module."""

    TYPE_ID = "intimacy_pod"

    @staticmethod
    def defaults() -> RoomSpec:
        return RoomSpec(
            name="Intimacy Pod",
            occupants=4,
            phase="adults",
            floor_area_m2=12.0,
            height_m=2.4,
        )

    @staticmethod
    def compute(spec: RoomSpec) -> RoomReport:
        rates = get_rates("intimacy_pod", activity="moderate_work")
        ventilation_lps = calc_env.ventilation_rate(
            occupants=spec.occupants,
            Lps_per_person=rates["ventilation"]["Rp_Lps_per_person"],
            area_m2=spec.floor_area_m2,
            lps_per_m2=rates["ventilation"]["Ra_Lps_per_m2"],
        )

        report = (
            ReportBuilder(IntimacyPod.TYPE_ID, spec.name)
            .geom(
                floor_area_m2=spec.floor_area_m2,
                height_m=spec.height_m,
                volume_m3=spec.floor_area_m2 * spec.height_m,
            )
            .hvac(
                ventilation_Lps=ventilation_lps,
            )
            .meta(phase=spec.phase)
            .build()
        )

        return report

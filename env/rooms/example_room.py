"""
example_room.py
----------------
Template for creating a new room type.

Usage
-----
1. Copy this file and rename it to match your room type (e.g. 'agriculture_bay.py').
2. Update TYPE_ID and the class name.
3. Fill in the TODOs to define:
   • default RoomSpec values
   • how to compute HVAC, power, water, etc.
   • what fields to include in the RoomReport

Notes
-----
• Always keep units SI unless clearly documented.
• Only populate the fields that matter for this room type.
• Return a full RoomReport object (using ReportBuilder for convenience).
"""

from __future__ import annotations
from typing import Any, Dict

# TODO: adjust imports as needed for your calculations
from env.hvac import calc_env
from env.hvac.calc_tables import get_rates
from env.rooms.base import RoomCalculator, RoomSpec, RoomReport, ReportBuilder


class ExampleRoom(RoomCalculator):
    """Template for a new room calculator."""

    # TODO: Change this to match your new room identifier
    TYPE_ID = "example_room"

    # ------------------------------------------------------------------
    # Default parameters
    # ------------------------------------------------------------------
    @staticmethod
    def defaults() -> RoomSpec:
        """
        Define default geometry, occupancy, and phase for this room type.
        TODO: replace placeholder values with realistic defaults.
        """
        return RoomSpec(
            name="Example Room",
            occupants=1,
            phase="general",
            floor_area_m2=10.0,
            height_m=2.6,
        )

    # ------------------------------------------------------------------
    # Core computation
    # ------------------------------------------------------------------
    @staticmethod
    def compute(spec: RoomSpec) -> RoomReport:
        """
        Perform all calculations for this room.

        TODO:
        [ ] Replace 'example' activity with a relevant one.
        [ ] Add equipment or water logic if needed.
        [ ] Only populate fields that matter for this space.
        """

        # --- 1) Lookup rates ---------------------------------------------------
        # TODO: adjust the table key ("example") and activity
        rates = get_rates("example", activity="rest")

        # --- 2) Compute HVAC requirements -------------------------------------
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

        # --- 3) Geometry -------------------------------------------------------
        volume_m3 = spec.floor_area_m2 * spec.height_m

        # --- 4) Assemble the report -------------------------------------------
        # TODO: Add/remove sections as needed for this room
        report = (
            ReportBuilder(ExampleRoom.TYPE_ID, spec.name)
            .geom(
                floor_area_m2=spec.floor_area_m2,
                height_m=spec.height_m,
                volume_m3=volume_m3,
            )
            .hvac(
                ventilation_Lps=ventilation_lps,
                sensible_load_kW=sensible_kW,
                latent_load_kW=latent_kW,
                # TODO: add supply/exhaust split or additional HVAC fields
            )
            # .elec(total_kW=...)       # TODO: add electrical loads if needed
            # .water(hot_L_per_day=...) # TODO: add water use
            # .waste(...)               # TODO: add waste streams
            # .safety(...)              # TODO: add safety notes or metrics
            .meta(phase=spec.phase)
            .build()
        )

        return report


# Optional alias for backward compatibility or registry import convenience
example_room = ExampleRoom

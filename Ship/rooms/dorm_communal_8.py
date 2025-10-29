"""
dorm_communal_8.py
------------------
Communal dormitory for 8 occupants.

Responsibilities:
    - Determine geometry, air, heat, water, and safety parameters.
    - Interface with calc_env for environmental calculations.
"""

from Ship.rooms.base import RoomSpec, RoomReport, RoomCalculator
from Ship.rooms import calc_env


class DormCommunal8(RoomCalculator):
    TYPE_ID = "dorm_communal_8"

    @staticmethod
    def defaults() -> RoomSpec:
        """
        Return default parameters for an 8-person dormitory.
        Example values: area, height, occupancy phase.
        """
        # TODO: define defaults
        pass

    @staticmethod
    def compute(spec: RoomSpec) -> RoomReport:
        """
        Perform calculations for the dormitory environment and systems.

        Steps:
            1. Determine geometry (volume, floor area).
            2. Calculate ventilation requirements.
            3. Estimate sensible and latent heat loads.
            4. Compute water and waste usage.
            5. Assemble data into a RoomReport.

        TODO: Implement actual logic.
        """
        pass

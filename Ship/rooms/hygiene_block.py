"""
hygiene_block.py
----------------
Communal hygiene facility handling showers and waste.
High ventilation and hot-water demand zone.
"""

from Ship.rooms.base import RoomSpec, RoomReport, RoomCalculator


class HygieneBlock(RoomCalculator):
    TYPE_ID = "hygiene_block"

    @staticmethod
    def defaults() -> RoomSpec:
        """Define default values for a hygiene block."""
        # TODO: implement
        pass

    @staticmethod
    def compute(spec: RoomSpec) -> RoomReport:
        """
        Compute environmental and utility data for the hygiene block.

        Considerations:
            - Hot water production per occupant
            - Greywater generation
            - Ventilation rate for humidity removal
            - Structural and fixture mass

        TODO: implement calculations.
        """
        pass

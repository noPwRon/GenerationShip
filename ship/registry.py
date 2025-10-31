"""
registry.py
------------
Central registry for all room calculators aboard the Generation Ship.

Responsibilities:
    • Maintain a dictionary mapping type_id → room calculator class.
    • Provide a single compute() interface for querying room models.
    • Support modular expansion as new room modules are created.
"""

from typing import Dict, Type

# Import core definitions
from Ship.rooms.base import RoomCalculator, RoomSpec, RoomReport

# Import known room calculators
from Ship.rooms.child_dorm_8 import child_dorm_8
from Ship.rooms.hygiene_block import HygieneBlock
from Ship.rooms.intimacy_pod import IntimacyPod


# --- Registry of room modules ------------------------------------------------
REGISTRY: Dict[str, Type[RoomCalculator]] = {
    child_dorm_8.TYPE_ID: child_dorm_8,
    HygieneBlock.TYPE_ID: HygieneBlock,
    IntimacyPod.TYPE_ID: IntimacyPod,
}


# --- Accessor Interface ------------------------------------------------------
def compute(type_id: str, **kwargs) -> RoomReport:
    """
    Retrieve the appropriate room calculator and return a computed report.

    Steps:
        1. Look up the calculator class by its type_id.
        2. Obtain default parameters using .defaults().
        3. Apply any overrides passed in **kwargs.
        4. Execute its .compute() method and return the RoomReport.

    TODO:
        - Add exception handling for unknown type_ids.
        - Add logging for traceability.
    """
    # 1. Fetch the class from registry
    calc_cls = REGISTRY[type_id]

    # 2. Build a default spec
    spec = calc_cls.defaults()

    # 3. Apply user overrides
    for k, v in kwargs.items():
        if hasattr(spec, k):
            setattr(spec, k, v)

    # 4. Compute the final report
    return calc_cls.compute(spec)

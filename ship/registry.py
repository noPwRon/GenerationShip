"""
registry.py
------------
Central registry for all room calculators aboard the Generation Ship.
"""

from __future__ import annotations

from typing import Dict, Type

from env.rooms.base import RoomCalculator, RoomReport, RoomSpec
from env.rooms.child_dorm_8 import ChildDorm8
from env.rooms.dorm_communal_8 import DormCommunal8
from env.rooms.hygiene_block import HygieneBlock
from env.rooms.intimacy_pod import IntimacyPod


REGISTRY: Dict[str, Type[RoomCalculator]] = {
    ChildDorm8.TYPE_ID: ChildDorm8,
    DormCommunal8.TYPE_ID: DormCommunal8,
    HygieneBlock.TYPE_ID: HygieneBlock,
    IntimacyPod.TYPE_ID: IntimacyPod,
}


def compute(type_id: str, **overrides) -> RoomReport:
    """Retrieve the appropriate room calculator and return a computed report."""

    try:
        calc_cls = REGISTRY[type_id]
    except KeyError as exc:
        known = ", ".join(sorted(REGISTRY))
        raise KeyError(f"Unknown room type '{type_id}'. Known types: {known}") from exc

    spec = calc_cls.defaults()

    for key, value in overrides.items():
        if hasattr(spec, key):
            setattr(spec, key, value)

    return calc_cls.compute(spec)
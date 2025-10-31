"""
registry.py
------------
Central registry for all room calculators aboard the Generation Ship.
"""

from __future__ import annotations
from typing import Dict, Type, Iterable

from env.rooms.base import RoomCalculator, RoomReport, RoomSpec
from env.rooms.child_dorm_8 import ChildDorm8
from env.rooms.dorm_communal_8 import DormCommunal8
from env.rooms.hygiene_block import HygieneBlock
from env.rooms.intimacy_pod import IntimacyPod
from env.rooms.warehouse import Warehouse


# Canonical map: type_id -> calculator class
REGISTRY: Dict[str, Type[RoomCalculator]] = {
    ChildDorm8.TYPE_ID: ChildDorm8,
    DormCommunal8.TYPE_ID: DormCommunal8,
    HygieneBlock.TYPE_ID: HygieneBlock,
    IntimacyPod.TYPE_ID: IntimacyPod,
    Warehouse.TYPE_ID: Warehouse,
}


def list_types() -> Iterable[str]:
    """Return known room type identifiers (sorted)."""
    # TODO: expose richer metadata if needed (docstrings, defaults preview)
    return sorted(REGISTRY.keys())


def compute(type_id: str, **overrides) -> RoomReport:
    """
    Retrieve the appropriate room calculator and return a computed report.

    Notes
    -----
    - Overrides are applied directly to the RoomSpec returned by `defaults()`.
    - Unknown override keys are ignored by default (see TODO below).

    TODO:
    [ ] Add strict=True flag to raise on unknown override keys.
    [ ] Optionally validate units/types for critical fields.
    """
    try:
        calc_cls = REGISTRY[type_id]
    except KeyError as exc:
        known = ", ".join(sorted(REGISTRY))
        raise KeyError(f"Unknown room type '{type_id}'. Known types: {known}") from exc

    spec: RoomSpec = calc_cls.defaults()  # expects a fresh instance each call

    # Apply overrides (only for attributes present on RoomSpec)
    # TODO: strict mode -> raise on unknown keys instead of ignore
    for key, value in overrides.items():
        if hasattr(spec, key):
            setattr(spec, key, value)
        # else: silently ignore; see TODO above

    return calc_cls.compute(spec)

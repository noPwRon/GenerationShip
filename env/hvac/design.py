"""
design.py
----------
Utilities for loading and interpreting HVAC design data.
"""

from __future__ import annotations

from typing import Dict, Any, Optional

from data.loader import load_hvac_design
from env.hvac.constants import (
    EXHAUST_KEYS,
    DEFAULT_ACTIVITY_LEVELS,
    DEFAULT_VENTILATION,
)


def validate_exhaust_keys(exhaust_dict: Dict[str, Any]) -> None:
    """Ensure exhaust definitions only use supported keys."""

    for key in exhaust_dict.keys():
        if key not in EXHAUST_KEYS:
            raise KeyError(f"Unknown exhaust key '{key}'. Valid keys: {EXHAUST_KEYS}")


def get_hvac_design(*, force_reload: bool = False) -> Dict[str, Any]:
    """Load the canonical hvac_design.yaml document."""

    cfg = load_hvac_design(force_reload=force_reload)
    if "rooms" not in cfg:
        raise KeyError("hvac_design.yaml is missing required 'rooms' section.")
    if "defaults" not in cfg:
        raise KeyError("hvac_design.yaml is missing required 'defaults' section.")
    return cfg


def resolve_room_activity(
    cfg: Dict[str, Any], room_type: str, activity: Optional[str] = None
) -> Dict[str, Any]:
    """
    Merge defaults and room-specific overrides into a unified rate dictionary.
    """

    rooms = cfg.get("rooms", {})
    if room_type not in rooms:
        raise KeyError(f"Room type '{room_type}' is not defined in hvac_design.yaml.")

    room_cfg = rooms[room_type]
    defaults = cfg.get("defaults", {})

    activity_levels = defaults.get("activity_levels", DEFAULT_ACTIVITY_LEVELS)
    ventilation_defaults = defaults.get("ventilation", DEFAULT_VENTILATION)

    # Determine which activity map to use
    room_activity_map = room_cfg.get("activity_map", {})
    if activity is None:
        if room_activity_map:
            activity = next(iter(room_activity_map))
        elif activity_levels:
            activity = next(iter(activity_levels))
        else:
            raise ValueError(f"No activity levels defined for room '{room_type}'.")

    activity_defaults = activity_levels.get(activity, {})
    activity_overrides = room_activity_map.get(activity, {})
    activity_final = {**activity_defaults, **activity_overrides}

    ventilation_overrides = room_cfg.get("ventilation", {})
    ventilation_final = {**ventilation_defaults, **ventilation_overrides}

    result: Dict[str, Any] = {
        "activity": activity_final,
        "ventilation": ventilation_final,
    }

    exhaust = room_cfg.get("exhaust")
    if exhaust:
        validate_exhaust_keys(exhaust)
        result["exhaust"] = exhaust

    return result

"""
calc_tables.py
---------------
Convenience helpers that expose HVAC rates for room calculators.
"""

from __future__ import annotations

from typing import Dict, Any, Optional

from env.hvac.design import get_hvac_design, resolve_room_activity

_CACHED_CONFIG: Optional[Dict[str, Any]] = None


def _load_cached_config(force_reload: bool = False) -> Dict[str, Any]:
    """Load and cache the HVAC design configuration."""

    global _CACHED_CONFIG
    if _CACHED_CONFIG is None or force_reload:
        _CACHED_CONFIG = get_hvac_design(force_reload=force_reload)
    return _CACHED_CONFIG


def get_rates(room_type: str, activity: Optional[str] = None) -> Dict[str, Any]:
    """
    Return sensible/latent/ventilation data for a given room type and activity.
    """

    cfg = _load_cached_config()
    return resolve_room_activity(cfg, room_type, activity)


def list_available_rooms(force_reload: bool = False) -> Dict[str, Any]:
    """
    Return a summary of rooms and their declared activity keys.
    """

    cfg = _load_cached_config(force_reload=force_reload)
    rooms = cfg.get("rooms", {})
    summary: Dict[str, Any] = {}
    for room_id, room_cfg in rooms.items():
        activity_map = room_cfg.get("activity_map", {})
        summary[room_id] = list(activity_map.keys())
    return summary

"""
calc_tables.py
---------------
High-level bridge between room computations and configuration data.

Each room can call:
    from Ship.rooms.calc_tables import get_rates
    rates = get_rates("dorm", "rest")

Returned dict shape:
    {
        "activity": {
            "sensible_W_per_person": float,
            "latent_W_per_person": float
        },
        "ventilation": {
            "Rp_Lps_per_person": float,
            "Ra_Lps_per_m2": float
        },
        # optional key if present in YAML
        "exhaust": {
            ...
        }
    }

This keeps YAML details and loader logic out of compute() methods.
"""

from typing import Dict, Any, Optional

# We import the config tools one level up
from Ship.config.hvac_config import get_hvac_design, resolve_room_activity


# ---------------
# Module level cache variable
# ---------------
_cached_config: Optional[Dict[str, Any]] = None


def _load_cached_config(force_reload: bool = False) -> Dict[str, Any]:
    """
    Load and cache the HVAC design configuration.
    """
    global _cached_config
    if _cached_config is None or force_reload:
        _cached_config = get_hvac_design()
    return _cached_config


def get_rates(room_type: str, activity: str) -> Dict[str, Any]:
    """
    Return sensible/latent/ventilation data for a given room type and activity.
    TODO:
        - call get_hvac_design()
        - call resolve_room_activity(cfg, room_type, activity)
        - (optional) cache the YAML data so it isn’t reloaded each time
    """
    # Example placeholder structure for your implementation:
    cfg = _load_cached_config(force_reload=True)
    rates = resolve_room_activity(cfg, room_type, activity)
    return rates


# Optional helper
def list_available_rooms(force_reload: bool = False) -> Dict[str, Any]:
    """
    Return a list or dict of all available room types and their activity keys
    from hvac_design.yaml. Useful for debugging or UI menus.

    TODO:
        - Load cfg via get_hvac_design()
        - Return keys(cfg['rooms']) and nested keys of 'activity_map'
    """
    cfg = _load_cached_config(force_reload=force_reload)
    rooms = cfg.get("rooms", {})
    summary = {room: list(activity.keys()) for room, activity in rooms.items()}
    return summary

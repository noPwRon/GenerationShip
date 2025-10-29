"""
hvac_config.py
---------------
HVAC configuration façade for the Generation Ship.
Replaces the old load_config.py.

Purpose:
    - Load and cache hvac_design.yaml
    - Merge default + room-specific HVAC data
    - Provide lookup helpers for activity/ventilation/exhaust data

Dependencies:
    - cache_config.py for generic YAML caching
"""

from typing import Dict, Any
from Ship.config.cache_config import get_yaml_config
from Ship.config.constants import EXHAUST_KEYS


def validate_exhaust_keys(exhaust_dict: Dict[str, Any]) -> None:
    for k in exhaust_dict.keys():
        if k not in EXHAUST_KEYS:
            raise KeyError(f"Unknown exhaust key '{k}' — check constants.EXHAUST_KEYS.")


def get_hvac_design(*, force_reload: bool = False) -> Dict[str, Any]:
    """
    Load hvac_design.yaml using the shared YAML cache.

    Parameters
    ----------
    force_reload : bool
        If True, re-reads from disk even if cached.

    Returns
    -------
    Dict[str, Any]
        Parsed configuration dictionary.

    TODO:
        - Call get_yaml_config("hvac_design.yaml", force_reload=force_reload)
        - (Optional) Validate presence of keys like 'defaults' and 'rooms'
    """
    hvac_design = get_yaml_config("hvac_design.yaml", force_reload=force_reload)

    # ensure hvac_design has required structure

    rooms = hvac_design.get("rooms", {})
    defaults = hvac_design.get("defaults", {})
    exhausts = hvac_design.get("exhausts", {})

    if not rooms:
        raise KeyError("hvac_design.yaml missing required 'rooms' section.")
    if not defaults:
        raise KeyError("hvac_design.yaml missing required 'defaults' section.")
    if exhausts:
        validate_exhaust_keys(exhausts)

    return hvac_design


def resolve_room_activity(
    cfg: Dict[str, Any], room_type: str, activity: str | None = None
) -> Dict[str, Any]:
    """
    Merge defaults and room-specific overrides into a unified rate dictionary.

    Parameters
    ----------
    cfg : Dict[str, Any]
        Full hvac_design configuration dictionary.
    room_type : str
        e.g., "dorm", "lab", "mess_hall"
    activity : str
        Activity level key, e.g., "rest", "light_work"

    Returns
    -------
    Dict[str, Any]
        {
          "activity":   {"sensible_W_per_person": ..., "latent_W_per_person": ...},
          "ventilation":{"Rp_Lps_per_person": ..., "Ra_Lps_per_m2": ...},
          "exhaust":    {...?}
        }

    TODO:
        - Start from cfg["defaults"]
        - Merge activity_levels[activity] + ventilation defaults
        - Apply room_type overrides (activity_map + ventilation + exhaust)
        - Return the merged dict
    """
    # TODO: implement

    # activity_defaults = cfg["defaults"]["activity_levels"][activity]
    # ventilation_defaults = cfg["defaults"]["ventilation"]
    # room_type = cfg["rooms"][room_type]

    #  --- 0) Get relevant sections safely
    cfg_room = cfg.get("rooms", {}).get(room_type, {})
    cfg_defaults = cfg.get("defaults", {})

    if activity is None:
        room_acts = list(cfg_room.get("activity_map", {}).keys())
        if room_acts:
            activity = room_acts[0]
        else:
            # fallback to global default
            default_acts = cfg_defaults.get("activity_levels", {})
            if default_acts:
                activity = default_acts[0]
            else:
                raise ValueError(f"No activity levels defined for room '{room_type}'.")

    act_defaults = cfg_defaults.get("activity_levels", {})
    vent_defaults = cfg_defaults.get("ventilation", {})

    # --- 1) room-level overrides (may be missing)
    room_activity_map = cfg_room.get("activity_map", {})
    room_ventilation = cfg_room.get("ventilation", {})
    room_exhaust = cfg_room.get("exhaust", None)

    # --- 2) Merge defaults + room overrides

    activity_final = {**act_defaults, **room_activity_map}
    ventilation_final = {**vent_defaults, **room_ventilation}

    # --- 3) Assemble result (include 'exhaust' only if present)

    result: Dict[str, Any] = {
        "activity": activity_final,
        "ventilation": ventilation_final,
    }
    if room_exhaust:
        result["exhaust"] = room_exhaust  # typically no defaults; straight pass-through

    # TODO
    # --- 4) (Optional) sanity checks / friendly errors
    # e.g., ensure required keys exist after merge
    # for key in ("sensible_W_per_person", "latent_W_per_person"):
    #     if key not in result["activity"]:
    #         raise ValueError(f"Missing activity key: {key} for {room_type}/{activity}")

    return result

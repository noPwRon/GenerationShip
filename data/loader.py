"""
loader.py
---------
Utility helpers for loading structured data sets from the repo.
"""

from __future__ import annotations

from typing import Dict, Any

from data.cache import get_yaml_config


def load_equipment_catalog(*, force_reload: bool = False) -> Dict[str, Any]:
    """
    Load the canonical equipment specification table.
    """

    return get_yaml_config("specs/equipment_specs.yaml", force_reload=force_reload)


def load_hvac_design(*, force_reload: bool = False) -> Dict[str, Any]:
    """Shortcut helper used by HVAC modules."""

    return get_yaml_config("specs/hvac_design.yaml", force_reload=force_reload)


def load_power_design(*, force_reload: bool = False) -> Dict[str, Any]:
    """Shortcut helper used by power modules."""

    return get_yaml_config("specs/power_design.yaml", force_reload=force_reload)


def load_materials(*, force_reload: bool = False) -> Dict[str, Any]:
    """Load materials library for thermal analysis."""

    return get_yaml_config("specs/materials.yaml", force_reload=force_reload)

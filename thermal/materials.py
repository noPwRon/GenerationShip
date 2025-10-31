"""
materials.py
-------------
Helpers for working with material property tables.
"""

from __future__ import annotations

from typing import Dict, Any

from data.loader import load_materials


def get_materials(*, force_reload: bool = False) -> Dict[str, Any]:
    """Load the materials library."""

    return load_materials(force_reload=force_reload)


def get_material_properties(cfg: Dict[str, Any], material_id: str) -> Dict[str, Any]:
    """Return the property dictionary for a given material ID."""

    materials = cfg.get("materials", {})
    if material_id not in materials:
        known = ", ".join(sorted(materials))
        raise KeyError(f"Material '{material_id}' not found. Known: {known}")
    return materials[material_id]

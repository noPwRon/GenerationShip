"""
materials_config.py
--------------------
Material and mass-property configuration façade.

Purpose:
    - Load and cache materials.yaml
    - Provide lookup helpers for density, thermal, and structural data
"""

from typing import Dict, Any
from Ship.config.cache_config import get_yaml_config


def get_materials(*, force_reload: bool = False) -> Dict[str, Any]:
    """
    Load materials.yaml using the shared YAML cache.

    Parameters
    ----------
    force_reload : bool
        Re-read from disk if True.

    Returns
    -------
    Dict[str, Any]
        Parsed configuration dictionary.

    TODO:
        - Call get_yaml_config("materials.yaml", force_reload=force_reload)
        - (Optional) Validate presence of keys like 'materials'
    """
    # TODO: implement
    materials = get_yaml_config("materials.yaml", force_reload=force_reload)

    props = materials.get("materials", {})
    for mat_id, mat_data in props.items():
        if "density_kg_per_m3" not in mat_data:
            raise KeyError(f"Material '{mat_id}' missing 'density_kg_per_m3' key.")

    return materials


def get_material_properties(cfg: Dict[str, Any], material_id: str) -> Dict[str, Any]:
    """
    Return the property dictionary for a given material ID.

    Parameters
    ----------
    cfg : Dict[str, Any]
        Full materials configuration.
    material_id : str
        Material key (e.g., 'aluminum_alloy_6061')

    Returns
    -------
    Dict[str, Any]
        Property map for the selected material.

    TODO:
        - Read cfg["materials"][material_id]
        - Handle missing keys gracefully
    """
    # TODO: implement
    raise NotImplementedError(
        "Implement get_material_properties() for material lookup."
    )

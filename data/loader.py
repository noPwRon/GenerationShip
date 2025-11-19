"""
loader.py
---------
Utility helpers for loading structured data sets from the repo.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping

from data.cache import get_yaml_config

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - defensive guard
    yaml = None  # type: ignore

_DATA_ROOT = Path(__file__).resolve().parent
_REPO_ROOT = _DATA_ROOT.parent


def load_equipment_catalog(
    *, path: str | Path = "specs/equipment_specs.yaml", force_reload: bool = False
) -> Dict[str, Any]:
    """
    Load the canonical equipment specification table.
    """

    return load_yaml(path, force_reload=force_reload)


def load_hvac_design(
    *, path: str | Path = "specs/hvac_design.yaml", force_reload: bool = False
) -> Dict[str, Any]:
    """Shortcut helper used by HVAC modules."""

    return load_yaml(path, force_reload=force_reload)


def load_power_design(
    *, path: str | Path = "specs/power_design.yaml", force_reload: bool = False
) -> Dict[str, Any]:
    """Shortcut helper used by power modules."""

    return load_yaml(path, force_reload=force_reload)


def load_materials(
    *, path: str | Path = _DATA_ROOT / "specs/materials.yaml", force_reload: bool = False
) -> Dict[str, Any]:
    """Load combined materials library for structural, thermal, and shielding uses."""

    return load_yaml(path, force_reload=force_reload)


def load_yaml(name_or_path: str | Path, *, force_reload: bool = False) -> Dict[str, Any]:
    """Generic YAML loader that shares the cache used by domain helpers."""

    return get_yaml_config(str(name_or_path), force_reload=force_reload)


def _resolve_output_path(name_or_path: str | Path) -> Path:
    """Resolve output path relative to repo/data roots, allowing simple keys."""

    candidate = Path(name_or_path)
    if candidate.is_absolute():
        return candidate
    if candidate.parts:
        head = candidate.parts[0]
        if head in {"data", "configs"}:
            return _REPO_ROOT / candidate
        if head in {"specs", "schemas"}:
            return _DATA_ROOT / candidate
    return _DATA_ROOT / candidate


def dump_yaml(name_or_path: str | Path, data: Mapping[str, Any]) -> None:
    """Write mapping data to YAML, creating directories as needed."""

    if yaml is None:
        raise ImportError(
            "PyYAML library is required to dump YAML files. Please install it."
        )

    target = _resolve_output_path(name_or_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(dict(data), handle, sort_keys=False)


def merge_dicts(base: Mapping[str, Any], override: Mapping[str, Any]) -> Dict[str, Any]:
    """Deep-merge two mappings without mutating inputs."""

    merged: Dict[str, Any] = dict(base)
    for key, value in override.items():
        if key in merged:
            existing = merged[key]
            if isinstance(existing, dict) and isinstance(value, dict):
                merged[key] = merge_dicts(existing, value)
                continue
        merged[key] = value
    return merged

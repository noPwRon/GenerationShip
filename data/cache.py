"""
cache.py
--------
Generic YAML caching utility for the Generation Ship simulation.

This module provides a single in-memory cache for all YAML datasets that live
under `data/specs/`, `data/schemas/`, or the runtime `configs/` tree.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - defensive guard
    yaml = None  # type: ignore


_CONFIG_CACHE: Dict[Path, Dict[str, Any]] = {}

_DATA_ROOT = Path(__file__).resolve().parent
_REPO_ROOT = _DATA_ROOT.parent
_SEARCH_ROOTS = [
    _DATA_ROOT,
    _DATA_ROOT / "specs",
    _DATA_ROOT / "schemas",
    _REPO_ROOT / "configs",
]


def _resolve_yaml_path(name_or_path: str) -> Path:
    """Resolve a filename or relative path to a YAML file within the repo."""

    candidate = Path(name_or_path)
    if candidate.is_absolute():
        if not candidate.exists():
            raise FileNotFoundError(f"YAML file not found: {candidate}")
        return candidate

    for root in _SEARCH_ROOTS:
        resolved = root / candidate
        if resolved.exists():
            return resolved

    searched = ", ".join(str(root) for root in _SEARCH_ROOTS)
    raise FileNotFoundError(
        f"Could not locate YAML file '{name_or_path}'. Searched: {searched}"
    )


def _load_yaml_file(path: Path) -> Dict[str, Any]:
    """Read and parse a YAML file into a dictionary."""

    if yaml is None:
        raise ImportError(
            "PyYAML library is required to load YAML files. Please install it."
        )

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if not isinstance(data, dict):
        raise ValueError(f"YAML file {path} did not parse into a dictionary.")

    return data


def get_yaml_config(name_or_path: str, *, force_reload: bool = False) -> Dict[str, Any]:
    """Retrieve (and cache) a YAML configuration as a dictionary."""

    path = _resolve_yaml_path(name_or_path)
    if force_reload or path not in _CONFIG_CACHE:
        _CONFIG_CACHE[path] = _load_yaml_file(path)
    return _CONFIG_CACHE[path]


def clear_cache() -> Dict[str, int]:
    """Clear cached YAML data and report how many entries were purged."""

    purged = len(_CONFIG_CACHE)
    _CONFIG_CACHE.clear()
    return {"cleared_items": purged}


def list_cached_files() -> Dict[str, int]:
    """List cached YAML files and the number of top-level keys for each."""

    summary: Dict[str, int] = {}
    for cache_path, data in _CONFIG_CACHE.items():
        summary[str(cache_path)] = len(data) if isinstance(data, dict) else 0
    return summary

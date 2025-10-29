"""
cache_config.py
----------------
Generic YAML caching utility for the Generation Ship simulation.

Purpose:
    Provides a single in-memory cache for all configuration YAML files
    (e.g., hvac_design.yaml, power_design.yaml, materials.yaml).
    This prevents repeated disk reads and keeps all design data synchronized
    during runtime.

Usage Example:
    from Ship.config.cache_config import get_yaml_config

    hvac = get_yaml_config("hvac_design.yaml")
    materials = get_yaml_config("materials.yaml")

Design Notes:
    - Caches YAML documents in a module-level dictionary.
    - Keyed by absolute Path to avoid name collisions.
    - Optionally supports force_reload to re-read files.
    - Keeps IO separate from specific schema validation.
"""

from pathlib import Path
from typing import Dict, Any, Optional

# ---------------------------------------------------------------------------
# Optional dependency: PyYAML (add to your environment later)
# ---------------------------------------------------------------------------
try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # TODO: handle missing library gracefully

# ---------------------------------------------------------------------------
# Module-level cache
#   _CONFIG_CACHE holds { Path: dict }
# ---------------------------------------------------------------------------
_CONFIG_CACHE: Dict[Path, Dict[str, Any]] = {}

# Base directory for configs (same folder as this file)
_BASE_DIR = Path(__file__).parent


def _resolve_yaml_path(name_or_path: str) -> Path:
    """
    Resolve a filename or absolute path to a valid YAML file under /config/.

    Parameters
    ----------
    name_or_path : str
        File name (e.g., 'hvac_design.yaml') or absolute path.

    Returns
    -------
    Path
        Absolute path to an existing YAML file.

    TODO:
        - If name_or_path is absolute, verify file exists and return Path.
        - Otherwise, join with _BASE_DIR.
        - Raise FileNotFoundError if the file does not exist.
    """
    path = Path(name_or_path)
    if path.is_absolute():
        if path.exists():
            return path
        else:
            raise FileNotFoundError(f"YAML file not found: {path}")
    local_path = _BASE_DIR / path
    if local_path.exists():
        return local_path

    raise FileNotFoundError(f"YAML file not found @ {local_path} or {path}")


def _load_yaml_file(path: Path) -> Dict[str, Any]:
    """
    Read and parse a YAML file into a dictionary.

    Parameters
    ----------
    path : Path
        Absolute path to the YAML file.

    Returns
    -------
    Dict[str, Any]
        Parsed contents of the YAML file.

    TODO:
        - Open the file using UTF-8 encoding.
        - If yaml is None, raise ImportError with helpful message.
        - Use yaml.safe_load().
        - Return the resulting dict.
        - Handle exceptions (FileNotFoundError, yaml.YAMLError).
    """

    if yaml is None:
        raise ImportError(
            "PyYAML library is required to load YAML files. Please install it."
        )

    summary: Dict[str, Any] = {}

    try:
        with path.open("r", encoding="utf-8") as f:
            summary = yaml.safe_load(f)
            if not isinstance(summary, dict):
                raise ValueError(f"YAML file {path} did not parse to a dictionary.")
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {path}: {e}")

    return summary


def get_yaml_config(name_or_path: str, *, force_reload: bool = False) -> Dict[str, Any]:
    """
    Retrieve (and cache) a YAML configuration as a Python dictionary.

    Parameters
    ----------
    name_or_path : str
        Filename or path to the YAML file.
    force_reload : bool, optional
        If True, reload the file from disk even if cached.

    Returns
    -------
    Dict[str, Any]
        Parsed YAML contents.

    TODO:
        - Resolve absolute Path via _resolve_yaml_path().
        - If force_reload or not cached:
            * Call _load_yaml_file(path)
            * Store dict in _CONFIG_CACHE[path]
        - Return _CONFIG_CACHE[path]
    """

    path: Path = _resolve_yaml_path(name_or_path)
    loaded_path: Dict[str, Any] = _load_yaml_file(path)
    if force_reload or path not in _CONFIG_CACHE:
        _CONFIG_CACHE[path] = loaded_path
    return _CONFIG_CACHE[path]


def clear_cache() -> None:
    """
    Clear all cached YAML data from memory.
    Useful for testing or live reload scenarios.

    TODO:
        - Call _CONFIG_CACHE.clear()
        - Optionally return number of cleared items or log action.
    """

    num_items = len(_CONFIG_CACHE)
    _CONFIG_CACHE.clear()
    return {"cleared_items": num_items}


def list_cached_files() -> Dict[str, int]:
    """
    Utility: List currently cached YAML files and their sizes (in keys count).

    Returns
    -------
    Dict[str, int]
        Mapping of filename → number of top-level keys in the cached dict.

    TODO:
        - Iterate _CONFIG_CACHE items.
        - For each path, compute len(value) if dict.
        - Return summary dictionary.
    """

    summary: Dict[str, int] = {}
    for cache_path, data in _CONFIG_CACHE.items():
        if isinstance(data, dict):
            size = len(data)
        else:
            size = 0
        summary[str(cache_path)] = size
    return summary

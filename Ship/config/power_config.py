"""
power_config.py
----------------
Power generation and distribution configuration façade.

Purpose:
    - Load and cache power_design.yaml
    - Provide simple accessors for generation, storage, and load data
"""

from typing import Dict, Any
from Ship.config.cache_config import get_yaml_config


def get_power_design(*, force_reload: bool = False) -> Dict[str, Any]:
    """
    Load power_design.yaml using the shared YAML cache.

    Parameters
    ----------
    force_reload : bool
        Force re-read from disk if True.

    Returns
    -------
    Dict[str, Any]
        Parsed configuration dictionary.

    TODO:
        - Call get_yaml_config("power_design.yaml", force_reload=force_reload)
        - Validate presence of keys like 'sources', 'sinks'
    """

    cfg = get_yaml_config("power_design.yaml", force_reload=force_reload)

    # Ensure all sources and sinks have required keys

    power_sources = cfg.get("sources", {})
    for name, source in power_sources.items():
        if "type" not in source:
            raise KeyError(f"Power source '{name}' missing a type")

    # power_sinks = cfg.get("sinks", {})
    # for name, sink in power_sinks.items():
    #     if "consumption_kW" not in sink:
    #         raise KeyError(f"Power sink '{name}' missing required keys.")
    return cfg


def summarize_power(cfg: Dict[str, Any]) -> Dict[str, float]:
    """
    Utility: return a summary of all generation sinks and sources (kW) from cfg.

    Parameters
    ----------
    cfg : Dict[str, Any]
        Parsed power design dictionary.

    Returns
    -------
    Dict[str, float]
        Two dicts: (power_source, power_sink)
        Each maps source/sink names to their kW values.

    TODO:
        - Extract from cfg["sources"]
        - Handle missing or malformed entries gracefully
    """
    # TODO: implement
    power_source: Dict[str, float] = {}
    sources = cfg.get("sources", {})

    power_sink: Dict[str, float] = {}
    sinks = cfg.get("sinks", {})

    # for src_name, src_info in sources.items():
    #     gen_kw = src_info.get("generation_kW", 0.0)
    #     power_source[src_name] = gen_kw

    # for sink_name, sink_info in sinks.items():
    #     cons_kw = sink_info.get("consumption_kW", 0.0)
    #     power_sink[sink_name] = cons_kw

    return power_source, power_sink


def get_total_generation(cfg: Dict[str, Any]) -> float:
    """Sum generation_kW of all active sources."""


def get_total_consumption(cfg: Dict[str, Any]) -> float:
    """Sum all sink consumption_kW (+ area/person scaled sinks)."""


def power_balance(cfg: Dict[str, Any]) -> float:
    """Return net available power (generation - consumption)."""

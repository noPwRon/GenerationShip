"""
bus.py
-------
Convenience helpers for the power distribution model.
"""

from __future__ import annotations

from typing import Dict, Any, Tuple

from data.loader import load_power_design


def get_power_design(*, force_reload: bool = False) -> Dict[str, Any]:
    """Load the canonical power_design.yaml document."""

    return load_power_design(force_reload=force_reload)


def summarize_power(cfg: Dict[str, Any]) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Return total generation and consumption per source/sink.
    """

    sources_summary: Dict[str, float] = {}
    sinks_summary: Dict[str, float] = {}

    for name, source in cfg.get("sources", {}).items():
        sources_summary[name] = float(source.get("generation_kW", 0.0))

    for name, sink in cfg.get("sinks", {}).items():
        sinks_summary[name] = float(sink.get("consumption_kW", 0.0))

    return sources_summary, sinks_summary


def get_total_generation(cfg: Dict[str, Any]) -> float:
    """Sum generation_kW of all active sources."""

    return sum(float(src.get("generation_kW", 0.0)) for src in cfg.get("sources", {}).values())


def get_total_consumption(cfg: Dict[str, Any]) -> float:
    """Sum all sink consumption_kW."""

    return sum(float(sink.get("consumption_kW", 0.0)) for sink in cfg.get("sinks", {}).values())


def power_balance(cfg: Dict[str, Any]) -> float:
    """Return net available power (generation - consumption)."""

    return get_total_generation(cfg) - get_total_consumption(cfg)

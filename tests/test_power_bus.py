"""
test_power_bus.py
-----------------
Lightweight checks for the power bus helpers.
"""

from power.bus import get_power_design, power_balance
from data.cache import clear_cache, list_cached_files


def test_power_design_loads():
    cfg = get_power_design(force_reload=True)
    assert "sources" in cfg and "sinks" in cfg


def test_power_balance_executes():
    cfg = get_power_design()
    balance = power_balance(cfg)
    assert isinstance(balance, (int, float))


def test_cache_reporting_roundtrip():
    clear_cache()
    _ = get_power_design()
    cached = list_cached_files()
    assert cached, "expected cache to contain at least one entry"

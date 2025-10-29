"""
test_power_config.py
--------------------
Simple test harness for validating the power configuration pipeline.

Goals:
    - Ensure YAML loads correctly from cache.
    - Confirm all numeric fields are accessible and default to 0.
    - Verify the caching mechanism (no duplicate loads unless forced).
"""

from Ship.config.power_config import get_power_design
from Ship.config.cache_config import list_cached_files, clear_cache


def print_dict_nested(d: dict, indent: int = 0) -> None:
    """Helper to pretty-print nested dictionaries for debugging."""
    pad = "  " * indent
    for k, v in d.items():
        if isinstance(v, dict):
            print(f"{pad}{k}:")
            print_dict_nested(v, indent + 1)
        else:
            print(f"{pad}{k}: {v}")


def test_power_config_pipeline():
    """
    Step-by-step diagnostic test.

    TODOs:
        - Implement get_power_design() in power_config.py
        - Implement get_yaml_config() in cache_config.py
    """

    print("\n[1] Loading power configuration...")
    cfg = get_power_design()
    print("   ✔ hvac_design.yaml successfully loaded from cache.")

    print("\n[2] Cached files summary:")
    print(list_cached_files())

    print("\n[3] Checking sources and sinks...")
    print("   Sources:")
    print_dict_nested(cfg.get("sources", {}), indent=1)
    print("\n   Sinks:")
    print_dict_nested(cfg.get("sinks", {}), indent=1)

    print("\n[4] Confirming numeric zero baseline:")
    errors = []
    for section in ("sources", "sinks"):
        for key, entry in cfg.get(section, {}).items():
            for subkey, value in entry.items():
                if isinstance(value, (int, float)) and value != 0:
                    errors.append(f"{section}.{key}.{subkey} = {value}")

    if errors:
        print("❌ Non-zero defaults found:")
        for e in errors:
            print("   ", e)
    else:
        print("✅ All numeric fields correctly initialized to 0.")

    print("\n[5] Testing cache reload...")
    clear_cache()
    _ = get_power_design(force_reload=True)
    print("   ✔ Cache cleared and reloaded successfully.")


# Run manually from terminal (not pytest):
if __name__ == "__main__":
    test_power_config_pipeline()

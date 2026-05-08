"""
Demo: ship-wide snapshot.
Shows power balance, room environment profiles, and thermal load excerpts.

Run from the repo root:
    uv run python scripts/demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from power.bus import get_power_design, summarize_power, power_balance
from ship.registry import compute, list_types
from data.loader import load_yaml

print("=== Power Bus ===")
cfg = get_power_design()
sources, sinks = summarize_power(cfg)
for name, kw in sources.items():
    print(f"  + {name}: {kw:.1f} kW")
for name, kw in sinks.items():
    print(f"  - {name}: {kw:.1f} kW")
print(f"  Net available: {power_balance(cfg):.1f} kW")

print("\n=== Room Environment Profiles ===")
for room_type in list_types():
    try:
        report = compute(room_type)
        hvac = report.hvac
        vent = hvac.get("ventilation_Lps", "—")
        sens = hvac.get("sensible_load_kW", "—")
        print(f"  {room_type:<20} ventilation={vent} L/s  sensible={sens} kW")
    except Exception as exc:
        print(f"  {room_type:<20} [skipped: {exc}]")

print("\n=== Thermal Loads (reactor / propulsion) ===")
tl = load_yaml(Path(__file__).resolve().parent.parent / "configs/thermal/loads.yaml")
for src in tl.get("sources", []):
    sid = src.get("id", "")
    svc = src.get("service", "")
    if "fusion" in sid or svc.lower() in {"reactor", "propulsion"}:
        print(f"  {sid}  service={svc}  duty={src.get('duty_profile')}")

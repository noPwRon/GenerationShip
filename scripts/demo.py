"""
Demo: fusion-aligned snapshot.
Shows power layout summary and fusion-related thermal loads.
"""

from power.bus import describe_layout
from data.loader import load_yaml

print("Power layout (reactor primary):")
print(describe_layout("configs/power/bus_layout_v0.yaml"))

print("\nThermal loads (fusion-related excerpts):")
tl = load_yaml("configs/thermal/loads.yaml")
for src in tl.get("sources", []):
    sid = src.get("id", "")
    svc = src.get("service", "")
    if "fusion" in sid or svc.lower() in {"reactor", "propulsion"}:
        print(f"- {sid}  service={svc}  duty={src.get('duty_profile')}")

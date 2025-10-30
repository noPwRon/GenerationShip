from __future__ import annotations
from pathlib import Path
import os
import yaml

# Resolve repo root from this file location (…/Ship/config/loader.py)
REPO_ROOT = Path(__file__).resolve().parents[2]  # repo/
SHIP_ROOT = REPO_ROOT / "Ship"
CONFIG_DIR = SHIP_ROOT / "config"

# Allow override if you ever need an alternate config tree
GS_CONFIG_ROOT = Path(os.getenv("GS_CONFIG_ROOT", CONFIG_DIR))

EQUIP_CATALOG = GS_CONFIG_ROOT / "Equipment" / "Generation_Ship_Equipment_v0.4.yaml"
EQUIP_SPEC    = GS_CONFIG_ROOT / "equipment_specs.yaml"       # your existing file

def _load_yaml(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Config missing: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_equipment():
    """Return {'catalog': <dict>, 'spec': <dict>} using your repo layout."""
    catalog = _load_yaml(EQUIP_CATALOG)
    spec = _load_yaml(EQUIP_SPEC) if EQUIP_SPEC.exists() else {}
    return {"catalog": catalog, "spec": spec}

"""
validate_equipment.py
---------------------
Check that:
  - the equipment catalog has required fields
  - the specs file references only defined catalog items
  - power and heat totals are reasonable
"""

from pathlib import Path
import yaml


def load_yaml(path: Path):
    """Load a YAML file and return its parsed contents."""
    # TODO: implement safe_load + error handling
    pass


def validate_catalog(catalog: dict, errors: list[str]):
    """Ensure all required fields exist in each catalog entry."""
    required_fields = [
        "category", "description", "dimensions_mm",
        "weight_kg", "clearance_mm", "electrical",
        "heat_load_w", "communications",
    ]
    # TODO: iterate catalog["equipment"]
    pass


def validate_specs(specs: dict, catalog: dict, errors: list[str]):
    """Check that each spec item exists in catalog and has valid quantity."""
    # TODO: implement lookup + accumulation of totals
    pass


def main():
    """Entry point."""
    repo_root = Path(__file__).resolve().parents[2]
    catalog_path = repo_root / "Ship/config/Equipment/Generation_Ship_Equipment_v0.4.yaml"
    specs_path = repo_root / "Ship/config/equipment_specs.yaml"

    # TODO: load YAMLs, run validators, print summary


if __name__ == "__main__":
    main()

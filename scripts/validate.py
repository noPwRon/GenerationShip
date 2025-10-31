"""
validate.py
------------
Minimal validator for the equipment specification table.
"""

from __future__ import annotations

from typing import List

from data.loader import load_equipment_catalog


REQUIRED_FIELDS = [
    "category",
    "description",
    "dimensions_mm",
    "weight_kg",
]


def validate_catalog(catalog: dict, errors: List[str]) -> None:
    equipment = catalog.get("equipment", {})
    for item_id, entry in equipment.items():
        for field in REQUIRED_FIELDS:
            if field not in entry:
                errors.append(f"{item_id}: missing required field '{field}'")


def main() -> None:
    catalog = load_equipment_catalog(force_reload=True)
    errors: List[str] = []
    validate_catalog(catalog, errors)

    if errors:
        print("[FAIL] Equipment catalog validation issues detected:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("[OK] Equipment catalog structure looks valid.")


if __name__ == "__main__":
    main()

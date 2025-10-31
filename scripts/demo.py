"""
demo.py
--------
Entry script for verifying room module functionality.
"""

from ship import compute


def main() -> None:
    report = compute(
        "dorm_communal_8",
        name="Dorm C-12",
        occupants=8,
        phase="senior",
        floor_area_m2=70.0,
    )
    print(report)


if __name__ == "__main__":
    main()

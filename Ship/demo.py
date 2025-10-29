"""
demo.py
--------
Entry script for verifying room module functionality.

This file demonstrates how to:
    • Access the registry
    • Instantiate a default room specification
    • Trigger a computation
    • Print the resulting RoomReport
"""

from Ship.registry import compute


if __name__ == "__main__":
    # --- Example invocation ---
    # Adjust these parameters for manual testing.
    report = compute(
        "dorm_communal_8",
        name="Dorm C-12",
        occupants=8,
        phase="senior",
        floor_area_m2=70.0,
    )

    # Display the resulting data structure.
    print(report)

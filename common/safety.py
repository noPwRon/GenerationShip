"""
safety.py
----------
Simple safety and design margin helpers.
These should be obvious, explicit multipliers — not hidden magic.
"""


def apply_margin(value: float, factor: float = 1.2, risk_type: str = "normal") -> float:
    """
    Apply a simple safety margin multiplier.
    TODO:
    [ ] Review default multipliers against your design standards.
    [ ] Consider reading factors from configs if scenario-specific.
    """
    adjustment = factor
    if risk_type == "high":
        adjustment *= 1.5
    elif risk_type == "low":
        adjustment *= 1.1
    return value * adjustment

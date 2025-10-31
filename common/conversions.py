"""
conversions.py
---------------
General unit conversion helpers (SI-centric).
Keep pure functions; no environment-specific logic.
"""


def Lps_to_m3h(lps: float) -> float:
    """Convert litres per second to cubic metres per hour."""
    # TODO: consider adding input validation (must be >= 0)
    return lps * 3.6


def m3h_to_Lps(m3h: float) -> float:
    """Convert cubic metres per hour to litres per second."""
    return m3h / 3.6


def W_to_kW(W: float) -> float:
    """Convert watts to kilowatts."""
    return W / 1000.0


def kW_to_W(kW: float) -> float:
    """Convert kilowatts to watts."""
    return kW * 1000.0


def C_to_K(C: float) -> float:
    """Convert degrees Celsius to Kelvin."""
    return C + 273.15


def K_to_C(K: float) -> float:
    """Convert Kelvin to degrees Celsius."""
    return K - 273.15


def C_to_F(C: float) -> float:
    """Convert degrees Celsius to degrees Fahrenheit."""
    return (C * 9.0 / 5.0) + 32.0


def F_to_C(F: float) -> float:
    """Convert degrees Fahrenheit to degrees Celsius."""
    return (F - 32.0) * 5.0 / 9.0


def hours_to_seconds(hours: float) -> float:
    """Convert hours to seconds."""
    return hours * 3600.0


def seconds_to_hours(seconds: float) -> float:
    """Convert seconds to hours."""
    return seconds / 3600.0


def minutes_to_seconds(minutes: float) -> float:
    """Convert minutes to seconds."""
    return minutes * 60.0


def seconds_to_minutes(seconds: float) -> float:
    """Convert seconds to minutes."""
    return seconds / 60.0


def hours_to_minutes(hours: float) -> float:
    """Convert hours to minutes."""
    return hours * 60.0


def minutes_to_hours(minutes: float) -> float:
    """Convert minutes to hours."""
    return minutes / 60.0


def deg_to_rad(degrees: float) -> float:
    """Convert degrees to radians."""
    from math import pi

    return degrees * (pi / 180.0)


def rad_to_deg(radians: float) -> float:
    """Convert radians to degrees."""
    from math import pi

    return radians * (180.0 / pi)


# TODO:
# [ ] Add temperature conversions (°C <-> K) if you find yourself repeating them
# [ ] Add flow/time conversions as needed

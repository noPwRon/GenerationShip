"""
constants.py
-------------
Core HVAC schema keys and baseline defaults shared across the env package.
"""

ACTIVITY_KEYS = [
    "sensible_W_per_person",
    "latent_W_per_person",
]

VENTILATION_KEYS = [
    "Rp_Lps_per_person",
    "Ra_Lps_per_m2",
]

EXHAUST_KEYS = [
    "Ra_Lps_per_m2",
    "per_shower_Lps_continuous",
    "per_shower_Lps_intermittent",
    "per_fixture_Lps",
]

DEFAULT_ACTIVITY_LEVELS = {
    "rest": {"sensible_W_per_person": 80.0, "latent_W_per_person": 35.0},
    "light_work": {"sensible_W_per_person": 110.0, "latent_W_per_person": 60.0},
    "moderate_work": {"sensible_W_per_person": 150.0, "latent_W_per_person": 130.0},
}

DEFAULT_VENTILATION = {
    "Rp_Lps_per_person": 2.5,
    "Ra_Lps_per_m2": 0.3,
}

# Optional normalized output keys (shared label names)
KEY_SUPPLY = "supply_Lps"
KEY_EXHAUST = "exhaust_Lps"

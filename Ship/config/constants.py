"""
constants.py
-------------
Central schema definitions for all config types.
"""

# -------------------------------------------------
# Power system keys (grouped by subtype)
# -------------------------------------------------
POWER_KEYS = {
    "sources": [
        "generation_kW",
        "efficiency_percent",
        "redundancy",
        "voltage_level",
    ],
    "sinks": [
        "consumption_kW",
        "consumption_kW_per_m2",
        "consumption_kW_per_person",
        "voltage_level",
    ],
    "storage": [
        "storage_kWh",
        "discharge_rate_kW",
        "charge_efficiency_percent",
        "discharge_efficiency_percent",
    ],
}

# -------------------------------------------------
# HVAC / Environmental keys
# -------------------------------------------------
HVAC_KEYS = {
    "activity": [
        "sensible_W_per_person",
        "latent_W_per_person",
    ],
    "ventilation": [
        "Rp_Lps_per_person",
        "Ra_Lps_per_m2",
    ],
    "exhaust": [
        "Ra_Lps_per_m2",
        "per_shower_Lps_continuous",
        "per_shower_Lps_intermittent",
        "per_fixture_Lps",
    ],
}

# -------------------------------------------------
# Materials schema keys
# -------------------------------------------------
MATERIAL_KEYS = {
    "properties": [
        "density_kg_per_m3",
        "specific_heat_J_per_kgK",
        "thermal_conductivity_W_per_mK",
        "yield_strength_MPa",
    ]
}

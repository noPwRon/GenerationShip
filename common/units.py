# common/units.py
# ---------------------------------------------------------------
# Single source of truth for all physical units in the ship.
# Import ureg and Q from here — never instantiate UnitRegistry
# elsewhere.
# ---------------------------------------------------------------

from pint import UnitRegistry

ureg = UnitRegistry()
Q = ureg.Quantity

# ---------------------------------------------------------------
# Ship-specific unit aliases (optional but recommended)
# Keeps domain language consistent across all subsystems.
# ---------------------------------------------------------------

# Ventilation / airflow
liters_per_second = ureg.liter / ureg.second

# Thermal
watts       = ureg.watt
kilowatts   = ureg.kilowatt
kelvin      = ureg.kelvin
celsius     = ureg.degC

# Mass / geometry
kilograms   = ureg.kilogram
meters      = ureg.meter
square_meters  = ureg.meter ** 2
cubic_meters   = ureg.meter ** 3

# Power
kilowatt_hours = ureg.kilowatt_hour

# ---------------------------------------------------------------
# TODO: add ship-specific custom units here if needed
# e.g. ureg.define('crew_equivalent = 1 * person')
# ---------------------------------------------------------------

"""
Ship package initializer
-------------------------
This file designates the 'Ship' directory as a Python package.

Future usage:
    - High-level system initialization
    - Global state configuration (logging, simulation flags)
    - Aggregating subpackages such as propulsion, habitat, etc.

Currently exposes the registry for convenience.
"""

from . import registry  # Expose top-level access to the registry
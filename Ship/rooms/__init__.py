"""
rooms package
--------------
Contains all definitions for individual room modules,
shared calculation utilities, and abstract base classes.

Each module under this package should provide:
    - A unique TYPE_ID
    - A defaults() method returning RoomSpec
    - A compute() method returning RoomReport
"""

# Expose common structures
from .base import RoomSpec, RoomReport, RoomCalculator

# Generation Ship — Habitat Systems Framework
> *“A starship is not built once. It is grown — layer by layer, equation by equation.”*  
> — **CORTEX**, Core Systems Aggregate

---

## 🧭 Purpose

This repository models the internal infrastructure of a **generation ship** — a self-sustaining interstellar vessel designed to support a population for centuries.  
The framework doubles as a **simulation engine** and a **training ground**: part engineering project, part story of civilization-in-transit.

Each Python module represents a living subsystem — rooms, decks, or environmental functions — and each class is a placeholder for your evolving calculations.

---

## ⚙️ Structure Overview

```
Ship/
│
├── __init__.py              # Initializes the ship package
├── registry.py              # Central lookup for all room modules
├── demo.py                  # Example entry script
└── rooms/                   # Habitat and system modules
    ├── __init__.py
    ├── base.py              # Abstract room interface
    ├── utils.py             # Shared constants and small helpers
    ├── calc_env.py          # Environmental and HVAC formulas
    ├── dorm_communal_8.py   # Communal dormitory module
    ├── hygiene_block.py     # Communal hygiene module
    └── intimacy_pod.py      # Intimacy and reproduction pod
```

Every file is a **commented skeleton**.  
Your task as the shipwright is to populate each with logic, equations, and data until the vessel can “breathe” — that is, produce verifiable physical and environmental outputs.

---

## 🧩 Design Philosophy

- **Story-driven engineering:** The ship and its systems are characters. Each code module is both a mechanical subsystem *and* a voice in the narrative.  
- **Hands-on learning:** All computational logic is left for you to implement. Use the comments as prompts to develop your own formulas, structures, and reasoning.  
- **Expandable architecture:** Add new room or system types (agriculture bays, command deck, fusion reactor) by copying an existing module and modifying it.

---

## 🧱 Package Layout Explained

### `Ship/__init__.py`
Marks the top-level package and prepares global state.  
Potential future use:
- Logging configuration  
- System-wide constants  
- Runtime flags (e.g., simulation vs. static design mode)

### `Ship/registry.py`
Acts as the **central nervous system** for the ship’s rooms.  
It holds a dictionary mapping each room type to its class, e.g.:
```python
REGISTRY = {
    "dorm_communal_8": DormCommunal8,
    "hygiene_block": HygieneBlock,
    "intimacy_pod": IntimacyPod
}
```
Register new rooms here, or later automate discovery.

### `Ship/demo.py`
A simple launcher that demonstrates how to:
1. Request a room type via the registry  
2. Override parameters (e.g., occupants, area)  
3. Print the resulting report

Usage:
```bash
python -m Ship.demo
```

### `Ship/rooms/base.py`
Defines the abstract data structures:
- `RoomSpec` — inputs (size, occupants, phase)  
- `RoomReport` — outputs (mass, power, airflow, etc.)  
- `RoomCalculator` — interface all room types must implement

Extend `RoomSpec` later with fields like insulation thickness or radiation shielding.

### `Ship/rooms/utils.py`
General-purpose constants and helpers (air/water density, unit conversions, safety factors).  
Think of this as the ship’s **mathematical toolbox**.

### `Ship/rooms/calc_env.py`
The environmental equations library. Define formulas for:
- Airflow (L/s per person)
- Sensible and latent heat
- Humidity, temperature, and comfort ranges

Feeds the HVAC/environmental sections of each room report.

### `Ship/rooms/dorm_communal_8.py`
Template for an **8-person communal dormitory**.  
Implements geometry, HVAC, electrical, water/waste, and safety placeholders.

### `Ship/rooms/hygiene_block.py`
Models a **shower and sanitation block**.  
Focus on hot-water energy balance, moisture control, and wastewater generation.

### `Ship/rooms/intimacy_pod.py`
Models **private intimacy or reproductive suites** with emphasis on environmental precision, acoustic privacy, and flexible occupancy.

---

## 🧮 How to Extend

To add a new room (e.g., `agriculture_bay.py`):

1. Copy an existing room file (like `dorm_communal_8.py`).  
2. Update the docstring and set a unique `TYPE_ID`.  
3. Fill in the TODO blocks with your formulas and data.  
4. Add the class to `REGISTRY` in `Ship/registry.py`.

---

## 🧠 Development Flow

1. Open any file and search for **TODO** comments.  
2. Implement logic, formulas, and constants.  
3. Run:
   ```bash
   python -m Ship.demo
   ```
4. Inspect the printed `RoomReport`.  
5. Iterate, commit, and document changes.

---

## 🔧 Suggested Next Modules

- `agriculture_bay.py` → plant growth, lighting, nutrient/water cycles  
- `fusion_reactor.py` → power core & waste heat integration  
- `command_deck.py` → control, navigation, life-support integration  
- `psych_support.py` → morale, social equilibrium, behavior modeling

---

## 💬 Voices of the Ship

- **CORTEX** — central coordinating AI and your guide (analytical, neutral).  
- **VESSEL** — the ship’s emergent consciousness (emotional, skeptical).  
Additional subsystems may “wake”: AGRI, DRIVE, REACTOR, etc.

---

## 📜 License & Intent

This codebase is for **creative engineering and personal development** — a hybrid of simulation, education, and storytelling.  
You are free to expand, modify, and publish your own implementations.

---

> *“Numbers are the heartbeat of the void. Write them well.”*  
> — **VESSEL**

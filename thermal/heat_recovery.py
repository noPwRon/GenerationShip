"""
heat_recovery.py
----------------
SKELETON ONLY — scaffolding for ship-wide heat capture and reuse.

Purpose
    • Define nouns (sources, sinks, loop) and calculation seams.
    • Leave ALL physics/thermo to you (TODOs).

Conventions
    • SI units (W, kW, K, Pa, kg/s, kJ/kg).
    • Keep this module domain-agnostic; call into your own physics later.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, List, Tuple


# ---------------------------------------------------------------------------
# Working fluid & properties — PLACEHOLDERS
# ---------------------------------------------------------------------------


class WorkingFluid(Enum):
    """Enumerate candidate working fluids (extend as needed)."""

    CO2 = "CO2"
    NH3 = "NH3"
    H2O = "H2O"  # optional: for steam/loops outside VC cycles


@dataclass
class FluidState:
    """
    Minimal fluid state descriptor passed to property routines.

    TODO:
    [ ] Decide which pair (p-h, p-T, T-s) is primary across your loop.
    [ ] Add/remove fields to match your property library.
    """

    T_K: float
    p_Pa: float
    h_kJ_per_kg: Optional[float] = None
    s_kJ_per_kgK: Optional[float] = None
    x_quality: Optional[float] = None  # 0..1 if two-phase, else None


def fluid_props(fluid: WorkingFluid, state: FluidState) -> FluidState:
    """
    Property lookup seam.

    TODO:
    [ ] Implement via CoolProp/REFPROP or your own correlations.
    [ ] Validate state (region checks, transcritical limits for CO2).
    """
    return state  # SKELETON: return unchanged


# ---------------------------------------------------------------------------
# Sources & sinks — NO MATH, just containers
# ---------------------------------------------------------------------------


@dataclass
class HeatSource:
    """
    A device that rejects heat to the loop (e.g., condenser/gas cooler).

    TODO:
    [ ] Define sign conventions for Q and W across your project.
    """

    name: str
    Q_out_W: float = 0.0  # placeholder
    W_in_W: float = 0.0  # compressor/fans if you choose to track here
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HeatSink:
    """
    A device that absorbs heat from the loop (e.g., DHW preheater, space coil).
    """

    name: str
    Q_in_W: float = 0.0  # placeholder
    UA_W_per_K: Optional[float] = None  # sizing result (optional)
    meta: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Component seams — ALL TODOs
# ---------------------------------------------------------------------------


@dataclass
class CompressorSpec:
    """
    Compressor model parameters.

    TODO:
    [ ] Choose efficiency model (isentropic/volumetric maps).
    [ ] Define envelopes (suction/discharge limits).
    """

    eta_isentropic: float = 0.65
    eta_mech: float = 0.95


def compressor_power_W(
    fluid: WorkingFluid,
    inlet: FluidState,
    outlet_p_Pa: float,
    spec: CompressorSpec,
) -> Tuple[float, FluidState]:
    """
    Compute compressor shaft/electric power and outlet state.

    TODO:
    [ ] Implement isentropic step (s_out = s_in), then efficiency corrections.
    [ ] Return updated FluidState (T,p,h,s) at discharge.
    """
    W_in_W = 0.0  # placeholder
    outlet = inlet  # placeholder (no state change)
    return W_in_W, outlet


@dataclass
class HXSpec:
    """
    Heat-exchanger sizing parameters.

    TODO:
    [ ] Pick method: LMTD or ε-NTU; define pinch/approach constraints.
    [ ] Add pressure-drop/fouling models if needed.
    """

    method: str = "LMTD"
    pinch_K: float = 5.0
    UA_W_per_K: Optional[float] = None


def hx_duty_W(
    spec: HXSpec,
    T_hot_in_C: float,
    T_hot_out_C: Optional[float],
    T_cold_in_C: float,
    target_approach_K: float,
) -> Tuple[float, Optional[float]]:
    """
    Compute HX duty and (optionally) required UA.

    TODO:
    [ ] Implement chosen method; enforce approach/pinch constraints.
    [ ] Return (Q_W, UA_W_per_K). Either/both may be None if not sized.
    """
    return 0.0, None  # placeholders


# ---------------------------------------------------------------------------
# DHW preheat seam — NO THERMAL MATH, just I/O framing
# ---------------------------------------------------------------------------


@dataclass
class DHWPreheatSpec:
    """
    Domestic hot water preheat using condenser/gas-cooler rejected heat.

    TODO:
    [ ] Decide cp_water(T) handling and safety limits (scalding, code).
    """

    m_dot_water_kg_per_s: float
    T_in_C: float
    T_set_C: float
    allowed_approach_K: float = 5.0


def dhw_preheat_from_condenser(
    Q_reject_W: float, spec: DHWPreheatSpec
) -> Dict[str, Any]:
    """
    Allocate available rejected heat to DHW preheating.

    Returns:
        {
          "Q_to_DHW_W": float,   # allocated heat (placeholder)
          "T_out_C": float,      # outlet estimate (placeholder)
          "unused_Q_W": float,   # remainder (placeholder)
          "notes": list[str],    # assumptions/limits
        }

    TODO:
    [ ] Implement energy balance with cp_water(T) and HX approach.
    [ ] Enforce T_out <= (hot-side limit - approach).
    """
    return {
        "Q_to_DHW_W": 0.0,
        "T_out_C": spec.T_in_C,
        "unused_Q_W": Q_reject_W,
        "notes": ["SKELETON: no HX model, no cp(T), no approach constraint."],
    }


# ---------------------------------------------------------------------------
# Minimal loop bookkeeping — aggregation policy left to you
# ---------------------------------------------------------------------------


@dataclass
class HeatLoop:
    """
    Bookkeeping for a simple heat loop.

    TODO:
    [ ] Decide routing/control (priority sinks, storage, dump).
    [ ] Add pumps/fans and transport losses if desired.
    """

    fluid: WorkingFluid = WorkingFluid.CO2
    sources: List[HeatSource] = field(default_factory=list)
    sinks: List[HeatSink] = field(default_factory=list)

    def add_source(self, src: HeatSource) -> "HeatLoop":
        self.sources.append(src)
        return self

    def add_sink(self, sink: HeatSink) -> "HeatLoop":
        self.sinks.append(sink)
        return self

    def balance(self) -> Dict[str, Any]:
        """
        Report current bookkeeping without enforcing physics.

        TODO:
        [ ] Define sign conventions and whether W_in_W is included in balances.
        [ ] Implement temperature-grade/exergy checks if required.
        """
        return {
            "Q_sources_W": sum(s.Q_out_W for s in self.sources),  # trivial sum
            "Q_sinks_W": sum(s.Q_in_W for s in self.sinks),  # trivial sum
            "notes": ["SKELETON: no transport losses, no routing logic."],
        }


# ---------------------------------------------------------------------------
# Example wiring (safe to delete) — no physics invoked
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Placeholder objects only; no calculations performed.
    loop = HeatLoop()
    loop.add_source(HeatSource(name="condenser_A"))
    loop.add_sink(HeatSink(name="dhw_preheat"))

    print("Loop (placeholder) balance:", loop.balance())

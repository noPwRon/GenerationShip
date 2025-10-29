"""
child_dorm_8.py
------------------
Communal dormitory for 8 occupants.

Responsibilities:
    - Determine geometry, air, heat, water, and safety parameters.
    - Interface with calc_env for environmental calculations.
"""

from ast import Dict
from typing import Optional, Any
from Ship.rooms.base import RoomSpec, RoomReport, RoomCalculator
from Ship.rooms import calc_env
from Ship.rooms.calc_tables import get_rates, resolve_room_activity


class child_dorm_8(RoomCalculator):
    TYPE_ID = "child_dorm_8"

    @staticmethod
    def defaults() -> RoomSpec:
        """
        Return default parameters for an 8-person dormitory.
        Example values: area, height, occupancy phase.
        """
        name: str = "Child Dorm 8"
        occupants: int = 8
        phase: str = "children"
        floor_area_m2: float = 24.0
        height_m: float = 2.6
        deck_level: int = 1
        notes: Optional[str] = "Children dormitory for 8 occupants."

    @staticmethod
    def compute(spec: RoomSpec) -> RoomReport:
        """
        Orchestrates all calculations for this room and packages results.

        Workflow:
            1) Validate/normalize the incoming spec
            2) Geometry (area, volume, envelope)
            3) Environmental (ventilation, sensible/latent loads)
            4) Electrical (lighting, devices, HVAC allowance)
            5) Water & waste (daily volumes)
            6) Mass & materials (structure, fixtures, buffers)
            7) Safety (egress, agents, acoustics)
            8) Schematics (file paths/ids)
            9) Metadata (phase, notes, tags)
        """
        # -------------------------------
        # 1) Validate / normalize inputs
        # -------------------------------
        # TODO: add checks for required fields and sensible ranges
        # Example:
        # if spec.occupants < 0:
        #     raise ValueError("occupants must be ≥ 0")
        # phase = spec.phase or "mixed"

        # -------------------------------
        # 2) Geometry
        # -------------------------------
        # TODO: compute geometric properties
        # floor_area_m2 = spec.floor_area_m2
        # height_m = spec.height_m
        # volume_m3 = floor_area_m2 * height_m  # implement when ready

        geometry: Dict[str, float] = {
            # "floor_area_m2": floor_area_m2,
            # "height_m": height_m,
            # "volume_m3": volume_m3,
        }

        # -------------------------------
        # 3) Environmental / HVAC
        # -------------------------------

        cfg = get_rates()  # load YAML once per run (you can later cache it)
        rates = resolve_room_activity(cfg, room_type="dorm")

        Rp = rates["ventilation"]["Rp_Lps_per_person"]
        Ra = rates["ventilation"]["Ra_Lps_per_m2"]
        sens_W = rates["activity"]["sensible_W_per_person"]
        lat_W = rates["activity"]["latent_W_per_person"]
        
        # Check for optional exhaust data
        exhaust_info: Optional[Dict[str, Any]] = None
        exhaust_info = rates.get("exhaust", None)

        # TODO: compute airflow and loads using calc_env (once implemented)
        vent_Lps = calc_env.ventilation_rate(
            occupants=spec.occupants,
            Lps_per_person=Rp,
            area=spec.floor_area_m2,
            lps_per_area=Ra,
        )
        # sens_kW = calc_env.metabolic_heat_kW(spec.occupants) + <devices>
        # coil_sens_kW = calc_env.coil_sensible_capacity_kW(sens_kW)
        # lat_kgph = calc_env.latent_load_kgph(spec.occupants)
        # coil_lat_kW = calc_env.latent_to_kW(lat_kgph)
        # tmin, tmax = calc_env.temp_band(phase)
        # rhmin, rhmax = calc_env.rh_band(phase)

        hvac: Dict[str, float] = {
            # "ventilation_Lps": vent_Lps,
            # "coil_sensible_kW": coil_sens_kW,
            # "coil_latent_kW": coil_lat_kW,
            # "design_temp_C_min": tmin,
            # "design_temp_C_max": tmax,
            # "design_rh_pct_min": rhmin,
            # "design_rh_pct_max": rhmax,
        }

        # -------------------------------
        # 4) Electrical
        # -------------------------------
        # TODO: estimate base and peak device+lighting power and HVAC allowance
        electrical_kW: Dict[str, float] = {
            # "base_kW": ...,
            # "peak_device_kW": ...,
            # "HVAC_allowance_kW": ...,
            # "estimated_peak_total_kW": ...,
        }

        # -------------------------------
        # 5) Water & Waste
        # -------------------------------
        # TODO: compute daily water use and waste volumes
        water_L_per_day: Dict[str, float] = {
            # "cold": ...,
            # "hot": ...,
            # "total": ...,
        }
        waste_L_per_day: Dict[str, float] = {
            # "grey": ...,
            # "black": ...,
        }

        # -------------------------------
        # 6) Mass & Materials
        # -------------------------------
        # TODO: estimate structural mass, fixtures, local buffers
        mass_kg: Dict[str, float] = {
            # "structure": ...,
            # "fixtures": ...,
            # "water_buffer": ...,
            # "total": ...,
        }

        # -------------------------------
        # 7) Safety & Acoustics
        # -------------------------------
        # TODO: document basic safety assumptions and targets
        safety: Dict[str, Any] = {
            # "max_occupancy": spec.occupants,
            # "egress_door_min_width_mm": ...,
            # "clean_agent_canisters": ...,
            # "partition_STC_min": ...,
            # "sleep_noise_dBA_max": ...,
        }

        # -------------------------------
        # 8) Schematics
        # -------------------------------
        # TODO: point to drawing asset paths (SVG/PDF) when available
        schematics: Dict[str, str] = {
            # "plan_svg": "schematics/example_plan.svg",
            # "section_svg": "schematics/example_section.svg",
        }

        # -------------------------------
        # 9) Metadata
        # -------------------------------
        # TODO: store any tags or references you want to carry downstream
        metadata: Dict[str, Any] = {
            # "phase": phase,
            # "notes": spec.notes or "",
            # "revision": "A0",
        }

        # -------------------------------
        # Final assembly
        # -------------------------------
        return RoomReport(
            type_id=child_dorm_8.TYPE_ID,
            name=spec.name,
            geometry=geometry,
            mass_kg=mass_kg,
            electrical_kW=electrical_kW,
            hvac=hvac,
            water_L_per_day=water_L_per_day,
            waste_L_per_day=waste_L_per_day,
            safety=safety,
            schematics=schematics,
            metadata=metadata,
        )

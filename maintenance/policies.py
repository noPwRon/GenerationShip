"""
maintenance/policies.py
-----------------------
Policy layer for PM/CM intervals, end-of-life handling, reuse/repurpose, teardown.

Intent
    • Express all rules in YAML, evaluated by planner/scheduler.
    • No probability math here — just policy shapes and TODO prompts.

Files (proposed)
    • configs/maintenance/policies.yaml       # PM templates, CM triggers, reuse trees
    • data/specs/maintenance_refurb.yaml      # canonical refurb steps/material recovery
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

try:
    from data.loader import load_yaml  # type: ignore
except Exception:
    def load_yaml(path: str) -> Dict[str, Any]: return {}

@dataclass
class PMTemplate:
    """
    Preventive-maintenance template.

    TODO (YAML):
      - key: "hvac_blower_pm_v1"
      - applies_to: ["hvac_blower_v2", "hvac_blower_v3"]
      - interval_hours: null
      - steps: [clean, balance, bearings_lube]
      - required_parts: { bearing_6001: 2 }
      - required_skills: [tech_mech_lvl1]
      - downtime_hours: null
    """
    key: str
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EOLRoute:
    """
    End-of-life routes: refurb, repurpose, dismantle.

    TODO (YAML):
      - key: "hvac_blower_refurb_v1"
      - route: refurb | repurpose | dismantle
      - outputs:
          refurb: { new_type_id: "hvac_blower_v2_refurb", expected_life_hours: null }
          repurpose: { new_role: "low_duty_circulation", derating: null }
          dismantle: { materials_out: { copper_kg: null, steel_kg: null } }
      - constraints: [contamination, fatigue_limit, tooling_required]
    """
    key: str
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MaintenancePolicies:
    """Aggregated policies loaded from YAML."""
    pm_templates: Dict[str, PMTemplate] = field(default_factory=dict)
    eol_routes: Dict[str, EOLRoute] = field(default_factory=dict)
    skills_matrix: Dict[str, Any] = field(default_factory=dict)

def load_policies(path: str = "configs/maintenance/policies.yaml") -> MaintenancePolicies:
    """
    Load policy YAML.

    TODO:
      [ ] Validate references (applies_to type_ids exist).
      [ ] Ensure no circular EOL routes.
    """
    raw = load_yaml(path)
    pm = {k: PMTemplate(key=k, meta=v) for k, v in raw.get("pm_templates", {}).items()}
    eol = {k: EOLRoute(key=k, meta=v) for k, v in raw.get("eol_routes", {}).items()}
    return MaintenancePolicies(pm_templates=pm, eol_routes=eol, skills_matrix=raw.get("skills_matrix", {}))

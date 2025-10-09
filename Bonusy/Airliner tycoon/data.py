from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class PolicyDef:
    key: str
    name: str
    base_income: int     # income per unit funding
    base_upkeep: int     # upkeep per unit funding
    max_funding: int     # slider max
    ap_change_cost: int  # AP per step change

# Some sample policies for the MVP.
POLICIES = [
    PolicyDef("marketing", "Global Marketing", base_income=1800, base_upkeep=1200, max_funding=10, ap_change_cost=1),
    PolicyDef("maintenance", "Fleet Maintenance", base_income=1100, base_upkeep=1500, max_funding=10, ap_change_cost=1),
    PolicyDef("routes", "Open New Routes", base_income=2500, base_upkeep=2000, max_funding=8, ap_change_cost=2),
    PolicyDef("it", "IT & Automation", base_income=1600, base_upkeep=900, max_funding=10, ap_change_cost=1),
    PolicyDef("lounge", "Premium Lounges", base_income=2200, base_upkeep=1700, max_funding=6, ap_change_cost=2),
]

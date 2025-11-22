from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import IntEnum
from typing import Dict, Any

from config import START_CASH, BASE_AP_PER_TURN, AP_COST_BUY_UPGRADE

class Tier(IntEnum):
    T1 = 1
    T2 = 2
    T3 = 3
    T4 = 4

@dataclass
class Policy:
    key: str
    name: str
    funding: int = 0  # 0..max_funding

@dataclass
class PlayerState:
    cash: int = START_CASH
    turn: int = 1
    action_points: int = BASE_AP_PER_TURN

@dataclass
class Upgrades:
    airline: Tier = Tier.T1
    airport: Tier = Tier.T1
    points: Tier = Tier.T1

@dataclass
class GameState:
    player: PlayerState = field(default_factory=PlayerState)
    upgrades: Upgrades = field(default_factory=Upgrades)
    policies: Dict[str, Policy] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "player": asdict(self.player),
            "upgrades": {
                "airline": int(self.upgrades.airline),
                "airport": int(self.upgrades.airport),
                "points": int(self.upgrades.points),
            },
            "policies": {k: {"key": v.key, "name": v.name, "funding": v.funding} for k, v in self.policies.items()},
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "GameState":
        st = cls()
        st.player = PlayerState(**d["player"])
        up = d["upgrades"]
        st.upgrades = Upgrades(airline=Tier(up["airline"]), airport=Tier(up["airport"]), points=Tier(up["points"]))
        st.policies = {k: Policy(**v) for k, v in d["policies"].items()}
        return st

# --- Economy math for tiers ---

def tier_perf_multiplier(airline: Tier) -> float:
    # Airline perf scales income (revenue side)
    if airline == Tier.T1:
        return 1.00
    if airline == Tier.T2:
        return 1.40  # +40 percent vs T1
    if airline == Tier.T3:
        return 1.54  # +10 percent vs T2 (1.4 * 1.1)
    if airline == Tier.T4:
        return 2.156  # 1.54 * 1.4
    return 1.0

def tier_airport_cost_multiplier(airport: Tier) -> float:
    # Airport tier influences upkeep side (costs) in this MVP:
    if airport == Tier.T1:
        return 1.00
    if airport == Tier.T2:
        return 1.40   # T2 upkeep much higher
    if airport == Tier.T3:
        return 1.05   # 25 percent cheaper than T2 -> 1.40 * 0.75 ~ 1.05
    if airport == Tier.T4:
        return 1.155  # +10 percent vs T3
    return 1.0

def tier_ap_per_turn(points: Tier) -> int:
    base = BASE_AP_PER_TURN
    if points == Tier.T1:
        return base
    if points == Tier.T2:
        return int(base * 1.4)
    if points == Tier.T3:
        return int(base * 1.55)  # modest bump vs T2
    if points == Tier.T4:
        return int(base * 2.2)
    return base

def adjust_policy(gs: GameState, policy_key: str, delta: int, ap_cost: int, max_funding: int) -> bool:
    pol = gs.policies[policy_key]
    new_val = max(0, min(max_funding, pol.funding + delta))
    steps = abs(new_val - pol.funding)
    total_ap = steps * ap_cost
    if steps > 0 and gs.player.action_points >= total_ap:
        gs.player.action_points -= total_ap
        pol.funding = new_val
        return True
    return False

def buy_upgrade(gs: GameState, attr: str) -> bool:
    cur = getattr(gs.upgrades, attr)
    if cur >= Tier.T4:
        return False
    # price curve in cash
    price_table = {Tier.T1: 200_000, Tier.T2: 600_000, Tier.T3: 1_200_000}
    price = price_table[cur]
    if gs.player.cash < price:
        return False
    if gs.player.action_points < 5:
        return False
    gs.player.cash -= price
    gs.player.action_points -= 5
    setattr(gs.upgrades, attr, Tier(cur + 1))
    return True

def compute_turn_delta(gs: GameState, policy_defs: dict[str, Any]) -> tuple[int, int, int]:
    # Return (income, upkeep, net).
    perf_mul = tier_perf_multiplier(gs.upgrades.airline)
    cost_mul = tier_airport_cost_multiplier(gs.upgrades.airport)

    income = 0
    upkeep = 0
    for key, pol in gs.policies.items():
        pdef = policy_defs[key]
        income += int(pol.funding * pdef.base_income * perf_mul)
        upkeep += int(pol.funding * pdef.base_upkeep * cost_mul)

    net = income - upkeep
    return income, upkeep, net

def end_turn(gs: GameState, policy_defs: dict[str, Any]) -> None:
    inc, upk, net = compute_turn_delta(gs, policy_defs)
    gs.player.cash += net
    gs.player.turn += 1
    gs.player.action_points = tier_ap_per_turn(gs.upgrades.points)

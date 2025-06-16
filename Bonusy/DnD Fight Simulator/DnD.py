import re
import random

class Character:
    def __init__(self, name, base_ac, armor, dex_bonus, hp, shields, weapon_roll, team):
        self.name = name
        self.base_ac = base_ac
        self.armor = armor
        self.dex = dex_bonus
        self.max_hp = hp
        self.hp = hp
        self.shields = shields
        self.weapon_roll = weapon_roll
        self.team = team
        self.initiative = 0
        self.alive = True

    def total_ac(self):
        return self.base_ac + self.armor + self.dex

    def __repr__(self):
        return f"{self.name}(T{self.team}, Init={self.initiative}, HP={self.hp}, SH={self.shields})"

def roll_dice(notation):
    """
    Parse strings like '2d6+3', 'd8', '1d10-1', or just '4' and return an int roll.
    """
    notation = notation.strip().lower()
    m = re.match(r'(\d*)d(\d+)([+-]\d+)?$', notation)
    if m:
        n = int(m.group(1)) if m.group(1) else 1
        sides = int(m.group(2))
        mod = int(m.group(3)) if m.group(3) else 0
        return sum(random.randint(1, sides) for _ in range(n)) + mod
    else:
        # fallback: treat it as a flat number
        return int(notation)

def input_characters():
    chars = []
    while True:
        name = input("character designation? ")
        base_ac = int(input("character base AC? "))
        armor = int(input("character Armor? "))
        dex = int(input("character Dexterity bonus? "))
        hp = int(input("character HP? "))
        shields = int(input("character Shields? "))
        weapon = input("character weapon roll? ")
        team = input("team? ")
        chars.append(Character(name, base_ac, armor, dex, hp, shields, weapon, team))
        if input("add other? (y/n) ").lower() != 'y':
            break
    return chars

def roll_initiative(chars):
    # initial roll
    for c in chars:
        c.initiative = random.randint(1,20) + c.dex
    # resolve ties by rerolling tied groups until all unique
    while True:
        # group by initiative
        inv = {}
        for c in chars:
            inv.setdefault(c.initiative, []).append(c)
        # find ties
        ties = [group for group in inv.values() if len(group) > 1]
        if not ties:
            break
        for group in ties:
            for c in group:
                c.initiative = random.randint(1,20) + c.dex
    # sort descending
    chars.sort(key=lambda c: c.initiative, reverse=True)

def choose_target(attacker, chars):
    foes = [c for c in chars if c.team != attacker.team and c.alive]
    return random.choice(foes) if foes else None

def simulate_fight(chars):
    log = []
    roll_initiative(chars)
    turn_order = chars[:]  # will keep same order each round
    print("\n--- Initiative order ---")
    for c in turn_order:
        print(f"{c.name}: {c.initiative}")
    round_num = 1
    while True:
        alive_teams = {c.team for c in chars if c.alive}
        if len(alive_teams) <= 1:
            break
        print(f"\n-- Round {round_num} --")
        for c in turn_order:
            if not c.alive:
                continue
            target = choose_target(c, chars)
            if target is None:
                continue
            atk_roll = random.randint(1,20) + c.dex
            hit = atk_roll >= target.total_ac()
            dmg = roll_dice(c.weapon_roll) if hit else 0
            # apply damage
            remaining = dmg
            shield_lost = min(target.shields, remaining)
            target.shields -= shield_lost
            remaining -= shield_lost
            hp_lost = min(target.hp, remaining)
            target.hp -= hp_lost
            if target.hp <= 0:
                target.alive = False
            log.append({
                'Attacker': c.name,
                'Target': target.name,
                'AtkRoll': atk_roll,
                'Needed': target.total_ac(),
                'Hit': hit,
                'Damage': dmg,
                'Shield↓': shield_lost,
                'HP↓': hp_lost,
                'Target SH': target.shields,
                'Target HP': target.hp,
            })
            print(f"{c.name} attacks {target.name} (roll {atk_roll} vs AC {target.total_ac()}): "
                  f"{'HIT' if hit else 'miss'}; dmg={dmg}, "
                  f"shields→{target.shields}, hp→{target.hp}")
            if len({c.team for c in chars if c.alive}) <= 1:
                break
        round_num += 1
    return log

def print_log_table(log):
    if not log:
        print("No attacks were made.")
        return
    headers = ['Attacker','Target','AtkRoll','Needed','Hit','Damage','Shield↓','HP↓','Target SH','Target HP']
    # print header
    print("\n=== Combat Log ===")
    print(" | ".join(f"{h:^10}" for h in headers))
    print("-" * (12 * len(headers)))
    for entry in log:
        row = []
        for h in headers:
            val = entry[h]
            if isinstance(val, bool):
                val = '✔' if val else '✘'
            row.append(f"{str(val):^10}")
        print(" | ".join(row))

def main():
    random.seed()  # remove or set seed for reproducibility
    chars = input_characters()
    combat_log = simulate_fight(chars)
    print_log_table(combat_log)
    # announce winner(s)
    alive = [c for c in chars if c.alive]
    if alive:
        winners = ", ".join(f"{c.name}(T{c.team})" for c in alive)
        print(f"\n🎉 Combat over! Winner(s): {winners}")
    else:
        print("\n⚔️ Everyone fell!")

if __name__ == "__main__":
    main()

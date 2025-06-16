'''
DnD 5e Fight Simulator

This script allows you to enter multiple D&D 5e characters, organize them
into teams, roll for initiative, and simulate combat until one team remains.
At the end, a detailed combat log is printed in tabular format.

Usage:
    python dnd_fight_simulator.py

Attributes:
    None (all data collected via user input)
'''

import re
import random


class Character:
    """
    Represents a single combatant in the fight.

    Attributes:
        name (str): The character's designation.
        base_ac (int): The character's base Armor Class.
        armor (int): Armor bonus to AC.
        dex (int): Dexterity bonus (also used for initiative and attack rolls).
        max_hp (int): Maximum hit points.
        hp (int): Current hit points.
        shields (int): Temporary layers of shielding before HP is damaged.
        weapon_roll (str): Dice notation for weapon damage (e.g., '1d8+2').
        team (str): Identifier for the team this character belongs to.
        initiative (int): Initiative score for turn order.
        alive (bool): Whether the character is still in the fight.
    """
    def __init__(
        self,
        name: str,
        base_ac: int,
        armor: int,
        dex_bonus: int,
        hp: int,
        shields: int,
        weapon_roll: str,
        team: str
    ):
        # Basic defenses and identity
        self.name = name
        self.base_ac = base_ac
        self.armor = armor
        self.dex = dex_bonus

        # Health and shields
        self.max_hp = hp
        self.hp = hp
        self.shields = shields

        # Combat details
        self.weapon_roll = weapon_roll
        self.team = team
        self.initiative = 0
        self.alive = True

    def total_ac(self) -> int:
        """
        Calculate the character's total Armor Class (AC).

        Returns:
            int: Sum of base AC, armor bonus, and Dexterity bonus.
        """
        return self.base_ac + self.armor + self.dex

    def __repr__(self) -> str:
        """
        Developer-friendly representation including key stats.
        """
        return (
            f"{self.name}(T{self.team}, Init={self.initiative}, "
            f"HP={self.hp}, SH={self.shields})"
        )


def roll_dice(notation: str) -> int:
    """
    Parse and roll dice based on standard D&D notation.

    Supported formats:
        - 'NdM+K' or 'NdM-K'
        - 'dM+K', which is shorthand for '1dM+K'
        - Single integers (just returns the integer)

    :param notation: Dice string (e.g., '2d6+3').
    :return: Integer result of rolling the dice plus modifiers.
    """
    notation = notation.strip().lower()
    # Regex to match dice notation
    m = re.match(r"(\d*)d(\d+)([+-]\d+)?$", notation)
    if m:
        # Number of dice (default 1 if omitted)
        n = int(m.group(1)) if m.group(1) else 1
        # Number of sides per die
        sides = int(m.group(2))
        # Modifier +K or -K
        mod = int(m.group(3)) if m.group(3) else 0
        # Roll N times and sum
        total = sum(random.randint(1, sides) for _ in range(n)) + mod
        return total
    else:
        # If not dice notation, assume integer
        return int(notation)


def input_characters() -> list[Character]:
    """
    Prompt the user to input multiple characters until they choose to stop.

    :return: List of Character instances based on user input.
    """
    chars = []
    while True:
        # Gather each attribute from user
        name = input("character designation? ")
        base_ac = int(input("character base AC? "))
        armor = int(input("character Armor? "))
        dex = int(input("character Dexterity bonus? "))
        hp = int(input("character HP? "))
        shields = int(input("character Shields? "))
        weapon = input("character weapon roll? ")
        team = input("team? ")

        # Create and store the character
        chars.append(
            Character(name, base_ac, armor, dex, hp, shields, weapon, team)
        )

        # Option to add more characters
        if input("add other? (y/n) ").lower() != 'y':
            break

    return chars


def roll_initiative(chars: list[Character]) -> None:
    """
    Roll initiative for each character, reroll ties, and sort descending.

    :param chars: List of Character instances.
    :side-effect: Updates each Character.initiative and sorts the list.
    """
    # Initial roll: 1d20 + Dex modifier
    for c in chars:
        c.initiative = random.randint(1, 20) + c.dex

    # Reroll any ties until all unique
    while True:
        # Group by initiative value
        inv = {}
        for c in chars:
            inv.setdefault(c.initiative, []).append(c)
        # Identify groups with more than one member
        ties = [group for group in inv.values() if len(group) > 1]
        if not ties:
            break
        # Reroll each tied character's initiative
        for group in ties:
            for c in group:
                c.initiative = random.randint(1, 20) + c.dex

    # Sort by initiative highest first
    chars.sort(key=lambda c: c.initiative, reverse=True)


def choose_target(attacker: Character, chars: list[Character]) -> Character | None:
    """
    Select a random living foe from opposing teams.

    :param attacker: The Character who is attacking.
    :param chars: List of all Character instances.
    :return: A living foe Character, or None if no foes remain.
    """
    foes = [c for c in chars if c.team != attacker.team and c.alive]
    return random.choice(foes) if foes else None


def simulate_fight(chars: list[Character]) -> list[dict]:
    """
    Run the full combat simulation until one team remains.

    1. Roll initiative and display order.
    2. Loop through rounds and turns.
    3. Each character attacks a random foe.
    4. Resolve damage against shields and HP.
    5. Log each attack in a dict.

    :param chars: List of Character instances.
    :return: Combat log as a list of dictionaries.
    """
    log = []

    # Determine turn order
    roll_initiative(chars)
    turn_order = chars.copy()

    # Display initiative results
    print("\n--- Initiative order ---")
    for c in turn_order:
        print(f"{c.name}: {c.initiative}")

    round_num = 1
    # Continue until only one team left
    while True:
        alive_teams = {c.team for c in chars if c.alive}
        if len(alive_teams) <= 1:
            break

        print(f"\n-- Round {round_num} --")
        for c in turn_order:
            if not c.alive:
                continue

            # Pick a random target
            target = choose_target(c, chars)
            if target is None:
                continue

            # Attack roll: d20 + Dex
            atk_roll = random.randint(1, 20) + c.dex
            # Determine if it hits
            hit = atk_roll >= target.total_ac()
            # Roll damage if hit
            dmg = roll_dice(c.weapon_roll) if hit else 0

            # Apply damage to shields first, then HP
            remaining = dmg
            shield_lost = min(target.shields, remaining)
            target.shields -= shield_lost
            remaining -= shield_lost

            hp_lost = min(target.hp, remaining)
            target.hp -= hp_lost
            if target.hp <= 0:
                target.alive = False

            # Record this attack in the log
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

            # Print live commentary for clarity
            print(
                f"{c.name} attacks {target.name} (roll {atk_roll} vs AC {target.total_ac()}): "
                f"{'HIT' if hit else 'miss'}; dmg={dmg}, "
                f"shields→{target.shields}, hp→{target.hp}"
            )

            # Check if combat ended mid-round
            if len({c.team for c in chars if c.alive}) <= 1:
                break

        round_num += 1
    return log


def print_log_table(log: list[dict]) -> None:
    """
    Print a formatted table of the combat log entries.

    :param log: List of attack dictionaries from simulate_fight().
    :side-effect: Prints to stdout.
    """
    if not log:
        print("No attacks were made.")
        return

    headers = [
        'Attacker','Target','AtkRoll','Needed','Hit',
        'Damage','Shield↓','HP↓','Target SH','Target HP'
    ]

    print("\n=== Combat Log ===")
    # Print header row
    print(" | ".join(f"{h:^10}" for h in headers))
    print("-" * (12 * len(headers)))

    # Print each entry
    for entry in log:
        row = []
        for h in headers:
            val = entry[h]
            # Display hits as checkmarks
            if isinstance(val, bool):
                val = '✔' if val else '✘'
            row.append(f"{str(val):^10}")
        print(" | ".join(row))


def main() -> None:
    """
    Main entry point: gather characters, simulate fight, and display results.
    """
    # Seed RNG for unpredictable results (remove for fixed reproducibility)
    random.seed()

    # Step 1: Input
    chars = input_characters()

    # Step 2: Simulate combat
    combat_log = simulate_fight(chars)

    # Step 3: Render results
    print_log_table(combat_log)

    # Announce the winner(s)
    alive = [c for c in chars if c.alive]
    if alive:
        winners = ", ".join(f"{c.name}(T{c.team})" for c in alive)
        print(f"\n🎉 Combat over! Winner(s): {winners}")
    else:
        print("\n⚔️ Everyone fell!")


if __name__ == "__main__":
    main()

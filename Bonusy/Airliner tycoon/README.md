Airline Tycoon (working title) - Python MVP
==========================================

Single-player, turn-based airline management prototype built with pygame. Mouse-only UI.
Tested on Python 3.13 + pygame 2.6.

Run
---
1) Create a venv (recommended) and install requirements:

   pip install -r requirements.txt

2) Launch the game:

   python main.py

Controls
--------
- Mouse: interact with buttons and sliders.
- End Turn button: processes income/expenses and advances the turn.
- Shop panel (right): buy Tier upgrades for Airline, Airport, and Points subsystems.
- Policies list (center): adjust funding using the - / + buttons. Funding affects income/expenses.
- F11: toggle fullscreen.
- S: save to savegame.json
- L: load from savegame.json
- ESC or Quit: exit.

Design Notes (MVP)
------------------
- Action Points (AP): You get AP each turn; changing policy funding or buying upgrades costs AP.
- Tiers (T1-T4):
  * T1: baseline.
  * T2: +40 percent performance vs T1, upkeep much higher.
  * T3: about +10 percent performance vs T2 but about 25 percent cheaper upkeep than T2.
  * T4: +40 percent performance vs T3, upkeep +10 percent vs T3.
- Infinite loop game: survive early, optimize mid, chase best-in-class endgame.

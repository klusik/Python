"""
EDMC Plugin: SSF Tally
Track BGS contribution for one faction (Sirius Special Forces) only,
and upload cumulative data to an online database for a commander leaderboard.

Usage:
- Place this file (plugin.py) in a folder named SSF_Tally (or similar) inside EDMC's plugins directory.
- Configure Firebase credentials if using Firebase (or adapt for another DB).
- Restart EDMC to load the plugin.

Requires:
- Python 3.7+ (for type hints)
- Additional libraries if using Firebase or other DB (install them accordingly).
"""

import sys
import tkinter as tk
import requests
import json
from typing import Any, Dict, Optional

# If using Firebase:
# import firebase_admin
# from firebase_admin import credentials, firestore

PLUGIN_NAME = "SSF Tally"
PLUGIN_VERSION = "0.1"

# Global instance of the SSF_Handler class
ssf_handler: Optional["SSF_Handler"] = None


class SSF_Handler:
    """
    Main class handling all logic for tracking BGS contributions to
    the 'Sirius Special Forces' faction and uploading them to an online DB.

    Attributes:
        plugin_dir (str): The directory where the plugin is located.
        target_faction (str): The name of the faction to track. Defaults to 'Sirius Special Forces'.
        commander_stats (Dict[str, Dict[str, int]]): A nested dict storing stats per commander.
            Example:
            {
                "CMDR Name": {
                    "tradeProfit": 0,
                    "bountyClaims": 0,
                    "bondClaims": 0,
                    "missionsCompleted": 0,
                    "combatZones": 0,
                    ...
                },
                ...
            }
    """

    def __init__(self, plugin_dir: str, target_faction: str = "Sirius Special Forces") -> None:
        """
        Initialize the SSF_Handler instance.

        Args:
            plugin_dir (str): Path to the directory containing this plugin.
            target_faction (str): The faction name we care about. Defaults to 'Sirius Special Forces'.
        """
        self.plugin_dir: str = plugin_dir
        self.target_faction: str = target_faction

        # Holds commander stats in memory; you may want to load from disk if you have a local cache
        self.commander_stats: Dict[str, Dict[str, int]] = {}

        # Optionally, initialize Firebase or other DB connections here:
        # self._init_firebase()

    def _init_firebase(self) -> None:
        """
        Initialize Firebase connections and credentials.
        This is a stub—fill in your actual Firebase logic here.
        """
        # Example for Firebase Admin SDK:
        # cred = credentials.Certificate("/path/to/your-service-account.json")
        # firebase_admin.initialize_app(cred)
        # self.db = firestore.client()
        pass

    def handle_journal_entry(self, cmdr: str, entry: Dict[str, Any]) -> None:
        """
        Process a single journal entry and update stats if it involves the target faction.

        Args:
            cmdr (str): Commander name.
            entry (Dict[str, Any]): The journal entry payload.
        """
        if cmdr not in self.commander_stats:
            # Initialize stats for this commander
            self.commander_stats[cmdr] = {
                "tradeProfit": 0,
                "bountyClaims": 0,
                "bondClaims": 0,
                "missionsCompleted": 0,
                "combatZones": 0
            }

        event = entry.get("event", "")
        # Example: Bounty claim
        if event == "Bounty":
            rewards = entry.get("Rewards", [])
            for reward in rewards:
                faction = reward.get("Faction", "")
                amount = reward.get("Reward", 0)
                if faction == self.target_faction:
                    self.commander_stats[cmdr]["bountyClaims"] += amount
                    self.upload_data_to_server(cmdr)

        # Example: Combat bond
        elif event == "RedeemVoucher":
            vouchertype = entry.get("Type", "")
            faction = entry.get("Faction", "")
            amount = entry.get("Amount", 0)
            if vouchertype == "CombatBond" and faction == self.target_faction:
                self.commander_stats[cmdr]["bondClaims"] += amount
                self.upload_data_to_server(cmdr)

        # Example: Mission completed
        elif event == "MissionCompleted":
            faction = entry.get("Faction", "")
            if faction == self.target_faction:
                self.commander_stats[cmdr]["missionsCompleted"] += 1
                self.upload_data_to_server(cmdr)

        # Example: Market Sell / Buy for trade profit
        elif event in ["MarketSell", "MarketBuy"]:
            station_faction = entry.get("StationFaction", "")
            if station_faction == self.target_faction:
                if event == "MarketSell":
                    profit = entry.get("TotalSale", 0)
                    self.commander_stats[cmdr]["tradeProfit"] += profit
                    self.upload_data_to_server(cmdr)
                elif event == "MarketBuy":
                    cost = entry.get("TotalCost", 0)
                    # If you want to consider MarketBuy as negative profit:
                    self.commander_stats[cmdr]["tradeProfit"] -= cost
                    self.upload_data_to_server(cmdr)

        # Example: Conflict Zone kill bond
        elif event == "FactionKillBond":
            awarding_faction = entry.get("AwardingFaction", "")
            reward = entry.get("Reward", 0)
            if awarding_faction == self.target_faction:
                self.commander_stats[cmdr]["combatZones"] += reward
                self.upload_data_to_server(cmdr)

    def upload_data_to_server(self, cmdr: str) -> None:
        """
        Upload the stats for the given commander to the online DB.

        Args:
            cmdr (str): Commander name whose data to upload.
        """
        data = self.commander_stats[cmdr]
        # Stub: Replace with your actual DB logic (Firebase, REST API, etc.)
        # Example if using a REST endpoint:
        # response = requests.post("https://your-api-server.com/update", json={
        #     "commander": cmdr,
        #     "stats": data
        # })
        #
        # If using Firebase Firestore:
        # self.db.collection("commanders").document(cmdr).set(data, merge=True)
        print(f"Uploading stats for {cmdr}: {data}")

    def handle_plugin_update(self, cmdr: str, market_json: Dict[str, Any], ship_json: Dict[str, Any],
                             outpost_json: Dict[str, Any]) -> None:
        """
        Handle updates from the EDMC companion API.

        Args:
            cmdr (str): Commander name.
            market_json (Dict[str, Any]): Market data from EDMC.
            ship_json (Dict[str, Any]): Ship data from EDMC.
            outpost_json (Dict[str, Any]): Outpost data from EDMC.
        """
        # If you want to parse the market/ship/outpost data to track trades or other stats,
        # do so here. This is a stub.
        pass

    def fetch_leaderboard(self) -> Dict[str, Dict[str, int]]:
        """
        Fetch the latest leaderboard from the online DB, or return local stats.

        Returns:
            Dict[str, Dict[str, int]]: A dictionary containing commander stats from the DB.
        """
        # If you store everything online, do a GET request or Firebase query.
        # For now, just return the local dictionary as a placeholder.
        # Example:
        # response = requests.get("https://your-api-server.com/leaderboard")
        # leaderboard = response.json()
        # return leaderboard
        return self.commander_stats

    def save_local_data(self) -> None:
        """
        Save local data (commander_stats) to disk as a simple backup/cache.

        This is optional but recommended if you want to preserve data between sessions.
        """
        # Example: Save to a JSON file in the plugin directory.
        file_path = f"{self.plugin_dir}/ssf_tally_data.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.commander_stats, f, indent=2)
        print("Local SSF data saved.")

    def load_local_data(self) -> None:
        """
        Load previously saved local data (commander_stats) from disk, if present.
        """
        file_path = f"{self.plugin_dir}/ssf_tally_data.json"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.commander_stats = json.load(f)
            print("Local SSF data loaded.")
        except FileNotFoundError:
            # No local file yet, that's fine.
            pass


#
# EDMC Plugin Lifecycle Functions
# These are the standard plugin entry points for EDMC.
#

def plugin_start3(plugin_dir: str) -> str:
    """
    Called by EDMC when the plugin is loaded.

    Args:
        plugin_dir (str): The directory where the plugin is located.

    Returns:
        str: A string to identify the plugin in EDMC's log.
    """
    global ssf_handler
    print(f"{PLUGIN_NAME} v{PLUGIN_VERSION} starting up...")
    ssf_handler = SSF_Handler(plugin_dir)
    # Optionally load local data or do other init tasks
    ssf_handler.load_local_data()
    return f"{PLUGIN_NAME} v{PLUGIN_VERSION}"


def plugin_stop() -> None:
    """
    Called by EDMC when the plugin is about to be unloaded.
    Use this to do any cleanup or final data saves.
    """
    global ssf_handler
    print(f"{PLUGIN_NAME} stopping...")
    if ssf_handler:
        ssf_handler.save_local_data()
    ssf_handler = None


def plugin_prefs(parent: tk.Frame, cmdr: str, is_beta: bool) -> tk.Frame:
    """
    Build the plugin's preferences UI (Preferences tab in EDMC).

    Args:
        parent (tk.Frame): The parent TK frame.
        cmdr (str): The current commander name (EDMC supplies this).
        is_beta (bool): True if running in beta mode.

    Returns:
        tk.Frame: The frame containing any preference widgets.
    """
    frame = tk.Frame(parent)
    tk.Label(frame, text="SSF Tally Plugin Settings").grid(row=0, column=0, sticky=tk.W)

    # Example: Add text field or config for server URL / API key
    # ...
    return frame


def plugin_app(parent: tk.Frame) -> tk.Frame:
    """
    Build a small UI in the main EDMC window, if desired.

    Args:
        parent (tk.Frame): The parent TK frame.

    Returns:
        tk.Frame: The frame for this plugin's UI.
    """
    frame = tk.Frame(parent, borderwidth=1, relief="groove")
    label = tk.Label(frame, text="SSF Tally Leaderboard")
    label.pack()

    # Example: A refresh button to fetch the leaderboard from server
    def refresh_leaderboard_ui() -> None:
        if ssf_handler:
            leaderboard_data = ssf_handler.fetch_leaderboard()
            # Display it in some way, e.g. in a popup or a label
            print("Leaderboard:", leaderboard_data)

    btn_refresh = tk.Button(frame, text="Refresh Leaderboard", command=refresh_leaderboard_ui)
    btn_refresh.pack()
    return frame


def plugin_update(cmdr: str, is_beta: bool, system: str, station: str,
                  market_json: Dict[str, Any], ship_json: Dict[str, Any],
                  outpost_json: Dict[str, Any]) -> None:
    """
    Called by EDMC when new data is available from the companion API (e.g. commodity market).

    Args:
        cmdr (str): Commander name.
        is_beta (bool): True if running in beta mode.
        system (str): Current star system name.
        station (str): Current station name.
        market_json (Dict[str, Any]): Market data.
        ship_json (Dict[str, Any]): Ship data.
        outpost_json (Dict[str, Any]): Outpost data.
    """
    if ssf_handler:
        ssf_handler.handle_plugin_update(cmdr, market_json, ship_json, outpost_json)


def journal_entry(cmdr: str, is_beta: bool, system: str, station: str,
                  entry: Dict[str, Any], state: Dict[str, Any]) -> None:
    """
    Called by EDMC for each journal entry.

    Args:
        cmdr (str): Commander name.
        is_beta (bool): True if running in beta mode.
        system (str): Current star system name.
        station (str): Current station name.
        entry (Dict[str, Any]): The journal event data.
        state (Dict[str, Any]): The current game state.
    """
    if ssf_handler:
        ssf_handler.handle_journal_entry(cmdr, entry)

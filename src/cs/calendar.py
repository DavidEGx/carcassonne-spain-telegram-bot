"""Module for Carcassonne Spain Calendar class."""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, TypedDict

from cachetools.func import ttl_cache

from src.cs.player import Player

CACHE_TTL = 3600  # in seconds


class DuelInfo(TypedDict):
    """Duel info type."""

    player_1: Player
    player_2: Player


class RoundData(TypedDict):
    """Round data type."""

    start: datetime
    duels: List[DuelInfo]


class Calendar:
    """Represent a calendar for a group."""

    def __init__(self):
        """Build a calendar."""
        self._calendar: Dict[int, RoundData] = {}

    def add(self, player_1: Player, player_2: Player, duel_round: int, start: datetime):
        """Add game to calendar."""
        if duel_round not in self._calendar:
            self._calendar[duel_round] = {"start": start, "duels": []}

        self._calendar[duel_round]["duels"].append(
            {"player_1": player_1, "player_2": player_2}
        )

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def current_round(self) -> int:
        """Return the current round."""
        for duel_round, data in self._calendar.items():
            start = data["start"]
            end = start + timedelta(days=7)

            if start <= datetime.now(timezone.utc) <= end:
                return duel_round

        return 0

    def duels(self, duel_round: int) -> List[DuelInfo]:
        """Return duels for a given round."""
        return self._calendar[duel_round]["duels"]

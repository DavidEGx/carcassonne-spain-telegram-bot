"""Module for Carcassonne Spain Group class."""
import csv
from datetime import date, datetime
from urllib import request
from cachetools.func import ttl_cache

from src.settings import config, logger
from src.cs.player import Player
from src.cs.duel import Duel

CACHE_TTL = 3600  # in seconds


# pyright: strict
class Group:
    """Represent a group.

    A group within the tournament contains
    a list of players that play against each other.
    Therefore also contains duels between those players,
    some already played, some that will be played in the future.
    """

    def __init__(self, name: str):
        """Build a group."""
        self.name = name

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def players(self) -> list[Player]:
        """List of players within the group."""
        logger.info(f"Fetching players for {self} group")

        url = config['groups'][self.name]['players']
        with request.urlopen(url) as resp:
            lines = [line.decode('utf-8') for line in resp.readlines()]
            return [Player(int(row['id']), row['name'])
                    for row in csv.DictReader(lines)]

    def _find_player(self, name: str) -> Player:
        """Find a player given its name."""
        for player in self.players:
            if player.name == name:
                return player

        raise LookupError(f"Player '{name}' not found in group {self}")

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def schedule(self) -> list[Duel]:
        """Duels scheduled for the group."""
        logger.info(f"Fetching schedule for {self} group")

        schedule: list[Duel] = []
        url = config['groups'][self.name]['schedule']
        with request.urlopen(url) as resp:
            lines = [line.decode('utf-8') for line in resp.readlines()]
            for row in csv.DictReader(lines):
                player_1 = self._find_player(row['player1'])
                player_2 = self._find_player(row['player2'])

                date_str = f'{row["date"]} {row["time"]}'
                ddate = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')

                schedule.append(Duel(p1=player_1,
                                     p2=player_2,
                                     duel_date=ddate))

            return schedule

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def outcome(self) -> list[Duel]:
        """Duels already played within group."""
        logger.info(f"Fetching outcome for {self} group")

        outcome: list[Duel] = []
        url = config['groups'][self.name]['results']
        with request.urlopen(url) as resp:
            lines = [line.decode('utf-8') for line in resp.readlines()]

            for row in csv.DictReader(lines):
                player_1 = self._find_player(row['player1'])
                player_2 = self._find_player(row['player2'])
                date_str = row['timestamp']
                ddate = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
                score_1 = int(row['score1'])
                score_2 = int(row['score2'])

                outcome.append(Duel(p1=player_1,
                                    p2=player_2,
                                    duel_date=ddate,
                                    p1_score=score_1,
                                    p2_score=score_2))

            return outcome

    def duels(self,
              query_date: date,
              force_schedule: bool = False) -> list[Duel]:
        """Return ordered duels for a given date.

        If query date is in the future, it will return scheduled duels.
        If query date is in the past, it will return already played duels.
        """
        if force_schedule or query_date >= date.today():
            duels = self.schedule
        else:
            duels = self.outcome

        filtered = filter(lambda m: m.duel_date.date() == query_date, duels)
        return sorted(list(filtered), key=lambda m: m.duel_date)

    def __str__(self):
        """Name of the group."""
        return self.name
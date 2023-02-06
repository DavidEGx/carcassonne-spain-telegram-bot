"""Module for Carcassonne Spain Group class."""
import csv
from datetime import date, datetime
from urllib import request
from cachetools.func import ttl_cache

from src.cs.player import Player
from src.cs.duel import Duel
from src.settings import logger

CACHE_TTL = 3600  # in seconds


# pyright: strict
class Group:
    """Represent a group.

    A group within the tournament contains
    a list of players that play against each other.
    Therefore also contains duels between those players,
    some already played, some that will be played in the future.
    """

    def __init__(self, name: str, cnf: dict[str, str]):
        """Build a group."""
        self.name = name
        self.config = cnf

    @property
    def gcalendar_color(self) -> int:
        """Return Google Calendar color Id."""
        return int(self.config.get('gcalendar_color', "8"))

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def players(self) -> list[Player]:
        """List of players within the group."""
        logger.info(f"Fetching players for {self} group")

        url = self.config['players']
        with request.urlopen(url) as resp:
            lines = [line.decode('utf-8') for line in resp.readlines()]
            return [Player(int(row['id']), row['name'])
                    for row in csv.DictReader(lines)]

    def _find_player(self, name: str) -> Player:
        """Find a player given its name."""
        for player in self.players:
            if player.name.lower() == name.lower():
                return player

        raise LookupError(f"Player '{name}' not found in group {self}")

    def _find_scheduled_duel(self, p1: Player, p2: Player) -> Duel:
        for duel in self.schedule:
            if p1 == duel.p1 and p2 == duel.p2:
                return duel

        raise LookupError(f"Duel for {p1} and {p2} not found")

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def schedule(self) -> list[Duel]:
        """Duels scheduled for the group."""
        logger.info(f"Fetching schedule for {self} group")

        schedule: list[Duel] = []
        url = self.config['schedule']
        with request.urlopen(url) as resp:
            lines = [line.decode('utf-8') for line in resp.readlines()]
            for row in csv.DictReader(lines):
                player_1 = self._find_player(row['player1'])
                player_2 = self._find_player(row['player2'])
                timestamp = datetime.strptime(row["timestamp"], '%d/%m/%Y %H:%M:%S')

                date_str = f'{row["date"]} {row["time"]}'
                try:
                    planned = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
                except Exception:
                    planned = datetime.strptime(date_str, '%d/%m/%Y %H:%M')

                schedule.append(Duel(p1=player_1,
                                     p2=player_2,
                                     planned=planned,
                                     schedule_timestamp=timestamp))

            return schedule

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def outcome(self) -> list[Duel]:
        """Duels already played within group."""
        logger.info(f"Fetching outcome for {self} group")

        outcome: list[Duel] = []
        url = self.config['results']
        with request.urlopen(url) as resp:
            lines = [line.decode('utf-8') for line in resp.readlines()]

            for row in csv.DictReader(lines):
                player_1 = self._find_player(row['player1'])
                player_2 = self._find_player(row['player2'])
                date_str = row['timestamp']
                odate = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
                score_1 = int(row['score1'])
                score_2 = int(row['score2'])
                played = not row.get('not played', False)

                try:
                    pduel = self._find_scheduled_duel(player_1, player_2)
                    pdate = pduel.planned
                    sdate = pduel.schedule_timestamp
                except LookupError:
                    pdate = odate
                    sdate = odate

                outcome.append(Duel(p1=player_1,
                                    p2=player_2,
                                    planned=pdate,
                                    schedule_timestamp=sdate,
                                    outcome_timestamp=odate,
                                    p1_score=score_1,
                                    p2_score=score_2,
                                    played=True,
                                    played_for_real=played))

            return outcome

    def duels(self,
              query_date: date,
              force_schedule: bool = False) -> list[Duel]:
        """Return ordered duels for a given date.

        If query date is in the future, it will return scheduled duels.
        If query date is in the past, it will return already played duels.
        """
        if force_schedule or query_date >= date.today():
            all = self.schedule
            duels = filter(lambda m: m.planned.date() == query_date, all)
        else:
            all = self.outcome
            duels = filter(lambda m: m.outcome_timestamp.date() == query_date, all)

        return sorted(list(duels), key=lambda m: m.planned)

    def __str__(self):
        """Name of the group."""
        return self.name

"""Module for Carcassonne Spain Group class."""

import csv
import time
from datetime import date
from urllib import request

from cachetools.func import ttl_cache

from src.bga import BGA
from src.cs.calendar import Calendar
from src.cs.date import utc_datetime
from src.cs.duel import Duel
from src.cs.player import Player
from src.settings import config, logger

CACHE_TTL = 3600  # in seconds


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
        return int(self.config.get("gcalendar_color", "8"))

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def calendar(self) -> Calendar | None:
        """Return calendar for this group."""
        logger.info("Fetching calendar for %s group", self)
        url = self.config.get("calendar", "")

        if not url:
            logger.info("No calendar found")
            return None

        calendar = Calendar()
        for row in self._read_csv(url):
            if not row["player1"] or not row["player2"]:
                continue
            if row["player1"].strip() == "" or row["player2"].strip() == "":
                continue

            start = utc_datetime(row["date"])
            player_1 = self._find_player(row["player1"])
            player_2 = self._find_player(row["player2"])
            duel_round = int(row["round"])

            calendar.add(
                player_1=player_1, player_2=player_2, duel_round=duel_round, start=start
            )

        return calendar

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def players(self) -> list[Player]:
        """List of players within the group."""
        logger.info("Fetching players for %s group", self)

        url = self.config["players"]
        return [
            Player(int(row["id"]), row["name"], row.get("telegram", ""))
            for row in self._read_csv(url)
        ]

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
        logger.info("Fetching schedule for %s group", self)

        schedule: list[Duel] = []
        url = self.config["schedule"]
        for row in self._read_csv(url):
            player_1 = self._find_player(row["player1"])
            player_2 = self._find_player(row["player2"])
            timestamp = utc_datetime(row["timestamp"])
            planned = utc_datetime(f'{row["date"]} {row["time"]}')

            schedule.append(
                Duel(
                    p1=player_1,
                    p2=player_2,
                    planned=planned,
                    schedule_timestamp=timestamp,
                )
            )

        return schedule

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def outcome(self) -> list[Duel]:
        """Duels already played within group."""
        logger.info("Fetching outcome for %s group", self)

        outcome: list[Duel] = []
        url = self.config["results"]

        for row in self._read_csv(url):
            player_1 = self._find_player(row["player1"])
            player_2 = self._find_player(row["player2"])
            odate = utc_datetime(row["timestamp"])
            played = not row.get("not played", False)

            try:
                pduel = self._find_scheduled_duel(player_1, player_2)
                pdate = pduel.planned
                sdate = pduel.schedule_timestamp
            except LookupError:
                pdate = odate
                sdate = odate

            outcome.append(
                Duel(
                    p1=player_1,
                    p2=player_2,
                    planned=pdate,
                    schedule_timestamp=sdate,
                    outcome_timestamp=odate,
                    p1_score=int(row["score1"]),
                    p2_score=int(row["score2"]),
                    played=True,
                    played_for_real=played,
                )
            )

        return outcome

    def unschedule(self) -> list[list[Player]]:
        """Return unscheduled duels."""
        unscheduled: list[list[Player]] = []
        if not self.calendar:
            return unscheduled

        duel_round = self.calendar.current_round - 1
        duels_for_round = self.calendar.duels(duel_round)
        for duel_info in duels_for_round:
            player_1 = duel_info["player_1"]
            player_2 = duel_info["player_2"]
            try:
                self._find_scheduled_duel(player_1, player_2)
            except LookupError:
                unscheduled.append([player_1, player_2])

        return unscheduled

    def duels(self, query_date: date, force_schedule: bool = False) -> list[Duel]:
        """Return ordered duels for a given date.

        If query date is in the future, it will return scheduled duels.
        If query date is in the past, it will return already played duels.
        """
        if force_schedule or query_date >= date.today():
            all_duels = self.schedule
            duels = filter(lambda m: m.planned.date() == query_date, all_duels)
        else:
            all_duels = self.outcome
            duels = filter(
                lambda m: m.outcome_timestamp
                and m.outcome_timestamp.date() == query_date,
                all_duels,
            )

        return sorted(list(duels), key=lambda m: m.planned)

    def wrong_outcome(self, query_date: date) -> list[Duel]:
        """Return duels with outcome that need to be checked."""
        bga = BGA()
        wrong_duels: list[Duel] = []
        for duel in self.duels(query_date):
            if not bga.check_duel(duel):
                wrong_duels.append(duel)
            time.sleep(config["bga"]["interval"])

        return wrong_duels

    def __str__(self):
        """Name of the group."""
        return self.name

    def _read_csv(self, url: str) -> list[dict[str, str]]:
        """Fetch URL and return CSV object."""
        result: list[dict[str, str]] = []

        with request.urlopen(url) as resp:
            lines = [line.decode("utf-8") for line in resp.readlines()]
            csv_reader = csv.DictReader(lines)

            for row in csv_reader:
                result.append(row)

        return result

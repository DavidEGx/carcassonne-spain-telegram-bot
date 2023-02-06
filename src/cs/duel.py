"""Module for Carcassonne Spain Duel class."""
from datetime import datetime, timedelta
from functools import cache
from typing import Any, Optional
import time

from src.cs.player import Player
from src.bga import BGA
from src.settings import config, logger


# pyright: strict
class Game:
    """Represents a game within a duel."""

    def __init__(self, p1_score: int, p2_score: int, elo_win: int):
        """Create game object."""
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.elo_win = elo_win
        self._stats: dict[str, Any] = {}

    @property
    def tie(self) -> bool:
        """Return True if game was a tie."""
        return self.p1_score == self.p2_score

    @property
    def p1_victory(self) -> bool:
        """Return True if player 1 won."""
        return self.p1_score > self.p2_score

    @property
    def p2_victory(self) -> bool:
        """Return True if player 2 won."""
        return self.p2_score > self.p1_score

    @property
    def diff(self) -> int:
        """Return different in points in the game."""
        return self.p1_score - self.p2_score

    @property
    def stats(self) -> dict[str, Any]:
        return self._stats

    @stats.setter
    def stats(self, stats: dict[str, Any]):
        self._stats = stats


class Duel:
    """Represents a duel.

    A duel consists of several games between two players.
    """

    def __init__(self,
                 p1: Player,
                 p2: Player,
                 planned: datetime,
                 schedule_timestamp: datetime,
                 outcome_timestamp: Optional[datetime] = None,
                 p1_score: Optional[int] = None,
                 p2_score: Optional[int] = None,
                 played: bool = False,
                 played_for_real: bool = False):
        """Build a duel.

        Parameters
        ----------
            p1 Player acting as host.
            p2 Player acting as visitor.
            planned Planned datetime for a duel
            schedule_timestamp When the duel was scheduled
            outcome_timestamp Datetime when results were submitted
            p1_score Score of player 1 (If the duel was played already)
            p1_score Score of player 2 (If the duel was played already)
            played: True if the duel was played
            played_for_real: Same as played except when one player didn't show
                             (In that case played=True, played_for_real=False)
        """
        self.p1 = p1
        self.p2 = p2
        self.planned = planned
        self.schedule_timestamp = schedule_timestamp
        self.outcome_timestamp = outcome_timestamp
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.played = played
        self.played_for_real = played_for_real
        self._url = None

    @property
    @cache
    def games(self) -> list[Game]:
        """Return games within this duel."""
        bga = BGA()
        games: list[Game] = []
        tables = bga.fetch_tables(self)

        for table in tables:
            p1, p2 = [x.lower() for x in table['player_names'].split(',')]
            s1, s2 = [int(x) for x in table['scores'].split(',')]
            elo_win = int(table['elo_win'])

            if p1 == self.p1.name.lower():
                game = Game(s1, s2, elo_win)
            elif p2 == self.p1.name.lower():
                game = Game(s2, s1, elo_win)
            else:
                raise ValueError(f"Wrong players {p1}, {p2} for duel {self}")

            game.stats = bga.fetch_table_stats(int(table['table_id']))
            games.append(game)
            # stats['reflexion_time']['values'][self.p1.id]
            # stats['reflexion_time']['values'][self.p2.id]
            # stats['points_road']['values'][self.p1.id]
            # stats['points_road']['values'][self.p2.id]
            # stats['points_city']['values'][self.p1.id]
            # stats['points_city']['values'][self.p2.id]
            # stats['points_abbey']['values'][self.p1.id]
            # stats['points_abbey']['values'][self.p2.id]
            # stats['points_field']['values'][self.p1.id]
            # stats['points_field']['values'][self.p2.id]

        return games

    def valid_outcome(self) -> bool:
        """Return True if the outcome submitted by players matched BGA data."""
        if self.p1_score is None or self.p2_score is None:
            raise ValueError("Game not played yet")

        if not self.played_for_real:
            if len(self.games) == 0:
                return True
            else:
                logger.warn(f"Duel was not played but I found games {self}")
                return False

        tied_games = len([g for g in self.games if g.tie])
        p1_wins = len([g for g in self.games if g.p1_victory])
        p2_wins = len([g for g in self.games if g.p2_victory])

        if not ((p1_wins - tied_games) <= self.p1_score <= (p1_wins + tied_games)):
            logger.warn(f"Wrong score for duel {self}")
            return False

        if not((p2_wins - tied_games) <= self.p2_score <= (p2_wins + tied_games)):
            logger.warn(f"Wrong score for duel {self}")
            return False

        return True

    @property
    def winner(self) -> Player:
        """Return winner of the Duel."""
        if self.p1_score is None or self.p2_score is None:
            raise ValueError("Game not played yet")

        if self.p1_score > self.p2_score:
            return self.p1
        else:
            return self.p2

    @property
    def games_landslide_score(self) -> int:
        """Return big number for landslide duel. Small for tight duel."""
        if (self.p1_score == 2 and self.p2_score == 0) or \
           (self.p2_score == 2 and self.p1_score == 0):
            # 2-0 game, add extra 200 so these games are
            # the ones with higher landslide_score.
            return 200 + abs(self.games_score_diff)
        else:
            # 2-1 games.
            # Give last game more importance ading score again.
            return (
                abs(self.games_score_diff) +
                abs(self.games[2].diff)
            )

    @property
    def games_score_diff(self) -> int:
        """Return added difference for scores in each played game."""
        return sum([game.diff for game in self.games])

    @property
    def games_elo_diff(self) -> int:
        """Return added difference for elo in each played game."""
        return sum([game.elo_win for game in self.games])

    @property
    def p1_abbey_score(self) -> int:
        return sum([int(g.stats['points_abbey']['values'][str(self.p1.id)]) for g in self.games])

    @property
    def p2_abbey_score(self) -> int:
        return sum([int(g.stats['points_abbey']['values'][str(self.p2.id)]) for g in self.games])

    @property
    def p1_field_score(self) -> int:
        return sum([int(g.stats['points_field']['values'][str(self.p1.id)]) for g in self.games])

    @property
    def p2_field_score(self) -> int:
        return sum([int(g.stats['points_field']['values'][str(self.p2.id)]) for g in self.games])

    @property
    def p1_road_score(self) -> int:
        return sum([int(g.stats['points_road']['values'][str(self.p1.id)]) for g in self.games])

    @property
    def p2_road_score(self) -> int:
        return sum([int(g.stats['points_road']['values'][str(self.p2.id)]) for g in self.games])

    @property
    def url(self) -> Optional[str]:
        """BGA url of a given duel."""
        if self._url:
            return self._url

        ddate = self.outcome_timestamp or self.planned
        base_url = config['bga']['urls']['outcome_link']
        start = int(time.mktime(ddate.date().timetuple()))
        end = int(time.mktime((ddate.date() + timedelta(days=1)).timetuple()))
        self._url = base_url.format(self.p1.id, self.p2.id, start, end)
        return self._url

    def html(self):
        """HTML representation of the game."""
        if self.p1_score is None:
            p1_html = self.p1.html()
            p2_html = self.p2.html()
            time_str = self.planned.time().strftime("%H:%M")
            return f'{p1_html} - {p2_html}: {time_str}'

        return (f'{self.p1.name} <a href="{self.url}">'
                f'{self.p1_score} - {self.p2_score}'
                f'</a> {self.p2.name}')

    def __str__(self):
        """Duel formatted like "{player_1} - {player_2}."""
        p1_str = self.p1.name
        p2_str = self.p2.name

        if self.p1_score is None:
            time_str = self.planned.time().strftime("%H:%M")
            return f"{p1_str} - {p2_str}: {time_str}"

        return f"{p1_str} {self.p1_score} - {self.p2_score} {p2_str}"

    def __repr__(self):
        """Duel formatted properly."""
        p1_str = repr(self.p1)
        p2_str = repr(self.p2)
        pdate = self.planned
        sdate = self.schedule_timestamp
        odate = f"'{self.outcome_timestamp}'" \
                if self.outcome_timestamp else 'None'

        return (f"Duel({p1_str}, {p2_str}, {pdate}, {sdate}, {odate},"
                f"{self.p1_score}, {self.p2_score})")

    def __eq__(self, other: object) -> bool:
        """Hopefully sensible eq method for Duel."""
        if not isinstance(other, self.__class__):
            return False

        return (self.p1 == other.p1 and
                self.p2 == other.p2 and
                self.p1_score == other.p1_score and
                self.p2_score == other.p2_score and
                self.planned == other.planned and
                self.schedule_timestamp == other.schedule_timestamp and
                self.outcome_timestamp == other.outcome_timestamp)

    def __hash__(self):
        """Return hash of this object."""
        return hash(self.__repr__())

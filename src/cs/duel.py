"""Module for Carcassonne Spain Duel class."""
from datetime import datetime, timedelta
from typing import Optional
import time

from src.settings import config
from src.cs.player import Player


# pyright: strict
class Duel:
    """Represents a duel.

    A duel consists of several games between two players.
    """

    def __init__(self,
                 p1: Player,
                 p2: Player,
                 duel_date: datetime,
                 p1_score: Optional[int] = None,
                 p2_score: Optional[int] = None,
                 played: bool = False,
                 played_for_real: bool = False):
        """Build a duel.

        Parameters
        ----------
            p1 Player acting as host.
            p2 Player acting as visitor.
            duel_date Approximate date of the duel.
            p1_score Score of player 1 (If the duel was played already)
            p1_score Score of player 2 (If the duel was played already)
            played: True if the duel was played
            played_for_real: Same as played except when one player didn't show
                             (In that case played=True, played_for_real=False)
        """
        self.p1 = p1
        self.p2 = p2
        self.duel_date = duel_date
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.played = played
        self.played_for_real = played_for_real
        self._url = None

    @property
    def url(self) -> Optional[str]:
        """BGA url of a given duel."""
        if self._url:
            return self._url

        ddate = self.duel_date
        base_url = config['bga']['urls']['outcome_link']
        start = int(time.mktime(ddate.date().timetuple()))
        end = int(time.mktime((ddate.date() + timedelta(days=1)).timetuple()))
        self._url = base_url.format(self.p1.id, self.p2.id, start, end)
        return self._url

    def html(self):
        """HTML representation of the game."""
        p1_html = self.p1.html()
        p2_html = self.p2.html()
        url = self.url
        time_str = self.duel_date.time().strftime("%H:%M")

        if self.p1_score is None:
            return f'{p1_html} - {p2_html}: {time_str}'

        return (f'{self.p1.name} <a href="{url}">'
                f'{self.p1_score} - {self.p2_score}'
                f'</a> {self.p2.name}')

    def __str__(self):
        """Duel formatted like "{player_1} - {player_2}."""
        p1_str = self.p1.name
        p2_str = self.p2.name

        if self.p1_score is None:
            time_str = self.duel_date.time().strftime("%H:%M")
            return f"{p1_str} - {p2_str}: {time_str}"

        return f"{p1_str} {self.p1_score} - {self.p2_score} {p2_str}"

    def __repr__(self):
        """Duel formatted properly."""
        p1_str = repr(self.p1)
        p2_str = repr(self.p2)
        ddate = f"'{self.duel_date}'" if self.duel_date else 'None'
        return (f"Duel({p1_str}, {p2_str}, {ddate}, "
                f"{self.p1_score}, {self.p2_score})")

    def __eq__(self, other: object) -> bool:
        """Hopefully sensible eq method for Duel."""
        if not isinstance(other, self.__class__):
            return False

        return (self.p1 == other.p1 and
                self.p2 == other.p2 and
                self.p1_score == other.p1_score and
                self.p2_score == other.p2_score and
                self.duel_date == other.duel_date)

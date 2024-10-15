"""Test Carcassonne Spain classes."""

import unittest
from datetime import date
from unittest.mock import patch

from src.cs.date import utc_datetime
from src.cs.duel import Duel
from src.cs.group import Group
from src.cs.league import League
from src.cs.player import Player
from tests.utils.mock import read_csv


@patch.object(Group, "_read_csv", read_csv)
class TestCS(unittest.TestCase):
    """Simple tests for Carcassonne Spain classes."""

    def test_players(self):
        """Check I can fetch players from a group."""
        expected = [
            Player(88229201, "alesiv"),
            Player(86272013, "Alfamar"),
            Player(89754915, "Carquinyolis"),
            Player(84486751, "estroncio"),
            Player(88183195, "gudul"),
            Player(85244368, "inigomartinez"),
            Player(88929304, "IQIUB"),
            Player(84343035, "JulianoApostata"),
            Player(86256371, "LOKU_ELO"),
            Player(85173793, "MadCan"),
            Player(85058291, "Manel_m_l"),
            Player(87670119, "migcrack"),
            Player(37324330, "oscaridis"),
            Player(88890760, "RaKaRoT"),
            Player(90496787, "texe1"),
            Player(88262806, "valle13"),
            Player(84874870, "ziamat"),
            Player(11329731, "Zokanero"),
        ]

        got = League(season=2).group("Élite").players
        self.assertEqual(got, expected)

    def test_duels(self):
        """Check duels for a given day are returned correctly."""
        league = League(season=2)
        mydate = date.fromisoformat("2022-11-01")

        with self.subTest(i="outcome"):
            expected = [
                Duel(
                    Player(86256371, "LOKU_ELO"),
                    Player(88262806, "valle13"),
                    utc_datetime("2022-11-01 22:00:00"),
                    utc_datetime("2022-10-31 19:41:01"),
                    utc_datetime("2022-11-01 22:26:50"),
                    2,
                    0,
                ),
                Duel(
                    Player(88929304, "IQIUB"),
                    Player(37324330, "oscaridis"),
                    utc_datetime("2022-11-01 22:00:00"),
                    utc_datetime("2022-10-30 22:34:10"),
                    utc_datetime("2022-11-01 22:34:04"),
                    1,
                    2,
                ),
            ]

            got = league.group("Élite").duels(mydate)
            self.assertEqual(got, expected)

        with self.subTest(i="schedule"):
            expected = [
                Duel(
                    Player(89619167, "ChicaPop"),
                    Player(83824802, "Fer_Nandet"),
                    utc_datetime("2022-11-01 11:00:00"),
                    utc_datetime("2022-11-01 09:19:03"),
                ),
                Duel(
                    Player(91775060, "dgsenande"),
                    Player(89456958, "Srta Meeple"),
                    utc_datetime("2022-11-01 19:00:00"),
                    utc_datetime("2022-10-30 18:01:27"),
                ),
                Duel(
                    Player(86463243, "FEIFER90"),
                    Player(1680842, "Fisiquito88"),
                    utc_datetime("2022-11-01 21:30:00"),
                    utc_datetime("2022-10-28 22:53:49"),
                ),
            ]

            got = league.group("Rojo").duels(mydate, force_schedule=True)
            self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main()

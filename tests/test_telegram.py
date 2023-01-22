"""Test Telegram messages."""
import unittest
from datetime import date
from src.io.telegramCS import Telegram


# pyright: strict
class TestTelegram(unittest.TestCase):
    """Test Telegram messages."""

    def test_schedule(self):
        """Check I get the right messasge for scheduled duels."""
        telegram = Telegram(season=2)
        mydate = date.fromisoformat('2022-11-01')
        expected = (['⏰ Duelos para hoy ⏰\n\n'
                     'Élite:\n'
                     '<a href="https://boardgamearena.com/player?id=<built-in function id>">IQIUB</a> - <a href="https://boardgamearena.com/player?id=<built-in function id>">oscaridis</a>: <a href="https://boardgamearena.com/gamestats?player=88929304&opponent_id=37324330&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">22:00</a>\n'
                     '<a href="https://boardgamearena.com/player?id=<built-in function id>">LOKU_ELO</a> - <a href="https://boardgamearena.com/player?id=<built-in function id>">valle13</a>: <a href="https://boardgamearena.com/gamestats?player=86256371&opponent_id=88262806&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">22:00</a>\n\n'
                     'Rojo:\n'
                     '<a href="https://boardgamearena.com/player?id=<built-in function id>">ChicaPop</a> - <a href="https://boardgamearena.com/player?id=<built-in function id>">Fer_Nandet</a>: <a href="https://boardgamearena.com/gamestats?player=89619167&opponent_id=83824802&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">11:00</a>\n'
                     '<a href="https://boardgamearena.com/player?id=<built-in function id>">dgsenande</a> - <a href="https://boardgamearena.com/player?id=<built-in function id>">Srta Meeple</a>: <a href="https://boardgamearena.com/gamestats?player=91775060&opponent_id=89456958&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">19:00</a>\n'
                     '<a href="https://boardgamearena.com/player?id=<built-in function id>">FEIFER90</a> - <a href="https://boardgamearena.com/player?id=<built-in function id>">Fisiquito88</a>: <a href="https://boardgamearena.com/gamestats?player=86463243&opponent_id=1680842&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">21:30</a>'])

        got = telegram.create_msg(mydate, force_schedule=True)
        self.assertEqual(got, expected)

    def test_outcome(self):
        """Check I get the right messasge for played duels."""
        telegram = Telegram(season=2)
        mydate = date.fromisoformat('2022-11-01')
        expected = (['📡 Últimos resultados 📡\n\n'
                     'Élite:\n'
                     'LOKU_ELO <a href="https://boardgamearena.com/gamestats?player=86256371&opponent_id=88262806&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">2 - 0</a> valle13\n'
                     'IQIUB <a href="https://boardgamearena.com/gamestats?player=88929304&opponent_id=37324330&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">1 - 2</a> oscaridis\n\n'
                     'Rojo:\n'
                     'ChicaPop <a href="https://boardgamearena.com/gamestats?player=89619167&opponent_id=83824802&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">0 - 2</a> Fer_Nandet\n'
                     'dgsenande <a href="https://boardgamearena.com/gamestats?player=91775060&opponent_id=89456958&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">2 - 0</a> Srta Meeple\n'
                     'FEIFER90 <a href="https://boardgamearena.com/gamestats?player=86463243&opponent_id=1680842&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">1 - 2</a> Fisiquito88'])

        got = telegram.create_msg(mydate)
        self.assertEqual(got, expected)

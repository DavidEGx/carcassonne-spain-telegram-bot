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
        expected = (['<b><a href="https://docs.google.com/spreadsheets/d/e/2PACX-1vTQgViRubR7qSeJubBOYR335aVaLBdD9jpxkqqIb-KRC1u4iUt7rtCs4j_zY_zC8ycLKO95u98TFgVC/pubhtml">⏰ Duelos para hoy ⏰</a></b>\n\n'
                     '<b>Élite</b>:\n'
                     '<a href="https://boardgamearena.com/player?id=88929304">IQIUB</a> - <a href="https://boardgamearena.com/player?id=37324330">oscaridis</a>: 22:00\n'
                     '<a href="https://boardgamearena.com/player?id=86256371">LOKU_ELO</a> - <a href="https://boardgamearena.com/player?id=88262806">valle13</a>: 22:00\n\n'
                     '<b>Rojo</b>:\n'
                     '<a href="https://boardgamearena.com/player?id=89619167">ChicaPop</a> - <a href="https://boardgamearena.com/player?id=83824802">Fer_Nandet</a>: 11:00\n'
                     '<a href="https://boardgamearena.com/player?id=91775060">dgsenande</a> - <a href="https://boardgamearena.com/player?id=89456958">Srta Meeple</a>: 19:00\n'
                     '<a href="https://boardgamearena.com/player?id=86463243">FEIFER90</a> - <a href="https://boardgamearena.com/player?id=1680842">Fisiquito88</a>: 21:30'])

        got = telegram.create_msg(mydate, force_schedule=True)
        self.assertEqual(got, expected)

    def test_outcome(self):
        """Check I get the right messasge for played duels."""
        telegram = Telegram(season=2)
        mydate = date.fromisoformat('2022-11-01')
        expected = (['<b>📡 Últimos resultados 📡</b>\n\n'
                     '<b>Élite</b>:\n'
                     'LOKU_ELO <a href="https://boardgamearena.com/gamestats?player=86256371&opponent_id=88262806&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">2 - 0</a> valle13\n'
                     'IQIUB <a href="https://boardgamearena.com/gamestats?player=88929304&opponent_id=37324330&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">1 - 2</a> oscaridis\n\n'
                     '<b>Rojo</b>:\n'
                     'ChicaPop <a href="https://boardgamearena.com/gamestats?player=89619167&opponent_id=83824802&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">0 - 2</a> Fer_Nandet\n'
                     'dgsenande <a href="https://boardgamearena.com/gamestats?player=91775060&opponent_id=89456958&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">2 - 0</a> Srta Meeple\n'
                     'FEIFER90 <a href="https://boardgamearena.com/gamestats?player=86463243&opponent_id=1680842&game_id=1&finished=1&start_date=1667260800&end_date=1667347200">1 - 2</a> Fisiquito88'])

        got = telegram.create_msg(mydate)
        self.assertEqual(got, expected)

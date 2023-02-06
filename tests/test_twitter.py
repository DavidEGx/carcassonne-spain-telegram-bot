"""Test Twitter messages."""
import unittest
from datetime import date
from src.io.twitter import Twitter


# pyright: strict
class TestTwitter(unittest.TestCase):
    """Test Twitter messages."""

    def test_schedule(self):
        """Check I get the right message for scheduled duels."""
        twitter = Twitter(season=2)

        with self.subTest(i="Single Msg"):
            mydate = date.fromisoformat('2022-11-01')
            expected = [("\n⏰ Duelos para hoy #LigaCarcassonneSpain ⏰\n\n"
                         "𝗘́𝗹𝗶𝘁𝗲:\n"
                         "IQIUB - oscaridis: 22:00\n"
                         "LOKU_ELO - valle13: 22:00\n\n"
                         "𝗥𝗼𝗷𝗼:\n"
                         "ChicaPop - Fer_Nandet: 11:00\n"
                         "dgsenande - Srta Meeple: 19:00\n"
                         "FEIFER90 - Fisiquito88: 21:30")]

            got = twitter.create_msg(mydate, force_schedule=True)
            self.assertEqual(got, expected)

        with self.subTest(i="Split Msg"):
            mydate = date.fromisoformat('2022-11-15')
            expected = [("\n⏰ Duelos para hoy #LigaCarcassonneSpain ⏰\n\n"
                         "𝗘́𝗹𝗶𝘁𝗲:\n"
                         "gudul - ziamat: 20:00\n"
                         "MadCan - RaKaRoT: 20:30\n\n"
                         "𝗔𝘇𝘂𝗹:\n"
                         "senglar - camares: 15:00\n"
                         "senglar - Deskey: 19:00\n"
                         "2020Rafa - thePOC: 22:00\n"
                         "Presmanes - danisvh: 22:30"),
                        (
                         "\n𝗥𝗼𝗷𝗼:\n"
                         "Rolente - dgsenande: 19:00\n"
                         "saizechezarreta - Elige Juego: 22:00\n\n"
                         "𝗩𝗲𝗿𝗱𝗲:\n"
                         "Douglasgti - Felipelpm: 20:30\n"
                         "Jsoutinho - Miguel Eiffel: 21:00\n"
                         "Ardacho - Algueroth: 21:45\n"
                         "Pandemias86 - cesarhf73: 22:45")]

            got = twitter.create_msg(mydate, force_schedule=True)
            self.assertEqual(got, expected)

    def test_outcome(self):
        """Check I get the right message for played duels."""
        twitter = Twitter(season=2)

        with self.subTest(i="Single Msg"):
            mydate = date.fromisoformat('2022-11-01')
            expected = [("\n📡 Últimos resultados #LigaCarcassonneSpain 📡\n\n"
                         "𝗘́𝗹𝗶𝘁𝗲:\n"
                         "LOKU_ELO 2 - 0 valle13\n"
                         "IQIUB 1 - 2 oscaridis\n\n"
                         "𝗥𝗼𝗷𝗼:\n"
                         "ChicaPop 0 - 2 Fer_Nandet\n"
                         "dgsenande 2 - 0 Srta Meeple\n"
                         "FEIFER90 1 - 2 Fisiquito88")]

            got = twitter.create_msg(mydate)
            self.assertEqual(got, expected)

        with self.subTest(i="Split Msg"):
            mydate = date.fromisoformat('2022-11-15')
            expected = [("\n📡 Últimos resultados #LigaCarcassonneSpain 📡\n\n"
                         "𝗘́𝗹𝗶𝘁𝗲:\n"
                         "gudul 2 - 1 ziamat\n"
                         "MadCan 2 - 0 RaKaRoT\n\n"
                         "𝗔𝘇𝘂𝗹:\n"
                         "senglar 2 - 1 camares\n"
                         "senglar 2 - 0 Deskey\n"
                         "2020Rafa 2 - 1 thePOC\n"
                         "Presmanes 0 - 2 danisvh"),
                        (
                         "\n𝗥𝗼𝗷𝗼:\n"
                         "FEIFER90 2 - 0 Pescatore\n"
                         "Rolente 0 - 2 dgsenande\n"
                         "saizechezarreta 0 - 2 Elige Juego\n\n"
                         "𝗩𝗲𝗿𝗱𝗲:\n"
                         "Douglasgti 2 - 0 Felipelpm\n"
                         "Jsoutinho 0 - 2 Miguel Eiffel\n"
                         "Ardacho 2 - 0 Algueroth\n"
                         "Pandemias86 2 - 0 cesarhf73")]

            got = twitter.create_msg(mydate)
            self.assertEqual(got, expected)


if __name__ == '__main__':
    unittest.main()

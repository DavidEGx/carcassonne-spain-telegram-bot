"""Test Twitter messages."""
import unittest
from datetime import date
from src.io.twitter import Twitter


# pyright: strict
class TestTwitter(unittest.TestCase):
    """Test Twitter messages."""

    def test_schedule(self):
        """Check I get the right messasge for scheduled duels."""
        twitter = Twitter(season=2)

        with self.subTest(i="Single Msg"):
            mydate = date.fromisoformat('2022-11-01')
            expected = [("\n⏰ Duelos para hoy ⏰\n\n"
                         "𝗘́𝗹𝗶𝘁𝗲:\n"
                         "IQIUB - oscaridis\n"
                         "LOKU_ELO - valle13\n\n"
                         "𝗥𝗼𝗷𝗼:\n"
                         "ChicaPop - Fer_Nandet\n"
                         "dgsenande - Srta Meeple\n"
                         "FEIFER90 - Fisiquito88")]

            got = twitter.create_msg(mydate, force_schedule=True)
            self.assertEqual(got, expected)

        with self.subTest(i="Split Msg"):
            mydate = date.fromisoformat('2022-11-15')
            expected = [("\n⏰ Duelos para hoy ⏰\n\n"
                         "𝗘́𝗹𝗶𝘁𝗲:\n"
                         "gudul - ziamat\n"
                         "MadCan - RaKaRoT\n\n"
                         "𝗔𝘇𝘂𝗹:\n"
                         "senglar - camares\n"
                         "senglar - Deskey\n"
                         "2020Rafa - thePOC\n"
                         "Presmanes - danisvh\n\n"
                         "𝗥𝗼𝗷𝗼:\n"
                         "Rolente - dgsenande\n"
                         "saizechezarreta - Elige Juego"),
                        ("\n𝗩𝗲𝗿𝗱𝗲:\n"
                         "Douglasgti - Felipelpm\n"
                         "Jsoutinho - Miguel Eiffel\n"
                         "Ardacho - Algueroth\n"
                         "Pandemias86 - cesarhf73")]

            got = twitter.create_msg(mydate, force_schedule=True)
            self.assertEqual(got, expected)

    def test_outcome(self):
        """Check I get the right messasge for played duels."""
        twitter = Twitter(season=2)

        with self.subTest(i="Single Msg"):
            mydate = date.fromisoformat('2022-11-01')
            expected = [("\n📡 Últimos resultados 📡\n\n"
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
            expected = [("\n📡 Últimos resultados 📡\n\n"
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

"""Module for handling connections to Board Game Arena."""
import re
import requests
from cachetools.func import ttl_cache
from functools import cache
from src.cs.duel import Duel
from src.settings import config, logger

CACHE_TTL = 3600  # in seconds


# pyright: strict
@cache
class BGA:
    """Handles connections to BGA to fetch games outcome."""

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def session(self) -> requests.Session:
        """Create a session in BGA so I can make requests.

        Logs in, set headers appropriately, return session.
        """
        bga = config['bga']
        s = requests.Session()

        # First need to fetch some page in order to get request token for login
        # Note: Using a very poor method to extract CSRF ID but... meh
        # Proper way would be to run js code to get `bgaConfig.requestToken`
        r = s.get(bga['urls']['home'])
        csrf_id = re.findall("requestToken:\\ '(.*)'", r.text)[0]  # Bad :(

        # Now I can login
        post_data = {
            'email': bga['user'],
            'password': bga['password'],
            'request_token': csrf_id
        }
        r = s.post(bga['urls']['login'], data=post_data)

        # But before doing anything else I need to get csrf id
        r = s.get(bga['urls']['csrf'])
        csrf_id = re.findall("requestToken:\\ '(.*)'", r.text)[0]  # Bad :(
        s.headers['X-Request-Token'] = csrf_id

        # Finally I can return a session that can be used
        return s

    def check_duel(self, duel: Duel) -> bool:
        """Check submitted outcome for single duel matches reality."""
        base_date = round(duel.duel_date.timestamp())
        start_date = str(base_date - 24 * 1 * 3600)
        end_date = str(base_date + 24 * 1 * 3600)

        bga = config['bga']
        url = bga['urls']['outcome']
        url = url.format(duel.p1.id, duel.p2.id, start_date, end_date)

        r = self.session.get(url)
        tables = r.json()['data']['tables']
        tables = [table for table in tables if table['arena_win'] is None]

        if len(tables) > 3:
            # Remove unranked games if there are more than 3 tables
            tables = [t for t in tables if t['unranked'] == '0']
            if len(tables) > 3:
                # Still more than 3 games, dunno which ones are the good ones
                logger.warn(f"More than 3 games found for {duel}")
                return False

        if not duel.played_for_real:
            # Someone marked the game as not played
            return (len(tables) == 0 and (
                        (duel.p1_score == 2 and duel.p2_score == 0) or
                        (duel.p1_score == 0 and duel.p2_score == 2))
                    )

        if len(tables) < 2:
            # Try older games, maybe game results were submitted late
            start_date = str(base_date - 24 * 3 * 3600)

            url = bga['urls']['outcome']
            url = url.format(duel.p1.id, duel.p2.id, start_date, end_date)

            r = self.session.get(url)
            tables = r.json()['data']['tables']

            if len(tables) < 2:
                # Dunno where are the games
                logger.warn(f"Less than 2 games found for {duel}")
                return False

        p1_real_score = 0
        p2_real_score = 0
        for table in tables:
            p1, p2 = [x.lower() for x in table['player_names'].split(',')]
            r1, r2 = [int(x) for x in table['scores'].split(',')]

            if r1 == r2:
                logger.warn(f"Tie, need to manually check {duel}")
                return False

            if p1 == duel.p1.name.lower() and r1 > r2:
                p1_real_score += 1
            elif p2 == duel.p2.name.lower() and r2 > r1:
                p1_real_score += 1
            else:
                p2_real_score += 1

        if duel.p1_score != p1_real_score or duel.p2_score != p2_real_score:
            logger.warn((f"Wrong score for {duel}, "
                         f"got: {p1_real_score} - {p2_real_score}"))
            return False

        return True

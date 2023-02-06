"""Module for handling connections to Board Game Arena."""
import re
import requests
import time
from cachetools.func import ttl_cache
from functools import cache
from src.settings import config, logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.cs.duel import Duel

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

    def fetch_tables(self, duel: 'Duel') -> list[dict[str, str]]:
        """Fetch BGA game tables for a duel."""
        if duel.outcome_timestamp is None:
            logger.error(f"Duel not played, something went wrong. {duel}")
            return []

        base_date = round(duel.outcome_timestamp.timestamp())
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

        if len(tables) < 2:
            # Try older games, maybe game results were submitted late
            start_date = str(base_date - 24 * 3 * 3600)

            url = bga['urls']['outcome']
            url = url.format(duel.p1.id, duel.p2.id, start_date, end_date)

            r = self.session.get(url)
            tables = r.json()['data']['tables']

        # Sleep to avoid hammering bga
        time.sleep(config['bga']['interval'])
        return tables

    def fetch_table_stats(self, table_id: int) -> list[dict[str, str]]:
        """Fetch game stats."""
        bga = config['bga']
        url = bga['urls']['game_stats']
        url = url.format(table_id)

        r = self.session.get(url)
        stats = r.json()['data']['result']['stats']['player']

        # Sleep to avoid hammering bga
        time.sleep(config['bga']['interval'])
        return stats

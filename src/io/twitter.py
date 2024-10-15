"""Module for Carcassonne Spain Twitter class."""

from datetime import date
from typing import Optional

import tweepy

from src.cs.league import League
from src.io.io_base import IoBase
from src.settings import config, logger


class Twitter(IoBase):
    """Encapsulate all Carcassonne Spain league tweeter communication."""

    def __init__(self, season: Optional[int] = None):
        """Initialize the Tweet object."""
        self.league = League(season)
        self.max_size = 280  # Tweet size

    def _make_bold(self, text: str) -> str:
        # fmt: off
        regular = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                   'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                   'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                   'J', 'K', 'L', 'M', 'N', 'O', 'P', 'K', 'R', 'S', 'T', 'U',
                   'V', 'W', 'X', 'Y', 'Z', 'á', 'é', 'í', 'ó', 'ú', 'Á', 'É',
                   'Í', 'Ó', 'Ú', 'ü', 'Ü']
        bold = ['𝗮', '𝗯', '𝗰', '𝗱', '𝗲', '𝗳', '𝗴', '𝗵', '𝗶', '𝗷', '𝗸', '𝗹',
                '𝗺', '𝗻', '𝗻̃', '𝗼', '𝗽', '𝗾', '𝗿', '𝘀', '𝘁', '𝘂', '𝘃', '𝘄',
                '𝘅', '𝘆', '𝘇', '𝗔', '𝗕', '𝗖', '𝗗', '𝗘', '𝗙', '𝗚', '𝗛', '𝗜',
                '𝗝', '𝗞', '𝗟', '𝗠', '𝗡', '𝗢', '𝗣', '𝗞', '𝗥', '𝗦', '𝗧', '𝗨',
                '𝗩', '𝗪', '𝗫', '𝗬', '𝗭', '𝗮́', '𝗲́', '𝗶́', '𝗼́', '𝘂́', '𝗔́', '𝗘́',
                '𝗜́', '𝗢́', '𝗨́', '𝘂̈', '𝗨̈']
        # fmt: on

        for c_original, c_new in zip(regular, bold):
            text = text.replace(c_original, c_new)

        return text

    def create_msg(self, query_date: date, force_schedule: bool = False) -> list[str]:
        """Create a message containing all the duels for a give date.

        Parameters
        ----------
            query_date You'll get the duels for this date.
            force_schedule If the date is in the past, you'll get the
                           duels outcome for that day.
                           Set this to true to get the duels schedule
                           instead. For testing purposes mainly.
        Returns
        -------
        List of strings. Each string should fit in a single Tweet.
        """
        # Get formatted text for each group
        group_texts: list[str] = []
        for group in self.league.groups:
            name = group.name
            duels = group.duels(query_date, force_schedule)
            if duels:
                body_txt = "\n".join([str(d) for d in duels])
                group_header = self._make_bold(f"\n{name}:\n")
                group_texts.append(f"{group_header}{body_txt}")

        if not group_texts:
            return []

        # Add header to first group
        if force_schedule or query_date >= date.today():
            header = config["twitter"]["header"]["schedule"]
        else:
            header = config["twitter"]["header"]["results"]

        group_texts[0] = header + "\n" + group_texts[0]

        messages = [""]
        # Divide groups in separate messages depending
        # upon text size. Normally all fits in a single tweet,
        # sometimes two.
        for txt in group_texts:
            if len(txt) >= self.max_size:
                # TODO
                print("HELP! FIXME")
                continue

            updated_msg = messages[-1] + f"\n{txt}"
            if len(updated_msg.encode("utf-8")) < self.max_size:
                messages[-1] = updated_msg
            else:
                messages.append(txt)

        return messages

    def send(self, query_date: date, force_schedule: bool = False):
        """Create a Tweet.

        The tweet (or tweets) created will contain the duels
        scheduled for the query_date used, if query_date is the future.
        If query_date is in the past, the tweet will contain the
        outcome of the duels.

        Parameters
        ----------
            query_date You'll get the duels for this date.
            force_schedule Set this to true to get duels schedule
                           even if query_date is in the past.
                           For testing purposes mainly.
        """
        client = tweepy.Client(
            consumer_key=config["twitter"]["api_key"],
            consumer_secret=config["twitter"]["api_key_secret"],
            access_token=config["twitter"]["access_token"],
            access_token_secret=config["twitter"]["access_token_secret"],
        )

        logger.info("Creating tweet for %s", query_date)
        msgs = self.create_msg(query_date, force_schedule)
        if not msgs:
            return

        first_msg = msgs.pop(0)
        response = client.create_tweet(text=first_msg)
        last_tweet_id: int = response.data["id"]
        logger.info("Created tweet %s", last_tweet_id)

        for msg in msgs:
            response = client.create_tweet(text=msg, in_reply_to_tweet_id=last_tweet_id)
            last_tweet_id = response.data["id"]
            logger.info("Created tweet %s", last_tweet_id)

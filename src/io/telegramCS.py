# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2023 David Escribano <davidegx@gmail.com>

"""Telegram message creation."""
import asyncio
from datetime import date
from typing import Optional
from telegram.ext import Application
import telegram

from src.cs.league import League
from src.io.io_base import IoBase
from src.settings import config, logger


# pyright: strict
class Telegram(IoBase):
    """Encapsulate all Carcassonne Spain league telegram communication."""

    def __init__(self, season: Optional[int] = None):
        """Initialize the Telegram object."""
        self.league = League(season)

    def create_msg(self,
                   query_date: date,
                   force_schedule: bool = False) -> list[str]:
        """Return a string corresponding to the expected summary type."""
        html_body = ""
        for group in self.league.groups:
            name = group.name
            duels = group.duels(query_date, force_schedule)
            if duels:
                html_body += f"\n\n<b>{name}</b>:\n"
                html_body += "\n".join([d.html() for d in duels])

        if not html_body:
            return [""]

        # Add header
        if force_schedule or query_date >= date.today():
            header = config['header']['schedule']
        else:
            header = config['header']['results']

        return [f"<b>{header}</b>{html_body}"]

    def send(self, query_date: date, force_schedule: bool = False) -> None:
        """Send Telgram message with duels schedule/outcome for a date."""
        token = config['telegram']['token']
        application = Application.builder().token(token).build()
        bot = application.bot
        asyncio.run(self.send_async(bot, query_date, force_schedule))

    async def send_async(self,
                         bot: telegram.Bot,
                         query_date: date,
                         force_schedule: bool = False):
        """Send Telegram message with duels schedule/outcome for a date."""
        msg = self.create_msg(query_date, force_schedule)[0]

        if not msg:
            return

        for group in config['telegram']['groups']:
            group_id = group['id']
            thread_id = group.get('thread_id')
            logger.info(f'Going to send message to {group_id}')

            await bot.send_message(chat_id=group_id,
                                   text=msg,
                                   message_thread_id=thread_id,
                                   parse_mode=telegram.constants.ParseMode.HTML,
                                   disable_web_page_preview=True)

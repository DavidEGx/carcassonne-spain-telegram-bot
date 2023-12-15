# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2022 Iñigo Martinez <inigomartinez@gmail.com>
# Copyright (C) 2023 David Escribano <davidegx@gmail.com>

"""Module implementing commands supported by the Telegram BOT."""

from datetime import date, datetime, timedelta
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from src.io.telegram_cs import Telegram


def _parse_date(update: Update) -> Optional[date]:
    msg = update.message.text
    params = msg.split(" ")
    if len(params) == 2:
        str_date = params[1]
        try:
            # Try YYYY-mm-dd format
            return date.fromisoformat(str_date)
        except ValueError:
            # Try dd/mm/YY format
            try:
                return datetime.strptime(str_date, "%d/%m/%y").date()
            except ValueError:
                update.message.reply_text(f"Wrong date format {str_date}")

    return None


# pylint: disable=redefined-builtin
async def help(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Describe the set of available commands."""
    await update.message.reply_text(
        """Available Commands :-
    /schedule [dd/mm/yy] - Get duels for a given date (today by default)
    /results [dd/mm/yy] - Get duels outcome for a given date (yesterday by default)"""
    )


# pylint: enable=redefined-builtin


async def schedule(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with the set of the next scheduled duels."""
    query_date = _parse_date(update) or date.today()
    msg = Telegram().create_msg(query_date, force_schedule=True)[0]

    if msg:
        await update.message.reply_html(msg, disable_web_page_preview=True)
    else:
        await update.message.reply_text("Nothing found")


async def results(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with the set of the last results."""
    query_date = _parse_date(update) or date.today() - timedelta(1)
    msg = Telegram().create_msg(query_date)[0]

    if msg:
        await update.message.reply_html(msg, disable_web_page_preview=True)
    else:
        await update.message.reply_text("Nothing found")

# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2022 Iñigo Martinez <inigomartinez@gmail.com>

"""Module implementing commands supported by the BOT."""

from telegram import Update
from telegram.ext import CallbackContext

from src.io import fetch
from src.settings import SUMMARY_DATA


def help(update: Update, context: CallbackContext):
    """Describe the set of available commands."""
    update.message.reply_text("""Available Commands :-
    /schedule - Get next matches
    /results - Get last results""")


def schedule(update: Update, context: CallbackContext):
    """Reply with the set of the next scheduled matches."""
    msg = fetch(**SUMMARY_DATA['schedule'])
    update.message.reply_html(msg, disable_web_page_preview=True)


def results(update: Update, context: CallbackContext):
    """Reply with the set of the last results."""
    msg = fetch(**SUMMARY_DATA['results'])
    update.message.reply_html(msg, disable_web_page_preview=True)

# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2022 Iñigo Martinez <inigomartinez@gmail.com>

from telegram import Update
from telegram.ext import CallbackContext

from src.io import fetch
from src.settings import SUMMARY_DATA


def help(update: Update, context: CallbackContext):
    """Describes the set of available commands."""
    update.message.reply_text("""Available Commands :-
    /schedule - Get next matches
    /results - Get last results""")


def schedule(update: Update, context: CallbackContext):
    """Replies with the set of the next scheduled matches."""
    update.message.reply_html(fetch(**SUMMARY_DATA['schedule']), disable_web_page_preview=True)


def results(update: Update, context: CallbackContext):
    """Replies with the set of the last results."""
    update.message.reply_html(fetch(**SUMMARY_DATA['results']), disable_web_page_preview=True)

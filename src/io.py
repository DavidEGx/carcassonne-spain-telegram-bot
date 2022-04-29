# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2022 David Escribano <davidegx@gmail.com>
# Copyright (C) 2022 Iñigo Martinez <inigomartinez@gmail.com>

"""Module implementing operations of data input and output."""

import csv
import telegram
from telegram.ext import CallbackContext
from typing import Callable
import urllib.request

from src.settings import config, logger, SUMMARY_DATA


def fetch(summary_type: str, function: Callable, text: str) -> str:
    """Return string containing the results in the last 24h."""
    data = {name: [] for name in config['players']['groups']}

    logger.info(f'Going to fetch {summary_type}')
    with urllib.request.urlopen(config['data'][summary_type]) as response:
        for row in csv.reader([line.decode('utf-8')
                               for line in response.readlines()]):
            data[row[0]].append(function(row))

    if not data:
        return ''

    msg = ' '.join([f'\n{name}:\n' + ''.join(rows)
                    for name, rows in data.items()])
    return f'<b>{text}\n{msg}</b>'


def send(context: CallbackContext):
    """Send message to all groups with the results in the last 24h."""
    summary_type = context.job.context
    msg = fetch(**SUMMARY_DATA[summary_type])
    if not msg:
        return

    for group_id in config['telegram']['groups']:
        try:
            logger.info(f'Going to send {summary_type} to {group_id}')
            context.bot.send_message(chat_id=group_id,
                                     text=msg,
                                     parse_mode=telegram.ParseMode.HTML,
                                     disable_web_page_preview=True)
        except telegram.error.TelegramError:
            # Completely ignore error ¯_(ツ)_/¯
            # Changes are that the bot is no longer in the group as
            # bot going out of groups is not being handled (due to laziness).
            logger.error(f'Could not send message to group {group_id}')

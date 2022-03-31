# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2022 David Escribano <davidegx@gmail.com>
# Copyright (C) 2022 Iñigo Martinez <inigomartinez@gmail.com>

import csv
import telegram
import urllib

from src.settings import config, logger, SUMMARY_DATA


def fetch(summary_type, function, text):
    """Return string containing the results in the last 24h."""

    # FIXME: Used dict comprehension instead of `defaultdict(list)` to set a custom order
    data = {name: [] for name in config['players']['groups']}

    logger.info(f'Going to fetch {summary_type}')
    with urllib.request.urlopen(config['data'][summary_type]) as response:
        for row in csv.reader([line.decode('utf-8') for line in response.readlines()]):
            data[row[0]].append(function(row))

    if not data:
        return ''

    message = ' '.join([f'\n{name}:\n' + ''.join(rows) for name, rows in data.items()])
    return f'<b>{text}\n{message}</b>'


def send(context):
    """Send message to all groups with the results in the last 24h."""
    summary_type = context.job.context
    message = fetch(summary_type, **SUMMARY_DATA[summary_type])
    if not message:
        return

    for group_id in config['telegram']['groups']:
        try:
            logger.info(f'Going to send {summary_type} to {group_id}')
            context.bot.send_message(chat_id=group_id,
                                     text=message,
                                     parse_mode=telegram.ParseMode.HTML,
                                     disable_web_page_preview=True)
        except telegram.error.TelegramError:
            # Completely ignore error ¯_(ツ)_/¯
            # Changes are that the bot is no longer in the group as
            # bot going out of groups is not being handled (due to laziness).
            logger.error(f'Could not send message to group {group_id}')
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2022 David Escribano <davidegx@gmail.com>
# Copyright (C) 2022 Iñigo Martinez <inigomartinez@gmail.com>

"""Module implementing operations of data input and output."""

import csv
from datetime import date, datetime, timedelta
from operator import itemgetter
import telegram
from telegram.ext import CallbackContext
import time
from typing import Callable
import urllib.request

from src.settings import config, logger


def __create_player_link(player_id: int) -> str:
    """Return a string containing the player BGA url."""
    return config['bga']['player_url'].format(player_id)


def __create_match_link(local_id: int, visitor_id: int,
                        match_date: datetime) -> str:
    """Return a string containing BGA matches url."""
    start_date = int(time.mktime(match_date.date().timetuple()))
    end_date = int(time.mktime((match_date.date() + timedelta(days=1)).timetuple()))
    return config['bga']['results_url'].format(local_id, visitor_id,
                                               start_date, end_date)


def __create_result_row(players: dict[str, int], result: dict) -> str:
    """Return a string containing the result row."""
    local_id = players[result['local_name']]
    visitor_id = players[result['visitor_name']]
    local_result = result["local_result"]
    visitor_result = result["visitor_result"]
    match_link = __create_match_link(local_id, visitor_id, result['date'])
    return f'{result["local_name"]} ' \
           f'<a href="{match_link}">{local_result} - {visitor_result}</a> ' \
           f'{result["visitor_name"]}'


def __create_schedule_row(players: dict[str, int], row: dict) -> str:
    """Return a string containing the schedule match row."""
    local_id = players[row['local_name']]
    visitor_id = players[row['local_name']]
    local_link = __create_player_link(local_id)
    visitor_link = __create_player_link(visitor_id)
    match_link = __create_match_link(local_id, visitor_id, row['date'])
    time_str = row["date"].time().strftime("%H:%M")
    return f'<a href="{local_link}">{row["local_name"]}</a> - ' \
           f'<a href="{visitor_link}">{row["visitor_name"]}</a>: ' \
           f'<a href="{match_link}">{time_str}</a>'


def __create_group_text(group: str, query_date: datetime,
                        fetch_func: Callable, row_func: Callable) -> str:
    """Return a string containing the text corresponding to a group."""
    players = fetch_group_players(group)
    data = sorted(fetch_func(group, query_date), key=itemgetter('date'))
    return '\n'.join([row_func(players, row) for row in data])


def create_msg(summary_type: str) -> str:
    """Return a string corresponding to the expected summary type."""
    data = fetch(summary_type)
    text = '\n'.join([f'\n{name}:\n' + ''.join(rows)
                      for name, rows in data.items() if rows])

    if not text:
        return ''

    return f'<b>{config["header"][summary_type]}\n{text}</b>'


def fetch_group_players(group: str) -> dict[str, id]:
    """Return a dict with the information of players names and BGA ids."""
    with urllib.request.urlopen(config['groups'][group]['players']) as resp:
        return {row['Nombre']: row['Id']
                for row in csv.DictReader([line.decode('utf-8')
                                           for line in resp.readlines()])}


def fetch_group_results(group, results_date: date) -> list[dict]:
    """Return a list of dicts with the results of a group in a given date."""
    with urllib.request.urlopen(config['groups'][group]['results']) as resp:
        results = [{'date': datetime.strptime(row['Marca temporal'],
                                              '%d/%m/%Y %H:%M:%S'),
                    'matchday': int(row['Nº Jornada']),
                    'local_name': row['Jugador Local'],
                    'visitor_name': row['Jugador Visitante'],
                    'local_result': int(row['Partidas ganadas jugador local']),
                    'visitor_result': int(row['Partidas ganadas jugador visitante'])}
                   for row in csv.DictReader([line.decode('utf-8')
                                              for line in resp.readlines()])]

    return list(filter(lambda r: r['date'].date() == results_date, results))


def fetch_group_schedule(group, results_date: date) -> list[dict]:
    """Return a list of dicts with the schedule of a group in a given date."""
    with urllib.request.urlopen(config['groups'][group]['schedule']) as resp:
        results = [{'date': datetime.strptime(f'{row["Fecha duelo"]} {row["Hora duelo"]}',
                                              '%d/%m/%Y %H:%M:%S'),
                    'matchday': int(row['Nº Jornada']),
                    'local_name': row['Nick BGA anfitrión'],
                    'visitor_name': row['Nick BGA visitante']}
                   for row in csv.DictReader([line.decode('utf-8')
                                              for line in resp.readlines()])]

    return list(filter(lambda r: r['date'].date() == results_date, results))


__SUMMARY_DATA = {
    'results': {
        'fetch': fetch_group_results,
        'row': __create_result_row,
        'delta': timedelta(days=-1)},
    'schedule': {
        'fetch': fetch_group_schedule,
        'row': __create_schedule_row,
        'delta': timedelta()},
}


def fetch(summary_type: str, query_date: date = None) -> dict[str, str]:
    """Return string containing the results in the last 24h."""
    summary_data = __SUMMARY_DATA[summary_type]
    if not query_date:
        query_date = date.today() + summary_data['delta']

    return {group: __create_group_text(group, query_date,
                                       summary_data['fetch'],
                                       summary_data['row'])
            for group in config['groups'].keys()}


def send(context: CallbackContext):
    """Send message to all groups with the results in the last 24h."""
    summary_type = context.job.context
    logger.info(f'Going to fetch {summary_type}')
    msg = create_msg(summary_type)

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

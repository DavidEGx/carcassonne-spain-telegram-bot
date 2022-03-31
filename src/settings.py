# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2022 David Escribano <davidegx@gmail.com>
# Copyright (C) 2022 Iñigo Martinez <inigomartinez@gmail.com>


import logging
import yaml

CONFIG_FILE = 'config.yml'

with open(CONFIG_FILE, 'r') as f:
    config = yaml.safe_load(f)

logging.basicConfig(
   level=logging.DEBUG,
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def __create_text_result(row):
    group, date_time, matchday, local_name, visitor_name, local_result, visitor_result, match_link = row
    return f'{local_name} <a href="{match_link}">{local_result} - {visitor_result}</a> {visitor_name}\n'


def __create_text_schedule(row):
    group, local_name, visitor_name, matchday, date, time, local_link, visitor_link, match_link = row
    return f'<a href="{local_link}">{local_name}</a> - <a href="{visitor_link}">{visitor_name}</a>: <a href="{match_link}">{time[:-3]}</a>\n'


SUMMARY_DATA = {
    'results': {
        'summary_type': 'results',
        'function': __create_text_result,
        'text': '📡 Últimos resultados 📡',
    },
    'schedule': {
        'summary_type': 'schedule',
        'function': __create_text_schedule,
        'text': f'<a href="{config["data"]["calendar"]}">⏰ Duelos para hoy ⏰</a>',
    },
}


def update():
    # Update config file with new group so everything
    # keeps working when the bot is restarted.
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2022 David Escribano <davidegx@gmail.com>
# Copyright (C) 2022 Iñigo Martinez <inigomartinez@gmail.com>

"""Module implementing operations related to settings."""

import logging
import yaml

CONFIG_FILE = 'config.yml'

with open(CONFIG_FILE, 'r') as f:
    config = yaml.safe_load(f)

logging.basicConfig(
   level=logging.DEBUG,
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def update():
    """Update config file."""
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

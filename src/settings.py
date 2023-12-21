# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2022 David Escribano <davidegx@gmail.com>
# Copyright (C) 2022 Iñigo Martinez <inigomartinez@gmail.com>

"""Module implementing operations related to settings."""

import logging
import os

import yaml

CONFIG_FILE = os.environ.get("CS_CONFIG_FILE", "config.yml")

with open(CONFIG_FILE, "r", encoding="utf8") as f:
    config = yaml.safe_load(f)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

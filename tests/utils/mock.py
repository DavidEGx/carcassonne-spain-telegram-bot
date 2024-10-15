"""Mock functions for testing."""

import csv

from src.cs.group import Group


def read_csv(group: Group, url: str) -> list[dict[str, str]]:
    """Mock _read_csv in Group."""
    data = []
    filename = _csv_filename(group, url)
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    return data


def _csv_filename(group: Group, url: str) -> str:
    filename_base = f"tests/fixtures/season_02/{group.name}"
    if url == group.config["results"]:
        return f"{filename_base}/outcome.csv"

    if url == group.config["schedule"]:
        return f"{filename_base}/schedule.csv"

    if url == group.config["players"]:
        return f"{filename_base}/players.csv"

    raise ValueError("URL not found in config")

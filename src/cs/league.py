"""Module containg Carcassonne Spain League class."""

from functools import cache
from typing import Optional

from src.cs.group import Group
from src.settings import config


@cache
class League:
    """Represent Carcassonne Spain League tournament.

    The league is divided in separate groups that act
    as separate tournements themselves.

    @cache decorator is used so only a single instance of
    this class exists.
    """

    def __init__(self, season: Optional[int] = None):
        """Initialize Carcassonne Spain League object."""
        if season:
            self.season = season
        else:
            self.season = max(int(cnf["season"]) for cnf in config["league"])

        self._groups: list[Group] = []

    @property
    def groups(self) -> list[Group]:
        """List of groups within the League."""
        cnf_groups = [
            cnf["groups"] for cnf in config["league"] if cnf["season"] == self.season
        ]
        if cnf_groups:
            cnf_groups = cnf_groups[0]
        else:
            raise ValueError(f"Season {self.season} not found")

        if not self._groups:
            group_names = sorted(
                cnf_groups, key=lambda group: cnf_groups[group]["order"]
            )
            self._groups = [Group(name, cnf_groups[name]) for name in group_names]

        return self._groups

    def group(self, name: str) -> Group:
        """Fetch group by name."""
        for group in self.groups:
            if group.name == name:
                return group

        raise LookupError(f"Group '{name}' not found in League")

"""Module containg Carcassonne Spain League class."""
from functools import cache

from src.cs.group import Group
from src.settings import config


# pyright: strict
@cache
class League:
    """Represent Carcassonne Spain League tournament.

    The league is divided in separate groups that act
    as separate tournements themselves.

    @cache decorator is used so only a single instance of
    this class exists.
    """

    def __init__(self):
        """Initialize Carcassonne Spain League object."""
        self._groups: list[Group] = []

    @property
    def groups(self) -> list[Group]:
        """List of groups within the League."""
        if not self._groups:
            group_names = sorted(
                            config['groups'],
                            key=lambda group: config['groups'][group]['order'])
            self._groups = [Group(name) for name in group_names]

        return self._groups

    def group(self, name: str) -> Group:
        """Fetch group by name."""
        for group in self.groups:
            if group.name == name:
                return group

        raise LookupError(f"Group '{name}' not found in League")

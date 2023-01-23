"""Module for Carcassonne Spain Player class."""
from src.settings import config


# pyright: strict
class Player:
    """Represent a Carcassonne Spain league player."""

    def __init__(self, player_id: int, name: str):
        """Build a player."""
        self.id = player_id
        self.name = name
        self.url = config['bga']['urls']['player_link'].format(player_id)

    def html(self):
        """Player name with link to BGA profile."""
        return f'<a href="{self.url}">{self.name}</a>'

    def __str__(self):
        """Player formatted like "{name} ({id})."""
        return f"{self.name} ({self.id})"

    def __repr__(self):
        """Player formatted like "Player({id}, {name})."""
        return f"Player({self.id}, '{self.name}')"

    def __eq__(self, other: object) -> bool:
        """Hopefully sensible eq method for Player."""
        if not isinstance(other, self.__class__):
            return False
        return (self.id == other.id and
                self.name == other.name)

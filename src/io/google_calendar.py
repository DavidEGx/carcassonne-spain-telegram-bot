"""Module for Carcassonne Spain Google Calendar."""

from datetime import date, datetime, timedelta
from functools import cache
from typing import Any, Optional

from cachetools.func import ttl_cache
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.cs.duel import Duel
from src.cs.group import Group
from src.cs.league import League
from src.io.io_base import IoBase
from src.settings import config, logger

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CACHE_TTL = 3600  # in seconds


@cache
class GCalendar(IoBase):
    """Encapsulate all Google Calendar communication."""

    def __init__(self, season: Optional[int] = None):
        """Initialize the GCalendar object."""
        self.league = League(season)
        self.calendar_id = config["google"]["calendar_id"]
        # TODO: Move token.json to config.yml
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        # pylint: disable=E1101
        self.event_mgr = build("calendar", "v3", credentials=creds).events()
        self._events: dict[date, list[Any]] = {}

    def _summary(self, duel: Duel) -> str:
        return f"{duel.p1.name} - {duel.p2.name}"

    def _description(self, group: Group, duel: Duel) -> str:
        name = group.name
        if duel.played:
            return f"<b>Grupo {name}</b>\n{duel.html()}"

        return f"<b>Grupo {name}</b>\n{duel.p1.name} - {duel.p2.name}"

    @property
    @ttl_cache(ttl=CACHE_TTL)
    def events(self) -> list[dict[str, Any]]:
        """Existing events in Google Calendar."""
        start = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
        events_result = self.event_mgr.list(
            calendarId=self.calendar_id,
            timeMin=start,
            maxResults=1000,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        return events_result.get("items", [])

    def _find_event(self, expected_summary: str) -> Optional[dict[str, Any]]:
        """Find existing events for a duel."""
        for event in self.events:
            if event["summary"] == expected_summary:
                return event

        return None

    def create_msg(
        self, query_date: date, force_schedule: bool = False
    ) -> list[dict[str, Any]]:
        """Create a message containing all the duels for a give date.

        Parameters
        ----------
            query_date You'll get the duels for this date.
            force_schedule If the date is in the past, you'll get the
                           duels outcome for that day.
                           Set this to true to get the duels schedule
                           instead. For testing purposes mainly.
        Returns
        -------
        List of strings. Each string should fit in a single Tweet.
        """
        # Get formatted text for each group
        output: list[dict[str, Any]] = []
        for group in self.league.groups:
            for duel in group.duels(query_date, force_schedule):
                start = duel.planned.isoformat()
                end = (duel.planned + timedelta(hours=1)).isoformat()

                msg = {
                    "summary": self._summary(duel),
                    "description": self._description(group, duel),
                    "start": {"dateTime": start, "timeZone": "Europe/Madrid"},
                    "end": {"dateTime": end, "timeZone": "Europe/Madrid"},
                    "colorId": group.gcalendar_color,
                }
                output.append(msg)

        return output

    def send(self, query_date: date, force_schedule: bool = False):
        """Publish Google Calendar events."""
        logger.info("Creating events for %s", query_date)
        msgs = self.create_msg(query_date, force_schedule)

        for msg in msgs:
            event = self._find_event(msg["summary"])
            if event:
                logger.debug("Updating event %s %s", event["id"], msg["summary"])
                self.event_mgr.update(
                    calendarId=self.calendar_id, eventId=event["id"], body=msg
                ).execute()
            else:
                logger.debug("Inserting event %s", msg["summary"])
                self.event_mgr.insert(calendarId=self.calendar_id, body=msg).execute()

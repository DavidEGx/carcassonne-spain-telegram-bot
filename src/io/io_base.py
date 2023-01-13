"""Common IO stuff."""
from abc import ABC, abstractmethod
from datetime import date, timedelta


# pyright: strict
class IoBase(ABC):
    """Base IO class."""

    @abstractmethod
    def create_msg(self,
                   query_date: date,
                   force_schedule: bool = False) -> list[str]:
        """Return list of messages formatted appropiately."""

    @abstractmethod
    def send(self,
             query_date: date,
             force_schedule: bool = False):
        """Post message."""

    def test(self, start: date | str, end: date | str,
             do_print: bool = True, do_send: bool = False):
        """Test funtion to create/simulate all tweets between two dates.

        Parameters:
        -----------
            start Start date
            end End date
            do_print Print tweet messages. Default to true.
            do_send Actually tweet messages for real. Default to false.
        """
        if isinstance(start, str):
            start = date.fromisoformat(start)
        if isinstance(end, str):
            end = date.fromisoformat(end)

        current = start
        while current <= end:
            day_before = current - timedelta(1)

            if do_print:
                messages = self.create_msg(day_before)
                for idx, msg in enumerate(messages):
                    print(f"Msg: {idx}, date: {day_before}, size: {len(msg)}")
                    print("*********************************************\n")
                    print(msg)
                    print("*********************************************\n\n")

                messages = self.create_msg(current, force_schedule=True)
                for idx, msg in enumerate(messages):
                    print(f"Msg: {idx}, date: {current}, size: {len(msg)}")
                    print("*********************************************\n")
                    print(msg)
                    print("*********************************************\n\n")

            if do_send:
                self.send(day_before)
                self.send(current, force_schedule=True)

            current += timedelta(1)

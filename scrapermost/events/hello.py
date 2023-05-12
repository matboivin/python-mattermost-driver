"""Class defining the 'hello' event."""

from typing import Any

from .base import WebsocketEvent


class Hello(WebsocketEvent):
    """Class defining the 'hello' event: user successfully authenticated.

    Attributes
    ----------
    connection_id : str
        The connection ID.
    server_version : str
        The version of the server the user connected to.

    """

    def __init__(self, event: dict[str, Any]) -> None:
        """Initialize the attributes.

        Parameters
        ----------
        event : dict
            The websocket event as a JSON.

        Raises
        ------
        KeyError
            If a key is missing from event.
        TypeError
            If the wrong event type was passed as parameter.

        """
        if event.get("event") != "hello":
            raise TypeError(f"Event type '{event.get('event')}' was passed.")

        data: dict[str, Any] = event["data"]

        super().__init__(event)

        self.connection_id: str = data["connection_id"]
        self.server_version: str = data["server_version"]

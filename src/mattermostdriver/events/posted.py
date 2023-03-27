"""Class defining the 'posted' event."""

from typing import Any, Dict

from .post_edited import PostEdited


class Posted(PostEdited):
    """Class defining the 'posted' event: a new message was posted.

    Attributes
    ----------
    channel_display_name : str
    channel_name : str
    channel_type : str
    sender_name : str
    set_online : bool
    team_id : str

    """

    def __init__(self, event: Dict[str, Any]) -> None:
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
        if event.get("event") != "posted":
            raise TypeError(f"Event type '{event.get('event')}' was passed.")

        super().__init__(event)

        data: Dict[str, Any] = event["data"]

        self.channel_display_name: str = data["channel_display_name"]
        self.channel_name: str = data["channel_name"]
        self.channel_type: str = data["channel_type"]
        self.sender_name: str = data["sender_name"]
        self.set_online: bool = data["set_online"]
        self.team_id: str = data["team_id"]

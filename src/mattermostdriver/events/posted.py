"""Class defining the 'posted' event."""

from json import loads
from typing import Any, Dict

from mattermostdriver.classes import Post

from .base import WebsocketEvent


class Posted(WebsocketEvent):
    """Class defining the 'posted' event: a new message was posted.

    Attributes
    ----------
    post : Post
        The post data.
    channel_display_name : str
        The display name of the channel in which the message was posted.
    channel_name : str
        The name of the channel in which the message was posted.
    channel_type : str
        The type of the channel in which the message was posted.
    sender_name : str
        The name of the message sender.
    set_online : bool
        Whether the user status is online or not.
    team_id : str
        The team ID in which the message was posted.

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

        if isinstance(event["data"]["post"], str):
            self.post: Post = Post(loads(event["data"]["post"]))
        else:
            self.post: Post = Post(event["data"]["post"])

        data: Dict[str, Any] = event["data"]

        self.channel_display_name: str = data["channel_display_name"]
        self.channel_name: str = data["channel_name"]
        self.channel_type: str = data["channel_type"]
        self.sender_name: str = data["sender_name"]
        self.set_online: bool = data["set_online"]
        self.team_id: str = data["team_id"]

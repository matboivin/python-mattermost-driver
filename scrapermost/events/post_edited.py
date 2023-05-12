"""Class defining the 'post_edited' event."""

from json import loads
from typing import Any

from scrapermost.classes import Post

from .base import WebsocketEvent


class PostEdited(WebsocketEvent):
    """Class defining the 'post_edited' event: a message was edited.

    Attributes
    ----------
    post : Post
        The post data.

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
        if event.get("event") != "post_edited":
            raise TypeError(f"Event type '{event.get('event')}' was passed.")

        super().__init__(event)

        self.post: Post

        if isinstance(event["data"]["post"], str):
            self.post = Post(loads(event["data"]["post"]))
        else:
            self.post = Post(event["data"]["post"])

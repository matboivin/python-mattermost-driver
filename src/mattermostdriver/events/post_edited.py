"""Class defining the 'post_edited' event."""

from json import loads
from typing import Any, Dict

from mattermostdriver.classes import Post

from .base import WebsocketEvent


class PostEdited(WebsocketEvent):
    """Class defining the 'post_edited' event: a message was edited.

    Attributes
    ----------
    post : Post
        The post data.

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

        """
        super().__init__(event)
        self.post: Post = Post(loads(event["data"]["post"]))

"""Mattermost event classes."""

from json import loads
from typing import Any, Dict


class WebsocketEvent:
    """Class defining a websocket event.

    Attributes
    ----------
    event_type : str
        The event type.
    data : dict
        The event data.
    broadcast : dict
        Information about who the event was sent to.
    seq : int
        Sequence number set by the client.

    """

    def __init__(self, event: Any) -> None:
        """Initialize the attributes.

        Parameters
        ----------
        event : Any
            The websocket event as a JSON.

        Raises
        ------
        KeyError
            If either event, data, broadcast or seq is missing.

        """
        self.event_type: str = event["event"]
        self.broadcast: Dict[str, Any] = event["broadcast"]
        self.seq: int = event["seq"]


class PostEdited(WebsocketEvent):
    """Class defining the 'post_edited' event: a message was edited.

    Attributes
    ----------
    id : str
    create_at : int
    update_at : int
    edit_at : int
    delete_at : int
    is_pinned : bool
    user_id : str
    channel_id : str
    root_id : str
    original_id : str
    message : str
    type : str
    props : dict
    hashtags : str
    pending_post_id : str
    reply_count : int
    last_reply_at : int
    participants : Any
    metadata : dict

    """

    def __init__(self, event: Any, post: Dict[str, Any]) -> None:
        """Initialize the attributes.

        Parameters
        ----------
        event : Any
            The websocket event as a JSON.
        post : dict
            The Post data.

        Raises
        ------
        KeyError
            If a key is missing from event.

        """
        super().__init__(event)

        self.id: str = post["id"]
        self.create_at: int = post["create_at"]
        self.update_at: int = post["update_at"]
        self.edit_at: int = post["edit_at"]
        self.delete_at: int = post["delete_at"]
        self.is_pinned: bool = post["is_pinned"]
        self.user_id: str = post["user_id"]
        self.channel_id: str = post["channel_id"]
        self.root_id: str = post["root_id"]
        self.original_id: str = post["original_id"]
        self.message: str = post["message"]
        self.type: str = post["type"]
        self.props: Dict[str, Any] = post["props"]
        self.hashtags: str = post["hashtags"]
        self.pending_post_id: str = post["pending_post_id"]
        self.reply_count: int = post["reply_count"]
        self.last_reply_at: int = post["last_reply_at"]
        self.participants: Any = post["participants"]
        self.metadata: Dict[str, Any] = post["metadata"]


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

    def __init__(self, event: str) -> None:
        """Initialize the attributes.

        Parameters
        ----------
        event : str
            The websocket event as string.

        Raises
        ------
        KeyError
            If a key is missing from event.

        """
        event_json: Any = loads(event)
        data: Dict[str, Any] = event_json["data"]

        super().__init__(event_json, loads(data["post"]))

        self.channel_display_name: str = data["channel_display_name"]
        self.channel_name: str = data["channel_name"]
        self.channel_type: str = data["channel_type"]
        self.sender_name: str = data["sender_name"]
        self.set_online: bool = data["set_online"]
        self.team_id: str = data["team_id"]

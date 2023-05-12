"""Class defining a post."""

from typing import Any

from .metadata import EmbedMetadata, FileMetadata


class Post:
    """Class defining a post (i.e., a Mattermost message).

    Attributes
    ----------
    id : str
        The post ID.
    create_at : int
        Date and time the post was created in milliseconds.
    update_at : int
        Date and time the post was updated in milliseconds.
    edit_at : int
        Date and time the post was edited in milliseconds.
    delete_at : int
        Date and time the post was deleted in milliseconds.
    is_pinned : bool
        Whether the post is pinned.
    user_id : str
        The sender's user ID.
    channel_id : str
        The ID of the channel in which the message was posted.
    root_id : str
        If the post is a reply, ID of the replied-to post.
        If the post is in a thread, ID of the thread's first message.
    original_id : str
        TODO: Add description.
    message : str
        The post's content.
    type : str
        TODO: Add description.
    props : dict
        TODO: Add description.
    hashtags : str
        Hashtags contained in message, separated by a space.
    pending_post_id : str
        TODO: Add description.
    reply_count : int
        Count of replies from the root post.
    last_reply_at : int
        Date and time of the last reply.
    participants : Any
        TODO: Add description.
    metadata : Metadata
        Embedded links, emojis, reactions, and files metadata.

    """

    def __init__(self, attr: dict[str, Any]) -> None:
        """Initialize the attributes.

        Parameters
        ----------
        attr : dict
            The attributes as a dict.

        Raises
        ------
        KeyError
            If a key is missing from event.

        """
        self.id: str = attr["id"]
        self.create_at: int = attr["create_at"]
        self.update_at: int = attr["update_at"]
        self.edit_at: int = attr["edit_at"]
        self.delete_at: int = attr["delete_at"]
        self.is_pinned: bool = attr["is_pinned"]
        self.user_id: str = attr["user_id"]
        self.channel_id: str = attr["channel_id"]
        self.root_id: str = attr["root_id"]
        self.original_id: str = attr["original_id"]
        self.message: str = attr["message"]
        self.type: str = attr["type"]
        self.props: dict[str, Any] = attr["props"]
        self.hashtags: str = attr["hashtags"]
        self.pending_post_id: str = attr["pending_post_id"]
        self.reply_count: int = attr["reply_count"]
        self.last_reply_at: int = attr["last_reply_at"]
        self.participants: Any = attr["participants"]
        self.metadata: dict[str, list[Any]] = {}

        metadata: dict[str, Any] = attr.get("metadata", {})

        if metadata.get("embeds"):
            self.metadata["embeds"] = [
                EmbedMetadata(file) for file in metadata["embeds"]
            ]
        if metadata.get("files"):
            self.metadata["files"] = [
                FileMetadata(file) for file in metadata["files"]
            ]

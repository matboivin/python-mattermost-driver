"""Class defining a post."""

from typing import Any, Dict, List

from .metadata import EmbedMetadata, FileMetadata


class Post:
    """Class defining a post (i.e., a Mattermost message).

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
    metadata : Metadata

    """

    def __init__(self, attr: Dict[str, Any]) -> None:
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
        self.props: Dict[str, Any] = attr["props"]
        self.hashtags: str = attr["hashtags"]
        self.pending_post_id: str = attr["pending_post_id"]
        self.reply_count: int = attr["reply_count"]
        self.last_reply_at: int = attr["last_reply_at"]
        self.participants: Any = attr["participants"]
        self.metadata: Dict[str, List[Any]] = {}

        metadata: Dict[str, Any] = attr.get("metadata", {})

        if metadata.get("embeds"):
            self.metadata["embeds"] = [
                EmbedMetadata(file) for file in metadata.get("embeds")
            ]
        if metadata.get("files"):
            self.metadata["files"] = [
                FileMetadata(file) for file in metadata.get("files")
            ]

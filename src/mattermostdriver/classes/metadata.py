"""Class defining metadata."""

from typing import Any, Dict


class EmbedMetadata:
    """Class defining an embedded link.

    Attributes
    ----------
    type : str
    url : str
    data : dict

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
        self.type: str = attr["type"]
        self.url: str = attr["url"]
        self.data: Dict[str, Any] = attr.get("data", {})


class FileMetadata:
    """Class defining file's metadata.

    Attributes
    ----------
    id : str
    user_id : str
    post_id : str
    channel_id : str
    create_at : int
    update_at : int
    delete_at : int
    name : str
    extension : str
    size : int
    mime_type : str
    width : int
    height : int
    has_preview_image : bool
    mini_preview : str
    remote_id : str
    archived : bool

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
        self.user_id: str = attr["user_id"]
        self.post_id: str = attr["post_id"]
        self.channel_id: str = attr["channel_id"]
        self.create_at: int = attr["create_at"]
        self.update_at: int = attr["update_at"]
        self.delete_at: int = attr["delete_at"]
        self.name: str = attr["name"]
        self.extension: str = attr["extension"]
        self.size: int = attr["size"]
        self.mime_type: str = attr["mime_type"]
        self.width: int = attr["width"]
        self.height: int = attr["height"]
        self.has_preview_image: bool = attr["has_preview_image"]
        self.mini_preview: str = attr["mini_preview"]
        self.remote_id: str = attr["remote_id"]
        self.archived: bool = attr["archived"]

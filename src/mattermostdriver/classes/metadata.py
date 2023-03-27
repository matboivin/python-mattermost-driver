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
        The file ID.
    user_id : str
        The sender's user ID.
    post_id : str
        The file's post ID.
    channel_id : str
        The ID of the channel in which the file was posted.
    create_at : int
        Date and time the file was created in milliseconds.
    update_at : int
        Date and time the file was updated in milliseconds.
    delete_at : int
        Date and time the file was deleted in milliseconds.
    name : str
        Filename.
    extension : str
        The file extension.
    size : int
        The filesize.
    mime_type : str
        The file MIME type.
    width : int
        The file width in pixels.
    height : int
        The file height in pixels.
    has_preview_image : bool
        Whether the file has a preview.
    mini_preview : str
        The file bytes as string.
    remote_id : str
        No idea.
    archived : bool
        Whether the file is archived.

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

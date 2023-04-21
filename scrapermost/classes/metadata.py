"""Class defining metadata."""

from typing import Any, Dict


class EmbedMetadata:
    """Class defining an embedded link.

    Attributes
    ----------
    type : str
        The embed's type.
    url : str
        The embed's URL.
    data : dict
        TODO: Add description.

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
            If 'type' key is missing from event.

        """
        self.type: str = attr["type"]
        self.url: str = attr.get("url", "")
        self.data: Dict[str, Any] = attr.get("data", {})


class FileMetadata:
    """Class defining file's metadata.

    Attributes
    ----------
    id : str
        The unique identifier for this file.
    user_id : str
        The ID of the user that uploaded this file.
    post_id : str
        If this file is attached to a post, the ID of that post.
    channel_id : str
        The ID of the channel in which the file was posted.
    create_at : int
        The time in milliseconds a file was created.
    update_at : int
        The time in milliseconds a file was last updated.
    delete_at : int
        The time in milliseconds a file was deleted.
    name : str
        The filename.
    extension : str
        The file extension.
    size : int
        The file size in bytes.
    mime_type : str
        The file MIME type.
    remote_id : str
        TODO: Add description.
    archived : bool
        Whether the file is archived.
    width : int, optional
        If this file is an image, the width of the file in pixels.
    height : int, optional
        If this file is an image, the height of the file in pixels.
    has_preview_image : bool, optional
        If this file is an image, the height of the file.
    mini_preview : str, optional
        If this file is an image, the file bytes as string.

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
        self.remote_id: str = attr["remote_id"]
        self.archived: bool = attr["archived"]
        self.width: int | None = attr.get("width")
        self.height: int | None = attr.get("height")
        self.has_preview_image: bool | None = attr.get("has_preview_image")
        self.mini_preview: str | None = attr.get("mini_preview")

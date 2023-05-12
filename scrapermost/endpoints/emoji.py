"""Endpoints for creating, getting and interacting with emojis."""

from dataclasses import dataclass
from json import dumps
from typing import Any, Awaitable, Literal

from requests import Response

from .base import APIEndpoint, _ret_json


@dataclass
class Emoji(APIEndpoint):
    """Class defining the Emoji API endpoint.

    Attributes
    ----------
    endpoint : str, default='emoji'
        The endpoint path.
    get_emoji_list(page=0, per_page=60, sort='')
        Get a list of custom emoji.
    get_custom_emoji(emoji_id)
        Get some metadata for a custom emoji.
    delete_custom_emoji(emoji_id)
        Delete a custom emoji.
    get_custom_emoji_by_name(name)
        Get some metadata for a custom emoji using its name.
    get_custom_emoji_image(emoji_id)
        Get the image for a custom emoji.
    search_custom_emoji(term, prefix_only=None)
        Search for custom emoji by name based on search criteria.
    autocomplete_custom_emoji(name)
        Autocomplete custom emoji.

    Methods
    -------
    create_custom_emoji(emoji_name, image)
        Create a custom emoji for the team.

    """

    endpoint: str = "emoji"

    @_ret_json
    def create_custom_emoji(
        self, emoji_name: str, image: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Create a custom emoji for the team.

        Parameters
        ----------
        emoji_name : str
            The emoji name.
        image : str
            The image's bytes string to be uploaded.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        emoji: dict[str, Any] = {
            "name": emoji_name,
            "creator_id": self.client.user_id,
        }

        return self.client.post(
            self.endpoint,
            data={"emoji": dumps(emoji)},
            files={"image": image},
        )

    @_ret_json
    def get_emoji_list(
        self,
        page: int = 0,
        per_page: int = 60,
        sort: Literal["", "names"] = "",
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of public channels on a team.

        Parameters
        ----------
        page : int, default=0
            The page to select.
        per_page : int, default=60
            The number of members per page (max: 200).
        sort : '' or 'names', default=''
            Either blank for no sorting or "name" to sort by emoji names.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            self.endpoint,
            params={"page": page, "per_page": per_page, "sort": sort},
        )

    @_ret_json
    def get_custom_emoji(
        self, emoji_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get some metadata for a custom emoji.

        Parameters
        ----------
        emoji_id : str
            Emoji GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{emoji_id}")

    @_ret_json
    def delete_custom_emoji(
        self, emoji_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Delete a custom emoji.

        Parameters
        ----------
        emoji_id : str
            Emoji GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.delete(f"{self.endpoint}/{emoji_id}")

    @_ret_json
    def get_custom_emoji_by_name(
        self, name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get some metadata for a custom emoji using its name.

        Parameters
        ----------
        name : str
            Emoji GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/name/{name}")

    @_ret_json
    def get_custom_emoji_image(
        self, emoji_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get the image for a custom emoji.

        Parameters
        ----------
        emoji_id : str
            Emoji GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{emoji_id}/image")

    @_ret_json
    def search_custom_emoji(
        self, term: str, prefix_only: str | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Search for custom emoji by name based on search criteria.

        Parameters
        ----------
        term : str
            The term to match against the emoji name.
        prefix_only : str, optional
            Set to only search for names starting with the search term.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/search",
            body_json={"term": term, "prefix_only": prefix_only},
        )

    @_ret_json
    def autocomplete_custom_emoji(
        self, name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Autocomplete custom emoji.

        Get a list of custom emoji with names starting with or matching the
        provided name. Returns a maximum of 100 results.

        Parameters
        ----------
        name : str
            The emoji name to search.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{self.endpoint}/autocomplete", params={"name": name}
        )

"""Endpoints for creating, getting and interacting with channels."""

from dataclasses import dataclass
from logging import INFO, Logger, getLogger
from typing import Any, Awaitable, Dict, List

from requests import Response

from .base import APIEndpoint
from .teams import Teams
from .users import Users

log: Logger = getLogger("scrapermost.api.channels")
log.setLevel(INFO)


@dataclass
class Channels(APIEndpoint):
    """Class defining the Channels API endpoint.

    Attributes
    ----------
    endpoint : str, default='channels'
        The endpoint path.

    Methods
    -------
    create_channel(body_json)
        Create a new channel.
    create_direct_message_channel(first_user_id, second_user_id)
        Create a new direct message channel between two users.
    create_group_message_channel(user_ids)
        Create a new group message channel to group of users.
    get_list_of_channels_by_ids(team_id, channel_ids)
        Get a list of public channels on a team by ID.
    get_channel(channel_id)
        Get channel from the provided channel ID string.
    update_channel(channel_id, body_json)
        Update a channel.
    delete_channel(channel_id)
        Archive a channel.
    patch_channel(channel_id, body_json)
        Partially update a channel by providing only the fields to update.
    restore_channel(channel_id)
        Restore channel from the provided channel ID string.
    get_channel_statistics(channel_id)
        Get statistics for a channel.
    get_channel_pinned_posts(channel_id)
        Get a list of pinned posts for channel.
    get_public_channels(team_id, page=0, per_page=60)
        Get a page of public channels on a team.
    get_deleted_channels(team_id, page=0, per_page=60)
        Get a page of deleted channels on a team.
    autocomplete_channels(team_id, name)
        Autocomplete public channels on a team.
    search_channels(team_id, term)
        Search public channels on a team.
    get_channel_by_name(team_id, channel_name)
        Get channel from the provided team ID and channel name strings.
    get_channel_by_name_and_team_name(team_name, channel_name)
        Get a channel from the provided team channel name strings.
    get_channel_members(channel_id, page=0, per_page=60)
        Get a page of members for a channel.
    add_user(channel_id, user_id, post_root_id=None)
        Add a user to a channel by creating a channel member object.
    get_channel_members_by_ids(channel_id, user_ids)
        Get a list of channel members based on the provided user IDs.
    get_channel_member(channel_id, user_id)
        Get a channel member.
    remove_channel_member(channel_id, user_id)
        Delete a channel member,removing them from the channel.
    update_channel_roles(channel_id, user_id, roles)
        Update a user's roles for a channel.
    update_scheme_derived_roles_of_channel_member(
            channel_id, user_id, body_json
        )
        Update the scheme-derived roles of a channel member.
    update_channel_notifications(channel_id, user_id, body_json)
        Update a user's notification properties for a channel.
    view_channel(user_id, channel_id, prev_channel_id=None)
        Perform all the actions involved in viewing a channel.
    get_channel_members_for_user(user_id, team_id)
        Get channel memberships and roles for a user.
    get_channels_for_user(user_id, team_id)
        Get all the channels on a team for a user.
    get_unread_messages(user_id, channel_id)
        Get the total unread messages and mentions for a channel for a user.
    set_channel_scheme(channel_id)
        Set a channel's scheme.

    """

    endpoint: str = "channels"

    def create_channel(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        """Create a new channel.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.
            team_id, name, display_name and type are required.
            Example:
            {
                "team_id": "string",
                "name": "string",
                "display_name": "string",
                "purpose": "string",
                "header": "string",
                "type": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(self.endpoint, body_json=body_json)

    def create_direct_message_channel(
        self, first_user_id: str, second_user_id: str
    ) -> Any | Awaitable[Any]:
        """Create a new direct message channel between two users.

        Parameters
        ----------
        first_user_id : str
            User GUID.
        second_user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/direct",
            body_json=[first_user_id, second_user_id],
        )

    def create_group_message_channel(
        self, user_ids: List[str]
    ) -> Any | Awaitable[Any]:
        """Create a new group message channel to group of users.

        Parameters
        ----------
        user_ids : list of str
            List of user IDs (min: 3, max: 8).

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/group", body_json=user_ids)

    def get_list_of_channels_by_ids(
        self, team_id: str, channel_ids: List[str]
    ) -> Any | Awaitable[Any]:
        """Get a list of public channels on a team by ID.

        Parameters
        ----------
        team_id : str
            Team GUID.
        channel_ids : list of str
            List of channel ids.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{Teams.endpoint}/{team_id}/channels/ids", body_json=channel_ids
        )

    def get_channel(
        self, channel_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get channel from the provided channel ID string.

        Parameters
        ----------
        channel_id : str
            Channel GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{channel_id}")

    def update_channel(
        self, channel_id: str, body_json: Dict[str, Any]
    ) -> Any | Awaitable[Any]:
        """Update a channel.

        Parameters
        ----------
        channel_id : str
            Channel GUID.
        body_json : dict
            A JSON serializable object to include in the body of the request.
            Example:
            {
                "id": "string",
                "name": "string",
                "display_name": "string",
                "purpose": "string",
                "header": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{channel_id}", body_json=body_json
        )

    def delete_channel(self, channel_id: str) -> Any | Awaitable[Any]:
        """Archive a channel.

        Parameters
        ----------
        channel_id : str
            Channel GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.delete(f"{self.endpoint}/{channel_id}")

    def patch_channel(
        self, channel_id: str, body_json: Dict[str, Any]
    ) -> Any | Awaitable[Any]:
        """Partially update a channel by providing only the fields to update.

        Parameters
        ----------
        channel_id : str
            Channel GUID.
        body_json : dict
            A JSON serializable object to include in the body of the request.
            Example:
            {
                "name": "string",
                "display_name": "string",
                "purpose": "string",
                "header": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{channel_id}/patch", body_json=body_json
        )

    def restore_channel(self, channel_id: str) -> Any | Awaitable[Any]:
        """Restore channel from the provided channel ID string.

        Parameters
        ----------
        channel_id : str
            Channel GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/{channel_id}/restore",
        )

    def get_channel_statistics(
        self, channel_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get statistics for a channel.

        Parameters
        ----------
        channel_id : str
            Channel GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{self.endpoint}/{channel_id}/stats",
        )

    def get_channel_pinned_posts(
        self, channel_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of pinned posts for channel.

        Parameters
        ----------
        channel_id : str
            Channel GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{channel_id}/pinned")

    def get_public_channels(
        self, team_id: str, page: int = 0, per_page: int = 60
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of public channels on a team.

        Parameters
        ----------
        page : int, default=0
            The page to select.
        per_page : int, default=60
            The number of members per page (max: 200).

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Teams.endpoint}/{team_id}/channels",
            params={"page": page, "per_page": per_page},
        )

    def get_deleted_channels(
        self, team_id: str, page: int = 0, per_page: int = 60
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of deleted channels on a team.

        Parameters
        ----------
        page : int, default=0
            The page to select.
        per_page : int, default=60
            The number of members per page (max: 200).

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Teams.endpoint}/{team_id}/channels/deleted",
            params={"page": page, "per_page": per_page},
        )

    def autocomplete_channels(
        self, team_id: str, name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Autocomplete public channels on a team.

        Parameters
        ----------
        team_id : str
            Team GUID.
        name : str
            Name or display name.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Teams.endpoint}/{team_id}/channels/autocomplete",
            params={"name": name},
        )

    def search_channels(self, team_id: str, term: str) -> Any | Awaitable[Any]:
        """Search public channels on a team.

        Parameters
        ----------
        team_id : str
            Team GUID.
        term : str
            The search term to match against the name or display name of
            channels.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{Teams.endpoint}/{team_id}/channels/search",
            body_json={"term": term},
        )

    def get_channel_by_name(
        self, team_id: str, channel_name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get channel from the provided team ID and channel name strings.

        Parameters
        ----------
        team_id : str
            Team GUID.
        channel_name : str
            Channel Name.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Teams.endpoint}/{team_id}/channels/name/{channel_name}"
        )

    def get_channel_by_name_and_team_name(
        self, team_name: str, channel_name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a channel from the provided team channel name strings.

        Parameters
        ----------
        team_name : str
            Team name.
        channel_name : str
            Channel Name.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Teams.endpoint}/name/{team_name}/channels/name/{channel_name}"
        )

    def get_channel_members(
        self, channel_id: str, page: int = 0, per_page: int = 60
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of members for a channel.

        Parameters
        ----------
        channel_id : str
            Channel GUID.
        page : int, default=0
            The page to select.
        per_page : int, default=60
            The number of members per page (max: 200).

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{self.endpoint}/{channel_id}/members",
            params={"page": page, "per_page": per_page},
        )

    def add_user(
        self, channel_id: str, user_id: str, post_root_id: str | None = None
    ) -> Any | Awaitable[Any]:
        """Add a user to a channel by creating a channel member object.

        Parameters
        ----------
        channel_id : str
            Channel GUID.
        user_id : str
            The ID of user to add into the channel.
        post_root_id : str, optional
            The ID of root post where link to add channel member originates.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        options: Any = {"user_id": user_id}

        if post_root_id:
            options["post_root_id"] = post_root_id

        return self.client.post(
            f"{self.endpoint}/{channel_id}/members", body_json=options
        )

    def get_channel_members_by_ids(
        self, channel_id: str, user_ids: List[str]
    ) -> Any | Awaitable[Any]:
        """Get a list of channel members based on the provided user IDs.

        Parameters
        ----------
        channel_id : str
            Channel GUID.
        user_ids : list of str
            List of user IDs.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/{channel_id}/members/ids", body_json=user_ids
        )

    def get_channel_member(
        self, channel_id: str, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a channel member.

        Parameters
        ----------
        channel_id : str
            Channel GUID.
        user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{self.endpoint}/{channel_id}/members/{user_id}"
        )

    def remove_channel_member(
        self, channel_id: str, user_id: str
    ) -> Any | Awaitable[Any]:
        """Delete a channel member,removing them from the channel.

        Parameters
        ----------
        channel_id : str
            Channel GUID.
        user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.delete(
            f"{self.endpoint}/{channel_id}/members/{user_id}"
        )

    def update_channel_roles(
        self, channel_id: str, user_id: str, roles: str
    ) -> Any | Awaitable[Any]:
        """Update a user's roles for a channel.

        Parameters
        ----------
        channel_id : str
            Channel GUID.
        user_id : str
            User GUID.
        roles : str
            Space-delimited channel roles to assign to the user.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{channel_id}/members/{user_id}/roles",
            body_json={"roles": roles},
        )

    def update_scheme_derived_roles_of_channel_member(
        self,
        channel_id: str,
        user_id: str,
        body_json: Dict[str, Any],
    ) -> Any | Awaitable[Any]:
        """Update the scheme-derived roles of a channel member.

        Parameters
        ----------
        channel_id : str
            Channel GUID.
        user_id : str
            User GUID.
        body_json : dict
            A JSON serializable object to include in the body of the request.
            Example:
            {
                "scheme_admin": true,
                "scheme_user": true
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{channel_id}/members/{user_id}/schemeRoles",
            body_json=body_json,
        )

    def update_channel_notifications(
        self,
        channel_id: str,
        user_id: str,
        body_json: Dict[str, Any],
    ) -> Any | Awaitable[Any]:
        """Update a user's notification properties for a channel.

        Parameters
        ----------
        channel_id : str
            Channel GUID.
        user_id : str
            User GUID.
        body_json : dict
            A JSON serializable object to include in the body of the request.
            Example:
            {
                "email": "string",
                "push": "string",
                "desktop": "string",
                "mark_unread": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{channel_id}/members/{user_id}/notify_props",
            body_json=body_json,
        )

    def view_channel(
        self, user_id: str, channel_id: str, prev_channel_id: str | None = None
    ) -> Any | Awaitable[Any]:
        """Perform all the actions involved in viewing a channel.

        This includes marking channels as read, clearing push notifications,
        and updating the active channel.

        Parameters
        ----------
        user_id : str
            User GUID.
        channel_id : str
            The channel ID that is being viewed. Use a blank string to indicate
            that all channels have lost focus.
        prev_channel_id : str, optional
            The channel ID of the previous channel, used when switching
            channels. Providing this ID will cause push notifications to
            clear on the channel being switched to.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        options: Any = {"channel_id": channel_id}

        if prev_channel_id:
            options["prev_channel_id"] = prev_channel_id

        return self.client.post(
            f"{self.endpoint}/members/{user_id}/view", body_json=options
        )

    def get_channel_members_for_user(
        self, user_id: str, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get channel memberships and roles for a user.

        Parameters
        ----------
        user_id : str
            User GUID.
        team_id : str
            Team GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Users.endpoint}/{user_id}/teams/{team_id}/channels/members"
        )

    def get_channels_for_user(
        self, user_id: str, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get all the channels on a team for a user.

        Parameters
        ----------
        user_id : str
            User GUID.
        team_id : str
            Team GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Users.endpoint}/{user_id}/teams/{team_id}/channels"
        )

    def get_unread_messages(
        self, user_id: str, channel_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get the total unread messages and mentions for a channel for a user.

        Parameters
        ----------
        user_id : str
            User GUID.
        channel_id : str
            Channel GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Users.endpoint}/{user_id}/channels/{channel_id}/unread"
        )

    def set_channel_scheme(self, channel_id: str) -> Any | Awaitable[Any]:
        """Set a channel's scheme.

        More specifically sets the scheme_id value of a channel record.

        Parameters
        ----------
        channel_id : str
            Channel GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(f"{self.endpoint}/{channel_id}/scheme")

"""Endpoints for creating, getting and interacting with channels."""

from dataclasses import dataclass
from logging import INFO, Logger, getLogger
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint
from .teams import Teams
from .users import Users

log: Logger = getLogger("scrapermost.api.channels")
log.setLevel(INFO)


@dataclass
class Channels(APIEndpoint):
    """Class defining the /channels API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------

    """

    endpoint: str = "/channels"

    def create_channel(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(self.endpoint, body_json=body_json)

    def create_direct_message_channel(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/direct", body_json=body_json)

    def create_group_message_channel(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/group", body_json=body_json)

    def get_list_of_channels_by_ids(
        self, team_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{Teams.endpoint}/{team_id}/channels/ids", body_json=body_json
        )

    def get_channel(
        self, channel_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{channel_id}")

    def update_channel(
        self, channel_id: str, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{channel_id}", body_json=body_json
        )

    def delete_channel(self, channel_id: str) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/{channel_id}")

    def patch_channel(
        self, channel_id: str, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{channel_id}/patch", body_json=body_json
        )

    def restore_channel(self, channel_id: str) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{channel_id}/restore",
        )

    def get_channel_statistics(
        self, channel_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{self.endpoint}/{channel_id}/stats",
        )

    def get_channel_pinned_posts(
        self, channel_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{channel_id}/pinned")

    def get_channel_by_name(
        self, team_id: str, channel_name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Teams.endpoint}/{team_id}/channels/name/{channel_name}"
        )

    def get_channel_by_name_and_team_name(
        self, team_name: str, channel_name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Teams.endpoint}/name/{team_name}/channels/name/{channel_name}"
        )

    def get_channel_members(
        self, channel_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{self.endpoint}/{channel_id}/members", params=params
        )

    def add_user(
        self, channel_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{channel_id}/members", body_json=body_json
        )

    def get_channel_members_by_ids(
        self, channel_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{channel_id}/members/ids", body_json=body_json
        )

    def get_channel_member(
        self, channel_id: str, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{self.endpoint}/{channel_id}/members/{user_id}"
        )

    def remove_channel_member(
        self, channel_id: str, user_id: str
    ) -> Any | Awaitable[Any]:
        return self.client.delete(
            f"{self.endpoint}/{channel_id}/members/{user_id}"
        )

    def update_channel_roles(
        self, channel_id: str, user_id: str, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{channel_id}/members/{user_id}/roles",
            body_json=body_json,
        )

    def update_channel_notifications(
        self,
        channel_id: str,
        user_id: str,
        body_json: Dict[str, Any] | None = None,
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{channel_id}/members/{user_id}/notify_props",
            body_json=body_json,
        )

    def view_channel(
        self, user_id: str, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/members/{user_id}/view", body_json=body_json
        )

    def get_channel_members_for_user(
        self, user_id: str, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Users.endpoint}/{user_id}/teams/{team_id}/channels/members"
        )

    def get_channels_for_user(
        self, user_id: str, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Users.endpoint}/{user_id}/teams/{team_id}/channels"
        )

    def get_channel_for_user(
        self, user_id: str, team_id: str
    ) -> Any | Awaitable[Any]:
        log.warning(
            "Call to deprecated function get_channel_for_user, "
            "which will be removed in the next major version."
            "Use get_channels_for_user instead."
        )
        return self.get_channels_for_user(user_id, team_id)

    def get_unread_messages(
        self, user_id: str, channel_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Users.endpoint}/{user_id}/channels/{channel_id}/unread"
        )

    def get_public_channels(
        self, team_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Teams.endpoint}/{team_id}/channels", params=params
        )

    def get_deleted_channels(
        self, team_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Teams.endpoint}/{team_id}/channels/deleted", params=params
        )

    def search_channels(
        self, team_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{Teams.endpoint}/{team_id}/channels/search", body_json=body_json
        )

    def autocomplete_channels(
        self, team_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Teams.endpoint}/{team_id}/channels/autocomplete", params=params
        )

    def update_scheme_derived_roles_of_channel_member(
        self,
        channel_id: str,
        user_id: str,
        body_json: Dict[str, Any] | None = None,
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{channel_id}/members/{user_id}/schemeRoles",
            body_json=body_json,
        )

    def set_channel_scheme(self, channel_id: str) -> Any | Awaitable[Any]:
        return self.client.put(f"{self.endpoint}/{channel_id}/scheme")

    def convert_channel(self, channel_id: str) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/{channel_id}/convert")

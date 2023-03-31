"""Endpoints for creating, getting and interacting with teams."""

import warnings
from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint
from .users import Users


@dataclass
class Teams(APIEndpoint):
    """Class defining the /teams API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------

    """

    endpoint: str = "/teams"

    def create_team(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(self.endpoint, body_json)

    def get_teams(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(self.endpoint, params=params)

    def get_team(
        self, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{team_id}")

    def update_team(
        self, team_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(f"{self.endpoint}/{team_id}", body_json)

    def delete_team(
        self, team_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/{team_id}", params=params)

    def patch_team(
        self, team_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(f"{self.endpoint}/{team_id}/patch", body_json)

    def get_team_by_name(self, name: str) -> Any | Awaitable[Any]:
        return self.client.get(f"{self.endpoint}/name/{name}")

    def search_teams(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/search", body_json)

    def check_team_exists(
        self, name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/name/" + name + "/exists")

    def get_user_teams(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{Users.endpoint}/{user_id}/teams")

    def get_team_members(
        self, team_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{self.endpoint}/{team_id}/members", params=params
        )

    def add_user_to_team(
        self, team_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{team_id}/members", body_json=body_json
        )

    def add_user_to_team_from_invite(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/members/invite", params=params
        )

    def add_multiple_users_to_team(
        self, team_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{team_id}/members/batch", body_json=body_json
        )

    def get_team_members_for_user(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{Users.endpoint}/{user_id}/teams/members")

    def get_team_member(
        self, team_id: str, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{team_id}/members/" + user_id)

    def remove_user_from_team(
        self, team_id: str, user_id: str
    ) -> Any | Awaitable[Any]:
        return self.client.delete(
            f"{self.endpoint}/{team_id}/members/" + user_id
        )

    def get_team_members_by_id(
        self, team_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{team_id}/members/ids", body_json
        )

    def get_team_stats(
        self, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{team_id}/stats")

    def update_team_member_roles(
        self,
        team_id: str,
        user_id: str,
        body_json: Dict[str, Any] | None = None,
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{team_id}/members/{user_id}/roles",
            body_json,
        )

    def get_team_unreads_for_user(
        self, user_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Users.endpoint}/{user_id}/teams/unread", params=params
        )

    def get_unreads_for_team(
        self, user_id: str, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Users.endpoint}/{user_id}/teams/{team_id}/unread",
        )

    def invite_users_to_team_by_mail(
        self, team_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{team_id}/invite/email", body_json
        )

    def import_team_from_other_app(
        self, team_id: str, data: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/{team_id}/import", data=data)

    def get_invite_info_for_team(
        self, invite_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/invite/{invite_id}")

    def get_public_channels(
        self, team_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        warnings.warn(
            "Using deprecated endpoint Teams.get_public_channels(). "
            "Use Channels.get_public_channels() instead.",
            DeprecationWarning,
        )
        return self.client.get(
            f"{self.endpoint}/{team_id}/channels", params=params
        )

    def get_deleted_channels(
        self, team_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        warnings.warn(
            "Using deprecated endpoint Teams.get_deleted_channels(). "
            "Use Channels.get_deleted_channels() instead.",
            DeprecationWarning,
        )
        return self.client.get(
            f"{self.endpoint}/{team_id}/channels/deleted", params=params
        )

    def search_channels(
        self, team_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        warnings.warn(
            "Using deprecated endpoint Teams.search_channels(). "
            "Use Channels.search_channels() instead.",
            DeprecationWarning,
        )
        return self.client.post(
            f"{self.endpoint}/{team_id}/channels/search", body_json=body_json
        )

    def get_team_icon(
        self, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{team_id}/image")

    def set_team_icon(
        self, team_id: str, file: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/{team_id}/image", files=file)

    def update_scheme_derived_roles_of_team_member(
        self,
        team_id: str,
        user_id: str,
        body_json: Dict[str, Any] | None = None,
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{team_id}/members/{user_id}/schemeRoles",
            body_json=body_json,
        )

    def delete_team_icon(self, team_id: str) -> None:
        self.client.delete(f"{self.endpoint}/{team_id}/image")

    def set_team_scheme(self, team_id: str) -> Any | Awaitable[Any]:
        return self.client.put(f"{self.endpoint}/{team_id}/scheme")

"""Endpoints for creating, getting and interacting with teams."""

import warnings
from dataclasses import dataclass
from typing import Any, Awaitable, Dict, Literal

from requests import Response

from .base import APIEndpoint
from .users import Users


@dataclass
class Teams(APIEndpoint):
    """Class defining the Teams API endpoint.

    Attributes
    ----------
    endpoint : str, default='teams'
        The endpoint path.

    Methods
    -------
    create_team(name, diplay_name, channel_type)
        Create a new team on the system.
    get_teams(page=0, per_page=60, total_count=False, exclude_policy=False)
        Get teams.

    """

    endpoint: str = "teams"

    def create_team(
        self, name: str, diplay_name: str, channel_type: Literal["O", "I"]
    ) -> Any | Awaitable[Any]:
        """Create a new team on the system.

        Parameters
        ----------
        name : str
            Unique handler for a team, will be present in the team URL.
        diplay_name : str
            Non-unique UI name for the team.
        channel_type : 'O' or 'I
            'O' for open, 'I' for invite only.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        options: Any = {
            "name": name,
            "display_name": diplay_name,
            "type": channel_type,
        }

        return self.client.post(self.endpoint, body_json=options)

    def get_teams(
        self,
        page: int = 0,
        per_page: int = 60,
        total_count: bool = False,
        exclude_policy: bool = False,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get teams.

        Parameters
        ----------
        page : int, default=0
            The page to select.
        per_page : int, default=60
            The number of members per page (max: 200).
        total_count : bool, default=False
            Appends a total count of returned teams inside the response object.
        exclude_policy : bool, default=False
            Whether to exclude teams which are part of a data retention policy.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            self.endpoint,
            params={
                "page": page,
                "per_page": per_page,
                "include_total_count": total_count,
                "exclude_policy_constrained": exclude_policy,
            },
        )

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
        return self.client.get(f"{self.endpoint}/name/{name}/exists")

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
        return self.client.get(f"{self.endpoint}/{team_id}/members/{user_id}")

    def remove_user_from_team(
        self, team_id: str, user_id: str
    ) -> Any | Awaitable[Any]:
        return self.client.delete(
            f"{self.endpoint}/{team_id}/members/{user_id}"
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

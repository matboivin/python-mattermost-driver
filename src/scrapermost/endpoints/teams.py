"""Endpoints for creating, getting and interacting with teams."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict, List, Literal

from requests import Response

from .base import APIEndpoint, _ret_json
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
    get_team(team_id)
        Get a team on the system.
    update_team(team_id, body_json)
        Update a team by providing the team object.
    delete_team(team_id, permanent=False)
        Mark the team as deleted in the database.
    patch_team(team_id, body_json)
        Update a team partially by providing only the fields to update.
    get_team_by_name(name)
        Get a team based on provided name string.
    search_teams(body_json)
        Search teams based on search term and options provided.
    check_team_exists(name)
        Check if the team exists based on a team name.
    get_user_teams(user_id)
        Get a list of teams that a user is on.
    get_team_members(team_id, page=0, per_page=60)
        Get a page team members list based on query string parameters.
    add_user_to_team(team_id, user_id)
        Add user to the team by user_id.
    add_user_to_team_from_invite(token)
        Add user to team from invite.
    add_multiple_users_to_team(team_id, users_per_team)
        Add a number of users to the team by user_id.
    get_team_members_for_user(user_id)
        Get a list of team members for a user.
    get_team_member(team_id, user_id)
        Get a team member on the system.
    remove_user_from_team(team_id, user_id)
        Remove user from team.
    get_team_members_by_id(team_id, user_ids)
        Get a list of team members based on a provided array of user IDs.
    get_team_stats(team_id)
        Get a team stats on the system.
    get_team_icon(team_id)
        Get the team icon of the team.
    set_team_icon(team_id, files)
        Set the team icon for the team.
    delete_team_icon(team_id)
        Remove the team icon for the team.
    update_team_member_roles(team_id, user_id, roles)
        Update a team member roles.
    update_scheme_derived_roles_of_team_member(team_id, user_id, body_json)
        Update a team member's scheme_admin/scheme_user properties.
    get_team_unreads_for_user(user_id)
        Get team unreads for a user.
    get_unreads_for_team(user_id, team_id)
        Get the unread mention and message counts for a team for a user.
    invite_users_to_team_by_mail(team_id, email_addresses)
        Invite users to the existing team using their email addresses.
    import_team_from_other_app(team_id, data)
        Import a team into a existing team.
    get_invite_info_for_team(invite_id)
        Get invite info for a team.
    set_team_scheme(team_id)
        Set a team's scheme.

    """

    endpoint: str = "teams"

    @_ret_json
    def create_team(
        self, name: str, diplay_name: str, channel_type: Literal["O", "I"]
    ) -> Any:
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

    @_ret_json
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

    @_ret_json
    def get_team(
        self, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a team on the system.

        Parameters
        ----------
        team_id : str
            Team GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{team_id}")

    @_ret_json
    def update_team(self, team_id: str, body_json: Dict[str, Any]) -> Any:
        """Update a team by providing the team object.

        Parameters
        ----------
        team_id : str
            Team GUID.
        body_json : dict
            The team settings as a dict.
            Example:
            {
                "id": "string",
                "display_name": "string",
                "description": "string",
                "company_name": "string",
                "allowed_domains": "string",
                "invite_id": "string",
                "allow_open_invite": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(f"{self.endpoint}/{team_id}", body_json)

    @_ret_json
    def delete_team(self, team_id: str, permanent: bool = False) -> Any:
        """Mark the team as deleted in the database.

        Parameters
        ----------
        team_id : str
            Team GUID.
        permanent : bool, default=False
            Permanently delete the team, to be used for compliance reasons
            only.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.delete(
            f"{self.endpoint}/{team_id}", params={"permanent": permanent}
        )

    @_ret_json
    def patch_team(
        self, team_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any:
        """Update a team partially by providing only the fields to update.

        Parameters
        ----------
        team_id : str
            Team GUID.
        body_json : dict
            The team settings as a dict.
            Example:
            {
                "display_name": "string",
                "description": "string",
                "company_name": "string",
                "invite_id": "string",
                "allow_open_invite": true
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(f"{self.endpoint}/{team_id}/patch", body_json)

    @_ret_json
    def get_team_by_name(self, name: str) -> Any:
        """Get a team based on provided name string.

        Parameters
        ----------
        name : str
            Team name.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.get(f"{self.endpoint}/name/{name}")

    @_ret_json
    def search_teams(self, body_json: Dict[str, Any]) -> Any:
        """Search teams based on search term and options provided.

        Parameters
        ----------
        body_json : dict
            The team settings as a dict.
            Example:
            {
                "term": "string",
                "page": "string",
                "per_page": "string",
                "allow_open_invite": true,
                "group_constrained": true,
                "exclude_policy_constrained": false
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/search", body_json)

    @_ret_json
    def check_team_exists(
        self, name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Check if the team exists based on a team name.

        Parameters
        ----------
        name : str
            Team name.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/name/{name}/exists")

    @_ret_json
    def get_user_teams(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of teams that a user is on.

        Parameters
        ----------
        user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{Users.endpoint}/{user_id}/teams")

    @_ret_json
    def get_team_members(
        self, team_id: str, page: int = 0, per_page: int = 60
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page team members list based on query string parameters.

        Parameters
        ----------
        team_id : str
            Team GUID.
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
            f"{self.endpoint}/{team_id}/members",
            params={"page": page, "per_page": per_page},
        )

    @_ret_json
    def add_user_to_team(self, team_id: str, user_id: str) -> Any:
        """Add user to the team by user_id.

        Parameters
        ----------
        team_id : str
            Team GUID.
        user_id : str
            ID of the user to invite to team.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/{team_id}/members",
            body_json={"team_id": team_id, "user_id": user_id},
        )

    @_ret_json
    def add_user_to_team_from_invite(self, token: str) -> Any:
        """Add user to team from invite.

        Using either an invite id or hash/data pair from an email invite link,
        add a user to a team.

        Parameters
        ----------
        token : str
            Token ID from the invitation.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/members/invite", params={"token": token}
        )

    @_ret_json
    def add_multiple_users_to_team(
        self, team_id: str, users_per_team: List[Dict[str, Any]]
    ) -> Any:
        """Add a number of users to the team by user_id.

        Parameters
        ----------
        team_id : str
            Team GUID.
        users_per_team : list of dict
            The users to add as a list.
            Example:
            [
                {
                    "team_id": "string",
                    "user_id": "string",
                    "roles": "string",
                    "delete_at": 0,
                    "scheme_user": true,
                    "scheme_admin": true,
                    "explicit_roles": "string"
                }
            ]

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/{team_id}/members/batch",
            body_json=users_per_team,
        )

    @_ret_json
    def get_team_members_for_user(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of team members for a user.

        Parameters
        ----------
        user_id : str
            ID of the user to invite to team.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{Users.endpoint}/{user_id}/teams/members")

    @_ret_json
    def get_team_member(
        self, team_id: str, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a team member on the system.

        Parameters
        ----------
        team_id : str
            Team GUID.
        user_id : str
            ID of the user to invite to team.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{team_id}/members/{user_id}")

    @_ret_json
    def remove_user_from_team(self, team_id: str, user_id: str) -> Any:
        """Remove user from team.

        Parameters
        ----------
        team_id : str
            Team GUID.
        user_id : str
            ID of the user to invite to team.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.delete(
            f"{self.endpoint}/{team_id}/members/{user_id}"
        )

    @_ret_json
    def get_team_members_by_id(self, team_id: str, user_ids: List[str]) -> Any:
        """Get a list of team members based on a provided array of user IDs.

        Parameters
        ----------
        team_id : str
            Team GUID.
        user_ids : list of str
            List of user IDs.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/{team_id}/members/ids", body_json=user_ids
        )

    @_ret_json
    def get_team_stats(
        self, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a team stats on the system.

        Parameters
        ----------
        team_id : str
            Team GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{team_id}/stats")

    @_ret_json
    def get_team_icon(
        self, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get the team icon of the team.

        Parameters
        ----------
        team_id : str
            Team GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{team_id}/image")

    @_ret_json
    def set_team_icon(self, team_id: str, files: Dict[str, Any]) -> Any:
        """Set the team icon for the team.

        Parameters
        ----------
        team_id : str
            Team GUID.
        files : dict
            The image to be uploaded.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/{team_id}/image", files=files
        )

    @_ret_json
    def delete_team_icon(self, team_id: str) -> Any:
        """Remove the team icon for the team.

        Parameters
        ----------
        team_id : str
            Team GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.delete(f"{self.endpoint}/{team_id}/image")

    @_ret_json
    def update_team_member_roles(
        self, team_id: str, user_id: str, roles: str
    ) -> Any:
        """Update a team member roles.

        Parameters
        ----------
        team_id : str
            Team GUID.
        user_id : str
            User GUID.
        roles : str
            Space-delimited team roles to assign to the user.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{team_id}/members/{user_id}/roles",
            body_json={"roles": roles},
        )

    @_ret_json
    def update_scheme_derived_roles_of_team_member(
        self,
        team_id: str,
        user_id: str,
        body_json: Dict[str, Any],
    ) -> Any:
        """Update a team member's scheme_admin/scheme_user properties.

        Parameters
        ----------
        team_id : str
            Team GUID.
        user_id : str
            User GUID.
        body_json : dict
            The shceme properties as a dict.
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
            f"{self.endpoint}/{team_id}/members/{user_id}/schemeRoles",
            body_json=body_json,
        )

    @_ret_json
    def get_team_unreads_for_user(
        self, user_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get team unreads for a user.

        Get the count for unread messages and mentions in the teams the user is
        a member of.

        Parameters
        ----------
        user_id : str
            User GUID.
        params : dict, optional
            Query parameters to include.
            Example:
            {
                "exclude_team": "string",
                "include_collapsed_threads": false
            }

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Users.endpoint}/{user_id}/teams/unread", params=params
        )

    @_ret_json
    def get_unreads_for_team(
        self, user_id: str, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get the unread mention and message counts for a team for a user.

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
            f"{Users.endpoint}/{user_id}/teams/{team_id}/unread",
        )

    @_ret_json
    def invite_users_to_team_by_mail(
        self, team_id: str, email_addresses: List[str]
    ) -> Any:
        """Invite users to the existing team using their email addresses.

        Parameters
        ----------
        team_id : str
            Team GUID.
        email_addresses : list of str
            List of user's email addresses.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/{team_id}/invite/email",
            body_json=email_addresses,
        )

    @_ret_json
    def import_team_from_other_app(
        self, team_id: str, data: Dict[str, Any]
    ) -> Any:
        """Import a team into a existing team.

        Import users, channels, posts, hooks.

        Parameters
        ----------
        team_id : str
            Team GUID.
        data : dict
            The file data as a dict:
            file : str
                A file to be uploaded in zip format.
            filesize : int
                The size of the zip file to be imported.
            importFrom : str
                String that defines from which application the team was
                exported to be imported into Mattermost.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/{team_id}/import", data=data)

    @_ret_json
    def get_invite_info_for_team(
        self, invite_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get invite info for a team.

        Parameters
        ----------
        invite_id : str
            Invite ID for a team.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/invite/{invite_id}")

    @_ret_json
    def set_team_scheme(self, team_id: str) -> Any:
        """Set a team's scheme.

        Parameters
        ----------
        team_id : str
            Team GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(f"{self.endpoint}/{team_id}/scheme")

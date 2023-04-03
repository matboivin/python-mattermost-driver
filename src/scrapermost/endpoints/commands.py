"""Endpoints for creating, getting and updating slash commands."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint
from .teams import Teams


@dataclass
class Commands(APIEndpoint):
    """Class defining the Commands API endpoint.

    Attributes
    ----------
    endpoint : str, default='commands'
        The endpoint path.

    Methods
    -------
    create_command(body_json)
        Create a command for a team.
    list_commands_for_team(team_id, custom_only=False)
        List commands for a team.
    list_autocomplete_commands(team_id)
        List autocomplete commands in the team.
    update_command(command_id, body_json)
        Update a command.
    delete_command(command_id)
        Delete a command based on command ID string.
    generate_new_token(command_id)
        Generate a new token for the command based on command ID string.
    execute_command(channel_id, command)
        Execute a command on a team.

    """

    endpoint: str = "commands"

    def create_command(
        self, body_json: Dict[str, Any]
    ) -> Any | Awaitable[Any]:
        """Create a command for a team.

        Parameters
        ----------
        body_json : dict
            A JSON serializable object to include in the body of the request.
            Example:
            {
                "team_id": "string",
                "method": "string",
                "trigger": "string",
                "url": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(self.endpoint, body_json=body_json)

    def list_commands_for_team(
        self, team_id: str, custom_only: bool = False
    ) -> Any | Response | Awaitable[Any | Response]:
        """List commands for a team.

        Parameters
        ----------
        team_id : str
            Team GUID.
        custom_only : bool, default=False
            Whether to get only the custom commands.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.get(
            self.endpoint,
            params={"team_id": team_id, "custom_only": custom_only},
        )

    def list_autocomplete_commands(
        self, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """List autocomplete commands in the team.

        Parameters
        ----------
        team_id : str
            Team GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Teams.endpoint}{team_id}/{self.endpoint}/autocomplete"
        )

    def update_command(
        self, command_id: str, body_json: Dict[str, Any]
    ) -> Any | Awaitable[Any]:
        """Update a command.

        Parameters
        ----------
        command_id : str
            ID of the command to update.
        body_json : dict
            The parameters to update as a dict.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{command_id}", body_json=body_json
        )

    def delete_command(self, command_id: str) -> Any | Awaitable[Any]:
        """Delete a command based on command ID string.

        Parameters
        ----------
        command_id : str
            ID of the command to update.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.delete(f"{self.endpoint}/{command_id}")

    def generate_new_token(self, command_id: str) -> Any | Awaitable[Any]:
        """Generate a new token for the command based on command ID string.

        Parameters
        ----------
        command_id : str
            ID of the command to update.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(f"{self.endpoint}/{command_id}/regen_token")

    def execute_command(
        self, channel_id: str, command: str
    ) -> Any | Awaitable[Any]:
        """Execute a command on a team.

        Parameters
        ----------
        channel_id : str
            ID of the channel in which the command will execute.
        command : str
            The slash command to execute, including parameters.
            Example: '/echo bounces around the room'

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/execute",
            body_json={"channel_id": channel_id, "command": command},
        )

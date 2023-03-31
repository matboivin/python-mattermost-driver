"""Endpoints for creating, getting and updating slash commands."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint
from .teams import Teams


@dataclass
class Commands(APIEndpoint):
    """Class defining the /commands API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------

    """

    endpoint: str = "/commands"

    def create_command(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(self.endpoint, body_json=body_json)

    def list_commands_for_team(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(self.endpoint, params=params)

    def list_autocomplete_commands(
        self, team_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Teams.endpoint}{team_id}/commands/autocomplete"
        )

    def update_command(
        self, command_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(self.endpoint + command_id, body_json=body_json)

    def delete_command(self, command_id: str) -> Any | Awaitable[Any]:
        return self.client.delete(self.endpoint + command_id)

    def generate_new_token(self, command_id: str) -> Any | Awaitable[Any]:
        return self.client.put(f"{self.endpoint}/{command_id}/regen_token")

    def execute_command(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/execute", body_json=body_json
        )

"""Class defining the user preferences API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint
from .users import Users


@dataclass
class Preferences(APIEndpoint):
    """Class defining the user preferences API endpoint.

    Note the endpoint is /user and not /preferences.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = Users.endpoint

    def get_user_preferences(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{user_id}/preferences")

    def save_user_preferences(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{user_id}/preferences", options=options
        )

    def delete_user_preferences(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{user_id}/preferences/delete",
            options=options,
        )

    def list_user_preferences_by_category(
        self, user_id: str, category: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{self.endpoint}/{user_id}/preferences/{category}"
        )

    def get_specific_user_preference(
        self, user_id: str, category: str, preference_name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{self.endpoint}/{user_id}/preferences/{category}/name/"
            f"{preference_name}"
        )

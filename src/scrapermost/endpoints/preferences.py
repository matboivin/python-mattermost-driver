"""Endpoints for saving and modifying user preferences."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict, List

from requests import Response

from .base import APIEndpoint, _ret_json
from .users import Users


@dataclass
class Preferences(APIEndpoint):
    """Class defining the user preferences API endpoint.

    Note the endpoint is /user and not /preferences.

    Attributes
    ----------
    endpoint : str, default='user'
        The endpoint path.

    Methods
    -------
    get_user_preferences(user_id)
        Get a list of the user's preferences.
    save_user_preferences(user_id, preferences)
        Save a list of the user's preferences.
    delete_user_preferences(user_id, preferences)
        Delete a list of the user's preferences.
    list_user_preferences_by_category(user_id, category)
        List the current user's stored preferences in the given category.
    get_specific_user_preference(user_id, category, preference_name)
        Get a single preference for the current user.

    """

    endpoint: str = Users.endpoint

    @_ret_json
    def get_user_preferences(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of the user's preferences.

        Parameters
        ----------
        user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{user_id}/preferences")

    @_ret_json
    def save_user_preferences(
        self, user_id: str, preferences: List[Dict[str, Any]]
    ) -> Any:
        """Save a list of the user's preferences.

        Parameters
        ----------
        user_id : str
            User GUID.
        preferences : list of dict
            List of preference objects.
            Example:
            [
                {
                    "user_id": "string",
                    "category": "string",
                    "name": "string",
                    "value": "string"
                }
            ]

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{user_id}/preferences", body_json=preferences
        )

    @_ret_json
    def delete_user_preferences(
        self, user_id: str, preferences: List[Dict[str, Any]]
    ) -> Any:
        """Delete a list of the user's preferences.

        Parameters
        ----------
        user_id : str
            User GUID.
        preferences : list of dict
            List of preference objects.
            Example:
            [
                {
                    "user_id": "string",
                    "category": "string",
                    "name": "string",
                    "value": "string"
                }
            ]

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/{user_id}/preferences/delete",
            body_json=preferences,
        )

    @_ret_json
    def list_user_preferences_by_category(
        self, user_id: str, category: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """List the current user's stored preferences in the given category.

        Parameters
        ----------
        user_id : str
            User GUID.
        category : str
            The category of a group of preferences.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{self.endpoint}/{user_id}/preferences/{category}"
        )

    @_ret_json
    def get_specific_user_preference(
        self, user_id: str, category: str, preference_name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a single preference for the current user.

        Parameters
        ----------
        user_id : str
            User GUID.
        category : str
            The category of a group of preferences.
        preference_name : str
            Preference name.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{self.endpoint}/{user_id}/preferences/{category}/name/"
            f"{preference_name}"
        )

"""Endpoints for creating, getting and interacting with users."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint, _ret_json


@dataclass
class Users(APIEndpoint):
    """Class defining the Users API endpoint.

    Attributes
    ----------
    endpoint : str, default='users'
        The endpoint path.

    Methods
    -------
    login_user(body_json)
        Login to Mattermost server.
    logout_user()
        Logout from the Mattermost server.
    create_user(body_json=None, params=None)
        Create a new user on the system.
    get_users(params=None)
        Get a page of a list of users.
    get_users_by_ids(body_json=None)
        Get a list of users based on a provided list of user IDs.
    get_users_by_usernames(body_json=None)
        Get a list of users based on a provided list of usernames.
    search_users(body_json=None)
        Get a list of users based on search criteria in the request body.
    autocomplete_users(params=None)
        Autocomplete users.
    get_stats()
        Get a total count of users in the system.
    get_user(user_id)
        Get a user a object.
    update_user(user_id, body_json=None)
        Update a user by providing the user object.
    deactivate_user(user_id)
        Deactivate the user.
    patch_user(user_id, body_json=None)
        Update a user partially.
    update_user_role(user_id, body_json=None)
        Update a user's system-level roles.
    update_user_active_status(user_id, body_json=None)
        Update user active or inactive status.
    get_user_profile_image(user_id)
        Get user's profile image.
    set_user_profile_image(user_id, files)
        Set user's profile image.
    get_user_by_username(username)
        Get a user object by providing a username.
    reset_password(body_json=None)
        Reset password.
    update_user_mfa(user_id, body_json=None)
        Activate multi-factor authentication for the user.
    generate_mfa(user_id)
        Generate an multi-factor authentication secret for a user.
    check_mfa(body_json=None)
        Check if a user has multi-factor authentication active.
    update_user_password(user_id, body_json=None)
        Update a user's password.
    send_password_reset_mail(body_json=None)
        Send an email containing a link for resetting the user's password.
    get_user_by_email(email)
        Get a user object by providing a user email.
    get_user_sessions(user_id)
        Get a list of sessions by providing the user GUID.
    revoke_user_session(user_id, body_json=None)
        Revoke a user session from the provided user ID and session ID.
    revoke_all_user_sessions(user_id)
        Revoke all user sessions from the provided user ID and session ID.
    attach_mobile_device(body_json=None)
        Attach a mobile device ID to the currently logged in session.
    get_user_audits(user_id)
        Get a list of audit by providing the user GUID.
    verify_user_email(body_json=None)
        Verify the email used by a user to sign-up their account with.
    send_verification_mail(body_json=None)
        Send verification email.
    create_user_access_token(user_id, body_json=None)
        Create a user access token.
    get_user_access_token(token_id)
        Get a user access token.
    disable_personal_access_token(body_json=None)
        Disable a personal access token.
    enable_personal_access_token(body_json=None)
        Re-enable a personal access token that has been disabled.
    search_tokens(body_json=None)
        Get a list of tokens based on search criteria in the request body.
    update_user_authentication_method(user_id, body_json=None)
        Update a user's authentication method.

    """

    endpoint: str = "users"

    def login_user(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        """Login to Mattermost server.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/login", body_json=body_json)

    @_ret_json
    def logout_user(self) -> Any | Response | Awaitable[Any | Response]:
        """Logout from the Mattermost server.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(f"{self.endpoint}/logout")

    @_ret_json
    def create_user(
        self,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Create a new user on the system.

        Password is required for email login. For other authentication types
        such as LDAP or SAML, auth_data and auth_service fields are required.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.
        params : dict, optional
            Query parameters to include.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            self.endpoint, body_json=body_json, params=params
        )

    @_ret_json
    def get_users(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of a list of users.

        Parameters
        ----------
        params : dict, optional
            Query parameters to include.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(self.endpoint, params=params)

    @_ret_json
    def get_users_by_ids(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of users based on a provided list of user IDs.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(f"{self.endpoint}/ids", body_json=body_json)

    @_ret_json
    def get_users_by_usernames(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of users based on a provided list of usernames.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/usernames", body_json=body_json
        )

    @_ret_json
    def search_users(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of users based on search criteria in the request body.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(f"{self.endpoint}/search", body_json=body_json)

    @_ret_json
    def autocomplete_users(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Autocomplete users.

        Get a list of users for the purpose of autocompleting based on the
        provided search term.

        Parameters
        ----------
        params : dict, optional
            Query parameters to include.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/autocomplete", params=params)

    @_ret_json
    def get_stats(self) -> Any | Response | Awaitable[Any | Response]:
        """Get a total count of users in the system.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/stats")

    @_ret_json
    def get_user(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a user a object.

        Sensitive information will be sanitized out.

        Parameters
        ----------
        user_id : str
            User GUID.
            This can also be "me" which will point to the current user.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{user_id}")

    @_ret_json
    def update_user(
        self, user_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Update a user by providing the user object.

        Parameters
        ----------
        user_id : str
            User GUID.
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/{user_id}", body_json=body_json
        )

    @_ret_json
    def deactivate_user(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Deactivate the user.

        Revoke all its sessions by archiving its user object.

        Parameters
        ----------
        user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.delete(f"{self.endpoint}/{user_id}")

    @_ret_json
    def patch_user(
        self, user_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Update a user partially.

        Provide only the fields you want to update.

        Parameters
        ----------
        user_id : str
            User GUID.
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/{user_id}/patch", body_json=body_json
        )

    @_ret_json
    def update_user_role(
        self, user_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Update a user's system-level roles.

        Valid user roles are "system_user", "system_admin" or both of them.

        Parameters
        ----------
        user_id : str
            User GUID.
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/{user_id}/roles", body_json=body_json
        )

    @_ret_json
    def update_user_active_status(
        self, user_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Update user active or inactive status.

        Parameters
        ----------
        user_id : str
            User GUID.
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/{user_id}/active", body_json=body_json
        )

    @_ret_json
    def get_user_profile_image(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get user's profile image.

        Parameters
        ----------
        user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{user_id}/image")

    @_ret_json
    def set_user_profile_image(
        self, user_id: str, files: Dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Set user's profile image.

        Parameters
        ----------
        user_id : str
            User GUID.
        files : dict
            The image's bytes string to be uploaded.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/{user_id}/image", files=files
        )

    @_ret_json
    def get_user_by_username(
        self, username: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a user object by providing a username.

        Sensitive information will be sanitized out.

        Parameters
        ----------
        username : str
            Username.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/username/{username}")

    @_ret_json
    def reset_password(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Reset password.

        Update the password for a user using a one-use, timed recovery code
        tied to the user's account.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/password/reset", body_json=body_json
        )

    @_ret_json
    def update_user_mfa(
        self, user_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Activate multi-factor authentication for the user.

        Parameters
        ----------
        user_id : str
            User GUID.
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/{user_id}/mfa", body_json=body_json
        )

    @_ret_json
    def generate_mfa(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Generate an multi-factor authentication secret for a user.

        Parameters
        ----------
        user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(f"{self.endpoint}/{user_id}/mfa/generate")

    @_ret_json
    def check_mfa(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Check if a user has multi-factor authentication active.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(f"{self.endpoint}/mfa", body_json=body_json)

    @_ret_json
    def update_user_password(
        self, user_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Update a user's password.

        Parameters
        ----------
        user_id : str
            User GUID.
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/{user_id}/password", body_json=body_json
        )

    @_ret_json
    def send_password_reset_mail(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Send an email containing a link for resetting the user's password.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/password/reset/send", body_json=body_json
        )

    @_ret_json
    def get_user_by_email(
        self, email: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a user object by providing a user email.

        Sensitive information will be sanitized out.

        Parameters
        ----------
        email : str
            User email.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/email/{email}")

    @_ret_json
    def get_user_sessions(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of sessions by providing the user GUID.

        Sensitive information will be sanitized out.

        Parameters
        ----------
        user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{user_id}/sessions")

    @_ret_json
    def revoke_user_session(
        self, user_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Revoke a user session from the provided user ID and session ID.

        Parameters
        ----------
        user_id : str
            User GUID.
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/{user_id}/sessions/revoke", body_json
        )

    @_ret_json
    def revoke_all_user_sessions(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Revoke all user sessions from the provided user ID and session ID.

        Parameters
        ----------
        user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/{user_id}/sessions/revoke/all",
        )

    @_ret_json
    def attach_mobile_device(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Attach a mobile device ID to the currently logged in session.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/sessions/device", body_json=body_json
        )

    @_ret_json
    def get_user_audits(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of audit by providing the user GUID.

        Parameters
        ----------
        user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{user_id}/audits")

    @_ret_json
    def verify_user_email(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Verify the email used by a user to sign-up their account with.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/email/verify", body_json=body_json
        )

    @_ret_json
    def send_verification_mail(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Send verification email.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/email/verify/send", body_json=body_json
        )

    @_ret_json
    def switch_login_method(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Send verification email.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/login/switch", body_json=body_json
        )

    @_ret_json
    def create_user_access_token(
        self, user_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Create a user access token.

        Generate a user access token that can be used to authenticate with
        the Mattermost REST API.

        Parameters
        ----------
        user_id : str
            User GUID.
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/{user_id}/tokens", body_json=body_json
        )

    @_ret_json
    def get_user_access_token(
        self, token_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a user access token.

        Does not include the actual authentication token.

        Parameters
        ----------
        token_id : str
            Token GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/tokens/{token_id}")

    @_ret_json
    def disable_personal_access_token(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Disable a personal access token.

        Delete any sessions using the token.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/tokens/disable", body_json=body_json
        )

    @_ret_json
    def enable_personal_access_token(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Re-enable a personal access token that has been disabled.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/tokens/enable", body_json=body_json
        )

    @_ret_json
    def search_tokens(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of tokens based on search criteria in the request body.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/tokens/search", body_json=body_json
        )

    @_ret_json
    def update_user_authentication_method(
        self, user_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Update a user's authentication method.

        Parameters
        ----------
        user_id : str
            User GUID.
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/{user_id}/auth", body_json=body_json
        )

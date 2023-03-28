"""Class defining the /users API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Users(APIEndpoint):
    """Class defining the /users API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/users"

    def login_user(
        self, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/login", options=options)

    def logout_user(self) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/logout")

    def create_user(
        self,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Any | Awaitable[Any]:
        return self.client.post(self.endpoint, options=options, params=params)

    def get_users(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(self.endpoint, params=params)

    def get_users_by_ids(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/ids", options=options)

    def get_users_by_usernames(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/usernames", options=options)

    def search_users(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/search", options=options)

    def autocomplete_users(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/autocomplete", params=params)

    def get_user(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{user_id}")

    def update_user(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(f"{self.endpoint}/{user_id}", options=options)

    def deactivate_user(self, user_id: str) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/{user_id}")

    def patch_user(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{user_id}/patch", options=options
        )

    def update_user_role(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{user_id}/roles", options=options
        )

    def update_user_active_status(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{user_id}/active", options=options
        )

    def get_user_profile_image(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{user_id}/image")

    def set_user_profile_image(
        self, user_id: str, files: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{user_id}/image", files=files
        )

    def get_user_by_username(
        self, username: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/username/{username}")

    def reset_password(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/password/reset", options=options
        )

    def update_user_mfa(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{user_id}/mfa", options=options
        )

    def generate_mfa(self, user_id: str) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/{user_id}/mfa/generate")

    def check_mfa(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/mfa", options=options)

    def update_user_password(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{user_id}/password", options=options
        )

    def send_password_reset_mail(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/password/reset/send", options=options
        )

    def get_user_by_email(
        self, email: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/email/{email}")

    def get_user_sessions(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{user_id}/sessions")

    def revoke_user_session(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{user_id}/sessions/revoke", options
        )

    def revoke_all_user_sessions(self, user_id: str) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{user_id}/sessions/revoke/all",
        )

    def attach_mobile_device(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/sessions/device", options=options
        )

    def get_user_audits(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{user_id}/audits")

    def verify_user_email(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/email/verify", options=options
        )

    def send_verification_mail(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/email/verify/send", options=options
        )

    def switch_login_method(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/login/switch", options=options
        )

    def disable_personal_access_token(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/tokens/disable", options=options
        )

    def enable_personal_access_token(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/tokens/enable", options=options
        )

    def get_user_access_token(self, token_id: str) -> Any | Awaitable[Any]:
        return self.client.get(f"{self.endpoint}/tokens/" + token_id)

    def search_tokens(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/tokens/search", options=options
        )

    def update_user_authentication_method(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{user_id}/auth", options=options
        )

    def create_user_access_token(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{user_id}/tokens", options=options
        )

    def get_stats(self) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/stats")

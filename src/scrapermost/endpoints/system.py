"""General endpoints for interacting with the server.

Example usages: configuration and logging.
"""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class System(APIEndpoint):
    """Class defining the system API endpoint.

    This endpoint has a mix of different endpoints, not only /system

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------

    """

    def check_system_health(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get("system/ping")

    def recycle_database_connection(self) -> Any | Awaitable[Any]:
        return self.client.post("database/recycle")

    def send_test_email(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post("email/test", body_json=body_json)

    def get_configuration(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get("config")

    def update_configuration(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.put("config", body_json=body_json)

    def reload_configuration(self) -> Any | Awaitable[Any]:
        return self.client.post("config/reload")

    def get_client_configuration(
        self, params: Dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get("config/client", params=params)

    def upload_license_file(
        self, files: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post("license", files=files)

    def remove_license_file(self) -> Any | Awaitable[Any]:
        return self.client.delete("license")

    def get_client_license(
        self, params: Dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get("license/client", params=params)

    def get_audits(
        self, params: Dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get("audits", params=params)

    def invalidate_all_caches(self) -> Any | Awaitable[Any]:
        return self.client.post("/caches/invalidate")

    def get_logs(
        self, params: Dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get("logs", params=params)

    def add_log_message(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post("logs", body_json=body_json)

    def get_webrtc_token(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get("webrtc/token")

    def get_analytics(
        self, params: Dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get("analytics/old", params=params)

    def get_configuration_environment(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get("config/environment")

    def test_aws_s3_connection(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post("file/s3_test", body_json=body_json)

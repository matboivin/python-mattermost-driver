"""General endpoints for interacting with the server.

Example usages: configuration and logging.
"""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint, _ret_json


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
    check_system_health()
        Check system health.
    recycle_database_connection()
        Recycle database connections.
    send_test_email(body_json)
        Send a test email.
    get_configuration()
        Retrieve the current server configuration.
    update_configuration(body_json)
        Submit a new configuration for the server to use.
    reload_configuration()
        Reload the configuration file to pick up on any changes made to it.
    get_client_configuration(params)
        Get a subset of the server configuration needed by the client.
    upload_license_file(files)
        Upload a license to enable enterprise features.
    remove_license_file()
        Remove the license file from the server.
    get_client_license(params)
        Get a subset of the server license needed by the client.
    get_audits(page=0, per_page=60)
        Get a page of audits for all users on the system.
    invalidate_all_caches()
        Purge all the in-memory caches for the Mattermost server.
    get_logs(page=0, per_page=60)
        Get a page of server logs.
    add_log_message(level, message)
        Add log messages to the server logs.
    get_analytics(params)
        Get some analytics data about the system.
    get_configuration_environment()
        Get configuration made through environment variables.
    test_aws_s3_connection(body_json=None)
        Test AWS S3 connection.

    """

    @_ret_json
    def check_system_health(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Check system health.

        Check if the server is up and healthy based on the configuration
        setting GoRoutineHealthThreshold.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get("system/ping")

    @_ret_json
    def recycle_database_connection(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Recycle database connections.

        Recycle database connections by closing and reconnecting all
        connections to master and read replica databases.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post("database/recycle")

    @_ret_json
    def send_test_email(
        self, body_json: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Send a test email.

        Parameters
        ----------
        body_json : dict
            Mattermost configuration as a dict.
            https://api.mattermost.com/#tag/system/operation/TestEmail

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post("email/test", body_json=body_json)

    @_ret_json
    def get_configuration(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Retrieve the current server configuration.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get("config")

    @_ret_json
    def update_configuration(
        self, body_json: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Submit a new configuration for the server to use.

        Parameters
        ----------
        body_json : dict
            Mattermost configuration as a dict.
            https://api.mattermost.com/#tag/system/operation/UpdateConfig

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put("config", body_json=body_json)

    @_ret_json
    def reload_configuration(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Reload the configuration file to pick up on any changes made to it.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post("config/reload")

    @_ret_json
    def get_client_configuration(
        self, params: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a subset of the server configuration needed by the client.

        Parameters
        ----------
        params : dict
            Query parameters to include such as format.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get("config/client", params=params)

    @_ret_json
    def upload_license_file(
        self, files: dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Upload a license to enable enterprise features.

        Parameters
        ----------
        files : dict
            The licence to be uploaded.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post("license", files=files)

    @_ret_json
    def remove_license_file(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Remove the license file from the server.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.delete("license")

    @_ret_json
    def get_client_license(
        self, params: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a subset of the server license needed by the client.

        Parameters
        ----------
        params : dict
            Query parameters to include such as format.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get("license/client", params=params)

    @_ret_json
    def get_audits(
        self, page: int = 0, per_page: int = 60
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of audits for all users on the system.

        Parameters
        ----------
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
            "audits", params={"page": page, "per_page": per_page}
        )

    @_ret_json
    def invalidate_all_caches(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Purge all the in-memory caches for the Mattermost server.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post("/caches/invalidate")

    @_ret_json
    def get_logs(
        self, page: int = 0, per_page: int = 60
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of server logs.

        Parameters
        ----------
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
            "logs", params={"page": page, "per_page": per_page}
        )

    @_ret_json
    def add_log_message(
        self, level: str, message: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Add log messages to the server logs.

        Parameters
        ----------
        level : str
            The error level, ERROR or DEBUG.
        message : str
            Message to send to the server logs

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            "logs", body_json={"level": level, "message": message}
        )

    @_ret_json
    def get_analytics(
        self, params: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get some analytics data about the system.

        Parameters
        ----------
        params : dict
            Query parameters to include.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get("analytics/old", params=params)

    @_ret_json
    def get_configuration_environment(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get configuration made through environment variables.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get("config/environment")

    @_ret_json
    def test_aws_s3_connection(
        self, body_json: dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Test AWS S3 connection.

        Send a test to validate if can connect to AWS S3. Optionally provide a
        configuration in the request body to test.
        If no valid configuration is present in the request body the current
        server configuration will be tested.

        Parameters
        ----------
        body_json : dict, optional
            Mattermost configuration to test.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post("file/s3_test", body_json=body_json)

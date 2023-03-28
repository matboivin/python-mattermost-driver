"""Driver options class."""

from typing import Any, Dict


class DriverOptions:
    """Class to hold the driver options.

    Attributes
    ----------
    debug : bool, default=False
        Whether to run debugging mode.
    scheme : str, default='https'
        The protocol to be used to access the Mattermost server.
    hostname : str, default='localhost'
        The Mattermost server host name.
    port : int, default=8065
        The post to be used to access the Mattermost server.
    basepath : str, default='/api/v4'
        The path to the API endoint.
    login_id : str, default=None
        The user account's email address or username.
    password : str, default=None
        The user's password.
    token : str, default=None
        The user's token.
    mfa_token : Any, default=None
        The Multi-Factor Authentication token. If MFA is enabled, the user has
        to provide a secure one-time code.
    auth : Any, default=None
        An authentication class used by the httpx client when sending requests.
    verify : bool, default=True
        Whether instantiating a httpx client with SSL verification enabled.
    http2 : bool, default=False
        Whether instantiating a httpx client with HTTP/2.
    proxy : str, default=None
        Proxy URL for every request.
    request_timeout : int, default=None
        The timeout configuration used by the httpx client when sending
        request. If none, use default httpx client timeout (5 seconds).
    timeout : float, default=30
        The Mattermost websocket connection's timeout in seconds.
    keepalive : bool, default=False
        Whether to keep the websocket connection alive.
    keepalive_delay : float, default=5
        Duration in seconds between two keepalive transmissions.
    websocket_kw_args : dict, default=None

    """

    def __init__(self, options: Dict[str, Any]) -> None:
        """Send a DELETE request.

        Parameters
        ----------
        options : dict
            The driver options as a dict.

        Raises
        ------
        RuntimeError
            If 'login_id' and 'password' or 'token' are missing.

        """
        if not all(
            [options.get("login_id"), options.get("password")]
        ) or not options.get("token"):
            raise RuntimeError(
                "Required options are 'login_id' and 'password', or 'token.'"
            )

        self.debug: bool = options.get("debug", False)
        self.scheme: str = options.get("scheme", "https")
        self.hostname: str = options.get("hostname", "localhost")
        self.port: int = options.get("port", 8065)
        self.basepath: str = options.get("basepath", "/api/v4")
        self.login_id: str | None = options.get("login_id")
        self.password: str | None = options.get("password")
        self.token: str | None = options.get("token")
        self.mfa_token: Any | None = options.get("mfa_token")
        # httpx client options
        self.auth: Any | None = options.get("auth")
        self.verify: bool = options.get("verify", True)
        self.http2: bool = options.get("http2", False)
        self.proxy: str | None = options.get("proxy")
        self.request_timeout: int | None = options.get("request_timeout")
        # websocket options
        self.timeout: float = options.get("timeout", 30)
        self.keepalive: bool = options.get("keepalive", False)
        self.keepalive_delay: float = options.get("keepalive_delay", 5)
        self.websocket_kw_args: Dict[str, Any] = options.get(
            "websocket_kw_args", {}
        )

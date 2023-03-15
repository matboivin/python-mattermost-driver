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
    password : str, default=None
    token : str, default=None
    mfa_token : Any, default=None
    auth : Any, default=None
    proxy : dict, default=None
    verify : bool, default=True
    http2 : bool, default=False
    timeout : int, default=30
    request_timeout : int, default=None
    keepalive : bool, default=False
    keepalive_delay : int, default=5
    websocket_kw_args : dict, default=None

    """

    def __init__(
        self,
        options: Dict[str, Any] | None,
    ) -> None:
        self.debug: bool = options.get("debug", False)
        self.scheme: str = options.get("scheme", "https")
        self.hostname: str = options.get("hostname", "localhost")
        self.port: int = options.get("port", 8065)
        self.basepath: str = options.get("basepath", "/api/v4")
        self.login_id: str | None = options.get("login_id")
        self.password: str | None = options.get("password")
        self.token: str | None = options.get("token")
        self.mfa_token: Any | None = options.get("mfa_token")
        self.auth: Any | None = options.get("auth")
        self.proxy: Dict[str, Any] | None = options.get("proxy")
        self.verify: bool = options.get("verify", True)
        self.http2: bool = options.get("http2", False)
        self.timeout: int = options.get("timeout", 30)
        self.request_timeout: int = options.get("request_timeout", 30)
        self.keepalive: bool = options.get("keepalive", False)
        self.keepalive_delay: int = options.get("keepalive_delay", 5)
        self.websocket_kw_args: Dict[str, Any] = options.get(
            "websocket_kw_args", dict()
        )

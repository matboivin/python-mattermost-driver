"""Client base class.

This class holds information about the logged-in user and actually makes the
requests to the Mattermost server.
"""

from abc import ABC
from logging import DEBUG, INFO, Logger, getLogger
from typing import Any, Dict

from .options import DriverOptions

logger: Logger = getLogger("scrapermost.client")
logger.setLevel(INFO)


class BaseClient(ABC):
    """Base for creating client classes.

    Attributes
    ----------
    _url : str
        URL to make API requests. Example: 'https://server.com/api/v4'.
    _user_id : str, default=None
        Mattermost user ID.
    _username : str, default=None
        Mattermost username.
    _auth : Any, default=None
        An authentication class used by the httpx client when sending requests.
    _token : str, default=None
        Mattermost user token.
    _cookies : Any, default=None
        The cookies given when the driver login to the Mattermost server.
    httpx_client : httpx.AsyncClient or httpx.Client
        The underlying httpx client object.

    Static methods
    --------------
    activate_verbose_logging()
        Enable trace level logging in httpx.

    Methods
    -------
    get_auth_header()
        Get Authorization header.

    """

    def __init__(self, options: DriverOptions) -> None:
        """Initialize client.

        Parameters
        ----------
        options : options.DriverOptions
            The client options.

        """
        self._url: str = (
            f"{options.scheme}://"
            f"{options.hostname}:{options.port}{options.basepath}"
        )
        self._user_id: str = ""
        self._username: str = ""
        self._auth: Any | None = options.auth
        self._token: str = ""
        self._cookies: Any | None = None

        if options.debug:
            logger.setLevel(DEBUG)
            self.activate_verbose_logging()

    # ############################################################ Properties #

    @property
    def httpx_client(self):  # type: ignore
        """Get the underlying httpx client object."""
        ...

    @property
    def url(self) -> str:
        """Get the Mattermost server's URL.

        Returns
        -------
        str

        """
        return self._url

    @property
    def user_id(self) -> str:
        """Get the user ID of the logged-in user.

        Returns
        -------
        str

        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str) -> None:
        """Set the user ID of the logged-in user.

        Parameters
        ----------
        user_id : str
            The new user ID value.

        """
        self._user_id = user_id

    @property
    def username(self) -> str:
        """Get the username of the logged-in user.

        Returns
        -------
        str
            The username set. Otherwise an empty string.

        """
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        """Set the username of the logged-in user.

        Parameters
        ----------
        username : str
            The new username value.

        """
        self._username = username

    @property
    def auth(self) -> Any | None:
        """Get the authentication class used by the httpx client.

        Returns
        -------
        Any or None

        """
        return self._auth

    @property
    def token(self) -> str:
        """Get the token for the login.

        Returns
        -------
        str

        """
        return self._token

    @token.setter
    def token(self, token: str) -> None:
        """Set the token for the login.

        Parameters
        ----------
        token : str
            The new token value.

        """
        self._token = token

    @property
    def cookies(self) -> Any | None:
        """Get the cookies given on login.

        Returns
        -------
        Any or None

        """
        return self._cookies

    @cookies.setter
    def cookies(self, cookies: Any) -> None:
        """Set the cookies.

        Parameters
        ----------
        cookies : Any
            The new cookies value.

        """
        self._cookies = cookies

    # ######################################################## Static methods #

    @staticmethod
    def activate_verbose_logging() -> None:
        """Enable trace level logging in httpx."""
        httpx_log: Logger = getLogger("httpx")

        httpx_log.setLevel("TRACE")
        httpx_log.propagate = True

    # ############################################################### Methods #

    def get_auth_header(self) -> Dict[str, str] | None:
        """Get Authorization header.

        Returns
        -------
        dict or None

        """
        if self.auth:
            return None
        if not self.token:
            return {}

        return {"Authorization": f"Bearer {self.token}"}

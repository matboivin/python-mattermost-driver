"""Class defining the synchronous driver."""

from asyncio import AbstractEventLoop, get_event_loop
from typing import Any, Callable

from requests import Response

from .base_driver import BaseDriver, logger
from .client import Client
from .websocket import Handler, Websocket


class Driver(BaseDriver):
    """Class defining a synchronous Mattermost driver.

    Attributes
    ----------
    _client : client.Client
        The Mattermost client to interact with Web Service API.

    Properties
    ----------
    client : client.Client
        The Mattermost client to interact with Web Service API.
    login_id : str, optional
        The user account's email address or username.
    password : str, optional
        The user's password.
    mfa_token : Any, optional
        The Multi-Factor Authentication token.
    websocket : websocket.Websocket, optional
        The websocket to listen to Mattermost events.

    Methods
    -------
    _init_websocket(websocket_cls)
        Initialize the websocket connection.
    start_websocket(event_handler, loop=None)
        Start websocket listening loop.
    login()
        Log the user in.
    logout()
        Log the user out.

    """

    def __init__(self, options: dict[str, Any]) -> None:
        """Initialize driver.

        Parameters
        ----------
        options : dict
            The options as a dict.

        """
        super().__init__(options)

        self._client: Client = Client(self.options)

    def __enter__(self) -> Any:
        self.client.__enter__()

        return self

    def __exit__(self, *exc_info: tuple[Any]) -> Any:
        return self.client.__exit__(*exc_info)

    # Properties ##############################################################

    @property
    def client(self) -> Client:
        """Get the underlying Mattermost client.

        Returns
        -------
        client.Client

        """
        return self._client

    # Methods #################################################################

    def _init_websocket(
        self,
        websocket_cls: Callable[..., Websocket] = Websocket,
    ) -> None:
        """Initialize the websocket connection.

        Parameters
        ----------
        websocket_cls : function(), default=websocket.Websocket
            The Websocket class constructor.

        """
        self._websocket = websocket_cls(self.options, self.client.token)

    def start_websocket(
        self,
        event_handler: Handler,
        loop: AbstractEventLoop | None = None,
    ) -> AbstractEventLoop:
        """Start websocket listening loop.

        This should be run after login(), because the websocket needs to
        authenticate.

        Documentation: https://api.mattermost.com/v4/#tag/WebSocket

        Parameters
        ----------
        event_handler : async function(dict) -> None
            The function to handle the websocket events.
        loop : asyncio.AbstractEventLoop, default=None
            The running event loop.

        Returns
        -------
        asyncio.AbstractEventLoop
            The event loop.

        Raises
        ------
        asyncio.TimeoutError
            If the websocket connection timed out.
        aiohttp.client_exceptions.ClientConnectorError
            If the name resolution failed.
        aiohttp.client_exceptions.WSServerHandshakeError
            If websocket server handshake failed.

        """
        if not self._websocket:
            self._init_websocket()

        if loop and loop.is_running():
            loop.create_task(
                self._websocket.connect(event_handler)  # type: ignore
            )

        else:
            loop = get_event_loop()

            loop.run_until_complete(
                self._websocket.connect(event_handler)  # type: ignore
            )

        return loop

    def login(self) -> Any | Response:
        """Log the user in.

        The following information is saved in the client:
        - user_id
        - username
        - cookies

        Returns
        -------
        Any or requests.Response
            The json-encoded content of the response if any.
            Otherwise, the raw response.

        Raises
        ------
        requests.exceptions.HTTPError
            If the connection failed.

        """
        if self.client.token:
            result: Any | Response = self.users.get_user("me")

        else:
            response: Response = self.users.login_user(  # type: ignore
                {
                    "login_id": self.login_id,
                    "password": self.password,
                    "token": self.mfa_token,
                }
            )
            if response.status_code != 200:
                response.raise_for_status()

            self.client.token = response.headers["Token"]
            self.client.cookies = response.cookies

            try:
                result = response.json()

            except ValueError:
                logger.debug(
                    "Could not convert response to JSON. "
                    "Returning raw response."
                )
                result = response

        if not isinstance(result, Response):
            if result.get("id"):
                self.client.user_id = result["id"]

            if result.get("username"):
                self.client.username = result["username"]

        return result

    async def logout(self) -> Any:
        """Log the user out.

        Returns
        -------
        Any
            The json-encoded content of the response.

        """
        result: Any = await self.users.logout_user()

        self.client.user_id = ""
        self.client.username = ""
        self.client.token = None
        self.client.cookies = None

        return result

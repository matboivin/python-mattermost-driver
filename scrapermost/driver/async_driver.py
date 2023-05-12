"""Class defining the asynchronous driver."""

from typing import Any, Awaitable, Callable, Literal

from requests import Response

from .async_client import AsyncClient
from .base_driver import BaseDriver, logger
from .websocket import Websocket


class AsyncDriver(BaseDriver):
    """Class defining an asynchronous Mattermost driver.

    Attributes
    ----------
    client : client.AsyncClient
        The Mattermost client to interact with Web Service API.

    Methods
    -------
    init_websocket(websocket_cls)
        Initialize the websocket connection.
    start_websocket(event_handler, data_format='json')
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

        self._client = AsyncClient(self.options)

    async def __aenter__(self) -> Any:
        await self.client.__aenter__()

        return self

    async def __aexit__(self, *exc_info: tuple[Any]) -> Any:
        return await self.client.__aexit__(*exc_info)

    # ############################################################ Properties #

    @property
    def client(self) -> AsyncClient:
        """Get the underlying Mattermost client.

        Returns
        -------
        async_client.AsyncClient

        """
        return self._client

    # ############################################################### Methods #

    async def init_websocket(
        self,
        websocket_cls: Callable[..., Websocket] = Websocket,
    ) -> None:
        """Initialize the websocket connection.

        Parameters
        ----------
        websocket_cls : function() default=websocket.Websocket
            The Websocket class constructor.

        Raises
        ------
        asyncio.TimeoutError
            If the websocket connection timed out.
        aiohttp.client_exceptions.ClientConnectorError
            If the name resolution failed.
        aiohttp.client_exceptions.WSServerHandshakeError
            If websocket server handshake failed.

        """
        self.websocket = websocket_cls(self.options, self.client.token)

        await self.websocket.connect()

    async def start_websocket(
        self,
        event_handler: Callable[[str | dict[str, Any]], Awaitable[None]],
        data_format: Literal["json", "text"] = "json",
    ) -> Any:
        """Start websocket listening loop.

        Unlike the Driver.init_websocket, this one assumes you are async aware
        and returns a coroutine that can be awaited. It will not return until
        shutdown() is called.

        This should be run after login(), because the websocket needs to
        authenticate.

        Documentation: https://api.mattermost.com/v4/#tag/WebSocket

        Parameters
        ----------
        event_handler : async function(str or dict) -> None
            The function to handle the websocket events.
        data_format : 'json' or 'text', default='json'
            Whether to receive the websocket data as text or JSON.

        Returns
        -------
        Any

        """
        if not self.websocket:
            raise RuntimeError(
                "Websocket not initialized. Use init_websocket() first."
            )

        return await self.websocket.listen(event_handler, data_format)

    async def login(self) -> Any | Response:
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

        """
        if self.options.token:
            self.client.token = self.options.token
            result: Any | Response = await self.users.get_user("me")

        else:
            response: Response = await self.users.login_user(
                {
                    "login_id": self.options.login_id,
                    "password": self.options.password,
                    "token": self.options.mfa_token,
                }
            )

            if response.status_code == 200:
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

        self.client.token = ""
        self.client.user_id = ""
        self.client.username = ""
        self.client.cookies = None

        return result

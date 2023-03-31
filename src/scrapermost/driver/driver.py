"""Class defining the synchronous driver."""

from asyncio import AbstractEventLoop, get_event_loop, run
from typing import Any, Awaitable, Callable, Dict, Literal, Tuple

from requests import Response

from .base_driver import BaseDriver, logger
from .client import Client
from .websocket import Websocket


class Driver(BaseDriver):
    """Class defining a synchronous Mattermost driver.

    Attributes
    ----------
    client : client.Client
        The Mattermost client to interact with Web Service API.

    Methods
    -------
    init_websocket(event_handler, websocket_cls, data_format='json')
        Initialize the websocket connection to the Mattermost server.
    login()
        Log the user in.
    logout()
        Log the user out.

    """

    def __init__(self, options: Dict[str, Any]) -> None:
        """Initialize driver.

        Parameters
        ----------
        options : dict
            The options as a dict.

        """
        super().__init__(options)

        self.client = Client(self.options)

    def __enter__(self) -> Any:
        self.client.__enter__()

        return self

    def __exit__(self, *exc_info: Tuple[Any]) -> Any:
        return self.client.__exit__(*exc_info)

    # ############################################################ Properties #

    @property
    def client(self) -> Client:
        """Get the underlying Mattermost client.

        Returns
        -------
        client.Client

        """
        return self.client

    @BaseDriver.client.setter
    def client(self, client: Client) -> None:
        """Set the underlying Mattermost client.

        Parameters
        ----------
        client : client.Client
            The new synchronous client.

        """
        self.client = client

    # ############################################################### Methods #

    def init_websocket(
        self,
        event_handler: Callable[[str | Dict[str, Any]], Awaitable[None]],
        websocket_cls: Callable[..., Websocket] = Websocket,
        data_format: Literal["text", "json"] = "json",
    ) -> AbstractEventLoop:
        """Initialize the websocket connection to the Mattermost server.

        This should be run after login(), because the websocket needs to
        authenticate.

        Documentation: https://api.mattermost.com/v4/#tag/WebSocket

        Parameters
        ----------
        event_handler : async function(str or dict) -> None
            The function to handle the websocket events.
        websocket_cls : function(), default=websocket.Websocket
            The Websocket class constructor.
        data_format : 'text' or 'json', default='json'
            Whether to receive the websocket data as text or JSON.

        Returns
        -------
        asyncio.AbstractEventLoop
            The event loop.

        """
        self.websocket = websocket_cls(self.options, self.client.token)
        loop: AbstractEventLoop = get_event_loop()

        if loop.is_running():
            run(self.websocket.connect(event_handler, data_format))

        else:
            try:
                loop.run_until_complete(
                    self.websocket.connect(event_handler, data_format)
                )

            except RuntimeError as err:
                logger.error(err)

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

        """
        if self.options.token:
            self.client.token = self.options.token
            result: Any | Response = self.users.get_user("me")

        else:
            response: Any = self.users.login_user(
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

    def logout(self) -> Any:
        """Log the user out.

        Returns
        -------
        Any
            The json-encoded content of the response.

        """
        result: Any = self.users.logout_user()

        self.client.token = ""
        self.client.user_id = ""
        self.client.username = ""
        self.client.cookies = None

        return result

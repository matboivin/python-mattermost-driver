"""Class to use Mattermost websocket API."""

from asyncio import Task
from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio import create_task
from logging import DEBUG, INFO, Logger, getLogger
from ssl import CERT_NONE, Purpose, SSLContext, create_default_context
from typing import Any, Awaitable, Callable

from aiohttp import (
    ClientConnectorError,
    ClientSession,
    ClientWebSocketResponse,
    WSServerHandshakeError,
)

from .options import DriverOptions

# Type alias for event handlers
Handler = Callable[[dict[str, Any]], Awaitable[None]]

logger: Logger = getLogger("scrapermost.websocket")
logger.setLevel(INFO)


class Websocket:
    """Class defining a websocket handle Mattermost events.

    Attributes
    ----------
    _url : str
        Websocket server URL.
    _token : str
        The session token.
    _ws_options : dict
        Parameters to pass to aiohttp.ClientSession.ws_connect() to create a
        websocket connection.
    _alive : bool, default=False
        Whether the websocket is connected.
    _background_tasks : set of asyncio.Task
        Message processing tasks running in background.

    Methods
    -------
    _receive_ws_message(websocket)
        Wait for any websocket message from the server.
    _authenticate_websocket(websocket, event_handler)
        Send a authentication challenge over a websocket.
    _listen(websocket, event_handler)
        Start loop to listen to websocket events.
    is_connected()
        Return whether the websocket is connected.
    connect(event_handler)
        Connect the websocket to server.
    disconnect()
        Disconnect the websocket.

    """

    def __init__(self, options: DriverOptions, token: str) -> None:
        """Initialize websocket.

        Parameters
        ----------
        options : options.DriverOptions
            The websocket options.
        token : str
            The user token.

        """
        scheme: str = "wss" if options.scheme == "https" else "ws"
        self._url: str = (
            f"{scheme}://{options.hostname}:{options.port}{options.basepath}"
            "/websocket"
        )
        ssl_context: SSLContext | None = None

        if options.scheme == "https":
            ssl_context = create_default_context(purpose=Purpose.SERVER_AUTH)
            if not options.verify:
                ssl_context.verify_mode = CERT_NONE

        self._ws_options: dict[str, Any] = {
            "url": self._url,
            "proxy": options.proxy,
            "ssl": ssl_context,
            **options.websocket_options,
        }
        self._token: str = token
        self._alive: bool = False
        self._background_tasks: set[Task[None]] = set()

        if options.debug:
            logger.setLevel(DEBUG)

    # Methods #################################################################

    async def _receive_ws_message(
        self, websocket: ClientWebSocketResponse
    ) -> dict[str, Any]:
        """Wait for any websocket message from the server.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            The client-side websocket to connect to server.

        Returns
        -------
        dict of str:Any
            The response received in JSON format.

        Raises
        ------
        asyncio.TimeoutError
            If the websocket didn't receive complete message before timeout.
        TypeError
            If message is BINARY.
        ValueError
            If message is not valid JSON.

        """
        try:
            data: dict[str, Any] = await websocket.receive_json()

        except AsyncioTimeoutError as err:
            raise AsyncioTimeoutError(
                "Websocket didn't receive complete message before timeout."
            ) from err

        return data

    async def _authenticate_websocket(
        self,
        websocket: ClientWebSocketResponse,
        event_handler: Handler,
    ) -> None:
        """Send a authentication challenge over a websocket.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            The client-side websocket to connect to server.
        event_handler : async function(dict) -> None
            The function to handle the websocket events.

        Raises
        ------
        asyncio.TimeoutError
            If the websocket didn't connect before timeout.
        RuntimeError
            If couldn't connect websocket to server.
        TypeError
            If message is BINARY.
        ValueError
            If message is not valid JSON.

        """
        logger.debug("Authenticating websocket")

        # Send the following JSON to authenticate
        auth_challenge: dict[str, Any] = {
            "seq": 1,
            "action": "authentication_challenge",
            "data": {"token": self._token},
        }

        await websocket.send_json(auth_challenge)

        while self._alive:
            message: dict[str, Any] = await self._receive_ws_message(websocket)

            # Pass the events to the event_handler already because the
            # 'hello' event is sometimes received before the authentication
            # response.
            await event_handler(message)

            # Valid answer can be either one of the following:
            if (
                message.get("status") == "OK"
                and (message.get("seq") == 1 or message.get("seq_reply") == 1)
            ) or (message.get("event") == "hello" and message.get("seq") == 0):
                logger.info("Websocket authentication: Success.")
                return

            raise RuntimeError(
                f"Websocket authentication failed: Received {message}"
            )

    async def _listen(
        self,
        websocket: ClientWebSocketResponse,
        event_handler: Handler,
    ) -> None:
        """Start loop to listen to websocket events.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            The client-side websocket to connect to server.
        event_handler : async function(dict) -> None
            The function to handle the websocket events.

        Raises
        ------
        RuntimeError
            If the websocket authentication failed.
        asyncio.TimeoutError
            If the websocket connection timed out.
        aiohttp.client_exceptions.ClientConnectorError
            If the connection to server failed.
        aiohttp.client_exceptions.WSServerHandshakeError
            If the websocket server handshake failed.

        """
        logger.debug("Start websocket event loop.")

        while self._alive:
            message: dict[str, Any] = await self._receive_ws_message(websocket)

            if message:
                task: Task[None] = create_task(
                    event_handler(message)  # type: ignore
                )

                self._background_tasks.add(task)
                task.add_done_callback(self._background_tasks.discard)

    def is_connected(self) -> bool:
        """Return whether the websocket is connected."""
        return self._alive

    async def connect(self, event_handler: Handler) -> None:
        """Connect the websocket to server.

        Parameters
        ----------
        event_handler : async function(dict) -> None
            The function to handle the websocket events.

        Raises
        ------
        RuntimeError
            If any error occured.

        """
        async with ClientSession() as session:
            async with session.ws_connect(**self._ws_options) as websocket:
                self._alive = True

                try:
                    await self._authenticate_websocket(
                        websocket, event_handler
                    )
                    await self._listen(websocket, event_handler)

                except (
                    AsyncioTimeoutError,
                    ConnectionResetError,
                    ClientConnectorError,
                    WSServerHandshakeError,
                    TypeError,
                    ValueError,
                ) as err:
                    logger.error(err)
                    return

                finally:
                    self._alive = False

        logger.info("Websocket disconnected.")

    async def disconnect(
        self,
    ) -> None:
        """Disconnect the websocket.

        Set `self._alive` to False to end listening loop.

        """
        logger.info("Disconnecting websocket...")
        self._alive = False

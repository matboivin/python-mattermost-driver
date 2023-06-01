"""Class to use Mattermost websocket API."""

from asyncio import Task
from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio import create_task
from json import loads
from logging import DEBUG, INFO, Logger, getLogger
from ssl import CERT_NONE, Purpose, SSLContext, create_default_context
from typing import Any, Awaitable, Callable, Literal

from aiohttp import (
    ClientConnectorError,
    ClientSession,
    ClientWebSocketResponse,
    WSMsgType,
    WSServerHandshakeError,
)

from .options import DriverOptions

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
    _authenticate_websocket(websocket, event_handler)
        Send a authentication challenge over a websocket.
    _listen(websocket, event_handler, data_format='json')
        Start loop to listen to websocket events.
    is_connected()
        Return whether the websocket is connected.
    connect(event_handler, data_format='json')
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

    # ############################################################### Methods #

    async def _authenticate_websocket(
        self,
        websocket: ClientWebSocketResponse,
        event_handler: Callable[[str | dict[str, Any]], Awaitable[None]],
    ) -> None:
        """Send a authentication challenge over a websocket.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            The client-side websocket to connect to server.
        event_handler : async function(str or dict) -> None
            The function to handle the websocket events.

        Raises
        ------
        RuntimeError
            If couldn't connect websocket to server.

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
            try:
                message: dict[str, Any] = await websocket.receive_json()

            except TimeoutError as err:
                raise RuntimeError(
                    "Failed to establish websocket connection: time out."
                ) from err

            except (TypeError, ValueError) as err:
                raise RuntimeError(
                    "Failed to establish websocket connection: "
                    f"{type(err)}: {err}"
                ) from err

            # Pass the events to the event_handler already because the
            # 'hello' event is sometimes received before the authentication
            # ok response
            await event_handler(message)

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
        event_handler: Callable[[str | dict[str, Any]], Awaitable[None]],
        data_format: Literal["json", "text"] = "json",
    ) -> None:
        """Start loop to listen to websocket events.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            The client-side websocket to connect to server.
        event_handler : async function(str or dict) -> None
            The function to handle the websocket events.
        data_format : 'json' or 'text', default='json'
            Whether to receive the websocket data as text or JSON.

        Raises
        ------
        RuntimeError
            If the websocket authentication failed.
        asyncio.TimeoutError
            If the websocket connection timed out.
        aiohttp.client_exceptions.ClientConnectorError
            If the name resolution failed.
        aiohttp.client_exceptions.WSServerHandshakeError
            If the websocket server handshake failed.

        """
        logger.debug("Start websocket event loop.")

        while self._alive:
            async for message in websocket:
                match message.type:
                    case WSMsgType.ERROR | WSMsgType.CLOSED:
                        logger.error(f"{message.type}: {message.data}")
                        self._alive = False
                        return

                    case WSMsgType.TEXT:
                        if data_format == "json":
                            message = loads(message.data)

                        task: Task[None] = create_task(
                            event_handler(message)  # type: ignore
                        )

                        self._background_tasks.add(task)
                        task.add_done_callback(self._background_tasks.discard)

    def is_connected(self) -> bool:
        """Return whether the websocket is connected."""
        return self._alive

    async def connect(
        self,
        event_handler: Callable[[str | dict[str, Any]], Awaitable[None]],
        data_format: Literal["json", "text"] = "json",
    ) -> None:
        """Connect the websocket to server.

        Parameters
        ----------
        event_handler : async function(str or dict) -> None
            The function to handle the websocket events.
        data_format : 'json' or 'text', default='json'
            Whether to receive the websocket data as text or JSON.

        Raises
        ------
        asyncio.TimeoutError
            If the websocket connection timed out.
        aiohttp.client_exceptions.ClientConnectorError
            If the name resolution failed.
        aiohttp.client_exceptions.WSServerHandshakeError
            If websocket server handshake failed.
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
                    await self._listen(websocket, event_handler, data_format)

                except (
                    ConnectionResetError,
                    ClientConnectorError,
                    WSServerHandshakeError,
                    AsyncioTimeoutError,
                    RuntimeError,
                ) as err:
                    logger.error(err)
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

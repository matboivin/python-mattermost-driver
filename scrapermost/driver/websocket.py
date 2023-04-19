"""Class to use Mattermost websocket API."""

from asyncio import sleep
from logging import DEBUG, INFO, Logger, getLogger
from ssl import CERT_NONE, Purpose, SSLContext, create_default_context
from typing import Any, Awaitable, Callable, Dict, Literal

from aiohttp import ClientError, ClientSession, ClientWebSocketResponse

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
    _websocket_kw_args : dict
        Parameters to pass to aiohttp.ClientSession.ws_connect() to create a
        websocket connection.
    _keepalive_delay : float
        Duration in seconds between two keepalive transmissions.
    _alive : bool, default=False
        Whether the websocket is connected.

    Methods
    -------
    is_connected()
        Return whether the websocket is connected.
    _do_heartbeats(websocket)
        Keep connection alive.
    _start_loop(websocket, event_handler, data_format='json')
        Start loop to listen to websocket events.
    _authenticate_websocket(websocket, event_handler)
        Send a authentication challenge over a websocket.
    connect(event_handler, data_format='json')
        Connect the websocket, authenticate and start event loop.
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

        self._websocket_kw_args: Dict[str, Any] = {
            "url": self._url,
            "proxy": options.proxy,
            "receive_timeout": options.websocket_receive_timeout,
            "heartbeat": options.websocket_heartbeat,
            "ssl": ssl_context,
            **options.websocket_kw_args,
        }
        self._token: str = token
        self._keepalive_delay: float = options.websocket_keepalive_delay
        self._alive: bool = False

        if options.debug:
            logger.setLevel(DEBUG)

    # ############################################################### Methods #

    def is_connected(self) -> bool:
        """Return whether the websocket is connected."""
        return self._alive

    async def _start_loop(
        self,
        websocket: ClientWebSocketResponse,
        event_handler: Callable[[str | Dict[str, Any]], Awaitable[None]],
        data_format: Literal["json", "text"] = "json",
    ) -> None:
        """Start loop to listen to websocket events.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            Client-side websocket.
        event_handler : async function(str or dict) -> None
            The function to handle the websocket events.
        data_format : 'json' or 'text', default='json'
            Whether to receive the websocket data as text or JSON.

        Raises
        ------
        RuntimeError
            If an error occured while listening to events.

        """
        logger.debug("Start websocket event loop.")

        while self._alive:
            try:
                message: str | Dict[str, Any] = (
                    await websocket.receive_json()
                    if data_format == "json"
                    else await websocket.receive_str()
                )

                await event_handler(message)

            except (TypeError, ValueError):
                pass

            except (RuntimeError, ClientError) as err:
                raise RuntimeError(f"{type(err): {err}}") from err

    async def _authenticate_websocket(
        self,
        websocket: ClientWebSocketResponse,
        event_handler: Callable[[str | Dict[str, Any]], Awaitable[None]],
    ) -> None:
        """Send a authentication challenge over a websocket.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            Client-side websocket.
        event_handler : async function(str or dict) -> None
            The function to handle the websocket events.

        Raises
        ------
        RuntimeError
            If couldn't connect websocket to server.

        """
        logger.debug("Authenticating websocket")

        # Send the following JSON to authenticate
        auth_challenge: Dict[str, Any] = {
            "seq": 1,
            "action": "authentication_challenge",
            "data": {"token": self._token},
        }

        await websocket.send_json(auth_challenge)

        while self._alive:
            try:
                message: Dict[str, Any] = await websocket.receive_json()

            except (TypeError, ValueError) as err:
                raise RuntimeError(
                    "Failed to establish websocket connection: "
                    f"{type(err)}: {err}"
                ) from err

            # Pass the events to the event_handler already because the
            # 'hello' event is sometimes received before the authentication
            # ok response
            await event_handler(message)

            if (message.get("status") == "OK" and message.get("seq") == 1) or (
                message.get("event") == "hello" and message.get("seq") == 0
            ):
                logger.info("Websocket authentication: Success.")
                return

            raise RuntimeError(
                f"Websocket authentication failed: Received {message}"
            )

    async def connect(
        self,
        event_handler: Callable[[str | Dict[str, Any]], Awaitable[None]],
        data_format: Literal["json", "text"] = "json",
    ) -> None:
        """Connect the websocket, authenticate and start event loop.

        Parameters
        ----------
        event_handler : async function(str or dict) -> None
            The function to handle the websocket events.
        data_format : 'json' or 'text', default='json'
            Whether to receive the websocket data as text or JSON.

        """
        self._alive = True

        while self._alive:
            try:
                async with ClientSession() as session:
                    async with session.ws_connect(
                        **self._websocket_kw_args
                    ) as websocket:
                        await self._authenticate_websocket(
                            websocket, event_handler
                        )
                        await self._start_loop(
                            websocket, event_handler, data_format
                        )

            except RuntimeError as err:
                logger.error(err)
                await sleep(self._keepalive_delay)

            except Exception as err:  # FIXME
                logger.exception(
                    f"Failed to establish websocket connection: {type(err)}"
                    " thrown."
                )
                await sleep(self._keepalive_delay)

        logger.debug("Websocket disconnected.")

    def disconnect(self) -> None:
        """Disconnect the websocket.

        Set `self._alive` to False to end listening loop.

        """
        if self.is_connected():
            logger.info("Disconnecting websocket...")
            self._alive = False

        else:
            logger.debug("Can't disconnect websocket: Not connected.")

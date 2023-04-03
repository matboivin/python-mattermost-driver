"""Class to use Mattermost websocket API."""

from asyncio import CancelledError, Task, create_task, sleep
from logging import DEBUG, INFO, Logger, getLogger
from ssl import CERT_NONE, Purpose, SSLContext, create_default_context
from time import time
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
        Dict of websocket parameters for aiohttp.ClientSession.ws_connect().
    _timeout : float
        Timeout in seconds for websocket to close.
    _keepalive : bool
        Whether to keep the websocket connection alive.
    _keepalive_delay : float
        Duration in seconds between two keepalive transmissions.
    _alive : bool, default=False
        Whether the websocket is connected.
    _last_msg : float, default=0
        Time of the last message received.

    Methods
    -------
    _do_heartbeats(websocket)
        Keep connection alive.
    _start_loop(websocket, event_handler, data_format='json')
        Start main coroutine.
    _authenticate_websocket(websocket, event_handler)
        Send a authentication challenge over a websocket.
    connect(event_handler, data_format='json')
        Connect to the websocket and authenticate it.
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
            "proxy": options.proxy,
            "ssl": ssl_context,
            **options.websocket_kw_args,
        }
        self._token: str = token
        self._timeout: float = options.timeout
        self._keepalive: bool = options.keepalive
        self._keepalive_delay: float = options.keepalive_delay
        self._alive: bool = False
        self._last_msg: float = 0

        if options.debug:
            logger.setLevel(DEBUG)

    # ############################################################ Properties #

    @property
    def timeout(self) -> float:
        """Get the websocket connection timeout in seconds.

        Returns
        -------
        float

        """
        return self._timeout

    @property
    def last_msg(self) -> float:
        """Get the time of the last message received.

        Returns
        -------
        float

        """
        return self._last_msg

    @last_msg.setter
    def last_msg(self, last_msg: float) -> None:
        """Set the time of the last message received.

        Parameters
        ----------
        last_msg : float
            The new time of the last message received.

        """
        self._last_msg = last_msg

    # ############################################################### Methods #

    async def _do_heartbeats(self, websocket: ClientWebSocketResponse) -> None:
        """Keep connection alive.

        This is a little complicated, but we only need to pong the websocket if
        we haven't received a message inside the timeout window.

        Since messages can be received, while we are waiting we need to check
        after sleep.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            Client-side websocket.

        """
        while True:
            since_last_msg: float = time() - self.last_msg
            next_timeout: float = self.timeout

            if since_last_msg <= self.timeout:
                next_timeout -= since_last_msg

            await sleep(next_timeout)

            if time() - self._last_msg >= self.timeout:
                logger.debug("Sending heartbeat...")

                try:
                    await websocket.pong()

                    self.last_msg = time()

                except ConnectionResetError as err:
                    logger.error(err)

    async def _start_loop(
        self,
        websocket: ClientWebSocketResponse,
        event_handler: Callable[[str | Dict[str, Any]], Awaitable[None]],
        data_format: Literal["json", "text"] = "json",
    ) -> None:
        """Start main coroutine.

        We will listen for websockets events, sending a heartbeats on a timer.
        If we don't the webserver would close the idle connection,
        forcing us to reconnect.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            Client-side websocket.
        event_handler : async function(str or dict) -> None
            The function to handle the websocket events.
        data_format : 'json' or 'text', default='json'
            Whether to receive the websocket data as text or JSON.

        """
        logger.debug("Starting websocket loop.")
        keep_alive: Task[None] = create_task(self._do_heartbeats(websocket))

        logger.debug("Waiting for messages on websocket.")

        while self._alive:
            try:
                message: str | Dict[str, Any] = (
                    await websocket.receive_json()
                    if data_format == "json"
                    else await websocket.receive_str()
                )
                self.last_msg = time()

                await event_handler(message)

            except (TypeError, ValueError) as err:
                logger.error(err)

        logger.debug("Cancelling heartbeat task...")
        keep_alive.cancel()

        try:
            await keep_alive

        except CancelledError:
            pass

    async def _authenticate_websocket(
        self,
        websocket: ClientWebSocketResponse,
        event_handler: Callable[[str | Dict[str, Any]], Awaitable[None]],
    ) -> None:
        """Send a authentication challenge over a websocket.

        This is not needed when we just send the cookie we got on login
        when connecting to the websocket.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            Client-side websocket.
        event_handler : async function(str or dict) -> None
            The function to handle the websocket events.

        """
        logger.debug("Authenticating websocket")
        # Send the following JSON to authenticate
        auth_challenge: Dict[str, Any] = {
            "seq": 1,
            "action": "authentication_challenge",
            "data": {"token": self._token},
        }

        await websocket.send_json(auth_challenge)

        while True:
            try:
                message: Dict[str, Any] = await websocket.receive_json()

            except (TypeError, ValueError) as err:
                logger.error(err)

            else:
                # Pass the events to the event_handler already because the
                # 'hello' event is sometimes received before the authentication
                # ok response
                await event_handler(message)

                if (
                    message.get("status") == "OK" and message.get("seq") == 1
                ) or (
                    message.get("event") == "hello" and message.get("seq") == 0
                ):
                    logger.info("Websocket authentication OK")
                    return

                logger.error("Websocket authentication failed")

    async def connect(
        self,
        event_handler: Callable[[str | Dict[str, Any]], Awaitable[None]],
        data_format: Literal["json", "text"] = "json",
    ) -> None:
        """Connect to the websocket and authenticate it.

        When the authentication has finished, start the loop listening for
        messages, sending a ping to the server to keep the connection alive.

        Parameters
        ----------
        event_handler : async function(str or dict) -> None
            The function to handle the websocket events.
        data_format : 'json' or 'text', default='json'
            Whether to receive the websocket data as text or JSON.

        """
        self._alive = True

        while True:
            try:
                async with ClientSession() as session:
                    async with session.ws_connect(
                        self._url, **self._websocket_kw_args
                    ) as websocket:
                        await self._authenticate_websocket(
                            websocket, event_handler
                        )

                        while self._alive:
                            try:
                                await self._start_loop(
                                    websocket, event_handler, data_format
                                )

                            except ClientError:
                                break

                        if not all([self._keepalive, self._alive]):
                            break

            except Exception as err:  # FIXME
                logger.exception(
                    f"Failed to establish websocket connection: {type(err)}"
                    " thrown."
                )

                await sleep(self._keepalive_delay)

    def disconnect(self) -> None:
        """Disconnect the websocket.

        Set `self._alive` to False so the loop in `self._start_loop` ends.

        """
        logger.info("Disconnecting websocket...")

        self._alive = False

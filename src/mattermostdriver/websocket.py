"""Websocket class to listen to Mattermost events."""

from asyncio import CancelledError, Task, ensure_future, sleep
from json import dumps, loads
from logging import DEBUG, INFO, Logger, getLogger
from ssl import CERT_NONE, Purpose, SSLContext, create_default_context
from time import time
from typing import Any, Dict

from aiohttp import ClientError, ClientSession, ClientWebSocketResponse

log: Logger = getLogger("mattermostdriver.websocket")
log.setLevel(INFO)


class Websocket:
    """Class defining a websocket to listen to Mattermost events.

    Attributes
    ----------
    options : dict
        The connection options.
    _token : str
        The session token.
    _alive : bool, default=False
        Whether the websocket is connected.
    _last_msg : float, default=0
        Time of the last message received.

    Methods
    -------
    _authenticate_websocket(websocket, event_handler)
        Send a authentication challenge over a websocket.
    _do_heartbeats(websocket)
        Keep connection alive.
    _start_loop(websocket, event_handler)
        Start main coroutine.
    connect(event_handler)
        Connect to the websocket and authenticate it.
    disconnect()
        Disconnect the websocket.

    """

    def __init__(self, options: Dict[str, Any], token: str) -> None:
        self.options: Dict[str, Any] = options

        if options.get("debug"):
            log.setLevel(DEBUG)

        self._token: str = token
        self._alive: bool = False
        self._last_msg: float = 0

    async def _authenticate_websocket(
        self, websocket: ClientWebSocketResponse, event_handler: Any
    ) -> bool:
        """Send a authentication challenge over a websocket.

        This is not needed when we just send the cookie we got on login
        when connecting to the websocket.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            Object for handling client-side websockets.
        event_handler : Function(message)
            The function to handle the websocket events. Takes one argument.

        Returns
        -------
        bool
            Whether the connection was successful.

        """
        log.debug("Authenticating websocket")
        json_data: str = dumps(
            {
                "seq": 1,
                "action": "authentication_challenge",
                "data": {"token": self._token},
            }
        )

        await websocket.send_str(json_data)

        while True:
            message: Any = await websocket.receive_str()
            status: Any = loads(message)

            log.debug(status)
            # We want to pass the events to the event_handler already because
            # the hello event could arrive before the authentication ok
            # response
            await event_handler(message)

            if status.get("event") == "hello" and status.get("seq") == 0:
                log.info("Websocket authentification OK")
                return True

            log.error("Websocket authentification failed")

    async def _do_heartbeats(self, websocket: ClientWebSocketResponse) -> None:
        """Keep connection alive.

        This is a little complicated, but we only need to pong the websocket if
        we haven't received a message inside the timeout window.

        Since messages can be received, while we are waiting we need to check
        after sleep.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            Object for handling client-side websockets.

        """
        timeout: float = self.options.get("timeout")

        while True:
            since_last_msg: float = time() - self._last_msg
            next_timeout: float = (
                timeout - since_last_msg
                if since_last_msg <= timeout
                else timeout
            )

            await sleep(next_timeout)

            if time() - self._last_msg >= timeout:
                log.debug("sending heartbeat...")
                await websocket.pong()

                self._last_msg = time()

    async def _start_loop(
        self, websocket: ClientWebSocketResponse, event_handler: Any
    ) -> None:
        """Start main coroutine.

        We will listen for websockets events, sending a heartbeats on a timer.
        If we don't the webserver would close the idle connection,
        forcing us to reconnect.

        Parameters
        ----------
        websocket : aiohttp.ClientWebSocketResponse
            Object for handling client-side websockets.
        event_handler : Function(message)
            The function to handle the websocket events. Takes one argument.

        """
        log.debug("Starting websocket loop")
        # TODO: move to create_task when cpython 3.7 is minimum supported
        # python version
        keep_alive: Task[None] = ensure_future(self._do_heartbeats(websocket))

        log.debug("Waiting for messages on websocket")

        while self._alive:
            message: Any = await websocket.receive_str()
            self._last_msg = time()
            await event_handler(message)

        log.debug("cancelling heartbeat task")
        keep_alive.cancel()

        try:
            await keep_alive

        except CancelledError:
            pass

    async def connect(self, event_handler: Any) -> None:
        """Connect to the websocket and authenticate it.

        When the authentication has finished, start the loop listening for
        messages, sending a ping to the server to keep the connection alive.

        Parameters
        ----------
        event_handler : Function(message)
            The function to handle the websocket events. Takes one argument.

        """
        context: SSLContext | None = None
        scheme: str = "ws://"

        if self.options.get("scheme") == "https":
            context = create_default_context(purpose=Purpose.SERVER_AUTH)
            scheme = "wss://"

        if context and not self.options.get("verify"):
            context.verify_mode = CERT_NONE

        url: str = (
            f"{scheme}{self.options.get('url')}:{self.options.get('port')}"
            f"{self.options.get('basepath')}/websocket"
        )

        self._alive = True

        while True:
            try:
                kw_args: Dict[str, Any] = {}

                if self.options.get("websocket_kw_args"):
                    kw_args = self.options.get("websocket_kw_args")

                async with ClientSession() as session:
                    async with session.ws_connect(
                        url,
                        ssl=context,
                        proxy=self.options.get("proxy"),
                        **kw_args,
                    ) as websocket:
                        await self._authenticate_websocket(
                            websocket, event_handler
                        )

                        while self._alive:
                            try:
                                await self._start_loop(
                                    websocket, event_handler
                                )
                            except ClientError:
                                break

                        if not all(
                            [self.options.get("keepalive"), self._alive]
                        ):
                            break

            except Exception as err:  # FIXME
                log.exception(
                    f"Failed to establish websocket connection: {type(err)}"
                    " thrown"
                )
                await sleep(self.options["keepalive_delay"])

    def disconnect(self) -> None:
        """Disconnect the websocket.

        Set `self._alive` to False so the loop in `self._start_loop` will
        finish.

        """
        log.info("Disconnecting websocket")
        self._alive = False

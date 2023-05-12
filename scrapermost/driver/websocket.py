"""Class to use Mattermost websocket API."""

from asyncio import TimeoutError, sleep
from logging import DEBUG, INFO, Logger, getLogger
from ssl import CERT_NONE, Purpose, SSLContext, create_default_context
from typing import Any, Awaitable, Callable, Literal

from aiohttp import (
    ClientConnectorError,
    ClientError,
    ClientSession,
    ClientWebSocketResponse,
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
    _websocket_kw_args : dict
        Parameters to pass to aiohttp.ClientSession.ws_connect() to create a
        websocket connection.
    _keepalive_delay : float
        Duration in seconds between two keepalive transmissions.
    _alive : bool, default=False
        Whether the websocket is connected.
    _session : aiohttp.ClientSession, default=None
        The client session object.
    websocket : aiohttp.ClientWebSocketResponse, default=None
        The client-side websocket to connect to server.

    Methods
    -------
    is_connected()
        Return whether the websocket is connected.
    _start_loop(event_handler, data_format='json')
        Start loop to listen to websocket events.
    _authenticate_websocket(event_handler)
        Send a authentication challenge over a websocket.
    listen(event_handler, data_format='json')
        Authenticate the websocket and start event loop.
    connect()
        Initialize the websocket object.
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

        self._websocket_kw_args: dict[str, Any] = {
            "url": self._url,
            "proxy": options.proxy,
            "heartbeat": options.websocket_heartbeat,
            "ssl": ssl_context,
            **options.websocket_kw_args,
        }
        self._token: str = token
        self._keepalive_delay: float = options.websocket_keepalive_delay
        self._alive: bool = False
        self._session: ClientSession | None = None
        self.websocket: ClientWebSocketResponse | None = None

        if options.debug:
            logger.setLevel(DEBUG)

    # ############################################################### Methods #

    def is_connected(self) -> bool:
        """Return whether the websocket is connected."""
        return self._alive

    async def _start_loop(
        self,
        event_handler: Callable[[str | dict[str, Any]], Awaitable[None]],
        data_format: Literal["json", "text"] = "json",
    ) -> None:
        """Start loop to listen to websocket events.

        Parameters
        ----------
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
                message: str | dict[str, Any] = (
                    await self.websocket.receive_json()  # type: ignore
                    if data_format == "json"
                    else await self.websocket.receive_str()  # type: ignore
                )

                await event_handler(message)

            except (TypeError, ValueError) as err:
                logger.debug(err)

            except TimeoutError as err:
                raise RuntimeError(
                    "Websocket event loop interrupted: time out."
                ) from err

            except (RuntimeError, ClientError) as err:
                raise RuntimeError(
                    f"Websocket event loop interrupted: {type(err): {err}}"
                ) from err

    async def _authenticate_websocket(
        self,
        event_handler: Callable[[str | dict[str, Any]], Awaitable[None]],
    ) -> None:
        """Send a authentication challenge over a websocket.

        Parameters
        ----------
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

        await self.websocket.send_json(auth_challenge)  # type: ignore

        while self._alive:
            try:
                message: dict[
                    str, Any
                ] = await self.websocket.receive_json()  # type: ignore

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

            if (message.get("status") == "OK" and message.get("seq") == 1) or (
                message.get("event") == "hello" and message.get("seq") == 0
            ):
                logger.info("Websocket authentication: Success.")
                return

            raise RuntimeError(
                f"Websocket authentication failed: Received {message}"
            )

    async def listen(
        self,
        event_handler: Callable[[str | dict[str, Any]], Awaitable[None]],
        data_format: Literal["json", "text"] = "json",
    ) -> None:
        """Authenticate the websocket and start event loop.

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

        """
        try:
            await self._authenticate_websocket(event_handler)

        except RuntimeError as err:
            logger.error(err)

        else:
            while self._alive:
                try:
                    await self._start_loop(event_handler, data_format)

                except (RuntimeError, ConnectionResetError) as err:
                    logger.error(err)
                    await sleep(self._keepalive_delay)

                except Exception as err:  # FIXME
                    logger.exception(
                        f"Websocket connection closed: {type(err)} thrown."
                    )
                    await sleep(self._keepalive_delay)

    async def connect(self) -> None:
        """Initialize the websocket object.

        Raises
        ------
        asyncio.TimeoutError
            If the websocket connection timed out.
        aiohttp.client_exceptions.ClientConnectorError
            If the name resolution failed.
        aiohttp.client_exceptions.WSServerHandshakeError
            If websocket server handshake failed.

        """
        self._session = ClientSession()

        try:
            self.websocket = await self._session.ws_connect(
                **self._websocket_kw_args
            )
            self._alive = True

        except (
            ClientConnectorError,
            TimeoutError,
            WSServerHandshakeError,
        ) as err:
            if self._session and not self._session.closed:
                await self._session.close()
            raise RuntimeError(
                f"Failed to establish websocket connection: {type(err)}: {err}"
            ) from err

    async def disconnect(self) -> None:
        """Disconnect the websocket.

        Set `self._alive` to False to end listening loop.

        """
        if self.is_connected():
            logger.info("Disconnecting websocket...")
            self._alive = False

            if self.websocket and not self.websocket.closed:
                await self.websocket.close()

            if self._session and not self._session.closed:
                await self._session.close()

            logger.info("Websocket disconnected.")

        else:
            logger.debug("Can't disconnect websocket: Not connected.")

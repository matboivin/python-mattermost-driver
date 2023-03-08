import asyncio
import json
import logging
import ssl
import time

import aiohttp

log = logging.getLogger("mattermostdriver.websocket")
log.setLevel(logging.INFO)


class Websocket:
    def __init__(self, options, token):
        self.options = options
        if options.get("debug"):
            log.setLevel(logging.DEBUG)
        self._token = token
        self._alive = False
        self._last_msg = 0

    async def connect(self, event_handler):
        """
        Connect to the websocket and authenticate it.
        When the authentication has finished, start the loop listening for messages,
        sending a ping to the server to keep the connection alive.

        :param event_handler: Every websocket event will be passed there. Takes one argument.
        :type event_handler: Function(message)
        :return:
        """
        context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
        if not self.options.get("verify"):
            context.verify_mode = ssl.CERT_NONE

        scheme = "wss://"
        if self.options.get("scheme") != "https":
            scheme = "ws://"
            context = None

        url = (
            f"{scheme}{self.options.get('url')}:{self.options.get('port')}"
            f"{self.options.get('basepath')}/websocket"
        )

        self._alive = True

        while True:
            try:
                kw_args = {}
                if self.options.get("websocket_kw_args"):
                    kw_args = self.options["websocket_kw_args"]
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(
                        url,
                        ssl=context,
                        proxy=self.options["proxy"],
                        **kw_args,
                    ) as websocket:
                        await self._authenticate_websocket(websocket, event_handler)
                        while self._alive:
                            try:
                                await self._start_loop(websocket, event_handler)
                            except aiohttp.ClientError:
                                break
                        if not all([self.options.get("keepalive"), self._alive]):
                            break
            except Exception as e:
                log.exception(f"Failed to establish websocket connection: {type(e)} thrown")
                await asyncio.sleep(self.options["keepalive_delay"])

    async def _start_loop(self, websocket, event_handler):
        """
        We will listen for websockets events, sending a heartbeats on a timer.
        If we don't the webserver would close the idle connection,
        forcing us to reconnect.
        """
        log.debug("Starting websocket loop")
        # TODO: move to create_task when cpython 3.7 is minimum supported python version
        keep_alive = asyncio.ensure_future(self._do_heartbeats(websocket))
        log.debug("Waiting for messages on websocket")
        while self._alive:
            message = await websocket.receive_str()
            self._last_msg = time.time()
            await event_handler(message)
        log.debug("cancelling heartbeat task")
        keep_alive.cancel()
        try:
            await keep_alive
        except asyncio.CancelledError:
            pass

    async def _do_heartbeats(self, websocket):
        """
        This is a little complicated, but we only need to pong the websocket if
        we haven't recieved a message inside the timeout window.

        Since messages can be received, while we are waiting we need to check
        after sleep.
        """
        timeout = self.options["timeout"]
        while True:
            since_last_msg = time.time() - self._last_msg
            next_timeout = timeout - since_last_msg if since_last_msg <= timeout else timeout
            await asyncio.sleep(next_timeout)
            if time.time() - self._last_msg >= timeout:
                log.debug("sending heartbeat...")
                await websocket.pong()
                self._last_msg = time.time()

    def disconnect(self):
        """Sets `self._alive` to False so the loop in `self._start_loop` will finish."""
        log.info("Disconnecting websocket")
        self._alive = False

    async def _authenticate_websocket(self, websocket, event_handler):
        """
        Sends a authentication challenge over a websocket.
        This is not needed when we just send the cookie we got on login
        when connecting to the websocket.
        """
        log.debug("Authenticating websocket")
        json_data = json.dumps({"seq": 1, "action": "authentication_challenge", "data": {"token": self._token}})
        await websocket.send_str(json_data)
        while True:
            message = await websocket.receive_str()
            status = json.loads(message)
            log.debug(status)
            # We want to pass the events to the event_handler already
            # because the hello event could arrive before the authentication ok response
            await event_handler(message)
            if status.get("event") == "hello" and status.get("seq") == 0:
                log.info("Websocket authentification OK")
                return True
            log.error("Websocket authentification failed")

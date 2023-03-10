"""Driver classes."""

from asyncio import AbstractEventLoop, get_event_loop, run
from logging import DEBUG, INFO, Logger, getLogger
from typing import Any, Callable, Dict

from requests import Response

from .client import AsyncClient, Client, ClientType
from .endpoints import *
from .websocket import Websocket

log: Logger = getLogger("mattermostdriver.api")
log.setLevel(INFO)


class BaseDriver:
    """Base for creating driver classes.

    Contains the client, api and provides you with functions for login, logout
    and initializing a websocket connection.

    Attributes
    ----------
    options : dict
        The options for driver and client.
    driver : dict
        The options for driver.
    client : AsyncClient or Client
        The underlying client object.
    websocket : Websocket, default=None
        The websocket to listen to Mattermost events.

    Methods
    -------
    disconnect()
        Disconnect the driver from the server.

    """

    default_options: Dict[str, Any] = {
        "scheme": "https",
        "url": "localhost",
        "port": 8065,
        "basepath": "/api/v4",
        "verify": True,
        "timeout": 30,
        "request_timeout": None,
        "login_id": None,
        "password": None,
        "token": None,
        "mfa_token": None,
        "auth": None,
        "keepalive": False,
        "keepalive_delay": 5,
        "websocket_kw_args": None,
        "debug": False,
        "http2": False,
        "proxy": None,
    }
    """
    Required options
        - url

    Either
        - login_id
        - password

    Or
        - token (https://docs.mattermost.com/developer/personal-access-tokens.html)

    Optional
        - scheme ('https')
        - port (8065)
        - verify (True)
        - timeout (30)
        - request_timeout (None)
        - mfa_token (None)
        - auth (None)
        - debug (False)

    Should not be changed
        - basepath ('/api/v4') - unlikely this would do any good
    """

    def __init__(
        self,
        options: Dict[str, Any] | None,
        client_cls: Callable[..., ClientType],
    ) -> None:
        """Initialize driver.

        Parameters
        ----------
        options : dict, optional
            The options for driver and client.
        client_cls : Function()
            Constructor for the underlying client class.

        """
        self.options: Dict[str, Any] = self.default_options.copy()

        if options:
            self.options.update(options)

        self.driver: Dict[str, Any] = self.options

        if self.options.get("debug"):
            log.setLevel(DEBUG)
            log.warning(
                "Careful!!\nSetting debug to True, will reveal your password "
                "in the log output if you do driver.login()!\nThis is NOT for "
                "production!"
            )

        self.client: ClientType = client_cls(self.options)
        self.websocket: Websocket | None = None

    # ############################################################ Properties #

    @property
    def users(self) -> Users:
        """Get Api endpoint for users.

        Returns
        -------
        endpoints.users.Users

        """
        return Users(self.client)

    @property
    def teams(self) -> Teams:
        """Get Api endpoint for teams.

        Returns
        -------
        endpoints.teams.Teams

        """
        return Teams(self.client)

    @property
    def channels(self) -> Channels:
        """Get Api endpoint for channels.

        Returns
        -------
        endpoints.channels.Channels

        """
        return Channels(self.client)

    @property
    def posts(self) -> Posts:
        """Get Api endpoint for posts.

        Returns
        -------
        endpoints.posts.Posts

        """
        return Posts(self.client)

    @property
    def files(self) -> Files:
        """Get Api endpoint for files.

        Returns
        -------
        endpoints.files.Files

        """
        return Files(self.client)

    @property
    def preferences(self) -> Preferences:
        """Get Api endpoint for preferences.

        Returns
        -------
        endpoints.preferences.Preferences

        """
        return Preferences(self.client)

    @property
    def emoji(self) -> Emoji:
        """Get Api endpoint for emoji.

        Returns
        -------
        endpoints.emoji.Emoji

        """
        return Emoji(self.client)

    @property
    def reactions(self) -> Reactions:
        """Get Api endpoint for posts' reactions.

        Returns
        -------
        endpoints.reactions.Reactions

        """
        return Reactions(self.client)

    @property
    def system(self) -> System:
        """Get Api endpoint for system.

        Returns
        -------
        endpoints.system.System

        """
        return System(self.client)

    @property
    def webhooks(self) -> Webhooks:
        """Get Api endpoint for webhooks.

        Returns
        -------
        endpoints.webhooks.Webhooks

        """
        return Webhooks(self.client)

    @property
    def compliance(self) -> Compliance:
        """Get Api endpoint for compliance.

        Returns
        -------
        endpoints.compliance.Compliance

        """
        return Compliance(self.client)

    @property
    def cluster(self) -> Cluster:
        """Get Api endpoint for cluster.

        Returns
        -------
        endpoints.cluster.Cluster

        """
        return Cluster(self.client)

    @property
    def brand(self) -> Brand:
        """Get Api endpoint for brand.

        Returns
        -------
        endpoints.brand.Brand

        """
        return Brand(self.client)

    @property
    def oauth(self) -> OAuth:
        """Get Api endpoint for oauth.

        Returns
        -------
        endpoints.oauth.OAuth

        """
        return OAuth(self.client)

    @property
    def saml(self) -> SAML:
        """Get Api endpoint for SAML.

        Returns
        -------
        endpoints.saml.SAML

        """
        return SAML(self.client)

    @property
    def ldap(self) -> LDAP:
        """Get Api endpoint for LDAP.

        Returns
        -------
        endpoints.ldap.LDAP

        """
        return LDAP(self.client)

    @property
    def elasticsearch(self) -> Elasticsearch:
        """Get Api endpoint for ElasticSearch.

        Returns
        -------
        endpoints.elasticsearch.Elasticsearch

        """
        return Elasticsearch(self.client)

    @property
    def data_retention(self) -> DataRetention:
        """Get Api endpoint for data_retention.

        Returns
        -------
        endpoints.data_retention.DataRetention

        """
        return DataRetention(self.client)

    @property
    def status(self) -> Status:
        """Get Api endpoint for status.

        Returns
        -------
        endpoints.status.Status

        """
        return Status(self.client)

    @property
    def commands(self) -> Commands:
        """Get Api endpoint for commands.

        Returns
        -------
        endpoints.commands.Commands

        """
        return Commands(self.client)

    @property
    def roles(self) -> Roles:
        """Get Api endpoint for roles.

        Returns
        -------
        endpoints.roles.Roles

        """
        return Roles(self.client)

    @property
    def opengraph(self) -> Opengraph:
        """Get Api endpoint for opengraph.

        Returns
        -------
        endpoints.opengraph.Opengraph

        """
        return Opengraph(self.client)

    @property
    def integration_actions(self) -> IntegrationActions:
        """Get Api endpoint for integration actions.

        Returns
        -------
        endpoints.integration_actions

        """
        return IntegrationActions(self.client)

    @property
    def bots(self) -> Bots:
        """Get Api endpoint for bots.

        Returns
        -------
        endpoints.bots.Bots

        """
        return Bots(self.client)

    # ############################################################### Methods #

    def disconnect(self) -> None:
        """Disconnect the driver from the server.

        It stops the websocket event loop.

        """
        if self.websocket:
            self.websocket.disconnect()


class Driver(BaseDriver):
    """Class defining a synchronous Mattermost driver.

    Methods
    -------
    init_websocket(event_handler, websocket_cls)
        Initialize the websocket connection to the Mattermost server.
    login()
        Log the user in.
    logout()
        Log the user out.

    """

    def __init__(
        self,
        options: Dict[str, Any] | None = None,
        client_cls: Callable[..., ClientType] = Client,
    ) -> None:
        super().__init__(options, client_cls)

    def __enter__(self):
        self.client.__enter__()

        return self

    def __exit__(self, *exc_info) -> Any:
        return self.client.__exit__(*exc_info)

    def init_websocket(
        self,
        event_handler: Any,
        websocket_cls: Callable[..., Websocket] = Websocket,
    ) -> AbstractEventLoop:
        """Initialize the websocket connection to the Mattermost server.

        This should be run after login(), because the websocket needs to
        authenticate.

        See https://api.mattermost.com/v4/#tag/WebSocket for which
        websocket events mattermost sends.

        Example of a really simple event_handler function

        .. code:: python

                async def my_event_handler(message):
                        print(message)

        Parameters
        ----------
        event_handler : Function(message)
            The function to handle the websocket events. Takes one argument.
        websocket_cls : Function(), default=websocket.Websocket
            The Websocket class.

        Returns
        -------
        asyncio.AbstractEventLoop
            The event loop.

        """
        self.websocket = websocket_cls(self.options, self.client.token)
        loop: AbstractEventLoop = get_event_loop()

        if loop.is_running:
            run(self.websocket.connect(event_handler))

        else:
            try:
                loop.run_until_complete(self.websocket.connect(event_handler))

            except RuntimeError as err:
                log.error(err)

        return loop

    def login(self) -> Any | Response:
        """Log the user in.

        The log in information is saved in the client
        - userid
        - username
        - cookies

        Returns
        -------
        Any or requests.Response
            The reponse in JSON format or the raw response if couldn't be
            converted to JSON.

        """
        if self.options.get("token"):
            self.client.token = self.options["token"]
            result: Any = self.users.get_user("me")

        else:
            response: Response = self.users.login_user(
                {
                    "login_id": self.options["login_id"],
                    "password": self.options["password"],
                    "token": self.options["mfa_token"],
                }
            )
            if response.status_code == 200:
                self.client.token = response.headers["Token"]
                self.client.cookies = response.cookies

            try:
                result = response.json()

            except ValueError:
                log.debug(
                    "Could not convert response to json, returning raw response"
                )
                result = response

        if result.get("id"):
            self.client.userid = result["id"]

        if result.get("username"):
            self.client.username = result["username"]

        return result

    def logout(self) -> Any:
        """Log the user out.

        Returns
        -------
        Any
            The reponse in JSON format.

        """
        result: Any = self.users.logout_user()

        self.client.token = ""
        self.client.userid = ""
        self.client.username = ""
        self.client.cookies = None

        return result


class AsyncDriver(BaseDriver):
    """Class defining an asynchronous Mattermost driver.

    Methods
    -------
    init_websocket(event_handler, websocket_cls)
        Initialize the websocket connection to the Mattermost server.
    login()
        Log the user in.
    logout()
        Log the user out.

    """

    def __init__(
        self,
        options: Dict[str, Any] | None = None,
        client_cls: Callable[..., ClientType] = AsyncClient,
    ) -> None:
        super().__init__(options, client_cls)

    async def __aenter__(self):
        await self.client.__aenter__()

        return self

    async def __aexit__(self, *exc_info) -> Any:
        return await self.client.__aexit__(*exc_info)

    async def init_websocket(
        self,
        event_handler: Any,
        websocket_cls: Callable[..., Websocket] = Websocket,
    ) -> Any:
        """Initialize the websocket connection to the Mattermost server.

        Unlike the Driver.init_websocket, this one assumes you are async aware
        and returns a coroutine that can be awaited.  It will not return
        until shutdown() is called.

        This should be run after login(), because the websocket needs to
        authenticate.

        See https://api.mattermost.com/v4/#tag/WebSocket for which
        websocket events mattermost sends.

        Example of a really simple event_handler function

        .. code:: python

                async def my_event_handler(message):
                        print(message)

        Parameters
        ----------
        event_handler : Function(message)
            The function to handle the websocket events. Takes one argument.
        websocket_cls : websocket.Websocket, default=websocket.Websocket
            The Websocket class.

        Returns
        -------
        Coroutine

        """
        self.websocket = websocket_cls(self.options, self.client.token)

        return await self.websocket.connect(event_handler)

    async def login(self) -> Any | Response:
        """Log the user in.

        The log in information is saved in the client
        - userid
        - username
        - cookies

        Returns
        -------
        Any or requests.Response
            The reponse in JSON format or the raw response if couldn't be
            converted to JSON.

        """
        if self.options.get("token"):
            self.client.token = self.options["token"]
            result: Any = await self.users.get_user("me")

        else:
            response: Any = await self.users.login_user(
                {
                    "login_id": self.options["login_id"],
                    "password": self.options["password"],
                    "token": self.options["mfa_token"],
                }
            )

            if response.status_code == 200:
                self.client.token = response.headers["Token"]
                self.client.cookies = response.cookies

            try:
                result = response.json()

            except ValueError:
                log.debug(
                    "Could not convert response to json, returning raw response"
                )
                result = response

        if result.get("id"):
            self.client.userid = result["id"]

        if result.get("username"):
            self.client.username = result["username"]

        return result

    async def logout(self) -> Any:
        """Log the user out.

        Returns
        -------
        Any or requests.Response
            The reponse in JSON format or the raw response if couldn't be
            converted to JSON.

        """
        result: Any = await self.users.logout_user()

        self.client.token = ""
        self.client.userid = ""
        self.client.username = ""
        self.client.cookies = None

        return result

"""Driver base class."""

from abc import ABC
from logging import DEBUG, INFO, Logger, getLogger
from typing import Any

from ..endpoints import *
from .options import DriverOptions
from .websocket import Websocket

logger: Logger = getLogger("scrapermost.driver")
logger.setLevel(INFO)


class BaseDriver(ABC):
    """Base for creating driver classes.

    Contains the HTTP client, API endpoints, the websocket object to use the
    websocket API, and functions for login in and logout.

    Attributes
    ----------
    options : options.DriverOptions
        The options to configure how to connect to the Mattermost API.
    client : client.AsyncClient or client.Client
        The Mattermost client to interact with Web Service API.
    websocket : websocket.Websocket, default=None
        The websocket to listen to Mattermost events.

    Methods
    -------
    disconnect_websocket()
        Disconnect the driver from the server.

    """

    def __init__(self, options: dict[str, Any]) -> None:
        """Initialize driver.

        Parameters
        ----------
        options : dict
            The options as a dict.

        """
        self.options: DriverOptions = DriverOptions(options)
        self.websocket: Websocket | None = None

        if self.options.debug:
            logger.setLevel(DEBUG)
            logger.warning("Not suitable for production.")

    # ############################################################ Properties #

    @property
    def client(self):  # type: ignore
        """Get the underlying Mattermost client."""
        ...

    @property
    def users(self) -> Users:
        """Get API endpoint for users.

        Returns
        -------
        endpoints.users.Users

        """
        return Users(self.client)

    @property
    def teams(self) -> Teams:
        """Get API endpoint for teams.

        Returns
        -------
        endpoints.teams.Teams

        """
        return Teams(self.client)

    @property
    def channels(self) -> Channels:
        """Get API endpoint for channels.

        Returns
        -------
        endpoints.channels.Channels

        """
        return Channels(self.client)

    @property
    def posts(self) -> Posts:
        """Get API endpoint for posts.

        Returns
        -------
        endpoints.posts.Posts

        """
        return Posts(self.client)

    @property
    def files(self) -> Files:
        """Get API endpoint for files.

        Returns
        -------
        endpoints.files.Files

        """
        return Files(self.client)

    @property
    def preferences(self) -> Preferences:
        """Get API endpoint for preferences.

        Returns
        -------
        endpoints.preferences.Preferences

        """
        return Preferences(self.client)

    @property
    def emoji(self) -> Emoji:
        """Get API endpoint for emoji.

        Returns
        -------
        endpoints.emoji.Emoji

        """
        return Emoji(self.client)

    @property
    def reactions(self) -> Reactions:
        """Get API endpoint for posts' reactions.

        Returns
        -------
        endpoints.reactions.Reactions

        """
        return Reactions(self.client)

    @property
    def system(self) -> System:
        """Get API endpoint for system.

        Returns
        -------
        endpoints.system.System

        """
        return System(self.client)

    @property
    def webhooks(self) -> Webhooks:
        """Get API endpoint for webhooks.

        Returns
        -------
        endpoints.webhooks.Webhooks

        """
        return Webhooks(self.client)

    @property
    def compliance(self) -> Compliance:
        """Get API endpoint for compliance.

        Returns
        -------
        endpoints.compliance.Compliance

        """
        return Compliance(self.client)

    @property
    def cluster(self) -> Cluster:
        """Get API endpoint for cluster.

        Returns
        -------
        endpoints.cluster.Cluster

        """
        return Cluster(self.client)

    @property
    def brand(self) -> Brand:
        """Get API endpoint for brand.

        Returns
        -------
        endpoints.brand.Brand

        """
        return Brand(self.client)

    @property
    def oauth(self) -> OAuth:
        """Get API endpoint for oauth.

        Returns
        -------
        endpoints.oauth.OAuth

        """
        return OAuth(self.client)

    @property
    def saml(self) -> SAML:
        """Get API endpoint for SAML.

        Returns
        -------
        endpoints.saml.SAML

        """
        return SAML(self.client)

    @property
    def ldap(self) -> LDAP:
        """Get API endpoint for LDAP.

        Returns
        -------
        endpoints.ldap.LDAP

        """
        return LDAP(self.client)

    @property
    def elasticsearch(self) -> Elasticsearch:
        """Get API endpoint for ElasticSearch.

        Returns
        -------
        endpoints.elasticsearch.Elasticsearch

        """
        return Elasticsearch(self.client)

    @property
    def data_retention(self) -> DataRetention:
        """Get API endpoint for data_retention.

        Returns
        -------
        endpoints.data_retention.DataRetention

        """
        return DataRetention(self.client)

    @property
    def status(self) -> Status:
        """Get API endpoint for status.

        Returns
        -------
        endpoints.status.Status

        """
        return Status(self.client)

    @property
    def commands(self) -> Commands:
        """Get API endpoint for commands.

        Returns
        -------
        endpoints.commands.Commands

        """
        return Commands(self.client)

    @property
    def roles(self) -> Roles:
        """Get API endpoint for roles.

        Returns
        -------
        endpoints.roles.Roles

        """
        return Roles(self.client)

    @property
    def opengraph(self) -> Opengraph:
        """Get API endpoint for opengraph.

        Returns
        -------
        endpoints.opengraph.Opengraph

        """
        return Opengraph(self.client)

    @property
    def integration_actions(self) -> IntegrationActions:
        """Get API endpoint for integration actions.

        Returns
        -------
        endpoints.integration_actions

        """
        return IntegrationActions(self.client)

    @property
    def bots(self) -> Bots:
        """Get API endpoint for bots.

        Returns
        -------
        endpoints.bots.Bots

        """
        return Bots(self.client)

    # ############################################################### Methods #

    async def disconnect_websocket(self) -> None:
        """Disconnect the driver from the server."""
        if self.websocket:
            await self.websocket.disconnect()

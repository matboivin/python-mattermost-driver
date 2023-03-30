"""Generic base class for API endpoints."""

from dataclasses import dataclass

from scrapermost.client import ClientType


@dataclass
class APIEndpoint:
    """Base class defining an API endpoint.

    Attributes
    ----------
    client : AsyncClient or Client
        The underlying client object.

    """

    client: ClientType

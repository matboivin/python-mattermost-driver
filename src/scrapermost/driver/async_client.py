"""Client class for the asynchronous driver.

This class holds information about the logged-in user and actually makes the
requests to the Mattermost server.
"""

from typing import Any, Dict, Tuple

from httpx import AsyncClient as HttpxAsyncClient
from requests import Response

from .base_client import BaseClient, logger
from .options import DriverOptions


class AsyncClient(BaseClient):
    """Class defining an asynchronous Mattermost client.

    Attributes
    ----------
    client : httpx.AsyncClient
        The underlying httpx client object.

    Methods
    -------
    get(endpoint, params=None, get_json=True)
        Send an asynchronous GET request.
    post(
        endpoint, body_json=None, params=None, data=None, files=None,
        get_json=True
    )
        Send an asynchronous POST request.
    put(endpoint, body_json=None, params=None, data=None, get_json=True)
        Send an asynchronous PUT request.
    delete(endpoint, params=None, get_json=True)
        Send an asynchronous DELETE request.

    """

    def __init__(self, options: DriverOptions) -> None:
        """Initialize client.

        Parameters
        ----------
        options : options.DriverOptions
            The client options.

        """
        super().__init__(options)

        self.httpx_client = HttpxAsyncClient(
            auth=options.auth,
            verify=options.verify,
            http2=options.http2,
            proxies={"all://": options.proxy},
            timeout=options.request_timeout,
        )

    async def __aenter__(self) -> Any:
        await self.httpx_client.__aenter__()

        return self

    async def __aexit__(self, *exc_info: Tuple[Any]) -> Any:
        return await self.httpx_client.__aexit__(*exc_info)

    # ############################################################ Properties #

    @property
    def httpx_client(self) -> HttpxAsyncClient:
        """Get the underlying httpx client object.

        Returns
        -------
        httpx.AsyncClient

        """
        return self.httpx_client

    @BaseClient.httpx_client.setter
    def httpx_client(self, httpx_client: HttpxAsyncClient) -> None:
        """Set the underlying httpx client object.

        Parameters
        ----------
        httpx_client : httpx.AsyncClient
            The new client instance.

        """
        self.httpx_client = httpx_client

    # ############################################################### Methods #

    async def get(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
        get_json: bool = True,
    ) -> Any | Response:
        """Send an asynchronous GET request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        params : dict, default=None
            Query parameters to include in the URL.
        get_json : bool, default=True
            Whether to return the json-encoded content of the response.

        Returns
        -------
        Any or requests.Response
            The json-encoded content of the response or the raw response.

        """
        response: Response = await self.httpx_client.get(
            url=endpoint, params=params, headers=self.get_auth_header()
        )
        self._check_response(response)

        if response.headers.get("Content-Type") != "application/json":
            logger.debug(
                "Could not convert response to JSON," "returning raw response."
            )
            return response

        if get_json:
            try:
                return response.json()

            except ValueError:
                logger.debug(
                    "Could not convert response to JSON,"
                    "returning raw response."
                )

        return response

    async def post(
        self,
        endpoint: str,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
        get_json: bool = True,
    ) -> Any:
        """Send an asynchronous POST request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        body_json : dict, default=None
            A JSON serializable object to include in the body of the request.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None
            Form data to include in the body of the request.
        files : dict, default=None
            Upload files to include in the body of the request.
        get_json : bool, default=True
            Whether to return the json-encoded content of the response.

        Returns
        -------
        Any or requests.Response
            The json-encoded content of the response or the raw response.

        """
        response: Response = await self.httpx_client.post(
            url=endpoint,
            body_json=body_json,
            params=params,
            data=data,
            files=files,
            headers=self.get_auth_header(),
        )
        self._check_response(response)

        return response.json() if get_json else response

    async def put(
        self,
        endpoint: str,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        get_json: bool = True,
    ) -> Any:
        """Send an asynchronous PUT request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        body_json : dict, default=None
            A JSON serializable object to include in the body of the request.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None
            Form data to include in the body of the request.
        get_json : bool, default=True
            Whether to return the json-encoded content of the response.

        Returns
        -------
        Any or requests.Response
            The json-encoded content of the response or the raw response.

        """
        response: Response = await self.httpx_client.put(
            url=endpoint,
            body_json=body_json,
            params=params,
            data=data,
            headers=self.get_auth_header(),
        )
        self._check_response(response)

        return response.json() if get_json else response

    async def delete(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
        get_json: bool = True,
    ) -> Any:
        """Send an asynchronous DELETE request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        params : dict, default=None
            Query parameters to include in the URL.
        get_json : bool, default=True
            Whether to return the json-encoded content of the response.

        Returns
        -------
        Any or requests.Response
            The json-encoded content of the response or the raw response.

        """
        response: Response = await self.httpx_client.delete(
            url=endpoint, params=params, headers=self.get_auth_header()
        )
        self._check_response(response)

        return response.json() if get_json else response

"""Client class for the asynchronous driver.

This class holds information about the logged-in user and actually makes the
requests to the Mattermost server.
"""

from typing import Any, Awaitable, Callable, Dict, Tuple

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
    make_request(
        method, endpoint, body_json=None, params=None, data=None, files=None,
    )
        Make request to Mattermost API.
    get(endpoint, body_json=None, params=None)
        Send an asynchronous GET request.
    post(endpoint, body_json=None, params=None, data=None, files=None)
        Send an asynchronous POST request.
    put(endpoint, body_json=None, params=None, data=None)
        Send an asynchronous PUT request.
    delete(endpoint, body_json=None, params=None, data=None)
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

        self.client = HttpxAsyncClient(
            auth=options.auth,
            verify=options.verify,
            http2=options.http2,
            proxies={"all://": options.proxy},
            timeout=options.request_timeout,
        )

    async def __aenter__(self) -> Any:
        if self.client:
            await self.client.__aenter__()

        return self

    async def __aexit__(self, *exc_info: Tuple[Any]) -> Any:
        if self.client:
            return await self.client.__aexit__(*exc_info)

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

    async def make_request(
        self,
        method: str,
        endpoint: str,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
    ) -> Response:
        """Make request to Mattermost API.

        Parameters
        ----------
        method : str
            Either 'GET', 'POST', 'PUT' or 'DELETE'.
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

        Returns
        -------
        requests.Response
            Response to the HTTP request.

        """
        request: Callable[..., Awaitable[Response]] = self._get_request_method(
            method, self.client
        )
        request_params: Dict[str, Any] = self._get_request_params(
            method, body_json, params, data, files
        )
        request_params["headers"] = self.get_auth_header()

        response: Response = await request(
            f"{self._url}{endpoint}", **request_params
        )

        self._check_response(response)

        return response

    async def get(
        self,
        endpoint: str,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Any | Response:
        """Send an asynchronous GET request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        body_json : dict, default=None
            A JSON serializable object to include in the body of the request.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None

        Returns
        -------
        Any or requests.Response
            The json-encoded content of the response if any.
            Otherwise, the raw response.

        """
        response: Response = await self.make_request(
            "get", endpoint, body_json=body_json, params=params
        )

        if response.headers.get("Content-Type") != "application/json":
            logger.debug(
                "Response is not application/json, returning raw response."
            )
            return response

        try:
            return response.json()

        except ValueError:
            logger.debug(
                "Could not convert response to JSON, returning raw response."
            )
            return response

    async def post(
        self,
        endpoint: str,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
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

        Returns
        -------
        Any
            The json-encoded content of the response.

        """
        response: Response = await self.make_request(
            "post",
            endpoint,
            body_json=body_json,
            params=params,
            data=data,
            files=files,
        )

        return response.json()

    async def put(
        self,
        endpoint: str,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
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

        Returns
        -------
        Any
            The json-encoded content of the response.

        """
        response: Response = await self.make_request(
            "put", endpoint, body_json=body_json, params=params, data=data
        )

        return response.json()

    async def delete(
        self,
        endpoint: str,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
    ) -> Any:
        """Send an asynchronous DELETE request.

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

        Returns
        -------
        Any
            The json-encoded content of the response.

        """
        response: Response = await self.make_request(
            "delete", endpoint, body_json=body_json, params=params, data=data
        )

        return response.json()

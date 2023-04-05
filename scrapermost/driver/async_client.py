"""Client class for the asynchronous driver.

This class holds information about the logged-in user and actually makes the
requests to the Mattermost server.
"""

from typing import Any, Awaitable, Callable, Dict, Tuple

from httpx import AsyncClient as HttpxAsyncClient
from httpx import HTTPStatusError
from requests import Response

from scrapermost.exceptions import (
    ContentTooLarge,
    FeatureDisabled,
    InvalidOrMissingParameters,
    MethodNotAllowed,
    NoAccessTokenProvided,
    NotEnoughPermissions,
    ResourceNotFound,
)

from .base_client import BaseClient, logger
from .options import DriverOptions


def _check_response(
    async_func: Callable[..., Awaitable[Response]]
) -> Callable[..., Awaitable[Response]]:
    """Raise custom exception from response status code.

    To be used as a decorator.

    Parameters
    ----------
    async_func : Callable
        The asynchronous function to decorate.

    Returns
    -------
    Callable
        The asynchronous wrapper function.

    Raises
    ------
    httox.HTTPStatusError
        If any httpx.HTTPError occurred.

    """

    async def wrapper(*args: str, **kwargs: int) -> Response:
        try:
            response: Response = await async_func(*args, **kwargs)

            response.raise_for_status()
            logger.debug(response)

        except HTTPStatusError as err:
            message: Any

            try:
                data: Dict[str, Any] = err.response.json()
                message = data.get("message", data)

            except ValueError:
                logger.debug("Could not convert response to json.")
                message = response.text

            logger.error(message)

            if err.response.status_code == 400:
                raise InvalidOrMissingParameters(message) from err
            if err.response.status_code == 401:
                raise NoAccessTokenProvided(message) from err
            if err.response.status_code == 403:
                raise NotEnoughPermissions(message) from err
            if err.response.status_code == 404:
                raise ResourceNotFound(message) from err
            if err.response.status_code == 405:
                raise MethodNotAllowed(message) from err
            if err.response.status_code == 413:
                raise ContentTooLarge(message) from err
            if err.response.status_code == 501:
                raise FeatureDisabled(message) from err

            raise

        return response

    return wrapper


class AsyncClient(BaseClient):
    """Class defining an asynchronous Mattermost client.

    Attributes
    ----------
    client : httpx.AsyncClient
        The underlying httpx client object.

    Methods
    -------
    get(endpoint, params=None)
        Send an asynchronous GET request.
    post(
            endpoint, body_json=None, params=None, data=None, files=None,
        )
        Send an asynchronous POST request.
    put(endpoint, body_json=None, params=None, data=None)
        Send an asynchronous PUT request.
    delete(endpoint, params=None)
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

        self._httpx_client = HttpxAsyncClient(
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
        return self._httpx_client

    # ############################################################### Methods #

    @_check_response
    async def get(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
    ) -> Response:
        """Send an asynchronous GET request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        params : dict, default=None
            Query parameters to include in the URL.

        Returns
        -------
        requests.Response
            The raw response.

        Raises
        ------
        httox.HTTPStatusError
            If any httpx.HTTPError occurred.

        """
        response: Response = await self.httpx_client.get(
            url=f"{self.url}/{endpoint}",
            params=params,
            headers=self.get_auth_header(),
        )

        return response

    @_check_response
    async def post(
        self,
        endpoint: str,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
    ) -> Response:
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
        requests.Response
            The raw response.

        Raises
        ------
        httox.HTTPStatusError
            If any httpx.HTTPError occurred.

        """
        response: Response = await self.httpx_client.post(
            url=f"{self.url}/{endpoint}",
            data=data,
            files=files,
            json=body_json,
            params=params,
            headers=self.get_auth_header(),
        )

        return response

    @_check_response
    async def put(
        self,
        endpoint: str,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
    ) -> Response:
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
        requests.Response
            The raw response.

        Raises
        ------
        httox.HTTPStatusError
            If any httpx.HTTPError occurred.

        """
        response: Response = await self.httpx_client.put(
            url=f"{self.url}/{endpoint}",
            data=data,
            json=body_json,
            params=params,
            headers=self.get_auth_header(),
        )

        return response

    @_check_response
    async def delete(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
    ) -> Response:
        """Send an asynchronous DELETE request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        params : dict, default=None
            Query parameters to include in the URL.

        Returns
        -------
        requests.Response
            The raw response.

        Raises
        ------
        httox.HTTPStatusError
            If any httpx.HTTPError occurred.

        """
        response: Response = await self.httpx_client.delete(
            url=f"{self.url}/{endpoint}",
            params=params,
            headers=self.get_auth_header(),
        )

        return response
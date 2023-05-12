"""Client class for the synchronous driver.

This class holds information about the logged-in user and actually makes the
requests to the Mattermost server.
"""

from typing import Any, Callable

from httpx import Client as HttpxClient
from httpx import ConnectError, HTTPStatusError, RequestError
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


def _check_response(func: Callable[..., Response]) -> Callable[..., Response]:
    """Raise custom exception from response status code.

    To be used as a decorator.

    Parameters
    ----------
    func : Callable
        The function to decorate.

    Returns
    -------
    Callable
        The wrapper function.

    Raises
    ------
    exceptions.ContentTooLarge
    exceptions.FeatureDisabled
    exceptions.InvalidOrMissingParameters
    exceptions.MethodNotAllowed
    exceptions.NoAccessTokenProvided
    exceptions.NotEnoughPermissions
    exceptions.ResourceNotFound
        If any httpx.HTTPStatusError occurred.
    RuntimeError
        If any httpx.RequestError occurred.

    """

    def wrapper(*args: str, **kwargs: int) -> Response:
        try:
            response: Response = func(*args, **kwargs)

            response.raise_for_status()
            logger.debug(response)

        except HTTPStatusError as err:
            message: Any

            try:
                data: dict[str, Any] = err.response.json()
                message = data.get("message", data)

            except ValueError:
                logger.debug("Could not convert response to JSON.")
                message = response.text

            logger.error(f"{err.response.status_code}: {message}")

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

        except ConnectError as err:
            logger.error(f"httpx.ConnectError: {err}.")

            raise RuntimeError(
                "Failed to establish a connection to server."
            ) from err

        except RequestError as err:
            logger.error(f"httpx.RequestError: {err}.")
            raise RuntimeError(err) from err

        return response

    return wrapper


class Client(BaseClient):
    """Class defining a synchronous Mattermost client.

    Attributes
    ----------
    client : httpx.Client
        The underlying httpx client object.

    Methods
    -------
    get(endpoint, params=None)
        Send a GET request.
    post(
            endpoint, body_json=None, params=None, data=None, files=None,
        )
        Send a POST request.
    put(endpoint, body_json=None, params=None, data=None)
        Send a PUT request.
    delete(endpoint, params=None)
        Send a DELETE request.

    """

    def __init__(self, options: DriverOptions) -> None:
        """Initialize client.

        Parameters
        ----------
        options : options.DriverOptions
            The client options.

        """
        super().__init__(options)

        self._httpx_client = HttpxClient(
            auth=options.auth,
            verify=options.verify,
            http2=options.http2,
            proxies={"all://": options.proxy},
            timeout=options.request_timeout,
        )

    def __enter__(self) -> Any:
        self.httpx_client.__enter__()

        return self

    def __exit__(self, *exc_info: tuple[Any]) -> Any:
        return self.httpx_client.__exit__(*exc_info)

    # ############################################################ Properties #

    @property
    def httpx_client(self) -> HttpxClient:
        """Get the underlying httpx client object.

        Returns
        -------
        httpx.Client

        """
        return self._httpx_client

    # ############################################################### Methods #

    @_check_response
    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> Response:
        """Send a GET request.

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
        httpx.HTTPStatusError
            If any httpx.HTTPError occurred.

        """
        response: Response = self.httpx_client.get(
            url=f"{self.url}/{endpoint}",
            params=params,
            headers=self.get_auth_header(),
        )

        return response

    @_check_response
    def post(
        self,
        endpoint: str,
        body_json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> Response:
        """Send a POST request.

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
        httpx.HTTPStatusError
            If any httpx.HTTPError occurred.

        """
        response: Response = self.httpx_client.post(
            url=f"{self.url}/{endpoint}",
            data=data,
            files=files,
            json=body_json,
            params=params,
            headers=self.get_auth_header(),
        )

        return response

    @_check_response
    def put(
        self,
        endpoint: str,
        body_json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """Send a PUT request.

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
        httpx.HTTPStatusError
            If any httpx.HTTPError occurred.

        """
        response: Response = self.httpx_client.put(
            url=f"{self.url}/{endpoint}",
            data=data,
            json=body_json,
            params=params,
            headers=self.get_auth_header(),
        )

        return response

    @_check_response
    def delete(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> Response:
        """Send a DELETE request.

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
        httpx.HTTPStatusError
            If any httpx.HTTPError occurred.

        """
        response: Response = self.httpx_client.delete(
            url=f"{self.url}/{endpoint}",
            params=params,
            headers=self.get_auth_header(),
        )

        return response

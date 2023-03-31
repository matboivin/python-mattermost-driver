"""Client class for the synchronous driver.

This class holds information about the logged-in user and actually makes the
requests to the Mattermost server.
"""

from typing import Any, Callable, Dict, Tuple

from httpx import Client as HttpxClient
from requests import Response

from .base_client import BaseClient, logger
from .options import DriverOptions


class Client(BaseClient):
    """Class defining a synchronous Mattermost client.

    Attributes
    ----------
    client : httpx.Client
        The underlying httpx client object.

    Methods
    -------
    make_request(
        method, endpoint, options=None, params=None, data=None, files=None
    )
        Make request to Mattermost API.
    get(endpoint, options=None, params=None)
        Send a GET request.
    post(endpoint, options=None, params=None, data=None, files=None)
        Send a POST request.
    put(endpoint, options=None, params=None, data=None)
        Send a PUT request.
    delete(endpoint, options=None, params=None, data=None)
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

        self.client = HttpxClient(
            auth=options.auth,
            verify=options.verify,
            http2=options.http2,
            proxies={"all://": options.proxy},
            timeout=options.request_timeout,
        )

    def __enter__(self) -> Any:
        if self.client:
            self.client.__enter__()

        return self

    def __exit__(self, *exc_info: Tuple[Any]) -> Any:
        if self.client:
            return self.client.__exit__(*exc_info)

    # ############################################################ Properties #

    @property
    def httpx_client(self) -> HttpxClient:
        """Get the underlying httpx client object.

        Returns
        -------
        httpx.Client

        """
        return self.httpx_client

    @BaseClient.httpx_client.setter
    def httpx_client(self, httpx_client: HttpxClient) -> None:
        """Set the underlying httpx client object.

        Parameters
        ----------
        httpx_client : httpx.Client
            The new client instance.

        """
        self.httpx_client = httpx_client

    # ############################################################### Methods #

    def make_request(
        self,
        method: str,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
    ) -> Response:
        """Make a request to Mattermost API.

        Parameters
        ----------
        method : str
            Either 'GET', 'POST', 'PUT' or 'DELETE'.
        endpoint : str
            The API endpoint to make the request to.
        options : dict, default=None
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
        request: Callable[..., Response] = self._get_request_method(
            method, self.client
        )
        request_params: Dict[str, Any] = self._get_request_params(
            method, options, params, data, files
        )
        request_params["headers"] = self.get_auth_header()

        response: Response = request(f"{self.url}{endpoint}", **request_params)

        self._check_response(response)

        return response

    def get(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Any | Response:
        """Send a GET request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        options : dict, default=None
            A JSON serializable object to include in the body of the request.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None

        Returns
        -------
        Any or requests.Response
            The reponse in JSON format or the raw response if couldn't be
            converted to JSON.

        """
        response: Response = self.make_request(
            "get", endpoint, options=options, params=params
        )

        if response.headers.get("Content-Type") != "application/json":
            logger.debug(
                "Response is not application/json, returning raw response"
            )
            return response

        try:
            return response.json()

        except ValueError:
            logger.debug(
                "Could not convert response to json, returning raw response"
            )
            return response

    def post(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
    ) -> Any:
        """Send a POST request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        options : dict, default=None
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
            The reponse in JSON format.

        """
        return self.make_request(
            "post",
            endpoint,
            options=options,
            params=params,
            data=data,
            files=files,
        ).json()

    def put(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
    ) -> Any:
        """Send a PUT request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        options : dict, default=None
            A JSON serializable object to include in the body of the request.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None
            Form data to include in the body of the request.

        Returns
        -------
        Any
            The reponse in JSON format.

        """
        return self.make_request(
            "put", endpoint, options=options, params=params, data=data
        ).json()

    def delete(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
    ) -> Any:
        """Send a DELETE request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        options : dict, default=None
            A JSON serializable object to include in the body of the request.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None
            Form data to include in the body of the request.

        Returns
        -------
        Any
            The reponse in JSON format.

        """
        return self.make_request(
            "delete", endpoint, options=options, params=params, data=data
        ).json()

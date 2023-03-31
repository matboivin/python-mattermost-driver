"""Client class for the synchronous driver.

This class holds information about the logged-in user and actually makes the
requests to the Mattermost server.
"""

from typing import Any, Dict, Tuple

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
    get(endpoint, params=None, get_json=True)
        Send a GET request.
    post(
        endpoint, body_json=None, params=None, data=None, files=None,
        get_json=True
    )
        Send a POST request.
    put(endpoint, body_json=None, params=None, data=None, get_json=True)
        Send a PUT request.
    delete(endpoint, params=None, get_json=True)
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

        self.httpx_client = HttpxClient(
            auth=options.auth,
            verify=options.verify,
            http2=options.http2,
            proxies={"all://": options.proxy},
            timeout=options.request_timeout,
        )

    def __enter__(self) -> Any:
        self.httpx_client.__enter__()

        return self

    def __exit__(self, *exc_info: Tuple[Any]) -> Any:
        return self.httpx_client.__exit__(*exc_info)

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

    def get(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
        get_json: bool = True,
    ) -> Any | Response:
        """Send a GET request.

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
        response: Response = self.httpx_client.get(
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

    def post(
        self,
        endpoint: str,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
        get_json: bool = True,
    ) -> Any | Response:
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
        get_json : bool, default=True
            Whether to return the json-encoded content of the response.

        Returns
        -------
        Any or requests.Response
            The json-encoded content of the response or the raw response.

        """
        response: Response = self.httpx_client.post(
            url=endpoint,
            body_json=body_json,
            params=params,
            data=data,
            files=files,
            headers=self.get_auth_header(),
        )
        self._check_response(response)

        return response.json() if get_json else response

    def put(
        self,
        endpoint: str,
        body_json: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        get_json: bool = True,
    ) -> Any | Response:
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
        get_json : bool, default=True
            Whether to return the json-encoded content of the response.

        Returns
        -------
        Any or requests.Response
            The json-encoded content of the response or the raw response.

        """
        response: Response = self.httpx_client.put(
            url=endpoint,
            body_json=body_json,
            params=params,
            data=data,
            headers=self.get_auth_header(),
        )
        self._check_response(response)

        return response.json() if get_json else response

    def delete(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
        get_json: bool = True,
    ) -> Any | Response:
        """Send a DELETE request.

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
        response: Response = self.httpx_client.delete(
            url=endpoint, params=params, headers=self.get_auth_header()
        )
        self._check_response(response)

        return response.json() if get_json else response

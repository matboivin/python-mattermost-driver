"""Client classes for the driver.

This class holds information about the logged-in user and actually makes the
requests to the Mattermost server.
"""

from logging import DEBUG, INFO, Logger, getLogger
from typing import Any, Dict, Tuple, TypeAlias

from httpx import AsyncClient as HttpxAsyncClient
from httpx import Client as HttpxClient
from httpx import HTTPStatusError
from requests import Response

from .exceptions import (
    ContentTooLarge,
    FeatureDisabled,
    InvalidOrMissingParameters,
    MethodNotAllowed,
    NoAccessTokenProvided,
    NotEnoughPermissions,
    ResourceNotFound,
)

log: Logger = getLogger("mattermostdriver.websocket")
log.setLevel(INFO)


class BaseClient:
    """Base for creating client classes.

    Attributes
    ----------
    _url : str
    _scheme : str
    _basepath : str
    _port : int
    _auth : Any
    _options : dict
    _token : str
    _cookies : Any, default=None
    _userid : str
    _username : str
    _proxies : dict, default=None
    client : httpx.AsyncClient or httpx.Client, default=None

    Static methods
    --------------
    _get_request_method(method, client)
        Get the client's method from request's name.
    _check_response(response)
        Raise custom exception from response status code.
    activate_verbose_logging(level =DEBUG)
        Enable trace level logging in httpx.

    Methods
    -------
    auth_header()
        Get Authorization header.
    _build_request(
        method, options=None, params=None, data=None, files=None, basepath=None
    )
        Build request to Mattermost API.

    """

    def __init__(self, options: Dict[str, Any]) -> None:
        self._url: str = (
            f"{options['scheme']}://{options['url']}:{options['port']}"
        )
        self._scheme: str = options["scheme"]
        self._basepath: str = options["basepath"]
        self._port: int = options["port"]
        self._auth: Any = options["auth"]

        if options.get("debug"):
            self.activate_verbose_logging()

        self._options: Dict[str, Any] = options
        self._token: str = ""
        self._cookies: Any | None = None
        self._userid: str = ""
        self._username: str = ""
        self._proxies: Dict[str, Any] | None = None

        if options.get("proxy"):
            self._proxies = {"all://": options.get("proxy")}

        self.client: HttpxAsyncClient | HttpxClient | None = None

    # ############################################################ Properties #

    @property
    def url(self) -> str:
        """Get the Mattermost server's URL.

        Returns
        -------
        str

        """
        return self._url

    @property
    def basepath(self) -> str:
        """Get the API basepath.

        Returns
        -------
        str

        """
        return self._basepath

    @property
    def request_timeout(self) -> int | None:
        """Get the configured timeout for the requests.

        Returns
        -------
        int or None

        """
        return self._options.get("request_timeout")

    @property
    def token(self) -> str:
        """Get the token for the login.

        Returns
        -------
        str

        """
        return self._token

    @token.setter
    def token(self, token: str) -> None:
        """Set the token for the login.

        Parameters
        ----------
        token : str
            The new token value.

        """
        self._token = token

    @property
    def cookies(self) -> Any | None:
        """Get the cookies given on login.

        Returns
        -------
        Any or None

        """
        return self._cookies

    @cookies.setter
    def cookies(self, cookies: Any) -> None:
        """Set the cookies.

        Parameters
        ----------
        cookies : Any
            The new cookies value.

        """
        self._cookies = cookies

    @property
    def userid(self) -> str:
        """Get the user ID of the logged-in user.

        Returns
        -------
        str

        """
        return self._userid

    @userid.setter
    def userid(self, user_id: str) -> None:
        """Set the user ID of the logged-in user.

        Parameters
        ----------
        user_id : str
            The new user ID value.

        """
        self._userid = user_id

    @property
    def username(self) -> str:
        """Get the username of the logged-in user.

        Returns
        -------
        str
            The username set. Otherwise an empty string.

        """
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        """Set the username of the logged-in user.

        Parameters
        ----------
        username : str
            The new username value.

        """
        self._username = username

    # ######################################################## Static methods #

    @staticmethod
    def _get_request_method(
        method: str, client: HttpxAsyncClient | HttpxClient
    ) -> Any:
        """Get the client's method from request's name.

        Parameters
        ----------
        method : str
            Either 'GET', 'POST', 'PUT' or 'DELETE'.
        client : httpx.AsyncClient or httpx.Client
            The client instance.

        Returns
        -------
        Any
            Client's GET/POST/PUT/DELETE method.

        """
        return getattr(client, method.lower())

    @staticmethod
    def _check_response(response: Response) -> None:
        """Raise custom exception from response status code.

        Parameters
        ----------
        response : requests.Response
            Response to the HTTP request.

        """
        try:
            response.raise_for_status()
            log.debug(response)

        except HTTPStatusError as err:
            message: Any

            try:
                data: Any = err.response.json()
                message = data.get("message", data)

            except ValueError:
                log.debug("Could not convert response to json.")
                message = response.text

            log.error(message)

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
            else:
                raise

    @staticmethod
    def activate_verbose_logging(level: int = DEBUG) -> None:
        """Enable trace level logging in httpx.

        Parameters
        ----------
        level : int, default=logging.DEBUG
            Log level to set.

        """
        log.setLevel(level)

        httpx_log: Logger = getLogger("httpx")

        httpx_log.setLevel("TRACE")
        httpx_log.propagate = True

    # ############################################################### Methods #

    def auth_header(self) -> Dict[str, str] | None:
        """Get Authorization header.

        Returns
        -------
        dict or None

        """
        if self._auth:
            return None
        if not self._token:
            return {}

        return {"Authorization": f"Bearer {self._token}"}

    def _build_request(
        self,
        method: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
        basepath: str | None = None,
    ) -> Tuple[Any, str, Dict[str, Any]]:
        """Build request to Mattermost API.

        Parameters
        ----------
        method : str
            Either 'GET', 'POST', 'PUT' or 'DELETE'.
        options : dict, default=None
            Client settings to use to make URL.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None
            Form data to include in the body of the request.
        files : dict, default=None
            Upload files to include in the body of the request.
        basepath : str, default=None
            API path.

        Returns
        -------
        tuple
            The method, URL and parameters.

        """
        url: str = (
            f"{self.url}{basepath}"
            if basepath
            else f"{self.url}{self.basepath}"
        )

        request_params: Dict[str, Any] = {
            "headers": self.auth_header(),
            "timeout": self.request_timeout,
        }

        if params:
            request_params["params"] = params

        if method in ["post", "put"]:
            if options:
                request_params["json"] = options
            if data:
                request_params["data"] = data
            if files:
                request_params["files"] = files

        if self._auth:
            request_params["auth"] = self._auth()

        return (
            self._get_request_method(method, self.client),
            url,
            request_params,
        )


class Client(BaseClient):
    """Class defining a synchronous Mattermost client.

    Attributes
    ----------
    client : httpx.Client

    Methods
    -------
    make_request(
        method, endpoint, options=None, params=None, data=None, files=None,
        basepath=None
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

    def __init__(self, options: Dict[str, Any]) -> None:
        super().__init__(options)

        self.client = HttpxClient(
            http2=options.get("http2", False),
            proxies=self._proxies,
            verify=options.get("verify", True),
        )

    def __enter__(self):
        self.client.__enter__()

        return self

    def __exit__(self, *exc_info) -> Any:
        return self.client.__exit__(*exc_info)

    def make_request(
        self,
        method: str,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
        basepath: str | None = None,
    ) -> Response:
        """Make request to Mattermost API.

        Parameters
        ----------
        method : str
            Either 'GET', 'POST', 'PUT' or 'DELETE'.
        endpoint : str
            The API endpoint to make the request to.
        options : dict, default=None
            Client settings to use to make URL.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None
            Form data to include in the body of the request.
        files : dict, default=None
            Upload files to include in the body of the request.
        basepath : str, default=None
            API path.

        Returns
        -------
        requests.Response
            Response to the HTTP request.

        """
        request: Any
        url: str
        request_params: Dict[str, Any]

        request, url, request_params = self._build_request(
            method, options, params, data, files, basepath
        )
        response: Response = request(f"{url}{endpoint}", **request_params)

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
            Client settings to use to make URL.
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
            log.debug(
                "Response is not application/json, returning raw response"
            )
            return response

        try:
            return response.json()

        except ValueError:
            log.debug(
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
            Client settings to use to make URL.
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
            Client settings to use to make URL.
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
            Client settings to use to make URL.
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


class AsyncClient(BaseClient):
    """Class defining an asynchronous Mattermost client.

    Attributes
    ----------
    client : httpx.AsyncClient

    Methods
    -------
    make_request(
        method, endpoint, options=None, params=None, data=None, files=None,
        basepath=None
    )
        Make request to Mattermost API.
    get(endpoint, options=None, params=None)
        Send an asynchronous GET request.
    post(endpoint, options=None, params=None, data=None, files=None)
        Send an asynchronous POST request.
    put(endpoint, options=None, params=None, data=None)
        Send an asynchronous PUT request.
    delete(endpoint, options=None, params=None, data=None)
        Send an asynchronous DELETE request.

    """

    def __init__(self, options: Dict[str, Any]) -> None:
        super().__init__(options)

        self.client = HttpxAsyncClient(
            http2=options.get("http2", False),
            proxies=self._proxies,
            verify=options.get("verify", True),
        )

    async def __aenter__(self):
        await self.client.__aenter__()

        return self

    async def __aexit__(self, *exc_info) -> Any:
        return await self.client.__aexit__(*exc_info)

    async def make_request(
        self,
        method: str,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
        basepath: str | None = None,
    ) -> Response:
        """Make request to Mattermost API.

        Parameters
        ----------
        method : str
            Either 'GET', 'POST', 'PUT' or 'DELETE'.
        endpoint : str
            The API endpoint to make the request to.
        options : dict, default=None
            Client settings to use to make URL.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None
            Form data to include in the body of the request.
        files : dict, default=None
            Upload files to include in the body of the request.
        basepath : str, default=None
            API path.

        Returns
        -------
        requests.Response
            Response to the HTTP request.

        """
        request: Any
        url: str
        request_params: Dict[str, Any]

        request, url, request_params = self._build_request(
            method, options, params, data, files, basepath
        )
        response: Response = await request(
            f"{url}{endpoint}", **request_params
        )

        self._check_response(response)

        return response

    async def get(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Any | Response:
        """Send an asynchronous GET request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        options : dict, default=None
            Client settings to use to make URL.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None

        Returns
        -------
        Any or requests.Response
            The reponse in JSON format or the raw response if couldn't be
            converted to JSON.

        """
        response: Response = await self.make_request(
            "get", endpoint, options=options, params=params
        )

        if response.headers.get("Content-Type") != "application/json":
            log.debug(
                "Response is not application/json, returning raw response"
            )
            return response

        try:
            return response.json()

        except ValueError:
            log.debug(
                "Could not convert response to json, returning raw response"
            )
            return response

    async def post(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
    ) -> Any:
        """Send an asynchronous POST request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        options : dict, default=None
            Client settings to use to make URL.
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
        response: Any = await self.make_request(
            "post",
            endpoint,
            options=options,
            params=params,
            data=data,
            files=files,
        )

        return response.json()

    async def put(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
    ) -> Any:
        """Send an asynchronous PUT request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        options : dict, default=None
            Client settings to use to make URL.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None
            Form data to include in the body of the request.

        Returns
        -------
        Any
            The reponse in JSON format.

        """
        response: Any = await self.make_request(
            "put", endpoint, options=options, params=params, data=data
        )

        return response.json()

    async def delete(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
    ) -> Any:
        """Send an asynchronous DELETE request.

        Parameters
        ----------
        endpoint : str
            The API endpoint to make the request to.
        options : dict, default=None
            Client settings to use to make URL.
        params : dict, default=None
            Query parameters to include in the URL.
        data : dict, default=None
            Form data to include in the body of the request.

        Returns
        -------
        Any
            The reponse in JSON format.

        """
        response: Any = await self.make_request(
            "delete", endpoint, options=options, params=params, data=data
        )

        return response.json()


ClientType: TypeAlias = Client | AsyncClient

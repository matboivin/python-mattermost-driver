"""
Client for the driver, which holds information about the logged in user
and actually makes the requests to the mattermost server
"""

from logging import DEBUG, INFO, Logger, getLogger
from typing import Any, Dict, Tuple, TypeAlias

from httpx import AsyncClient as HttpxAsyncClient
from httpx import Client as HttpxClient
from httpx import HTTPStatusError

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
    def __init__(self, options: Dict[str, Any]) -> None:
        self._url: str = self._make_url(
            options["scheme"],
            options["url"],
            options["port"],
            options["basepath"],
        )
        self._scheme: str = options["scheme"]
        self._basepath: str = options["basepath"]
        self._port: int = options["port"]
        self._auth: str = options["auth"]

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

    @staticmethod
    def _make_url(scheme: str, url: str, port: int, basepath: str) -> str:
        return f"{scheme}://{url}:{port}{basepath}"

    @staticmethod
    def activate_verbose_logging(level: int = DEBUG) -> None:
        log.setLevel(level)
        # enable trace level logging in httpx
        httpx_log: Logger = getLogger("httpx")

        httpx_log.setLevel("TRACE")
        httpx_log.propagate = True

    @property
    def userid(self) -> str:
        """
        :return: The user id of the logged in user
        """
        return self._userid

    @userid.setter
    def userid(self, user_id: str) -> None:
        self._userid = user_id

    @property
    def username(self) -> str:
        """
        :return: The username of the logged in user. If none, returns an emtpy string.
        """
        return self._username

    @property
    def request_timeout(self) -> int | None:
        """
        :return: The configured timeout for the requests
        """
        return self._options.get("request_timeout")

    @username.setter
    def username(self, username: str) -> None:
        self._username = username

    @property
    def url(self) -> str:
        return self._url

    @property
    def cookies(self) -> Any | None:
        """
        :return: The cookie given on login
        """
        return self._cookies

    @cookies.setter
    def cookies(self, cookies: Any) -> None:
        self._cookies = cookies

    @property
    def token(self) -> str:
        """
        :return: The token for the login
        """
        return self._token

    @token.setter
    def token(self, token: str) -> None:
        self._token = token

    def auth_header(self) -> Dict[str, str] | None:
        if self._auth:
            return None
        if not self._token:
            return {}
        return {"Authorization": f"Bearer {self._token}"}

    def _build_request(
        self,
        method: Any,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data=None,
        files=None,
        basepath: str | None = None,
    ) -> Tuple[Any, str, Dict[str, Any]]:
        url: str = (
            self._make_url(
                self._options["scheme"],
                self._options["url"],
                self._options["port"],
                basepath,
            )
            if basepath
            else self.url
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

    @staticmethod
    def _check_response(response: Any) -> None:
        try:
            response.raise_for_status()

        except HTTPStatusError as err:
            try:
                data: Any = err.response.json()
                message = data.get("message", data)

            except ValueError:
                log.debug("Could not convert response to json")
                message: Any = response.text

            log.error(message)

            if err.response.status_code == 400:
                raise InvalidOrMissingParameters(message) from err
            elif err.response.status_code == 401:
                raise NoAccessTokenProvided(message) from err
            elif err.response.status_code == 403:
                raise NotEnoughPermissions(message) from err
            elif err.response.status_code == 404:
                raise ResourceNotFound(message) from err
            elif err.response.status_code == 405:
                raise MethodNotAllowed(message) from err
            elif err.response.status_code == 413:
                raise ContentTooLarge(message) from err
            elif err.response.status_code == 501:
                raise FeatureDisabled(message) from err
            else:
                raise

        log.debug(response)

    @staticmethod
    def _get_request_method(method: Any, client) -> Any:
        method = method.lower()

        if method == "post":
            return client.post
        if method == "put":
            return client.put
        if method == "delete":
            return client.delete

        return client.get


class Client(BaseClient):
    def __init__(self, options: Dict[str, Any]) -> None:
        super().__init__(options)

        self.client = HttpxClient(
            http2=options.get("http2", False),
            proxies=self._proxies,
            verify=options.get("verify", True),
        )

    def make_request(
        self,
        method: Any,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data=None,
        files=None,
        basepath=None,
    ) -> Any:
        request: Any
        url: str
        request_params: Dict[str, Any]

        request, url, request_params = self._build_request(
            method, options, params, data, files, basepath
        )
        response: Any = request(f"{url}{endpoint}", **request_params)

        self._check_response(response)

        return response

    def __enter__(self):
        self.client.__enter__()

        return self

    def __exit__(self, *exc_info) -> Any:
        return self.client.__exit__(*exc_info)

    def get(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Any:
        response: Any = self.make_request(
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
        data=None,
        files=None,
    ) -> Any:
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
        data=None,
    ) -> Any:
        return self.make_request(
            "put", endpoint, options=options, params=params, data=data
        ).json()

    def delete(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data=None,
    ) -> Any:
        return self.make_request(
            "delete", endpoint, options=options, params=params, data=data
        ).json()


class AsyncClient(BaseClient):
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
        method: Any,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data=None,
        files=None,
        basepath: str | None = None,
    ) -> Any:
        request: Any
        url: str
        request_params: Dict[str, Any]

        request, url, request_params = self._build_request(
            method, options, params, data, files, basepath
        )
        response: Any = await request(f"{url}{endpoint}", **request_params)

        self._check_response(response)

        return response

    async def get(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Any:
        response: Any = await self.make_request(
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
        data=None,
        files=None,
    ) -> Any:
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
        data=None,
    ) -> Any:
        response: Any = await self.make_request(
            "put", endpoint, options=options, params=params, data=data
        )

        return response.json()

    async def delete(
        self,
        endpoint: str,
        options: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
        data=None,
    ) -> Any:
        response: Any = await self.make_request(
            "delete", endpoint, options=options, params=params, data=data
        )

        return response.json()


ClientType: TypeAlias = Client | AsyncClient

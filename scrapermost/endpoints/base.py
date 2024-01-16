"""Generic base class for API endpoints."""

from asyncio import iscoroutine
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from requests import JSONDecodeError, Response

from scrapermost.driver.async_client import AsyncClient
from scrapermost.driver.client import Client


@dataclass
class APIEndpoint:
    """Base class defining an API endpoint.

    Attributes
    ----------
    client : driver.async_client.AsyncClient or driver.client.Client
        The underlying client object.

    """

    client: AsyncClient | Client


def _ret_json(
    func: Callable[..., Response | Awaitable[Response]]
) -> Callable[..., Awaitable[Any | Response]]:
    """Return the JSON-encoded content of the response.

    Handle both sync and async functions.
    To be used as a decorator.

    Parameters
    ----------
    func : Callable
        The function to decorate.

    Returns
    -------
    Callable
        The wrapper function.

    """

    async def helper_async(func: Awaitable[Response]) -> Response:
        """Run the asynchronous function."""
        return await func

    async def wrapper(*args, **kwargs) -> Any | Response:  # type: ignore
        """Return the JSON-encoded content of the response.

        Returns
        -------
        Any or requests.Response
            The JSON-encoded content of the response.
            Otherwise if decoding failed, the raw response.

        """
        func_ret: Response | Awaitable[Response] = func(*args, **kwargs)
        response: Response

        if iscoroutine(func_ret):
            response = await helper_async(func_ret)
        else:
            response = func_ret  # type: ignore

        try:
            return response.json()

        except (JSONDecodeError, ValueError):
            return response

    return wrapper

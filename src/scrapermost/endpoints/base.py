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

    async def helper(func) -> Any:  # type: ignore
        return await func

    async def wrapper(*args: str, **kwargs: int) -> Any | Response:
        try:
            result: Any = await func(*args, **kwargs)  # type: ignore
            response: Response

            if iscoroutine(result):
                response = await helper(result)
            else:
                response = result

            return response.json()

        except JSONDecodeError:
            return response

    return wrapper

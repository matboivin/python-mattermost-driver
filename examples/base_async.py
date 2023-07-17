"""Start driver and connect to a Mattermost server."""

import os
from asyncio import run
from typing import Any, Dict

from dotenv import load_dotenv
from requests import ConnectionError

from scrapermost import AsyncDriver
from scrapermost.events import Posted
from scrapermost.exceptions import NoAccessTokenProvided


async def print_new_post(event: Dict[str, Any]) -> None:
    """Print any new post in server.

    Parameters
    ----------
    event : dict
        The event data in JSON format.

    """
    if event.get("event") == "posted":
        try:
            post: Posted = Posted(event)

        except KeyError as err:
            print(f"Posted message missing key: {err}")

        else:
            print(f"New Post: {post.post.message}")


async def connect_driver_to_server(driver: AsyncDriver) -> None:
    """Connect driver to server and initialize websocket.

    Parameters
    ----------
    driver : scrapermost.AsyncDriver
        The Mattermost client.

    """
    try:
        await driver.login()
        await driver.start_websocket(print_new_post)
        print(f"Driver connected to {driver.options.hostname}.")

    except (ConnectionError, NoAccessTokenProvided, RuntimeError) as err:
        print(f"Driver login failed: {err}")

    finally:
        await driver.disconnect_websocket()
        await driver.logout()


def init_driver(server_host: str, email: str, password: str) -> AsyncDriver:
    """Initialize asynchronous Mattermost client.

    Parameters
    ----------
    server_host : str
        The Mattermost server host name (example: 'mattermost.server.com').
    email : str
        The user account's email address.
    password : str
        The user's password.

    Returns
    -------
    scrapermost.AsyncDriver

    """
    return AsyncDriver(
        {
            "hostname": server_host,
            "login_id": email,
            "password": password,
            "scheme": "https",
            "port": 443,
        }
    )


async def entrypoint() -> None:
    """Program's entrypoint."""
    host: str | None = os.getenv("HOST")
    email: str | None = os.getenv("EMAIL")
    password: str | None = os.getenv("PASSWORD")

    if not all([host, email, password]):
        print("Error: Missing parameters in env.")
        return

    driver: AsyncDriver = init_driver(host, email, password)

    await connect_driver_to_server(driver)


if __name__ == "__main__":
    load_dotenv()

    try:
        run(entrypoint())

    except KeyboardInterrupt:
        print("Program interrupted by user.")

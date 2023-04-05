"""Start driver and connect to a Mattermost server."""

import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

from scrapermost import Driver
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
        post: Posted = Posted(event)

        print(f"New Post: {post.post.message}")


def connect_driver_to_server(driver: Driver) -> None:
    """Connect driver to server and initialize websocket.

    Parameters
    ----------
    driver : scrapermost.Driver
        The Mattermost client.

    """
    try:
        driver.login()
        print(f"Driver connected to {driver.options.hostname}.")

    except (requests.exceptions.ConnectionError, NoAccessTokenProvided) as err:
        print(f"Driver login failed: {err}")

    else:
        driver.init_websocket(print_new_post, data_format="json")

    finally:
        driver.disconnect_websocket()


def init_driver(server_host: str, email: str, password: str) -> Driver:
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
    scrapermost.Driver

    """
    return Driver(
        {
            "hostname": server_host,
            "login_id": email,
            "password": password,
            "scheme": "https",
            "port": 443,
        }
    )


def entrypoint() -> None:
    """Program's entrypoint."""
    host: str | None = os.getenv("HOST")
    email: str | None = os.getenv("EMAIL")
    password: str | None = os.getenv("PASSWORD")

    if all([host, email, password]):
        driver: Driver = init_driver(host, email, password)

        connect_driver_to_server(driver)

    else:
        print("Error: Missing parameters in env.")


if __name__ == "__main__":
    load_dotenv()

    try:
        entrypoint()

    except KeyboardInterrupt:
        print("Program ended.")

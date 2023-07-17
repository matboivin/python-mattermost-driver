[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Scrapermost

Python library to use [Mattermost APIv4](https://api.mattermost.com/).

This repository is a fork of [Python Mattermost Driver](https://github.com/Vaelor/python-mattermost-driver).

<br />

## Table of Contents

1. [Getting Started](#getting-started)
   1. [Requirements](#requirements)
   2. [Installation](#installation)
2. [Usage](#usage)
   1. [Initialize client and connect to a Mattermost server](#initialize-client-and-connect-to-a-mattermost-server)
   2. [Use the Web service API](#use-the-web-service-api)
   3. [Connect to the Websocket API](#connect-to-the-websocket-api)
   4. [Disconnect](#disconnect)
3. [License](#license)
4. [Acknowledgments](#acknowledgments)

<br />

## Getting Started

### Requirements

- Python 3.10 or greater
- [`poetry`](https://python-poetry.org/)

<br />

### Installation

As this project is not published to Pypi yet, follow the guidelines below.

1. Clone the repository and change it to your working directory.

2. Install the project:

```console
$ poetry install
```

<br />

## Usage

1. Activate the virtual environment:

```console
$ source `poetry env info --path`/bin/activate
```

2. Use it as a library.

> Example usage in the [`examples` folder](examples/).

<br />

### Initialize client and connect to a Mattermost server

A [Driver](https://api.mattermost.com/#tag/drivers), or client, is an object used to interact with the Mattermost API.

At least the following options must be provided as a dict:

- `login_id` (user account's email address or username) and `password`
- or `token`

**Full list of Driver options [here](scrapermost/driver/options.py).**

Example with synchronous driver:

```python
from requests import ConnectionError
from scrapermost import AsyncDriver
from scrapermost.exceptions import NoAccessTokenProvided


def init_driver(server_host: str, email: str, password: str) -> Driver:
    return Driver(
        {
            "hostname": server_host,
            "login_id": email,
            "password": password,
            "scheme": "https",
            "port": 443,
        }
    )

def connect_driver_to_server(driver: Driver) -> None:
    try:
        driver.login()
    except (ConnectionError, NoAccessTokenProvided) as err:
        print(f"Driver login failed: {err}")
```

Example with asynchronous driver:

```python
from requests import ConnectionError
from scrapermost import AsyncDriver
from scrapermost.exceptions import NoAccessTokenProvided


def init_driver(server_host: str, email: str, password: str) -> AsyncDriver:
    return AsyncDriver(
        {
            "hostname": server_host,
            "login_id": email,
            "password": password,
            "scheme": "https",
            "port": 443,
        }
    )

async def connect_driver_to_server(driver: AsyncDriver) -> None:
    try:
        await driver.login()
    except (ConnectionError, NoAccessTokenProvided) as err:
        print(f"Driver login failed: {err}")
```

<br />

### Use the Web service API

You can make api calls by using calling `Driver.endpointofchoice`. For example, if you want to get a user's data (`http://your-mattermost-url.com/api/v4/users/{user_id}`), you would use `Driver.users.get_user(user_id)`. The returned data will be either in JSON format or the raw response.

Example with asynchronous driver:

```python
from typing import Any

response: Any = await driver.users.get_user(user_id="me")
```

<br />

### Connect to the Websocket API

It is possible to use a [websocket](scrapermost/driver/websocket.py) to listen to Mattermost events ([event list here](https://api.mattermost.com/#tag/WebSocket)).

Create a function to handle every Mattermost websocket event:

```python
from typing import Any, Dict

from scrapermost.events import Posted

# Minimalist event handler example
async def handle_new_post(event: Dict[str, Any]) -> None:
    if event.get("event") == "posted":
        post: Posted = Posted(event)

        ...
```

Assuming `Driver.login()` was called, connect the websocket to the Mattermost server using `Driver.start_websocket()`.

Example with synchronous driver:

```python
driver.start_websocket(handle_new_post)
```

Example with asynchronous driver:

```python
await driver.start_websocket(handle_new_post)
```

<br />

### Disconnect

Example with asynchronous driver:

```python
await driver.disconnect_websocket()
await driver.logout()
```

<br />

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

<br />

## Acknowledgments

Original project [Python Mattermost Driver](https://github.com/Vaelor/python-mattermost-driver) ([documentation here](https://vaelor.github.io/python-mattermost-driver/)) by Christian Plümer.

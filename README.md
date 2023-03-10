[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Python Mattermost Driver (APIv4)

Library to use [Mattermost API](https://api.mattermost.com/).

This repository is a fork of [Python Mattermost Driver](https://github.com/Vaelor/python-mattermost-driver).

<br />

## Table of Contents

1. [Getting Started](#getting-started)
   1. [Requirements](#requirements)
   2. [Installation](#installation)
2. [Usage](#usage)
3. [License](#license)
4. [Acknowledgments](#acknowledgments)

<br />

## Getting Started

### Requirements

- Python 3.9 or greater
- [`poetry`](https://python-poetry.org/)

### Installation

1. Clone the repository and change it to your working directory.

2. Install the project:

```console
$ poetry install
```

<br />

## Usage

This project is intended to be used as a library.

```python
from mattermostdriver import Driver

def init_driver(server_url: str, email: str, password: str) -> Driver:
    return Driver(
        {
            "url": server_url,
            "login_id": email,
            "password": password
        }
    )

def start_driver(driver: Driver) -> None:
    """Connect Mattermost Driver to server."""
    driver.login()
```

Example with asynchronous driver:

```python
from mattermostdriver import AsyncDriver

def init_driver(server_url: str, email: str, password: str) -> AsyncDriver:
    return AsyncDriver(
        {
            "url": server_url,
            "login_id": email,
            "password": password
        }
    )

async def start_driver(driver: AsyncDriver) -> None:
    """Connect Mattermost Driver to server."""
    await driver.login()
```

<br />

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

<br />

## Acknowledgments

Original project [Python Mattermost Driver](https://github.com/Vaelor/python-mattermost-driver) ([documentation here](https://vaelor.github.io/python-mattermost-driver/)) by Christian Plümer.

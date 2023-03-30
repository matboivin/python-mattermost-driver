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

A [Driver](https://api.mattermost.com/#tag/drivers), or client, is an object used to interact with the Mattermost API.

At least the following options must be provided as a dict:

- `login_id` (user account's email address or username) and `password`
- or `token`

Example with synchronous driver:

```python
from scrapermost import Driver

driver: Driver = Driver(
    {
        "hostname": server_hostname,
        "login_id": email,
        "password": password
    }
)

driver.login()
```

Example with asynchronous driver:

```python
from scrapermost import AsyncDriver

driver: AsyncDriver = AsyncDriver(
    {
        "hostname": server_hostname,
        "token": token
    }
)

await driver.login()
```

<br />

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

<br />

## Acknowledgments

Original project [Python Mattermost Driver](https://github.com/Vaelor/python-mattermost-driver) ([documentation here](https://vaelor.github.io/python-mattermost-driver/)) by Christian Plümer.

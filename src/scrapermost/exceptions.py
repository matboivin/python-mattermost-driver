"""Custom HTTP exceptions."""

from httpx import HTTPError


class InvalidOrMissingParameters(HTTPError):
    """Invalid Or Missing Parameters.

    Raised when mattermost returns a 400 Invalid or missing parameters in
    URL or request body.
    """


class NoAccessTokenProvided(HTTPError):
    """No Access Token Provided.

    Raised when mattermost returns a 401 No access token provided.
    """


class NotEnoughPermissions(HTTPError):
    """Not Enough Permissions.

    Raised when mattermost returns a 403 Do not have appropriate permissions.
    """


class ResourceNotFound(HTTPError):
    """Resource Not Found.

    Raised when mattermost returns a 404 Resource not found.
    """


class MethodNotAllowed(HTTPError):
    """Method Not Allowed.

    Raised when mattermost returns a 405 Method Not Allowed.
    """


class ContentTooLarge(HTTPError):
    """Content Too Large.

    Raised when mattermost returns a 413 Content too large.
    """


class FeatureDisabled(HTTPError):
    """Feature Disabled.

    Raised when mattermost returns a 501 Feature is disabled.
    """

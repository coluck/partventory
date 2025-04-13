
class PartCreationError(Exception):
    """Generic error for part creation failures."""


class PartAlreadyExists(Exception):
    """Raised when trying to create a part that already exists."""


class PartNotFound(Exception):
    """Raised when a part is not found in the database."""

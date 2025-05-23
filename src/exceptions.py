
class PartCreationError(Exception):
    """Generic error for part creation failures."""


class PartUpdateError(Exception):
    """Generic error for part creation failures."""


class PartDeletionError(Exception):
    """Generic error for part deletion failures."""

class PartAlreadyExists(Exception):
    """Raised when trying to create a part that already exists."""


class PartNotFound(Exception):
    """Raised when a part is not found in the database."""

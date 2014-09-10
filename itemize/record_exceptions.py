class RecordError(LookupError):
    """Base exception type for all exception in this package."""
    pass

class RecordDefaultError(RecordError):
    """Raised by ChainRecord.default(), if no default information was provided
    during initialization (via keywords)."""
    pass
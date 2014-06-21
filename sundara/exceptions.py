"""Custom exceptions used by Sundara."""


class Error(Exception):
    """Base exception class for all Sundara errors."""

class ConfigError(Error):
    """An error occurred while dealing with the config file."""

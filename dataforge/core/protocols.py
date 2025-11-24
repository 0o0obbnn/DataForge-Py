"""
DataForge Core Protocols and Mixins
"""

from typing import Any, Protocol, TypeVar

T = TypeVar("T", covariant=True)


class Validator(Protocol):
    """A protocol for data validators."""

    def validate(self, data: Any) -> bool:
        """Validate the given data."""
        ...

    @property
    def error_message(self) -> str:
        """Return the error message for invalid data."""
        ...


class Generator(Protocol[T]):
    """A protocol for data generators."""

    def generate(self, **kwargs: Any) -> T:
        """Generate a single data item."""
        ...
